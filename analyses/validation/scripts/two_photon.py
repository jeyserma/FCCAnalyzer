
import sys
import os
import array
import math
import copy

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter


def makePlot(hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False, logx=False, norm=True):

    h1 = copy.deepcopy(fIn.Get(f"{p1}/{hName}"))
    h2 = copy.deepcopy(fIn.Get(f"{p2}/{hName}"))

    m1 = copy.deepcopy(fIn.Get(f"{p1}/meta"))
    m2 = copy.deepcopy(fIn.Get(f"{p1}/meta"))
    evc1 = m1.GetBinContent(1)
    evc2 = m2.GetBinContent(2)

    h1.Rebin(rebin)
    h2.Rebin(rebin)

    scale1 = h1.Integral()
    scale2 = h2.Integral()

    if scale1 == 0: scale1 = h1.Integral()
    if scale2 == 0: scale2 = h2.Integral()


    h1.SetLineColor(ROOT.kRed)
    h1.SetLineWidth(2)
    if norm: h1.Scale(1./scale1)

    h2.SetLineColor(ROOT.kBlue)
    h2.SetLineWidth(2)
    if norm: h2.Scale(1./scale2)

    leg = ROOT.TLegend(.2, 0.75, 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetMargin(0.12)
    leg.SetTextSize(0.035)
    leg.AddEntry(h1, l1, "L")
    leg.AddEntry(h2, l2, "L")
    
    h_ratio = h1.Clone("ratio")
    h_ratio.Divide(h2)
    h_ratio.SetLineColor(ROOT.kBlack)

    yRatio=1.15

    cfg = {

        'logy'              : logy,
        'logx'              : logx,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else 1.3*max([h1.GetMaximum(), h2.GetMaximum()]),
            
        'xtitle'            : xTitle,
        'ytitle'            : yTitle,
            
        'topRight'          : "#sqrt{s} = 91.2 GeV", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",

        'ratiofraction'     : 0.3,
        'ytitleR'           : "Data/MC",

        'yminR'             : 1-(yRatio-1),
        'ymaxR'             : yRatio,
    }

    ## top panel
    plotter.cfg = cfg
    canvas, padT, padB = plotter.canvasRatio()
    dummyT, dummyB, dummyL = plotter.dummyRatio()

    ## top panel
    canvas.cd()
    padT.Draw()
    padT.cd()
    padT.SetGrid()
    dummyT.Draw("HIST")


    h1.Draw("SAME HIST")
    h2.Draw("SAME HIST")
    leg.Draw("SAME")
    plotter.auxRatio()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    ## bottom panel
    canvas.cd()
    padB.Draw()
    padB.SetFillStyle(0)
    padB.cd()
    dummyB.Draw("HIST")
    dummyL.Draw("SAME")

    h_ratio.Draw("PE0 SAME") # E2 SAME
    #h_err_ratio.Draw("E2 SAME")

    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs("%s/%s.png" % (outDir, hName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, hName))
    canvas.Close()




if __name__ == "__main__":

    outDir = "/home/submit/jaeyserm/public_html/fccee/two_photon/baseline/"
    outDir = "/eos/user/j/jaeyserm/www/fccee/two_photon"
    fIn = ROOT.TFile("output_two_photon.root")

    p1, l1 = "wz3p6_ee_gaga_mumu_ecm91p2", "Whizard"
    #p1, l1 = "wz3p6_ee_gaga_mumu_ecm91p2_cfg1", "Whizard (cfg1)"
    p2, l2 = "p8_ee_gaga_mumu_ecm91p2", "Pythia8"

    #makePlot("photons_gen_p", 0, 5, 0, -1, "Gen photon momentum (GeV)", "Events (normalized)", rebin=2)
    
    makePlot("electrons_gen_no", 0, 10, 0, -1, "Number of gen electrons", "Events (normalized)", rebin=1)
    #makePlot("electrons_gen_p", 0, 50, 0, -1, "Gen electrons momentum (GeV)", "Events (normalized)", rebin=1)
    #makePlot("electrons_gen_theta", 3.1, 3.15, 0, -1, "Gen electrons #theta (GeV)", "Events (normalized)", rebin=1)
    #makePlot("electrons_gen_costheta", 0.95, 1, 0, -1, "Gen electrons |cos(#theta)| (GeV)", "Events (normalized)", rebin=1)

    makePlot("muons_gen_no", 0, 10, 0, -1, "Number of gen muons", "Events (normalized)", rebin=1)
    #makePlot("muons_gen_p", 0, 50, 0, -1, "Gen muons momentum (GeV)", "Events (normalized)", rebin=1)
    #makePlot("muons_gen_theta", 0, 3.15, 0, -1, "Gen muons #theta (GeV)", "Events (normalized)", rebin=1)
    #makePlot("muons_gen_costheta", 0.98, 1, 0, -1, "Gen muons |cos(#theta)| (GeV)", "Events (normalized)", rebin=1)

    #makePlot("dimuon_m", 0, 30, 0, -1, "mumu m (GeV)", "Events (normalized)", rebin=1)
    makePlot("digamma_m", 0, 30, 0, -1, "m(#gamma#gamma) (GeV)", "Events (normalized)", rebin=1)
    #makePlot("digamma_m_scaled", 0, 1, 1e-8, -1, "m(#gamma#gamma)/#sqrt{s} (GeV)", "Events (normalized)", rebin=1, logy=True)
    
    makePlot("gamma_leading_p", 0, 30, 0, -1, "Momentum leading #gamma (GeV)", "Events (normalized)", rebin=5)
    makePlot("gamma_leading_costheta", 0.995, 1, 0, -1, "|cos#theta| leading #gamma)", "Events (normalized)", rebin=1)
    makePlot("gamma_subleading_p", 0, 30, 0, -1, "Momentum subleading #gamma (GeV)", "Events (normalized)", rebin=5)
    makePlot("gamma_subleading_costheta", 0.995, 1, 0, -1, "|cos#theta| subleading #gamma", "Events (normalized)", rebin=1)

    makePlot("muons_gen_p_leading", 0, 30, 0, -1, "Momentum leading muon (GeV)", "Events (normalized)", rebin=5)
    makePlot("muons_gen_costheta_leading", 0.5, 1, 0, -1, "|cos#theta| leading muon", "Events (normalized)", rebin=20)
    makePlot("muons_gen_p_subleading", 0, 30, 0, -1, "Momentum subleading muon (GeV)", "Events (normalized)", rebin=5)
    makePlot("muons_gen_costheta_subleading", 0.5, 1, 0, -1, "|cos#theta| subleading muon", "Events (normalized)", rebin=20)

    makePlot("electrons_gen_p_leading", 0, 50, 0, -1, "Momentum leading electron (GeV)", "Events (normalized)", rebin=5)
    makePlot("electrons_gen_costheta_leading", 0.995, 1, 0, -1, "|cos#theta| leading electron", "Events (normalized)", rebin=1)
    makePlot("electrons_gen_p_subleading", 0, 50, 0, -1, "Momentum subleading electron (GeV)", "Events (normalized)", rebin=5)
    makePlot("electrons_gen_costheta_subleading", 0.995, 1, 0, -1, "|cos#theta| subleading electron", "Events (normalized)", rebin=1)

