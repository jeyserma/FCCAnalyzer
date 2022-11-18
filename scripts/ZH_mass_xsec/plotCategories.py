
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


import plotter




def getHist(f, p, h):

    fIn = ROOT.TFile(f)
    hist = copy.deepcopy(fIn.Get("%s/%s" % (p, h)))
    fIn.Close()
    return hist

    
def makePlot(fIn_, flavor, doNorm=False):



    outName = "zll_recoil_m_categories"
    proc = "wzp6_ee_mumuH_ecm240"
    hist = "zll_recoil_m"
    rebin = 50

    fIn = ROOT.TFile(fIn_)
    zll_recoil_m = fIn.Get("%s/%s" % (proc, hist))
    
    h_cat1 = zll_recoil_m.ProjectionX("h_cat1", 1, 1)
    h_cat2 = zll_recoil_m.ProjectionX("h_cat2", 2, 2)
    h_cat3 = zll_recoil_m.ProjectionX("h_cat3", 3, 3)
    
    if doNorm: 
        outName += "_norm"
        h_cat1.Scale(1./h_cat1.Integral())
        h_cat2.Scale(1./h_cat2.Integral())
        h_cat3.Scale(1./h_cat3.Integral())
    
    h_cat1.Rebin(rebin)
    h_cat2.Rebin(rebin)
    h_cat3.Rebin(rebin)

    
    h_cat1.SetLineColor(ROOT.kRed)
    h_cat2.SetLineColor(ROOT.kBlue)
    h_cat3.SetLineColor(ROOT.kGreen+1)

    h_cat1.SetLineWidth(2)
    h_cat2.SetLineWidth(2)
    h_cat3.SetLineWidth(2)


    leg = ROOT.TLegend(.2, 0.75, 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetMargin(0.12)
    leg.SetTextSize(0.035)
    leg.AddEntry(h_cat1, "Leptons central", "L")
    leg.AddEntry(h_cat2, "Leptons central+forward", "L")
    leg.AddEntry(h_cat3, "Leptons forward", "L")

    cfg = {

        'logy'              : False,
        'logx'              : False,
        
        'xmin'              : 120,
        'xmax'              : 140,
        'ymin'              : 0,
        'ymax'              : 1.4*max([h_cat1.GetMaximum(), h_cat2.GetMaximum(), h_cat3.GetMaximum()]),
            
        'xtitle'            : "Recoil mass (GeV)",
        'ytitle'            : "Events",
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
    }

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")
        
    h_cat1.Draw("SAME HIST")
    h_cat2.Draw("SAME HIST")
    h_cat3.Draw("SAME HIST")
    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs("%s/%s.png" % (outDir, outName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, outName))
    canvas.Close()


def doFit(fIn_, flavor, cat=1):

    recoilMin = 120
    recoilMax = 140
    
    outName = "zll_recoil_m_categories"
    proc = "wzp6_ee_mumuH_ecm240"
    hist = "zll_recoil_m"
    rebin = 50

    fIn = ROOT.TFile(fIn_)
    zll_recoil_m = fIn.Get("%s/%s" % (proc, hist))
    
    hist_zh = zll_recoil_m.ProjectionX("hist", cat, cat)   



    recoilmass = ROOT.RooRealVar("zed_leptonic_recoil_m", "Recoil mass (GeV)", 125, recoilMin, recoilMax)
    
    param_yield, param_mh, param_mean, param_mean_gt, param_sigma, param_sigma_gt, param_alpha_1, param_alpha_2, param_n_1, param_n_2, param_cb_1, param_cb_2 = [], [], [], [], [], [], [], [], [], [], [], []
    param_yield_err, param_mean_err, param_sigma_err, param_mean_gt_err, param_sigma_gt_err, param_alpha_1_err, param_alpha_2_err, param_n_1_err, param_n_2_err, param_cb_1_err, param_cb_2_err  = [], [], [], [], [], [], [], [], [], [], []

    # recoil mass plot settings
    cfg = {

        'logy'              : False,
        'logx'              : False,
    
        'xmin'              : recoilMin,
        'xmax'              : recoilMax,
        'ymin'              : 0,
        'ymax'              : 25000,
        
        'xtitle'            : "Recoil mass (GeV)",
        'ytitle'            : "Events / 1 MeV",
        
        'topRight'          : "ZH, #sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Internal}}",
        
        'ratiofraction'     : 0.25,
        'ytitleR'           : "Pull",
        'yminR'             : -3.5,
        'ymaxR'             : 3.5,
    }
   

        
    mH = 125
    mH_ = ("%.2f" % mH).replace(".", "p")

     

     
    #hist_zh.Scale(lumi*ds.datasets[proc]['xsec']*1e6/ds.datasets[proc]['nevents'])
    rdh_zh = ROOT.RooDataHist("rdh_zh_%s" % mH_, "rdh_zh", ROOT.RooArgList(recoilmass), ROOT.RooFit.Import(hist_zh))
    yield_zh = rdh_zh.sum(False)
    


        
    # IDEA
     
    mean = ROOT.RooRealVar("mean_%s" % mH_, '', 1.25086e+02, mH-1., mH+1.)
    sigma = ROOT.RooRealVar("sigma_%s" % mH_, '', 4.10819e-01, 0, 1)
    #sigma = ROOT.RooRealVar("sigma_%s" % mH_, '', 4.1e-01) # fixed
    alpha_1 = ROOT.RooRealVar("alpha_1_%s" % mH_, '', -1.39903e-01, -10, 0)
    #alpha_1 = ROOT.RooRealVar("alpha_1_%s" % mH_, '', -0.14322)
    alpha_2 = ROOT.RooRealVar("alpha_2_%s" % mH_, '', 3.65257e+00, 0, 10)
    #alpha_2 = ROOT.RooRealVar("alpha_2_%s" % mH_, '', 3.60)
    n_1 = ROOT.RooRealVar("n_1_%s" % mH_, '', 2.35540e+00, -10, 10)
    #n_1 = ROOT.RooRealVar("n_1_%s" % mH_, '', 3.90)
    n_2 = ROOT.RooRealVar("n_2_%s" % mH_, '', 4.51050e-01, -10, 10)
    #n_2 = ROOT.RooRealVar("n_2_%s" % mH_, '', 0.6)

    mean_gt = ROOT.RooRealVar("mean_gt_%s" % mH_, '', 1.25442e+02, recoilMin, recoilMax)
    sigma_gt = ROOT.RooRealVar("sigma_gt_%s" % mH_, '', 8.47732e-01, 0, 1)
    #sigma_gt = ROOT.RooRealVar("sigma_gt_%s" % mH_, '', 0.842) # fixed  
        
    cb_1 = ROOT.RooRealVar("cb_1_%s" % mH_, '', 3.96333e-01 , 0, 1)
    cb_2 = ROOT.RooRealVar("cb_2_%s" % mH_, '', 4.75471e-01 , 0, 1)
        
        
       
            
        
    # construct the 2CBG and perform the fit: pdf = cb_1*cbs_1 + cb_2*cbs_2 + gauss (cb_1 and cb_2 are the fractions, floating)
    cbs_1 = ROOT.RooCBShape("CrystallBall_1_%s" % mH_, "CrystallBall_1", recoilmass, mean, sigma, alpha_1, n_1) # first CrystallBall
    cbs_2 = ROOT.RooCBShape("CrystallBall_2_%s" % mH_, "CrystallBall_2", recoilmass, mean, sigma, alpha_2, n_2) # second CrystallBall
    gauss = ROOT.RooGaussian("gauss_%s" % mH_, "gauss", recoilmass, mean_gt, sigma_gt) # the Gauss
    #cb_1 = ROOT.RooRealVar("cb_1_%s" % mH_, '', 3.96333e-01 , 0, 1)
    #cb_2 = ROOT.RooRealVar("cb_2_%s" % mH_, '', 4.75471e-01 , 0, 1)
    #cb_1 = ROOT.RooRealVar("cb_1_%s" % mH_, '', 0.458)
    #cb_2 = ROOT.RooRealVar("cb_2_%s" % mH_, '', 0.4114)
            
    sig_fit = ROOT.RooAddPdf("sig_%s" % mH_, '', ROOT.RooArgList(cbs_1, cbs_2, gauss), ROOT.RooArgList(cb_1, cb_2)) # half of both CB functions
    ###sig = ROOT.RooAddPdf("sig_%s" % mH_, '', ROOT.RooArgList(cbs_1, cbs_2), ROOT.RooArgList(cb_1)) # half of both CB functions
    sig_norm = ROOT.RooRealVar("sig_%s_norm" % mH_, '', yield_zh, 0, 1e6) # fix normalization
    #sig_fit = ROOT.RooAddPdf("zh_model_%s" % mH_, '', ROOT.RooArgList(sig), ROOT.RooArgList(sig_norm))
    sig_fit.fitTo(rdh_zh, ROOT.RooFit.Extended(ROOT.kFALSE), ROOT.RooFit.SumW2Error(ROOT.kFALSE))
        
        
    cb1__ = cb_1.getVal()
    cb2__ = cb_2.getVal()
        
    # do plotting
    plotter.cfg = cfg
        
    canvas, padT, padB = plotter.canvasRatio()
    dummyT, dummyB = plotter.dummyRatio()
        
    ## TOP PAD ##
    canvas.cd()
    padT.Draw()
    padT.cd()
    dummyT.Draw("HIST")
        
    plt = recoilmass.frame()
    plt.SetTitle("ZH signal")
    rdh_zh.plotOn(plt, ROOT.RooFit.Binning(200)) # , ROOT.RooFit.Normalization(yield_zh, ROOT.RooAbsReal.NumEvent)
        
    sig_fit.plotOn(plt, ROOT.RooFit.LineColor(ROOT.kRed))
    sig_fit.paramOn(plt, ROOT.RooFit.Format("NELU", ROOT.RooFit.AutoPrecision(2)), ROOT.RooFit.Layout(0.45, 0.9, 0.9))
        
    histpull = plt.pullHist()
    plt.Draw("SAME")
        
    plotter.auxRatio()
        
    ## BOTTOM PAD ##
    canvas.cd()
    padB.Draw()
    padB.cd()
    dummyB.Draw("HIST")
        

    plt = recoilmass.frame()
    plt.addPlotable(histpull, "P")
    plt.Draw("SAME")
        
    line = ROOT.TLine(120, 0, 140, 0)
    line.SetLineColor(ROOT.kBlue+2)
    line.SetLineWidth(2)
    line.Draw("SAME")
        
      
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs("%s/fit_cat%d.png" % (outDir, cat))
    canvas.SaveAs("%s/fit_cat%d.pdf" % (outDir, cat))
        
    '''
        del dummyB
        del dummyT
        del padT
        del padB
        del canvas
        

        cfg['ymax'] = 2500
        plotter.cfg = cfg
        canvas = plotter.canvas()
        dummy = plotter.dummy()
        dummy.Draw("HIST")
        plt = w_tmp.var("zed_leptonic_recoil_m").frame()
        colors = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack, ROOT.kGreen, ROOT.kCyan] 
        
        leg = ROOT.TLegend(.50, 0.7, .95, .90)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.04)
        leg.SetMargin(0.15)

        cbs_1.plotOn(plt, ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.Normalization(yield_zh*cb1__, ROOT.RooAbsReal.NumEvent))
        cbs_2.plotOn(plt, ROOT.RooFit.LineColor(ROOT.kBlue), ROOT.RooFit.Normalization(yield_zh*cb2__, ROOT.RooAbsReal.NumEvent))
        gauss.plotOn(plt, ROOT.RooFit.LineColor(ROOT.kCyan), ROOT.RooFit.Normalization(yield_zh*(1.-cb1__-cb2__), ROOT.RooAbsReal.NumEvent))
        sig_fit.plotOn(plt, ROOT.RooFit.LineColor(ROOT.kBlack), ROOT.RooFit.Normalization(yield_zh, ROOT.RooAbsReal.NumEvent))     
        
            
        # define TGraphs for legend
        tmp1 = ROOT.TGraph()
        tmp1.SetPoint(0, 0, 0)
        tmp1.SetLineColor(ROOT.kBlack)
        tmp1.SetLineWidth(3)
        tmp1.Draw("SAME")
        leg.AddEntry(tmp1, "Total PDF", "L")
        
        tmp2 = ROOT.TGraph()
        tmp2.SetPoint(0, 0, 0)
        tmp2.SetLineColor(ROOT.kRed)
        tmp2.SetLineWidth(3)
        tmp2.Draw("SAME")
        leg.AddEntry(tmp2, "CB1", "L")
        
        tmp3 = ROOT.TGraph()
        tmp3.SetPoint(0, 0, 0)
        tmp3.SetLineColor(ROOT.kBlue)
        tmp3.SetLineWidth(3)
        tmp3.Draw("SAME")
        leg.AddEntry(tmp3, "CB2", "L")
        
        tmp4 = ROOT.TGraph()
        tmp4.SetPoint(0, 0, 0)
        tmp4.SetLineColor(ROOT.kCyan)
        tmp4.SetLineWidth(3)
        tmp4.Draw("SAME")
        leg.AddEntry(tmp4, "Gauss", "L")
        
        plt.Draw("SAME")
        leg.Draw()
        plotter.aux()
        canvas.Modify()
        canvas.Update()
        canvas.Draw()
        canvas.SaveAs("%s/fit_mH%s_decomposition.png" % (outDir, mH_))
        canvas.SaveAs("%s/fit_mH%s_decomposition.pdf" % (outDir, mH_))
        cfg['ymax'] = 1500
        
        
        # import
        getattr(w_tmp, 'import')(rdh_zh)
        getattr(w_tmp, 'import')(sig_fit)
        
        
        param_mh.append(mH)
        param_mean.append(mean.getVal())
        param_sigma.append(sigma.getVal())
        param_mean_gt.append(mean_gt.getVal())
        param_sigma_gt.append(sigma_gt.getVal())
        param_alpha_1.append(alpha_1.getVal())
        param_alpha_2.append(alpha_2.getVal())
        param_n_1.append(n_1.getVal())
        param_n_2.append(n_2.getVal())
        param_yield.append(sig_norm.getVal())
        param_cb_1.append(cb_1.getVal())
        param_cb_2.append(cb_2.getVal())
        
        param_mean_err.append(mean.getError())
        param_sigma_err.append(sigma.getError())
        param_mean_gt_err.append(mean.getError())
        param_sigma_gt_err.append(sigma.getError())
        param_alpha_1_err.append(alpha_1.getError())
        param_alpha_2_err.append(alpha_2.getError())
        param_n_1_err.append(n_1.getError())
        param_n_2_err.append(n_2.getError())
        param_yield_err.append(sig_norm.getError())
        param_cb_1_err.append(cb_1.getError())
        param_cb_2_err.append(cb_2.getError())
    '''


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
    leg.AddEntry(h1, "%s (RMS=%.5f)" % (l1, h1.GetRMS()), "L")
    leg.AddEntry(h2, "%s (RMS=%.5f)" % (l2, h2.GetRMS()), "L")
    
    cfg = {

        'logy'              : logy,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax,
            
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


    
    
    
if __name__ == "__main__":

    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/mass_categories"
    #makePlot("tmp/output_mass_xsec_mumu.root", "mumu")
    #makePlot("tmp/output_mass_xsec_mumu.root", "mumu", doNorm=True)
    doFit("tmp/output_mass_xsec_mumu.root", "mumu", cat=1)
    doFit("tmp/output_mass_xsec_mumu.root", "mumu", cat=2)
    doFit("tmp/output_mass_xsec_mumu.root", "mumu", cat=3)
    quit()

    #outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison_noIso"
    #fIn = ROOT.TFile("tmp/output_mass_xsec_noIso.root")
    
    #outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison_iso"
    #fIn = ROOT.TFile("tmp/output_mass_xsec_iso.root")
    
    
    f1, p1, l1 = "tmp/output_mass_xsec_mumu_allmuons.root", "wzp6_ee_mumuH_ecm240", "Spring 2021, muons"
    f2, p2, l2 = "tmp/output_mass_xsec_mumu.root", "wz2p6_ee_mumuH_ecm240_winter_v2", "Winter 2023, muons"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/spring2021_winter2023_isolation/"
    
    
    
    f1, p1, l1 = "tmp/output_mass_xsec_mumu.root", "wz2p6_ee_mumuH_ecm240_winter_v2", "Winter 2023, muons"
    f2, p2, l2 = "tmp/output_mass_xsec_ee.root", "wzp6_ee_eeH_ecm240_winter", "Winter 2023, electrons"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electron_muon/"
    
    #f1, p1, l1 = "tmp/output_mass_xsec_ee.root", "wzp6_ee_eeH_ecm240_winter", "Winter 2023, electrons"
    #f2, p2, l2 = "tmp/output_mass_xsec_ee.root", "wzp6_ee_eeH_ecm240_winter_v2", "Winter 2023, electrons, smeared"
    #outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/sampleComparison/winter2023_electrons/"
    
   

    makePlot("muons_p_cut0", 0, 100, 0, 0.05, "p (GeV)", "Events (normalized)", rebin=100)
    makePlot("muons_p_gen_cut0", 0, 100, 0, 0.05, "p (GeV)", "Events (normalized)", rebin=100)
    makePlot("muons_no_cut0", 0, 8, 0, 1, "Multiplicity", "Events (normalized)", rebin=1)
    makePlot("muons_phi_cut0", -5, 5, 0, 0.005, "#phi (rad)", "Events (normalized)", rebin=1)
    makePlot("muons_theta_cut0", 0, 3.14, 0, 0.015, "#theta (rad)", "Events (normalized)", rebin=1)
    makePlot("muons_eta_cut0", -3, 3, 0, 0.015, "#eta", "Events (normalized)", rebin=1)
    makePlot("muons_iso_cut0", 0, 1, 0.0001, 1, "Isolation", "Events (normalized)", rebin=2, logy=True)
    makeResolutionPlot("muons_reso_cut0", 0.98, 1.02, 0, 0.03, "Resolution (p_{reco}/p_{gen})", "Events (normalized)", rebin=10)
    
    makePlot("deltaR_gen_leps", 0, 10, 0, 0.01, "#DeltaR(leptons)", "Events (normalized)", rebin=1) # 0.15
    
    
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
    
    makePlot("zed_leptonic_m_cut3", 60, 120, 0, 0.3, "m_{#mu^{#plus}, #mu^{#minus}} (Gev)", "Events (normalized)", rebin=1)
    makePlot("zed_leptonic_recoil_m", 120, 140, 0, 0.1, "Recoil (GeV)", "Events (normalized)", rebin=100)
    makePlot("mll_gen_leps", 80, 110, 0, 0.35, "m_{l^{#plus}, l^{#minus}}, gen (Gev)", "Events (normalized)", rebin=1)
    

    