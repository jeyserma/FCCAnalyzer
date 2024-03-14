
import sys, os, glob, shutil, json, math, re, random
import concurrent.futures
import time
import ROOT
from dataset import Dataset
import argparse
import pathlib
import json
import logging
import pickle
import subprocess

logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger("fcclogger")
logger.setLevel(logging.INFO)

slurm_script_template = """#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --output={fOut_template}.out
#SBATCH --error={fOut_template}.err
#SBATCH --time=06:00:00
##SBATCH --mem=2GB           # total memory per node
#SBATCH --mem-per-cpu=2G    # memory per cpu-core
#SBATCH --partition=submit

source ~/.bashrc
cd {work_dir}
source setup.sh
{cmd}
"""

class Submit:

    def __init__(self, datadict, datasets_to_run, args, treeName="events", output_file="output.root", norm=False, lumi=1.):

        self.args = args
        self.datadict = datadict
        self.datasets_to_run = datasets_to_run
        self.treeName = treeName
        self.output_file = output_file
        self.norm = norm
        self.lumi = lumi
        self.script_name = sys.argv[0]
        self.script_name_stripped = self.script_name.split("/")[-1].replace(".py", "")
        self.cwd = os.getcwd()
        self.jobDir = f"{self.cwd}/{self.args.jobDir}/"

        self.datasets = []
        for datasetName in self.datasets_to_run:
            if not datasetName in self.datadict:
                logger.warning(f"Cannot find dataset {datasetName} in the datadict, skipping")

            xsec = datadict[datasetName]['xsec']
            path = f"{self.datadict['basePath']}/{self.datadict[datasetName]['path']}"
            if not os.path.exists(path):
                logger.warning(f"directory {path} does not exist, skipping")
                continue
            dataset = Dataset(datasetName, path, xsec, treeName=self.treeName)
            self.datasets.append(dataset)


        if args.submit:
            self.submit()
        
        if args.status:
            self.status()

        if args.merge:
            self.merge()


    def submit(self):
        if os.path.exists(self.jobDir):
            logger.error(f"Job directory {self.args.jobDir} already exist, please remove it or submit to another directory using --jobDir")
            quit()
        os.makedirs(self.jobDir)

        files = []
        for d in self.datasets:
            files.extend(d.rootfiles)

        files = [d.rootfiles for d in self.datasets]
        chunks = self.split_files_into_chunks(files, self.args.nJobs)
        nJobs = len(chunks)
        logger.info(f"Prepare submission for around {self.args.nJobs} jobs, submit in total {nJobs} jobs")
        for iJob in range(0, nJobs):
            fOut_template = f"{self.jobDir}/job_{iJob:04d}"
            job_name = f"{self.script_name_stripped}_job_{iJob:04d}"

            # make custom job config
            job_cfg = {}
            job_cfg['norm'] = False
            job_cfg['output_file'] = f"{fOut_template}.root"
            job_cfg['input_files'] = chunks[iJob]
            with open(f"{fOut_template}.pkl", 'wb') as handle:
                pickle.dump(job_cfg, handle, protocol=pickle.HIGHEST_PROTOCOL)

            cmd = f"python {self.script_name} --cfg {fOut_template}.pkl"
            slurm_script_content = slurm_script_template.format(
                fOut_template=fOut_template,
                work_dir=self.cwd,
                cmd=cmd,
                name=job_name,
            )
            slurm_script_file = f"{fOut_template}.sh"
            with open(slurm_script_file, "w") as f:
                f.write(slurm_script_content)
            subprocess.run(["sbatch", "--export=NONE", slurm_script_file])


    def split_files_into_chunks(self, file_lists, num_chunks):
        total_files = sum(len(files) for files in file_lists)
        chunk_size = math.ceil(total_files / num_chunks)
        chunks = []

        current_chunk = []
        files_in_chunk = 0
        for file_list in file_lists:
            for file in file_list:
                current_chunk.append(file)
                files_in_chunk += 1
                if files_in_chunk >= chunk_size:
                    chunks.append(current_chunk)
                    current_chunk = []
                    files_in_chunk = 0

        if current_chunk: # leftover files
            chunks.append(current_chunk)

        return chunks


    def status(self):
        if not os.path.exists(self.jobDir):
            logger.error(f"Job directory {self.args.jobDir} not found")
        nJobsTotal = len(glob.glob(f"{self.jobDir}/*.sh"))
        nJobsStarted = len(glob.glob(f"{self.jobDir}/*.err"))

        try:
            cmd = f"grep -R 'Output written to' {self.jobDir} --include \*.err"
            result = subprocess.check_output(cmd, shell=True, universal_newlines=True).splitlines()
        except Exception as e:
            result = []
        nJobsFinished = len(result)
        nJobsRunning = nJobsStarted - nJobsFinished
        nJobsIdle = nJobsTotal - nJobsFinished - nJobsRunning

        logger.info(f"Check jobs for task {self.script_name}")
        logger.info(f"Total number of jobs: {nJobsTotal}")
        logger.info(f"Total idle jobs:      {nJobsIdle}/{nJobsTotal}")
        logger.info(f"Total running jobs:   {nJobsRunning}/{nJobsTotal}")
        logger.info(f"Total finished jobs:  {nJobsFinished}/{nJobsTotal}")
    
    def merge(self):
        if not os.path.exists(self.jobDir):
            logger.error(f"Job directory {self.args.jobDir} not found")
        files = glob.glob(f"{self.jobDir}/*.root")
        logger.info(f"Merge output files for task {self.script_name}")
        subprocess.run(["hadd", "-f", self.output_file, *files])

        # post-process the meta information: update xsec and do normalization if required
        fIn = ROOT.TFile(self.output_file, "UPDATE")
        for dataset in self.datasets:
            hists = []
            dir_ = fIn.Get(dataset.name)
            keys = dir_.GetListOfKeys()

            fIn.cd(dataset.name)
            h_meta = dir_.Get("meta")
            h_meta.SetBinContent(3, dataset.xsec)
            hists.append(h_meta)

            if not self.norm:
                continue

            for key in keys:
                h = key.ReadObj()
                if key.GetName() == "meta":
                    continue
                h.Scale(dataset.xsec*self.lumi/h_meta.GetBinContent(1))
                hists.append(h)
            for h in hists:
                h.Write(f"", ROOT.TObject.kOverwrite)
            fIn.cd()
        fIn.Close()
        logger.info(f"Done, merged file written to {self.output_file}")


