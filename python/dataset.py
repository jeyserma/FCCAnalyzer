
import os
import json
import logging
import ROOT

logger = logging.getLogger("fcclogger")

class Dataset:

    def __init__(self, name, path, xsec, treeName="events", input_files=[]):
        self.name = name
        self.path = path
        self.xsec = xsec
        self.treeName = treeName
        self.input_files = input_files
        self.rootfiles = self.findROOTFiles(self.path)
        self.get_meta()

    def get_meta(self):
        fName = f"{self.path}/meta.json"
        if not os.path.exists(fName):
            logging.warning(f"No meta information exist for {self.name}, compute it on the fly")
            chain = ROOT.TChain(self.treeName)
            for f in self.rootfiles:
                chain.Add(f)
            df = ROOT.ROOT.RDataFrame(chain)
            self.total_files = len(self.rootfiles)
            self.total_events = df.Count().GetValue()
        else:
            f = open(fName)
            d = json.load(f)
            self.total_files = d['total_files']
            self.total_events = d['total_events']
        self.nevents_per_file = self.total_events / self.total_files

    def findROOTFiles(self, basedir, regex = ""):
        if ".root" in basedir: return [basedir]
        if regex != "":
            if basedir[-1] == "/": basedir = basedir[:-1]
            regex = basedir + "/" + regex

        files = []
        for root, directories, filenames in os.walk(basedir):
            for f in filenames:
                filePath = os.path.join(os.path.abspath(root), f)
                if not ".root" in filePath:
                    continue
                if len(self.input_files) > 0 and filePath not in self.input_files:
                    continue
                if regex == "" or fnmatch.fnmatch(filePath, regex):
                    files.append(filePath)
        return files
