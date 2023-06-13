

import sys,copy,array,os,math
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


def unrollHist():
    
    pass

if __name__ == "__main__":

    dim = 6 
    bins = 10
    nbins = math.pow(bins, dim)

    fIn = ROOT.TFile("tmp/nunuH.root")
    
    
    procs = ["Hbb", "Hcc", "Hss", "Hgg", "Htautau", "HWW", "HZZ", "WW", "ZZ", "Zqq"]
    hists = []
    
    for proc in procs:
        print(proc)
        
        # unroll 6-DIM hist to 1DIM-hist
        h = fIn.Get(f"{proc}/multi_dim_bdt")
        nbins = h.GetNbins()
        h_unroll = ROOT.TH1D(f"hist_{proc}", "", nbins, 0, nbins)
       
        for iBin in range(1, nbins+1):
            h_unroll.SetBinContent(iBin, h.GetBinContent(iBin))
            h_unroll.SetBinError(iBin, h.GetBinError(iBin))
        hists.append(copy.deepcopy(h_unroll))
        
    fIn.Close()
    
    
    fIn = ROOT.TFile("output.root", "RECREATE")
    for h in hists:
        h.Write()
    fIn.Close()
    