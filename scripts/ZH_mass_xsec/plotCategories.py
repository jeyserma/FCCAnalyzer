
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter

    
def makePlot(doNorm=False):

    outName = "zll_recoil_m_categories"
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


def doFit(cat=1):

    recoilMin = 120
    recoilMax = 140
    
    outName = "zll_recoil_m_categories"
    zll_recoil_m = fIn.Get("%s/%s" % (proc, hist))
    
    if cat == 0: cat1, cat2 = 0, 5
    else: cat1, cat2 = cat, cat
    hist_zh = zll_recoil_m.ProjectionX("hist", cat1, cat2)   



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
        'ymax'              : 1500,
        
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

    
    
if __name__ == "__main__":

    flavor="ee"
    fIn = ROOT.TFile("tmp/output_mass_xsec_%s.root" % flavor)
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/plots_categories_%s/" % flavor
    
    proc = "wzp6_ee_%sH_ecm240" % flavor
    hist = "zll_recoil_m"
    rebin = 50


    makePlot()
    makePlot(doNorm=True)
    doFit(cat=1)
    doFit(cat=2)
    doFit(cat=3)
    doFit(cat=0) # all