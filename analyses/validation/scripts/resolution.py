
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
    
    print(evc1, evc2, m1.Integral(), m2.Integral())
    
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



def resolution(outName, hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False):

    h1 = getHist(f1, p1, hName)
    h2 = getHist(f2, p2, hName)
    
    print(h1.Integral())
    print(h2.Integral())
    
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
    #a, b = 0.98, 1.02
    gauss1 = ROOT.TF1("gauss1", "gaus", a, b)
    h1.Fit("gauss1", "R")
    
    a = h2.GetBinCenter(h2.FindFirstBinAbove(h2.GetMaximum()/2))
    b = h2.GetBinCenter(h2.FindLastBinAbove(h2.GetMaximum()/2))    
    #a, b = 0.98, 1.02
    gauss2 = ROOT.TF1("gauss2", "gaus", a, b)
    h2.Fit("gauss2", "R")                  
                
    sigma1 = gauss1.GetParameter(2)
    sigma2 = gauss2.GetParameter(2)
    sigma1_err = gauss1.GetParError(2)
    sigma2_err = gauss2.GetParError(2)
    
    leg.AddEntry(h1, "%s, RMS=%.2f #pm %.2f, #sigma=%.2f #pm %.2f" % (l1, h1.GetRMS()*1000., h1.GetRMSError()*1000., sigma1*1000., sigma1_err*1000.), "L")
    leg.AddEntry(h2, "%s, RMS=%.2f #pm %.2f, #sigma=%.2f #pm %.2f" % (l2, h2.GetRMS()*1000., h2.GetRMSError()*1000., sigma2*1000., sigma2_err*1000.), "L")

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

    canvas.SaveAs("%s/%s.png" % (outDir, outName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, outName))
    canvas.Close()


def resolutionVsTheta(xMin, xMax, yMin, yMax, xTitle, yTitle, logy=False):

    hName = "muons_theta_reso_cut0"
    
    h1_ = getHist(f1, p1, hName)
    h2_ = getHist(f2, p2, hName)
    rebin = 10
    
    h1_sigma = ROOT.TGraphErrors()
    h1_rms = ROOT.TGraphErrors()
    h2_sigma = ROOT.TGraphErrors()
    h2_rms = ROOT.TGraphErrors()
    
    ratio_sigma = ROOT.TGraphErrors()
    ratio_rms = ROOT.TGraphErrors()
    
    xbins = h1_.ProjectionX("xbins")
    
    iPoint = 0
    for thBin in range(1, h1_.GetNbinsX()+1):
    
        h1 = h1_.ProjectionY("h1_%d"%thBin, thBin, thBin)
        h2 = h2_.ProjectionY("h2_%d"%thBin, thBin, thBin)
        
        h1.Rebin(rebin)
        h2.Rebin(rebin)
        
        if h1.Integral() <= 0 or h2.Integral() <= 0: continue
        print(thBin, h1.GetRMS(), h2.GetRMS(), h2.GetRMS()/h1.GetRMS() if h2.GetRMS() > 0 else 0)
        
        

        h1.SetLineColor(ROOT.kRed)
        h1.SetLineWidth(2)
        h1.Scale(1./h1.Integral())
        
        h2.SetLineColor(ROOT.kBlue)
        h2.SetLineWidth(2)
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
            'ymax'              : 1.3*max([h1.GetMaximum(), h2.GetMaximum()]),
                
            'xtitle'            : xTitle,
            'ytitle'            : yTitle,
                
            'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
            'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
        }
        
        a = h1.GetBinCenter(h1.FindFirstBinAbove(h1.GetMaximum()/2))
        b = h1.GetBinCenter(h1.FindLastBinAbove(h1.GetMaximum()/2))
        a, b = 0.98, 1.02
        gauss1 = ROOT.TF1("gauss1", "gaus", a, b)
        h1.Fit("gauss1", "R")
        
        a = h2.GetBinCenter(h2.FindFirstBinAbove(h2.GetMaximum()/2))
        b = h2.GetBinCenter(h2.FindLastBinAbove(h2.GetMaximum()/2))
        a, b = 0.98, 1.02
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

        canvas.SaveAs("%s/resolution_thetaBin%d.png" % (outDir, thBin))
        canvas.SaveAs("%s/resolution_thetaBin%d.pdf" % (outDir, thBin))
        canvas.Close()
        
        
        h1_sigma.SetPoint(iPoint, xbins.GetBinCenter(thBin), sigma1*1000.)
        h2_sigma.SetPoint(iPoint, xbins.GetBinCenter(thBin), sigma2*1000.)
        h1_sigma.SetPointError(iPoint, 0, gauss1.GetParError(2)*1000.)
        h2_sigma.SetPointError(iPoint, 0, gauss2.GetParError(2)*1000.)
        
        h1_rms.SetPoint(iPoint, xbins.GetBinCenter(thBin), h1.GetRMS()*1000.)
        h2_rms.SetPoint(iPoint, xbins.GetBinCenter(thBin), h2.GetRMS()*1000.)
        h1_rms.SetPointError(iPoint, 0, h1.GetRMSError()*1000.)
        h2_rms.SetPointError(iPoint, 0, h2.GetRMSError()*1000.)
        
        s_sigma = sigma2/sigma1
        s_rms = h2.GetRMS()/h1.GetRMS()
        ratio_sigma.SetPoint(iPoint, xbins.GetBinCenter(thBin), s_sigma)
        ratio_rms.SetPoint(iPoint, xbins.GetBinCenter(thBin), s_rms)
        
        print(s_rms, s_sigma)
        ratio_sigma.SetPointError(iPoint, 0, s_sigma*((gauss1.GetParError(2)/sigma1)**2 + (gauss2.GetParError(2)/sigma2)**2)**0.5)
        ratio_rms.SetPointError(iPoint, 0, s_rms*((h1.GetRMSError()/h1.GetRMS())**2 + (h2.GetRMSError()/h2.GetRMS())**2)**0.5)
        
        iPoint += 1
        #if iPoint > 10: break
        
    leg = ROOT.TLegend(.4, 0.7, 0.90, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.1)
        
        
    cfg = {

        'logy'              : logy,
        'logx'              : False,
            
        'xmin'              : 0,
        'xmax'              : 1.6,
        'ymin'              : 0,
        'ymax'              : 20,
                
        'xtitle'            : "|#theta| (rad)",
        'ytitle'            : "Resolution (MeV)",
                
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
    }
        
           
    leg.AddEntry(h1_sigma, "%s, #sigma" % l1, "LP")
    leg.AddEntry(h2_sigma, "%s, #sigma" % l2, "LP")
    
    leg.AddEntry(h1_rms, "%s, RMS" % l1, "LP")
    leg.AddEntry(h2_rms, "%s, RMS" % l2, "LP")

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")
   
    
    h1_sigma.SetLineColor(ROOT.kBlack)
    h1_sigma.SetLineWidth(2)
    h1_sigma.SetMarkerStyle(20)
    h1_sigma.SetMarkerSize(1)
    h1_sigma.SetMarkerColor(ROOT.kBlack)
    
    h1_rms.SetLineColor(ROOT.kBlue)
    h1_rms.SetLineWidth(2)
    h1_rms.SetMarkerStyle(22)
    h1_rms.SetMarkerSize(1)
    h1_rms.SetMarkerColor(ROOT.kBlue)
    
    h2_sigma.SetLineColor(ROOT.kRed)
    h2_sigma.SetLineWidth(2)
    h2_sigma.SetMarkerStyle(20)
    h2_sigma.SetMarkerSize(1)
    h2_sigma.SetMarkerColor(ROOT.kRed)
    
    h2_rms.SetLineColor(ROOT.kGreen+1)
    h2_rms.SetLineWidth(2)
    h2_rms.SetMarkerStyle(22)
    h2_rms.SetMarkerSize(1)
    h2_rms.SetMarkerColor(ROOT.kGreen+1)
    
    h1_sigma.Draw("SAME LP")
    h2_sigma.Draw("SAME LP")
    h1_rms.Draw("SAME LP")
    h2_rms.Draw("SAME LP")

        
    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs("%s/resolution.png" % outDir)
    canvas.SaveAs("%s/resolution.pdf" % outDir)
    canvas.Close()
    
    ########### RATIO
    leg = ROOT.TLegend(.4, 0.8, 0.90, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.1)
        
        
    cfg = {

        'logy'              : logy,
        'logx'              : False,
            
        'xmin'              : 0,
        'xmax'              : 1.6,
        'ymin'              : 0,
        'ymax'              : 3,
                
        'xtitle'            : "|#theta| (rad)",
        'ytitle'            : "Ratio",
                
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
    }
        
           
    leg.AddEntry(ratio_sigma, "Ratio #sigma", "LP")
    leg.AddEntry(ratio_rms, "Ratio RMS", "LP")
    

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")
    
    ratio_sigma.SetLineColor(ROOT.kBlack)
    ratio_sigma.SetLineWidth(2)

    ratio_rms.SetLineColor(ROOT.kGreen+2)
    ratio_rms.SetLineWidth(2)
    
    ratio_rms.Draw("SAME L")
    ratio_sigma.Draw("SAME L")
        
    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs("%s/resolution_ratio.png" % outDir)
    canvas.SaveAs("%s/resolution_ratio.pdf" % outDir)
    canvas.Close()
    
    
if __name__ == "__main__":


    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Winter 2023, muons"  # wzp6_ee_mumuH_ecm240 p8_ee_ZZ_Zll_ecm240
    f2, p2, l2 = "tmp/validation_ee.root", "wzp6_ee_eeH_ecm240", "Winter 2023, electrons" # wzp6_ee_eeH_ecm240 p8_ee_ZZ_Zll_ecm240
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electron_muon_resolution/"
    
    
    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Winter 2023, muons"  # wzp6_ee_mumuH_ecm240 p8_ee_ZZ_Zll_ecm240
    f2, p2, l2 = "tmp/validation_ee.root", "wzp6_ee_eeH_ecm240_v1", "Winter 2023, electrons (v1)" # wzp6_ee_eeH_ecm240 p8_ee_ZZ_Zll_ecm240
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electronv1_muon_resolution/"
    #resolutionVsTheta(0.98, 1.02, 0, 0.03, "Resolution (p_{reco}/p_{gen})", "Events (normalized)")
    
    
    #let's say the factor is around 1.95, close to 2, but systematically lower than 2
    
    '''
    f1, p1, l1 = "tmp/validation_mumu.root", "muon_gun", "Muon"
    f2, p2, l2 = "tmp/validation_ee.root", "electron_gun", "Electron"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_gun/"
    resolution("muons_electrons", "muons_reso_cut0", 0.98, 1.02, 0, -1, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)

    f1, p1, l1 = "tmp/validation_mumu.root", "muon_gun_smear2x", "Muon (2x)"
    f2, p2, l2 = "tmp/validation_ee.root", "electron_gun", "Electron"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_gun/"
    resolution("muons2x_electrons", "muons_reso_cut0", 0.98, 1.02, 0, -1, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)
    
    '''
    
    f1, p1, l1 = "tmp/validation_mumu_prewinter.root", "wzp6_ee_mumuH_ecm240", "Muons pre-winter 2023"
    f2, p2, l2 = "tmp/validation_mumu_winter.root", "wzp6_ee_mumuH_ecm240", "Muons winter 2023"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/prewinter_winter2023/"
    resolution("mu_prewinter_winter", "muons_reso_cut0", 0.98, 1.02, 0, -1, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)
    quit()
    
    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Muons"
    f2, p2, l2 = "tmp/validation_ee.root", "wzp6_ee_eeH_ecm240_v1", "Electrons (v1)"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electron_muon_res/"
    resolution("mu_el_v1", "muons_reso_cut0", 0.98, 1.02, 0, -1, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)

    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Muons"
    f2, p2, l2 = "tmp/validation_ee.root", "wzp6_ee_eeH_ecm240_v2", "Electrons (v2)"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electron_muon_res/"
    resolution("mu_el_v2", "muons_reso_cut0", 0.98, 1.02, 0, -1, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)


    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Muons"
    f2, p2, l2 = "tmp/validation_ee.root", "wzp6_ee_eeH_ecm240_v3", "Electrons (v3)"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electron_muon_res/"
    resolution("mu_el_v3", "muons_reso_cut0", 0.98, 1.02, 0, -1, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)

    f1, p1, l1 = "tmp/validation_mumu.root", "wzp6_ee_mumuH_ecm240", "Muons"
    f2, p2, l2 = "tmp/validation_ee.root", "wzp6_ee_eeH_ecm240_v4", "Electrons (v4)"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electron_muon_res/"
    resolution("mu_el_v4", "muons_reso_cut0", 0.98, 1.02, 0, -1, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)