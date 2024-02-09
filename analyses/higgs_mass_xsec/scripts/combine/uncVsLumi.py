
import sys,copy,array,os,subprocess,math
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter




if __name__ == "__main__":
    outDir_ = "/work/submit/jaeyserm/public_html/fccee/ZH_mass/combine_out/"
    lumis = ["1", "2p5", "5", "7p2", "10", "15", "20"]

    gStat = ROOT.TGraph()
    gSyst = ROOT.TGraph()
    gTot = ROOT.TGraph()

    for i, lumi in enumerate(lumis):
        lumi_ = float(lumi.replace("p", "."))
        combineDir = f"/work/submit/jaeyserm/public_html/fccee/ZH_mass/combine_out/IDEA_LUMI_{lumi}/mumu_ee_combined_categorized/"

        fStat = float(open(f"{combineDir}/mass_stat.txt", "r").readlines()[0].rstrip().split()[2])*1000.
        fTot = float(open(f"{combineDir}/mass.txt", "r").readlines()[0].rstrip().split()[2])*1000.
        fSyst = (fTot**2 - fStat**2)**0.5

        gStat.SetPoint(i, lumi_, fStat)
        gSyst.SetPoint(i, lumi_, fSyst)
        gTot.SetPoint(i, lumi_, fTot)

    leg = ROOT.TLegend(.3, 0.75, 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)

    gTot.SetLineColor(ROOT.kBlack)
    gTot.SetMarkerColor(ROOT.kBlack)
    gTot.SetMarkerStyle(8)
    gTot.SetMarkerSize(1)
    gTot.SetLineWidth(2)
    leg.AddEntry(gTot, "Total uncertainty", "L")
    
    gStat.SetLineColor(ROOT.kBlue)
    gStat.SetMarkerColor(ROOT.kBlue)
    gStat.SetMarkerStyle(8)
    gStat.SetLineWidth(2)
    leg.AddEntry(gStat, "Statistical uncertainty", "L")

    gSyst.SetLineColor(ROOT.kRed)
    gSyst.SetMarkerColor(ROOT.kRed)
    gSyst.SetMarkerStyle(8)
    gSyst.SetLineWidth(2)
    leg.AddEntry(gSyst, "Systematic uncertainty", "L")

    cfg = {

        'logy'              : False,
        'logx'              : False,

        'xmin'              : 1,
        'xmax'              : 20,
        'ymin'              : 0,
        'ymax'              : 10,

        'xtitle'            : "Integrated Luminosity (ab^{-1})",
        'ytitle'            : "Higgs mass uncertainty (MeV)",

        'topRight'          : "#sqrt{s} = 240 GeV", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",

    }

    plotter.cfg = cfg
    canvas = plotter.canvas()

    dummy = plotter.dummy()
    dummy.Draw("HIST")

    gSyst.Draw("LP SAME")
    gStat.Draw("LP SAME")
    gTot.Draw("LP SAME")

    leg.Draw("SAME")
    canvas.SetGrid()
    canvas.Modify()
    canvas.Update()

    plotter.aux()
    ROOT.gPad.SetTicks()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs(f"{outDir_}/uncVsLumi_IDEA.png")
    canvas.SaveAs(f"{outDir_}/uncVsLumi_IDEA.pdf")
    canvas.Close()