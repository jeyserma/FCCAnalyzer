
import sys, os, glob, shutil, json, math, re, random
import concurrent.futures
import time
import ROOT
from dataset import Dataset
import argparse
import pathlib
import json
import logging

logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger("fcclogger")
logger.setLevel(logging.INFO)


ROOT.gROOT.SetBatch()
ROOT.gInterpreter.ProcessLine(".O3")

# load fcc libraries
logger.info("Load default cxx analyzers and libraries")
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

# load c++ macros
ROOT.gInterpreter.ProcessLine(".O3")
ROOT.gInterpreter.AddIncludePath(f"{pathlib.Path(__file__).parent}/../")
ROOT.gInterpreter.Declare('#include "include/defines.h"')
ROOT.gInterpreter.Declare('#include "include/utils.h"')
ROOT.gInterpreter.Declare('#include "include/gen.h"')

ROOT.TH1.SetDefaultSumw2(True)


def build_and_run(datadict, datasets_to_run, build_function, outfile, args, norm=False, lumi=1., treeName="events"):

    time0 = time.time()

    results = []
    hweights = []
    evtcounts = []
    chains = []
    datasets = []

    for datasetName in datasets_to_run:
        if not datasetName in datadict:
            logger.warning(f"Cannot find dataset {datasetName} in the datadict, skipping")

        xsec = datadict[datasetName]['xsec']
        path = f"{datadict['basePath']}/{datadict[datasetName]['path']}"
        if not os.path.exists(path):
            logger.warning(f"directory {path} does not exist, skipping")
            continue

        dataset = Dataset(datasetName, path, xsec)
        datasets.append(dataset)

        chain = ROOT.TChain(treeName)
        nFiles = 0
        for fpath in dataset.rootfiles:
            chain.Add(fpath)
            nFiles += 1
            if args.maxFiles > 0 and nFiles >= args.maxFiles: break
        logger.info(f"Imported dataset {datasetName} with {nFiles} files from directory {dataset.path}")

        chains.append(chain)
        df = ROOT.ROOT.RDataFrame(chain)
        evtcount = df.Count()
        res, hweight = build_function(df, dataset)

        results.append(res)
        hweights.append(hweight)
        evtcounts.append(evtcount)

    time_built = time.time()

    logger.info("Begin event loop")
    ROOT.ROOT.RDF.RunGraphs(evtcounts)
    logger.info("Done event loop")
    time_done_event = time.time()

    logger.info("Write output")
    fOut = ROOT.TFile(outfile, "RECREATE")
    for dataset, res, hweight, evtcount in zip (datasets, results, hweights, evtcounts):

        fOut.cd()
        fOut.mkdir(dataset.name)
        fOut.cd(dataset.name)

        histsToWrite = {}
        for r in res:
            hist = r.GetValue()
            hName = hist.GetName()
            if hist.GetName() in histsToWrite: # merge histograms in case histogram exists
                histsToWrite[hName].Add(hist)
            else:
                histsToWrite[hName] = hist

        for hist in histsToWrite.values():
            if norm:
                hist.Scale(dataset.xsec*lumi/evtcount.GetValue())
            hist.Write()

        h_meta = ROOT.TH1D("meta", "", 10, 0, 1)
        h_meta.SetBinContent(1, hweight.GetValue())
        h_meta.SetBinContent(2, evtcount.GetValue())
        h_meta.SetBinContent(3, dataset.xsec)
        h_meta.Write()
        logger.info(f"Processed {dataset.name}, number of events = {evtcount.GetValue()}, event weights = {hweight.GetValue()}, cross-section = {dataset.xsec}")

    time_done = time.time()

    fOut.cd()
    fOut.Close()

    logger.info("Done. Timing statistics:")
    logger.info(f"  Build graphs:     {time_built-time0}")
    logger.info(f"  Event loop:       {time_done_event-time_built}")
    logger.info(f"  Build results:    {time_done-time_done_event}")
    logger.info(f"  Write results:    {time.time()-time_done}")
    logger.info(f"  Total time:       {time.time()-time0}")
    logger.info(f"Output written to {outfile}")



def build_and_run_snapshot(datadict, datasets_to_run, build_function, outfile, args, treeName="events"):

    time0 = time.time()

    dataframes = []
    columns = []
    datasets = []
    eventCounts = []
    snapshots = []

    for datasetName in datasets_to_run:
        if not datasetName in datadict:
            logger.warning(f"Cannot find dataset {datasetName} in the datadict, skipping")

        xsec = datadict[datasetName]['xsec']
        path = f"{datadict['basePath']}/{datadict[datasetName]['path']}"
        if not os.path.exists(path):
            logger.warning(f"directory {path} does not exist, skipping")
            continue

        dataset = Dataset(datasetName, path, xsec)
        datasets.append(dataset)

        chain = ROOT.TChain(treeName)
        nFiles = 0
        for fpath in dataset.rootfiles:
            chain.Add(fpath)
            nFiles += 1
            if args.maxFiles > 0 and nFiles >= args.maxFiles: break
        logger.info(f"Imported dataset {datasetName} with {nFiles} files from directory {dataset.path}")

        df = ROOT.ROOT.RDataFrame(chain)
        evtcount = df.Count()
        df, cols = build_function(df, dataset)

        opts = ROOT.RDF.RSnapshotOptions()
        opts.fLazy = True # do not trigger the loop yet
        snapshot = df.Snapshot(treeName, outfile.format(datasetName=dataset.name), cols, opts)
        snapshots.append(snapshot)
        dataframes.append(df)
        columns.append(cols)
        eventCounts.append(evtcount)

    time_built = time.time()

    logger.info("Begin event loop")
    ROOT.ROOT.RDF.RunGraphs(snapshots)
    logger.info("Done event loop")
    time_done_event = time.time()

    logger.info("Write meta information")
    for dataset, df, cols, evtcount in zip (datasets, dataframes, columns, eventCounts):
        outfile_f = outfile.format(datasetName=dataset.name)
        logger.info(f"Processed {dataset.name}, number of events = {evtcount.GetValue()}, cross-section = {dataset.xsec}, output {outfile_f}")

        fIn = ROOT.TFile(outfile_f, "UPDATE")
        h_meta = ROOT.TH1D("meta", "", 10, 0, 1)
        h_meta.SetBinContent(2, evtcount.GetValue())
        h_meta.SetBinContent(3, dataset.xsec)
        h_meta.Write()
        fIn.Close()

    time_done = time.time()
    logger.info("Done. Timing statistics:")
    logger.info(f"  Build graphs:     {time_built-time0}")
    logger.info(f"  Event loop:       {time_done_event-time_built}")
    logger.info(f"  Write meta info:  {time.time()-time_done}")
    logger.info(f"  Total time:       {time.time()-time0}")



def build_and_run_snapshot_mt(datadict, build_function, outfile, maxFiles=-1, treeName="events"):

    time0 = time.time()
    
    dataframes = []
    columns = []
    datasets = []
    eventCounts = []

    for val in datadict:
    
        if not os.path.exists(val['datadir']):
            print(f"WARNING: directory {val['datadir']} does not exist, skipping dataset {val['name']}")
            continue

        dataset = Dataset(val)
        datasets.append(dataset)
        print(f"Read {dataset.name}")

        chain = ROOT.TChain(treeName)
        nFiles = 0
        for fpath in dataset.rootfiles:
            chain.Add(fpath)
            nFiles += 1
            if maxFiles > 0 and nFiles >= maxFiles: break
        print(f"Import {dataset.name} with {nFiles} files from directory {dataset.datadir}")

        df = ROOT.ROOT.RDataFrame(chain)
        #df.SetName(f"df_{dataset.name}")
        evtcount = df.Count()
        df, cols = build_function(df, dataset)
        dataframes.append(df)
        columns.append(cols)
        eventCounts.append(evtcount)
        
    time_built = time.time()

    def runGraph(dataset, df, cols):
        df.Snapshot(treeName, outfile.format(datasetName=dataset.name), cols)
    
    print("Run processes")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(runGraph, dataset, df, cols) for dataset, df, cols in zip (datasets, dataframes, columns)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            
    time_done_event = time.time()
    
    print("Write meta information")
    for dataset, df, cols, evtcount in zip (datasets, dataframes, columns, eventCounts):
    
        print(f" -> {dataset.name} done, number of events = {evtcount.GetValue()}, cross-section = {dataset.xsec}")
        
        fIn = ROOT.TFile(outfile.format(datasetName=dataset.name), "UPDATE")
        h_meta = ROOT.TH1D("meta", "", 10, 0, 1)
        h_meta.SetBinContent(2, evtcount.GetValue())
        h_meta.SetBinContent(3, dataset.xsec)
        h_meta.Write()
        fIn.Close()
    
    time_done = time.time()
    print("Done")
    print("build graphs:", time_built - time0)
    print("event loop:", time_done_event - time_built)
    print("write meta info:", time.time() - time_done)
    print("total time:", time.time() - time0)
    

def make_def_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
    parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
    return parser
 
def add_include_file(fIn):
    ROOT.gInterpreter.Declare(f'#include "{fIn}"')
 
def set_threads(args):
    ROOT.EnableImplicitMT()
    if args.nThreads: 
        ROOT.DisableImplicitMT()
        ROOT.EnableImplicitMT(int(args.nThreads))
    logger.info(f"Run over {ROOT.GetThreadPoolSize()} threads")

def get_hostname():
    import socket
    return socket.gethostname()

def get_basedir(sel=None):

    basedirs = {}
    basedirs['mit'] = "/data/submit/cms/store/fccee/" # "/scratch/submit/cms/fcc/samples/"
    basedirs['cmswmass2'] = "/data/shared/jaeyserm/fccee/"
    basedirs['fcc_eos'] = "/eos/experiment/fcc/ee/generation/DelphesEvents/"
    
    if sel: return basedirs[sel]
    else:
        hostname = get_hostname()
        if "mit.edu" in hostname: return basedirs['mit']
        if "cmswmass2" in hostname: return basedirs['cmswmass2']
        if "lxplus" in hostname: return basedirs['fcc_eos']
    return basedirs['fcc_eos']
    
    
def filter_datasets(datasets, filt=None):

    if isinstance(filt, str): return [dataset for dataset in datasets if fnmatch.fnmatch(dataset['name'], filt)]
    elif isinstance(filt, list): 
        ret = []
        for dataset in datasets:
            if dataset['name'] in filt: ret.append(dataset)
        return ret
    else: return datasets

    
def findROOTFiles(basedir, regex = ""):
        
    if ".root" in basedir: return [basedir] # single file
    if regex != "":
        if basedir[-1] == "/": basedir = basedir[:-1]
        regex = basedir + "/" + regex

    files = []
    for root, directories, filenames in os.walk(basedir):
        for f in filenames:
            if not ".root" in f:
                continue
            filePath = os.path.join(os.path.abspath(root), f)
            if regex == "" or fnmatch.fnmatch(filePath, regex): files.append(filePath)
                
    return files

def get_datadicts(campaign="winter2023"):
    basedirs = {}
    basedirs['mit'] = "/data/submit/cms/store/fccee/samples/"

    hostname = get_hostname()
    if "mit.edu" in hostname: basedir = basedirs['mit']
    else: basedir = ""
    catalog = f'{basedir}/{campaign}/catalog.json'
    f = open(catalog)
    datadict = json.load(f)
    datadict['basePath'] = os.path.dirname(catalog)
    return datadict