
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


def makePlot(hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False, norm=True):

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

    cfg = {

        'logy'              : logy,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else 1.3*max([h1.GetMaximum(), h2.GetMaximum()]),
            
        'xtitle'            : xTitle,
        'ytitle'            : yTitle,
            
        'topRight'          : "#sqrt{s} = 91.2 GeV", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
    }

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")
        
    h1.Draw("SAME HIST")
    h2.Draw("SAME HIST")
    leg.Draw("SAME")
    plotter.aux()
    canvas.SetGrid()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs("%s/%s.png" % (outDir, hName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, hName))
    canvas.Close()




if __name__ == "__main__":

    outDir = "/home/submit/jaeyserm/public_html/fccee/two_photon/baseline/"
    fIn = ROOT.TFile("output_two_photon.root")

    p1, l1 = "wz3p6_ee_gaga_mumu_ecm91p2", "Whizard"
    p1, l1 = "wz3p6_ee_gaga_mumu_ecm91p2_cfg1", "Whizard (cfg1)"
    p2, l2 = "p8_ee_gaga_mumu_ecm91p2", "Pythia8"

    makePlot("photons_gen_p", 0, 5, 0, -1, "Gen photon momentum (GeV)", "Events (normalized)", rebin=1)
    
    makePlot("electrons_gen_no", 0, 10, 0, -1, "Number of gen electrons", "Events (normalized)", rebin=1)
    makePlot("electrons_gen_p", 0, 50, 0, -1, "Gen electrons momentum (GeV)", "Events (normalized)", rebin=1)
    makePlot("electrons_gen_theta", 3.1, 3.15, 0, -1, "Gen electrons #theta (GeV)", "Events (normalized)", rebin=1)
    #makePlot("electrons_gen_costheta", 0.95, 1, 0, -1, "Gen electrons |cos(#theta)| (GeV)", "Events (normalized)", rebin=1)

    makePlot("muons_gen_no", 0, 10, 0, -1, "Number of gen muons", "Events (normalized)", rebin=1)
    makePlot("muons_gen_p", 0, 50, 0, -1, "Gen muons momentum (GeV)", "Events (normalized)", rebin=1)
    makePlot("muons_gen_theta", 0, 3.15, 0, -1, "Gen muons #theta (GeV)", "Events (normalized)", rebin=1)
    makePlot("muons_gen_costheta", 0.98, 1, 0, -1, "Gen muons |cos(#theta)| (GeV)", "Events (normalized)", rebin=1)

    makePlot("dimuon_m", 0, 30, 0, -1, "mumu m (GeV)", "Events (normalized)", rebin=1)
    makePlot("digamma_m", 0, 30, 0, -1, "gaga m (GeV)", "Events (normalized)", rebin=1)
    makePlot("digamma_m_scaled", 0, 1, 1e-8, -1, "m(#gamma#gamma)/#sqrt{s} (GeV)", "Events (normalized)", rebin=1, logy=True)
    
    makePlot("gamma1_e", 0, 50, 0, -1, "#gamma 1 energy (GeV)", "Events (normalized)", rebin=1)
    makePlot("gamma1_theta", 0, 0.1, 0, -1, "#gamma 1 #theta (GeV)", "Events (normalized)", rebin=1)
    
    makePlot("gamma2_e", 0, 50, 0, -1, "#gamma 2 energy (GeV)", "Events (normalized)", rebin=1)
    makePlot("gamma2_theta", 3.05, 3.15, 0, -1, "#gamma 2 #theta (GeV)", "Events (normalized)", rebin=1)
    
    quit()
    makePlot("photons_no", 0, 10, 0, 0.2, "Multiplicity", "Events (normalized)", rebin=1) # 0.2
    makePlot("photons_phi", -5, 5, 0, 0.005, "#phi (rad)", "Events (normalized)", rebin=1)
    makePlot("photons_theta", 0, 3.14, 0, 0.015, "#theta (rad)", "Events (normalized)", rebin=1)
    
    #quit()
    makePlot("muons_p_cut0", 0, 100, 0, 0.05, "p (GeV)", "Events (normalized)", rebin=100)
    makePlot("muons_p_gen_cut0", 0, 100, 0, 0.05, "p (GeV)", "Events (normalized)", rebin=100)
    makePlot("muons_no_cut0", 0, 8, 0, 1, "Multiplicity", "Events (normalized)", rebin=1)
    makePlot("muons_phi_cut0", -5, 5, 0, 0.005, "#phi (rad)", "Events (normalized)", rebin=1)
    makePlot("muons_theta_cut0", 0, 3.14, 0, 0.015, "#theta (rad)", "Events (normalized)", rebin=1)
    makePlot("muons_eta_cut0", -3, 3, 0, 0.015, "#eta", "Events (normalized)", rebin=1)
    makePlot("muons_iso_cut0", 0, 1, 0.0001, 1, "Isolation", "Events (normalized)", rebin=2, logy=True)
    makeResolutionPlot("muons_reso_cut0", 0.98, 1.02, 0, 0.03, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)
    
    #makePlot("deltaR_gen_leps", 0, 10, 0, 0.01, "#DeltaR(leptons)", "Events (normalized)", rebin=1) # 0.15
    
    
    makePlot("photons_p", 0, 10, 0, 0.15, "p (GeV)", "Events (normalized)", rebin=10) # 0.15
    makePlot("photons_no", 0, 10, 0, 0.2, "Multiplicity", "Events (normalized)", rebin=1) # 0.2
    makePlot("photons_phi", -5, 5, 0, 0.005, "#phi (rad)", "Events (normalized)", rebin=1)
    makePlot("photons_theta", 0, 3.14, 0, 0.015, "#theta (rad)", "Events (normalized)", rebin=1)
    
    makePlot("gen_photons_p", 0, 5, 0, 0.2, "p (GeV)", "Events (normalized)", rebin=5) # 0.2
    makePlot("gen_photons_no", 0, 50, 0, 0.1, "Multiplicity", "Events (normalized)", rebin=1) # 0.1
    makePlot("gen_photons_phi", -5, 5, 0, 0.005, "#phi (rad)", "Events (normalized)", rebin=1)
    makePlot("gen_photons_theta", 0, 3.14, 0, 0.05, "#theta (rad)", "Events (normalized)", rebin=1)
    
    
    #makeResolutionPlot("muons_central_reso_cut0", 0.98, 1.02, 0, 0.006, "Muon resolution, central (p reco / gen)", "Events (normalized)", rebin=2)
    #makeResolutionPlot("muons_forward_reso_cut0", 0.98, 1.02, 0, 0.006, "Muon resolution, forward (p reco / gen)", "Events (normalized)", rebin=2)
    #makeResolutionPlot("muons_forward_m_reso_cut0", 0.98, 1.02, 0, 0.006, "Muon resolution, forward minus (p reco / gen)", "Events (normalized)", rebin=2)
    #makeResolutionPlot("muons_forward_p_reso_cut0", 0.98, 1.02, 0, 0.006, "Muon resolution, forward plus (p reco / gen)", "Events (normalized)", rebin=2)
    #makeResolutionPlot("prompt_muons_reso_cut0", 0.98, 1.02, 0, 0.006, "Prompt muon resolution (p reco / gen)", "Events (normalized)", rebin=2)
    
    #makeResolutionPlot("muons_0_30_reso_cut0", 0.98, 1.02, 0, 0.006, "Muon [0,30] resolution (p reco / gen)", "Events (normalized)", rebin=2)
    #makeResolutionPlot("muons_30_50_reso_cut0", 0.98, 1.02, 0, 0.006, "Muon [30,50] resolution (p reco / gen)", "Events (normalized)", rebin=2)
    #makeResolutionPlot("muons_50_70_reso_cut0", 0.98, 1.02, 0, 0.006, "Muon [50,70] resolution (p reco / gen)", "Events (normalized)", rebin=2)
    #makeResolutionPlot("muons_70_100_reso_cut0", 0.98, 1.02, 0, 0.006, "Muon [70,100] resolution (p reco / gen)", "Events (normalized)", rebin=2)

    #makePlot("prompt_muons_no_cut0", 0, 8, 0, 1, "Prompt muon multiplicity", "Events (normalized)", rebin=1)
    #makePlot("muons_central_theta_cut0", 0, 3.14, 0, 0.015, "Bare muon #theta, central", "Events (normalized)", rebin=1)
    #makePlot("muons_forward_theta_cut0", 0, 3.14, 0, 0.015, "Bare muon #theta, forward", "Events (normalized)", rebin=1)
    #makePlot("muons_forward_m_theta_cut0", 0, 3.14, 0, 0.015, "Bare muon #theta, forward minus", "Events (normalized)", rebin=1)
    #makePlot("muons_forward_p_theta_cut0", 0, 3.14, 0, 0.015, "Bare muon #theta, forward plus", "Events (normalized)", rebin=1)
    #makePlot("prompt_muons_theta_cut0", 0, 3.14, 0, 0.015, "Prompt muon #theta, forward", "Events (normalized)", rebin=1)
    
    makePlot("selected_muons_p_cut0", 0, 100, 0, 0.05, "p (GeV)", "Events (normalized)", rebin=100)
    makePlot("selected_muons_no_cut0", 0, 8, 0, 1, "Multiplicity", "Events (normalized)", rebin=1)
    makePlot("selected_muons_phi_cut0", -5, 5, 0, 0.005, "#phi (rad)", "Events (normalized)", rebin=1)
    makePlot("selected_muons_theta_cut0", 0, 3.14, 0, 0.015, "#theta (rad)", "Events (normalized)", rebin=1)
    makePlot("selected_muons_iso_cut0", 0, 1, 0.0001, 1, "Isolation", "Events (normalized)", rebin=2, logy=True)
    makeResolutionPlot("selected_muons_reso_cut0", 0.98, 1.02, 0, 0.006, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=2)
    #makeResolutionPlot("selected_muons_central_reso_cut0", 0.98, 1.02, 0, 0.006, "Selected muon resolution, central (p reco / gen)", "Events (normalized)", rebin=2)
    #makeResolutionPlot("selected_muons_forward_reso_cut0", 0.98, 1.02, 0, 0.006, "Selected muon resolution, forward (p reco / gen)", "Events (normalized)", rebin=2)
    
    

    makePlot("photons_p_cut3", 0, 10, 0, 0.15, "p (GeV)", "Events (normalized)", rebin=10) # 0.15
    makePlot("photons_no_cut3", 0, 10, 0, 0.2, "Multiplicity", "Events (normalized)", rebin=1) # 0.2
    makePlot("photons_theta_cut3", 0, 3.14, 0, 0.015, "#theta (rad)", "Events (normalized)", rebin=1)    
    
    makePlot("zed_leptonic_m_cut3", 60, 120, 0, 0.3, "m_{#mu^{#plus}, #mu^{#minus}} (Gev)", "Events (normalized)", rebin=1)
    makePlot("zed_leptonic_recoil_m_cut3", 120, 140, 0, 0.1, "Recoil (GeV)", "Events (normalized)", rebin=100)
    makePlot("zed_leptonic_p_cut3", 0, 100, 0, 0.1, "Recoil (GeV)", "Events (normalized)", rebin=1)
    makePlot("zed_leptonic_recoil_m_cut4", 120, 140, 0, 0.1, "Recoil (GeV)", "Events (normalized)", rebin=100)
    makePlot("zed_leptonic_recoil_m_cut5", 120, 140, 0, 0.1, "Recoil (GeV)", "Events (normalized)", rebin=100)
    makePlot("zed_leptonic_recoil_m_cut6", 120, 140, 0, 0.1, "Recoil (GeV)", "Events (normalized)", rebin=100)
    makePlot("mll_gen_leps", 80, 110, 0, 0.35, "m_{l^{#plus}, l^{#minus}}, gen (Gev)", "Events (normalized)", rebin=1)
    makePlot("missingMass", 0, 150, 0, -1, "Missing mass (Gev)", "Events (normalized)", rebin=1)

    