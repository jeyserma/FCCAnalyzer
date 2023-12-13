
import sys,copy,array,os,subprocess,math
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter




if __name__ == "__main__":

    mode = "IDEA"
    lumi = "7p2" 

    lumi_suffix =  "" if lumi == "7p2" else "_LUMI_%s"%lumi
    combineDir = "combine/run/%s%s" % (mode, lumi_suffix)
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass/combine/"
    topRight = "#sqrt{s} = 240 GeV"
    lumis = ["2p5", "5", "7p2", "10", "15"]
    sf = lumiDict[lumi]

    combineOptions = ""
    freezeParameters = []
    setParameters = []
    suffix=""