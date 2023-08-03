
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


#sys.path.insert(0, '/afs/cern.ch/work/j/jaeyserm/pythonlibs')
import plotter




def getHist(f, p, h):

    fIn = ROOT.TFile(f)
    hist = copy.deepcopy(fIn.Get("%s/%s" % (p, h)))
    fIn.Close()
    return hist

    
def makePlot(hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False, norm=True):

    h1 = getHist(f1, p1, hName)
    h2 = getHist(f2, p2, hName)
    
    m1 = getHist(f1, p1, "meta")
    m2 = getHist(f2, p2, "meta")
    evc1 = m1.GetBinContent(1)
    evc2 = m2.GetBinContent(2)
    
    print(evc1, evc2, h1.Integral(), h2.Integral())
    
    h1.Rebin(rebin)
    h2.Rebin(rebin)
    
    scale1 = h1.Integral()
    scale2 = h2.Integral()
    

    #scale1 = h1.GetBinContent(h1.GetXaxis().FindBin(125))
    #scale2 = h2.GetBinContent(h2.GetXaxis().FindBin(125))
    
    #print(scale1, scale2)
    
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
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
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




def makeResolutionPlot(hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False):

    h1 = getHist(f1, p1, hName)
    h2 = getHist(f2, p2, hName)
    
    h1.Rebin(rebin)
    h2.Rebin(rebin)
    
    h1.SetLineColor(ROOT.kRed)
    h1.SetLineWidth(2)
    #h_old.Scale(1./h_old.Integral(h_old.FindBin(0.9925/2.), h_old.FindBin(1.0025/2.)))
    h1.Scale(1./h1.Integral())
    
    h2.SetLineColor(ROOT.kBlue)
    h2.SetLineWidth(2)
    #h_new.Scale(1./h_new.Integral(h_new.FindBin(0.9925/2.), h_new.FindBin(1.0025/2.)))
    h2.Scale(1./h2.Integral())

    leg = ROOT.TLegend(.2, 0.75, 0.85, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.1)
    
    
    cfg = {

        'logy'              : logy,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else 1.3*max([h1.GetMaximum(), h2.GetMaximum()]),
            
        'xtitle'            : xTitle,
        'ytitle'            : yTitle,
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
    }
    
    a = h1.GetBinCenter(h1.FindFirstBinAbove(h1.GetMaximum()/2))
    b = h1.GetBinCenter(h1.FindLastBinAbove(h1.GetMaximum()/2))
    gauss1 = ROOT.TF1("gauss1", "gaus", a, b)
    h1.Fit("gauss1", "R")
    
    a = h2.GetBinCenter(h2.FindFirstBinAbove(h2.GetMaximum()/2))
    b = h2.GetBinCenter(h2.FindLastBinAbove(h2.GetMaximum()/2))    
    gauss2 = ROOT.TF1("gauss2", "gaus", a, b)
    h2.Fit("gauss2", "R")                  
                
    sigma1 = gauss1.GetParameter(2)
    sigma2 = gauss2.GetParameter(2)
    
    leg.AddEntry(h1, "%s (RMS=%.2f, #sigma=%.2f MeV)" % (l1, h1.GetRMS()*1000, sigma1*1000), "L")
    leg.AddEntry(h2, "%s (RMS=%.2f, #sigma=%.2f MeV)" % (l2, h2.GetRMS()*1000, sigma2*1000), "L")

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")
        
    h1.Draw("SAME HIST")
    h2.Draw("SAME HIST")
    
    gauss1.Draw("L SAME")
    gauss1.SetLineColor(ROOT.kBlack)
    
    gauss2.Draw("L SAME")
    gauss2.SetLineColor(ROOT.kBlack)
    
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

    #outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison_noIso"
    #fIn = ROOT.TFile("tmp/output_mass_xsec_noIso.root")
    
    #outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison_iso"
    #fIn = ROOT.TFile("tmp/output_mass_xsec_iso.root")
    
    
    f1, p1, l1 = "tmp/output_mass_xsec_mumu_allmuons.root", "wzp6_ee_mumuH_ecm240", "Spring 2021, muons"
    f2, p2, l2 = "tmp/output_mass_xsec_mumu.root", "wz2p6_ee_mumuH_ecm240_winter_v2", "Winter 2023, muons"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/spring2021_winter2023_isolation/"
    
    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Spring 2021, muons"
    f2, p2, l2 = "tmp/validation_mumu.root", "wz2p6_ee_mumuH_ecm240_winter_v2", "Winter 2023, muons"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/spring2021_winter2023/"
    
    
    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Winter 2023, muons"
    f2, p2, l2 = "tmp/validation_ee.root", "wzp6_ee_eeH_ecm240", "Winter 2023, electrons"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electron_muon/"
    
    f1, p1, l1 = "tmp/validation_mumu.root", "muon_gun", "Winter 2023, muon gun"
    f2, p2, l2 = "tmp/validation_mumu.root", "muon_gun", "Winter 2023, muon gun"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_gun/"
    
    #f1, p1, l1 = "tmp/output_mass_xsec_ee.root", "wzp6_ee_eeH_ecm240_winter", "Winter 2023, electrons"
    #f2, p2, l2 = "tmp/output_mass_xsec_ee.root", "wzp6_ee_eeH_ecm240_winter_v2", "Winter 2023, electrons, smeared"
    #outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electrons/"
    
    #makeResolutionPlot("muons_reso_cut0", 0.98, 1.02, 0, 0.03, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)
    
    f1, p1, l1 = "tmp/validation_mumu_2021.root", "p8_ee_ZZ_Zll_ecm240", "2021"
    f2, p2, l2 = "tmp/validation_mumu.root", "p8_ee_ZZ_Zll_ecm240", "2023"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/photon_2021_2023/"
    
    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Pre-winter, v2"
    f2, p2, l2 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240_winter", "Winter"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter_prewinter/"
    
    makePlot("photons_p", 0, 10, 0, 0.15, "p (GeV)", "Events (normalized)", rebin=10) # 0.15
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

    