
import sys,copy,array,os,subprocess
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

doPlot = True
if doPlot:
    import plotter


def doSignal():

    global h_obs
    
    mHs = [125.0]
    if flavor == "mumu":
        procs = ["wzp6_ee_mumuH_ecm240"]

    if flavor == "ee":
        procs = ["wzp6_ee_eeH_ecm240"]

    # recoil mass plot settings
    cfg = {
 
        'logy'              : False,
        'logx'              : False,
    
        'xmin'              : 120 if not "Score" in hName else 0,
        'xmax'              : 140 if not "Score" in hName else 1,
        'ymin'              : 0,
        'ymax'              : 3000,
        
        'xtitle'            : "Recoil mass (GeV)" if not "Score" in hName else "BDT Score",
        'ytitle'            : "Events / 0.2 GeV",
        
        'topRight'          : "ZH, #sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Internal}}",
        
        'ratiofraction'     : 0.25,
        'ytitleR'           : "Pull",
        'yminR'             : -3.5,
        'ymaxR'             : 3.5,
    }
    
   
    for i, proc in enumerate(procs):
    
        fIn = ROOT.TFile(baseFileName.format(sampleName=proc))
        
        mH = mHs[i]
        mH_ = ("%.2f" % mH).replace(".", "p")

        hist_zh = copy.deepcopy(fIn.Get(hName))
        hist_zh = hist_zh.Rebin(rebin)
        hist_zh.SetName("signal")
        hist_zh.Scale(lumi)
        hists.append(hist_zh)
        fIn.Close()
        
        if mH == 125.0:
            if h_obs == None: h_obs = hist_zh.Clone("h_obs") # take 125.0 GeV to add to observed (need to add background later as well)
            else: h_obs.Add(hist_zh)

        if not doPlot:
            continue
        # do plotting
        plotter.cfg = cfg
        
        cfg['ymax'] = 1.3*hist_zh.GetMaximum()
        
        canvas, padT, padB = plotter.canvasRatio()
        dummyT, dummyB = plotter.dummyRatio()
        
        ## TOP PAD ##
        canvas.cd()
        padT.Draw()
        padT.cd()
        dummyT.Draw("HIST")
        
        hist_zh.SetLineColor(ROOT.kBlack)
        hist_zh.SetLineWidth(2)
        hist_zh.Draw("HIST E SAME")
        
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.045)
        latex.SetTextColor(1)
        latex.SetTextFont(42)
        latex.SetTextAlign(13)
        latex.DrawLatex(0.2, 0.88, label)
        plotter.auxRatio()
        
        ## BOTTOM PAD ##
        canvas.cd()
        padB.Draw()
        padB.cd()
        dummyB.Draw("HIST")

        line = ROOT.TLine(120, 0, 140, 0)
        line.SetLineColor(ROOT.kBlue+2)
        line.SetLineWidth(2)
        line.Draw("SAME")
        
      
        canvas.Modify()
        canvas.Update()
        canvas.Draw()
        canvas.SaveAs("%s/hist_mH%s.png" % (outDir, mH_))
        canvas.SaveAs("%s/hist_mH%s.pdf" % (outDir, mH_))
        
    
        del dummyB
        del dummyT
        del padT
        del padB
        del canvas
        

        
  
  


def doBackgrounds():

    global h_obs

    if flavor == "mumu":
        procs = ["p8_ee_WW_ecm240", "p8_ee_ZZ_ecm240", "wzp6_ee_mumu_ecm240", "wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_gaga_mumu_60_ecm240", "wzp6_ee_tautau_ecm240", "wzp6_ee_nuenueZ_ecm240"]
        
    if flavor == "ee":
        procs = ["p8_ee_WW_ecm240", "p8_ee_ZZ_ecm240", "wzp6_ee_ee_Mee_30_150_ecm240", "wzp6_gammae_eZ_Zee_ecm240", "wzp6_egamma_eZ_Zee_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_gaga_ee_60_ecm240", "wzp6_ee_tautau_ecm240", "wzp6_ee_nuenueZ_ecm240"]
        


    hist_bkg = None
    for proc in procs:
    
        fIn = ROOT.TFile(baseFileName.format(sampleName=proc))
        hist = copy.deepcopy(fIn.Get(hName))
        fIn.Close()
        hist.Scale(lumi)
        hist = hist.Rebin(rebin)
        
        if hist_bkg == None: hist_bkg = hist
        else: hist_bkg.Add(hist)
        
        # add to observed 
        if h_obs == None: h_obs = hist.Clone("h_obs")
        else: h_obs.Add(hist)


    hist_bkg.SetName("background")
    hists.append(hist_bkg)

    if not doPlot:
        return
    ########### PLOTTING ###########
    cfg = {

        'logy'              : False,
        'logx'              : False,
    
        'xmin'              : 120 if not "Score" in hName else 0,
        'xmax'              : 140 if not "Score" in hName else 1,
        'ymin'              : 0,
        'ymax'              : 1.3*hist_bkg.GetMaximum(),
        
        'xtitle'            : "Recoil mass (GeV)" if not "Score" in hName else "BDT Score",
        'ytitle'            : "Events / 0.1 GeV",
        
        'topRight'          : "BKGS, #sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Internal}}",
        
        'ratiofraction'     : 0.25,
        'ytitleR'           : "Pull",
        'yminR'             : -3.5,
        'ymaxR'             : 3.5,
    }
    
    plotter.cfg = cfg
    
    canvas, padT, padB = plotter.canvasRatio()
    dummyT, dummyB = plotter.dummyRatio()
    
    ## TOP PAD ##
    canvas.cd()
    padT.Draw()
    padT.cd()
    dummyT.Draw("HIST")
    
    hist_bkg.SetLineColor(ROOT.kBlack)
    hist_bkg.SetLineWidth(2)
    hist_bkg.Draw("HIST E SAME")
    

        
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.045)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(13)
    latex.DrawLatex(0.2, 0.88, label)

    plotter.auxRatio()
    
    ## BOTTOM PAD ##
    canvas.cd()
    padB.Draw()
    padB.cd()
    dummyB.Draw("HIST")

    line = ROOT.TLine(120, 0, 140, 0)
    line.SetLineColor(ROOT.kBlue+2)
    line.SetLineWidth(2)
    line.Draw("SAME")
    
  
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs("%s/binned_bkg.png" % (outDir))  
    canvas.SaveAs("%s/binned_bkg.pdf" % (outDir))  
    
  

 
if __name__ == "__main__":

    flavor = "mumu"
    mva = True
    
    #baseFileName = "/eos/user/l/lia/FCCee/NewWorkFlow/BDT_analysis_samples/final/{sampleName}_sel0_MRecoil_Mll_73_120_pll_05_histo.root"
    if flavor == "mumu":
        if mva:
            baseFileName = "/eos/user/l/lia/FCCee/Winter2023/mumu/BDT_analysis_samples/final/{sampleName}_sel_Baseline_no_costhetamiss_MVA02_histo.root"
            baseFileName = "/eos/user/l/lia/FCCee/Winter2023/mumu/BDT_analysis_samples/final/{sampleName}_sel_Baseline_no_costhetamiss_histo.root"
        else:
            baseFileName = "/eos/user/l/lia/FCCee/Winter2023/mumu/BDT_analysis_samples/final/{sampleName}_sel_Baseline_histo.root"
            baseFileName = "/eos/user/l/lia/FCCee/Winter2023/mumu/BDT_analysis_samples/final/{sampleName}_sel_Baseline_no_costhetamiss_histo.root"
        label = "#mu^{#plus}#mu^{#minus}"
    elif flavor == "ee":
        if mva:
            baseFileName = "/eos/user/l/lia/FCCee/Winter2023/ee/BDT_analysis_samples/final/{sampleName}_sel_Baseline_no_costhetamiss_MVA03_histo.root"
            baseFileName = "/eos/user/l/lia/FCCee/Winter2023/ee/BDT_analysis_samples/final/{sampleName}_sel_Baseline_no_costhetamiss_histo.root"
        else:
            baseFileName = "/eos/user/l/lia/FCCee/Winter2023/ee/BDT_analysis_samples/final/{sampleName}_sel_Baseline_histo.root"
            baseFileName = "/eos/user/l/lia/FCCee/Winter2023/ee/BDT_analysis_samples/final/{sampleName}_sel_Baseline_no_costhetamiss_histo.root"
        label = "e^{#plus}e^{#minus}"
                        
    hName = "leptonic_recoil_m_zoom2"
    hName = "BDT_Score"
    if mva:
        runDir = "combine/run_binned_BDT_{flavor}/".format(flavor=flavor)
        outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/combine_binned_BDT/{flavor}/".format(flavor=flavor)
        
        runDir = "combine/run_binned_BDTScore_{flavor}/".format(flavor=flavor)
        outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/combine_binned_BDTScore/{flavor}/".format(flavor=flavor)
    else:
        runDir = "combine/run_binned_baseline_{flavor}/".format(flavor=flavor)
        outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/combine_binned_baseline/{flavor}/".format(flavor=flavor)
        
        runDir = "combine/run_binned_baseline_no_costhetamiss_{flavor}/".format(flavor=flavor)
        outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/combine_binned_baseline_no_costhetamiss/{flavor}/".format(flavor=flavor)
    if not os.path.exists(outDir): os.makedirs(outDir)
    if not os.path.exists(runDir): os.makedirs(runDir)
    lumi = 5000000
    
    rebin = 5 # the recoil histograms are binned at 1 MeV
    recoilMin = 120
    recoilMax = 140
    h_obs = None # should hold the data_obs = sum of signal and backgrounds

    hists = []
    
    doSignal()
    doBackgrounds()
    h_obs.SetName("data_obs")
    
    fOut = ROOT.TFile("%s/datacard.root" % runDir, "RECREATE")
    for h in hists:
        h.Write()
    h_obs.Write()
    fOut.Close()

    # build the Combine workspace based on the datacard, save it to ws.root    
    cmd = "cp scripts/ZH_mass_xsec/combine/datacard_binned.txt %s/" % runDir
    subprocess.call(cmd, shell=True)
    
    
    cmd = "sed -i 's/bkg/bkg_{flavor}/g' datacard_binned.txt".format(flavor=flavor)
    subprocess.call(cmd, shell=True, cwd=runDir)
    
    cmd = "text2workspace.py datacard_binned.txt -o ws.root -v 10"
    subprocess.call(cmd, shell=True, cwd=runDir)