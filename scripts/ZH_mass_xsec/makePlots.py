
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

parser = argparse.ArgumentParser()
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", default="mumu")
parser.add_argument("--type", type=str, help="Run type (mass or xsec)", choices=["mass", "xsec"], default="mass")
args = parser.parse_args()


def getHist(proc, sel, hName, rebin):

    fIn = ROOT.TFile("%s/%s_hists.root" % (histDir, proc))
    h = copy.deepcopy(fIn.Get("%s_%s" % (hName, sel)))
    h.Rebin(rebin)
    h.Scale(lumi*ds.datasets[proc]['xsec']*1e6/ds.datasets[proc]['nevents'])
    fIn.Close()
    return h


def makePlot(hName, outName, xMin=0, xMax=100, yMin=1, yMax=1e5, xLabel="xlabel", yLabel="Events", logX=False, logY=True, rebin=1, legPos=[0.4, 0.65, 0.9, 0.9]):


    st = ROOT.THStack()
    st.SetName("stack")
        
    leg = ROOT.TLegend(legPos[0], legPos[1], legPos[2], legPos[3])
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.SetMargin(0.2)
    

    h_sig = plotter.getProc(fIn, hName, sigs)
    if "TH2" in h_sig.ClassName(): h_sig = h_sig.ProjectionX("h_sig")
    h_sig.SetLineColor(ROOT.TColor.GetColor("#BF2229"))
    h_sig.SetLineWidth(3)
    h_sig.SetLineStyle(1)
    h_sig.Scale(sig_scale)
    h_sig.Rebin(rebin)
    leg.AddEntry(h_sig, sig_legend, "L")

    st = ROOT.THStack()
    st.SetName("stack")
    h_bkg_tot = None
    for i,bkg in enumerate(bkgs):
		
        hist = plotter.getProc(fIn, hName, bgks_cfg[bkg])
        if "TH2" in hist.ClassName(): hist = hist.ProjectionX()
        hist.SetName(bkg)
        hist.SetFillColor(bkgs_colors[i])
        hist.SetLineColor(ROOT.kBlack)
        hist.SetLineWidth(1)
        hist.SetLineStyle(1)
        hist.Rebin(rebin)
		
        leg.AddEntry(hist, bkgs_legends[i], "F")
        st.Add(hist)
        if h_bkg_tot == None:
            h_bkg_tot = copy.deepcopy(hist)
            h_bkg_tot.SetName("h_bkg_tot")
        else: h_bkg_tot.Add(hist)
        

    cfg = {

        'logy'              : logY,
        'logx'              : logX,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else ath.ceil(h_bkg_tot.GetMaximum()*100)/10.,
            
        'xtitle'            : xLabel,
        'ytitle'            : yLabel,
            
        'topRight'          : "#sqrt{s} = 240 GeV, 10 ab^{#minus1}",
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",

    }
        

    plotter.cfg = cfg
    canvas = plotter.canvas()
        
    dummy = plotter.dummy()
    dummy.Draw("HIST") 
    st.Draw("HIST SAME")
    
    
    '''
    hTot_err = hTot.Clone("hTot_err")
    hTot_err.SetFillColor(ROOT.kBlack)
    hTot_err.SetMarkerColor(ROOT.kBlack)
    hTot_err.SetFillStyle(3004)
    leg.AddEntry(hTot_err, "Stat. Unc.", "F")
    '''
    
    h_bkg_tot.SetLineColor(ROOT.kBlack)
    h_bkg_tot.SetFillColor(0)
    h_bkg_tot.SetLineWidth(2)
    #hTot_err.Draw("E2 SAME")
    h_bkg_tot.Draw("HIST SAME")
    h_sig.Draw("HIST SAME")
    leg.Draw("SAME")
        
    canvas.SetGrid()
    canvas.Modify()
    canvas.Update()

    plotter.aux()
    ROOT.gPad.SetTicks()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs("%s/%s.png" % (outDir, outName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, outName))
    canvas.Close()



def significance(hName):

    h_sig = plotter.getProc(fIn, hName, sigs)
    if "TH2" in h_sig.ClassName(): h_sig = h_sig.ProjectionX("h_sig")


    h_bkg_tot = None
    for i,bkg in enumerate(bkgs):
		
        hist = plotter.getProc(fIn, hName, bgks_cfg[bkg])
        if "TH2" in hist.ClassName(): hist = hist.ProjectionX()
        hist.SetName(bkg)
        print(bkg, hist.Integral())
        if h_bkg_tot == None:
            h_bkg_tot = copy.deepcopy(hist)
            h_bkg_tot.SetName("h_bkg_tot")
        else: h_bkg_tot.Add(hist)
       
    b_low, b_high = h_sig.FindBin(124), h_sig.FindBin(128)
       
    y_sig = h_sig.Integral(b_low, b_high)
    y_bkg = h_bkg_tot.Integral(b_low, b_high)
    print(y_sig/y_bkg)
    print(y_sig)
    print(y_bkg)
        
	
if __name__ == "__main__":

    flavor = args.flavor
    fIn = ROOT.TFile(f"tmp/output_ZH_{args.type}_{flavor}.root")
    outDir = f"/eos/user/j/jaeyserm/www/FCCee/ZH_{args.type}/plots_{flavor}/"
    
    
    
    if flavor == "mumu":
    
        labels = ["All events", "#geq 1 #mu^{#pm}", "#geq 2 #mu^{#pm}", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{T}^{#mu^{+}#mu^{#minus}} < 70", "|cos#theta_{missing}| < 0.98", "120 < m_{rec} < 140"]
    
        sigs = ["p_wzp6_ee_mumuH_ecm240"]
        sig_scale = 1
        sig_legend = "Z(#mu^{+}#mu^{#minus})H"
    
        bkgs = ["WW", "ZZ", "Zg", "rare"] # this is the order of the plot
        bkgs_legends = ["W^{+}W^{#minus}", "ZZ", "Z/#gamma^{*} #rightarrow #mu^{+}#mu^{#minus}, #tau^{+}#tau^{#minus}", "Rare (e(e)Z, #gamma#gamma #rightarrow #mu^{+}#mu^{#minus}, #tau^{+}#tau^{#minus})"]
        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
        bgks_cfg = { 
            "WW"	    : ["p8_ee_WW_ecm240"],
            "ZZ"	    : ["p8_ee_ZZ_ecm240"],
            "Zg"        : ["wzp6_ee_mumu_ecm240", "wzp6_ee_tautau_ecm240"],
            "rare"      : ["wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gaga_mumu_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]
        }
        
    if flavor == "ee":
    
        labels = ["All events", "#geq 1 e^{#pm}", "#geq 2 e^{#pm}", "86 < m_{e^{+}e^{#minus}} < 96", "20 < p_{T}^{e^{+}e^{#minus}} < 70", "|cos#theta_{missing}| < 0.98", "120 < m_{rec} < 140"]
    
        sigs = ["p_wzp6_ee_eeH_ecm240"]
        sig_scale = 1
        sig_legend = "Z(e^{+}e^{#minus})H"
    
        bkgs = ["WW", "ZZ", "Zg", "rare"] # this is the order of the plot
        bkgs_legends = ["W^{+}W^{#minus}", "ZZ", "Z/#gamma^{*} #rightarrow e^{+}e^{#minus}, #tau^{+}#tau^{#minus}", "Rare (e(e)Z, #gamma#gamma #rightarrow e^{+}e^{#minus}, #tau^{+}#tau^{#minus})"]
        
        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
        bgks_cfg = { 
            "WW"	    : ["p8_ee_WW_ecm240"],
            "ZZ"	    : ["p8_ee_ZZ_ecm240"],
            "Zg"        : ["wzp6_ee_ee_Mee_30_150_ecm240", "wzp6_ee_tautau_ecm240"],
            "rare"      : ["wzp6_egamma_eZ_Zee_ecm240", "wzp6_gammae_eZ_Zee_ecm240", "wzp6_gaga_ee_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]
        }

    
    
    
    
    # N-1 plots
    
    #makePlot("leps_all_p_cut0", "leps_all_p_cut0", xMin=0, xMax=100, yMin=10, yMax=1e7, xLabel="Leptons p (GeV)", yLabel="Events", logY=True, rebin=10)
    
    # N-1 plots
    makePlot("zll_m_cut2", "zll_m_cut2", xMin=50, xMax=120, yMin=1e2, yMax=1e7, xLabel="m_{ll} (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("zll_p_cut3", "zll_p_cut3", xMin=0, xMax=100, yMin=1, yMax=1e7, xLabel="p_{ll} (GeV)", yLabel="Events", logY=True, rebin=2)
    makePlot("zll_recoil_cut4", "zll_recoil_cut4", xMin=100, xMax=150, yMin=1, yMax=1e6, xLabel="m_{rec} (GeV)", yLabel="Events", logY=True, rebin=6)
    makePlot("cosThetaMiss_cut5", "cosThetaMiss_cut5", xMin=0, xMax=1, yMin=1e2, yMax=1e6, xLabel="|cos(#theta_{miss})|", yLabel="Events", logY=True, rebin=100)
    makePlot("zll_recoil", "zll_recoil", xMin=120, xMax=140, yMin=0, yMax=3000, xLabel="m_{rec} (GeV)", yLabel="Events", logY=False, rebin=10)
    
    quit()
    makePlot("leps_p_cut7", "leps_p_cut7", xMin=0, xMax=100, yMin=10, yMax=1e7, xLabel="Leptons p (GeV)", yLabel="Events", logY=True, rebin=10)
    
    makePlot("cosThetaMiss_cut4", "cosThetaMiss_cut4", xMin=0, xMax=1, yMin=1e2, yMax=1e6, xLabel="|cos(#theta_{miss})|", yLabel="Events", logY=True, rebin=100)
    makePlot("acoplanarity_cut4", "acoplanarity_cut4", xMin=-3, xMax=3.5, yMin=1, yMax=1e6, xLabel="Acoplanarity (rad)", yLabel="Events", logY=True, rebin=1)
    makePlot("acolinearity_cut4", "acolinearity_cut4", xMin=-3, xMax=1.5, yMin=1, yMax=1e6, xLabel="Acolinearity (rad)", yLabel="Events", logY=True, rebin=1)
    
    makePlot("cosThetaMiss_cut5", "cosThetaMiss_cut5", xMin=0, xMax=1, yMin=1e2, yMax=1e6, xLabel="|cos(#theta_{miss})|", yLabel="Events", logY=True, rebin=100)
    makePlot("acoplanarity_cut5", "acoplanarity_cut5", xMin=-3, xMax=3.5, yMin=1, yMax=1e6, xLabel="Acoplanarity (rad)", yLabel="Events", logY=True, rebin=1)
    makePlot("acolinearity_cut5", "acolinearity_cut5", xMin=-3, xMax=1.5, yMin=1, yMax=1e6, xLabel="Acolinearity (rad)", yLabel="Events", logY=True, rebin=1)
    
    makePlot("cosThetaMiss_cut6", "cosThetaMiss_cut6", xMin=0, xMax=1, yMin=1e2, yMax=1e6, xLabel="|cos(#theta_{miss})|", yLabel="Events", logY=True, rebin=100)
    makePlot("acoplanarity_cut6", "acoplanarity_cut6", xMin=-3, xMax=3.5, yMin=1, yMax=1e6, xLabel="Acoplanarity (rad)", yLabel="Events", logY=True, rebin=1)
    makePlot("acolinearity_cut6", "acolinearity_cut6", xMin=-3, xMax=1.5, yMin=1, yMax=1e6, xLabel="Acolinearity (rad)", yLabel="Events", logY=True, rebin=1)
    
    significance("zll_recoil_cut7")