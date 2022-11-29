
import sys, os, glob, shutil, json, math, re, random
import time
import ROOT
from dataset import Dataset

ROOT.TH1.SetDefaultSumw2(True)


def build_and_run(datadict, build_function, outfile, maxFiles=-1, norm=False, lumi=1.):
    time0 = time.time()

    results = []
    hweights = []
    evtcounts = []
    chains = []
    datasets = []

    for val in datadict:

        dataset = Dataset(val)
        datasets.append(dataset)

        chain = ROOT.TChain("events")
        nFiles = 0
        for fpath in dataset.rootfiles:
            chain.Add(fpath)
            nFiles += 1
            if maxFiles > 0 and nFiles >= maxFiles: break
        nEvents = chain.GetEntries()
        print(f"Import {dataset.name} with {nFiles} files and {nEvents} events")
    
        # black magic why this needs to be protected from gc
        chains.append(chain)

        df = ROOT.ROOT.RDataFrame(chain)

        evtcount = df.Count()
        res, hweight = build_function(df, dataset)

        results.append(res)
        hweights.append(hweight)
        evtcounts.append(evtcount)

    time_built = time.time()

    print("Begin event loop")
    ROOT.ROOT.RDF.RunGraphs(evtcounts)
    print("Done event loop")
    time_done_event = time.time()
    
    print("Write output")
    fOut = ROOT.TFile(outfile, "RECREATE")
    for dataset, res, hweight, evtcount in zip (datasets, results, hweights, evtcounts):
        
        fOut.cd()
        fOut.mkdir(dataset.name)
        fOut.cd(dataset.name)

        for r in res:
            hist = r.GetValue()
            if norm:
                hist.Scale(dataset.xsec*lumi/evtcount.GetValue())
            hist.Write()
            
        h_meta = ROOT.TH1D("meta", "", 10, 0, 1)
        h_meta.SetBinContent(1, hweight.GetValue())
        h_meta.SetBinContent(2, evtcount.GetValue())
        h_meta.SetBinContent(3, dataset.xsec)
        h_meta.Write()

    time_done = time.time()
    
    fOut.cd()
    fOut.Close()
    
    print("Done")

    print("build graphs:", time_built - time0)
    print("event loop:", time_done_event - time_built)
    print("build results:", time_done - time_done_event)
    print("write results:", time.time() - time_done)
    print("total time:", time.time() - time_built)
    

   
