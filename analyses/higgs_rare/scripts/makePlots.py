
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

parser = argparse.ArgumentParser()
parser.add_argument("--flavor", type=str, help="Flavor (mumu or gaga)", default="mumu")
args = parser.parse_args()




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
            
        'topRight'          : "#sqrt{s} = 240 GeV, 7.2 ab^{#minus1}",
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

    if flavor == "mumu":
        fIn = ROOT.TFile(f"output_h_mumu.root")
        outDir = f"/home/submit/jaeyserm/public_html/fccee/higgs_rare_mumu/baseline/"

        labels = ["All events", "#geq 1 #mu^{#pm}", "#geq 2 #mu^{#pm}", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{T}^{#mu^{+}#mu^{#minus}} < 70", "|cos#theta_{missing}| < 0.98", "120 < m_{rec} < 140"]

        sigs = ["wzp6_ee_nunuH_Hmumu_ecm240", "wzp6_ee_eeH_Hmumu_ecm240", "wzp6_ee_tautauH_Hmumu_ecm240", "wzp6_ee_ccH_Hmumu_ecm240", "wzp6_ee_bbH_Hmumu_ecm240", "wzp6_ee_qqH_Hmumu_ecm240", "wzp6_ee_ssH_Hmumu_ecm240", "wzp6_ee_mumuH_Hmumu_ecm240"]
        sig_scale = 100
        sig_legend = "ZH(#mu^{+}#mu^{#minus}) (#times 100)"
    
        bkgs = ["WW", "ZZ", "Zg", "rare"]
        bkgs_legends = ["W^{+}W^{#minus}", "ZZ", "Z/#gamma^{*} #rightarrow #mu^{+}#mu^{#minus}, #tau^{+}#tau^{#minus}", "Rare (e(e)Z, #gamma#gamma #rightarrow #mu^{+}#mu^{#minus}, #tau^{+}#tau^{#minus})"]
        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
        bgks_cfg = { 
            "WW"        : ["p8_ee_WW_ecm240"],
            "ZZ"        : ["p8_ee_ZZ_ecm240"], # , "p8_ee_ZZ_ecm240_ext"
            "Zg"        : ["wzp6_ee_mumu_ecm240", "wzp6_ee_tautau_ecm240"], # kkmcee_ee_mumu_ecm240 wzp6_ee_mumu_ecm240
            "rare"      : ["wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gaga_mumu_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]
        }

        # N-1 plots
        makePlot("hmumu_m_nOne", "mumu_m_nOne", xMin=100, xMax=150, yMin=0, yMax=20000, xLabel="m_{#mu^{+}#mu^{#minus}} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("mumu_recoil_m_nOne", "mumu_recoil_m_nOne", xMin=0, xMax=150, yMin=0, yMax=1e6, xLabel="Recoil mass (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("mumu_p_nOne", "mumu_p_nOne", xMin=0, xMax=100, yMin=0, yMax=1e6, xLabel="p_{#mu^{+}#mu^{#minus}} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("cosThetaMiss_nOne", "cosThetaMiss_nOne", xMin=0, xMax=1, yMin=0, yMax=10000, xLabel="|cos(#theta_{miss})|", yLabel="Events", logY=False, rebin=100)
        makePlot("missingEnergy_nOne", "missingEnergy_nOne", xMin=0, xMax=150, yMin=0, yMax=10000, xLabel="Missing energy (GeV)", yLabel="Events", logY=False, rebin=1)

        makePlot("acoplanarity", "acoplanarity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=10)
        makePlot("acolinearity", "acolinearity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acolinearity", yLabel="Events", logY=False, rebin=10)

        makePlot("muon1_p", "muon1_p", xMin=25, xMax=150, yMin=0, yMax=500000, xLabel="Leading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("muon2_p", "muon2_p", xMin=25, xMax=150, yMin=0, yMax=500000, xLabel="Subleading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)

        makePlot("photon_leading_costheta", "photon_leading_costheta", xMin=0, xMax=1, yMin=1e2, yMax=1e8, xLabel="|cos(#theta|) leading #gamma", yLabel="Events", logY=True, rebin=100)
        makePlot("photon_leading_p", "photon_leading_p", xMin=0, xMax=150, yMin=1e2, yMax=1e9, xLabel="Momentum leading #gamma (Gev)", yLabel="Events", logY=True, rebin=1)

        makePlot("muons_no", "muons_no", xMin=0, xMax=8, yMin=1, yMax=1e7, xLabel="Number of muons", yLabel="Events", logY=True, rebin=1)
        makePlot("electrons_no", "electrons_no", xMin=0, xMax=8, yMin=1, yMax=1e7, xLabel="Number of electrons", yLabel="Events", logY=True, rebin=1)


        # categories -- for fit
        sig_scale = 10
        sig_legend = "ZH(#mu^{+}#mu^{#minus}) (#times 10)"
        makePlot("zqq_hmumu_m_nOne", "zqq_hmumu_m_nOne", xMin=110, xMax=130, yMin=0, yMax=500, xLabel="m_{h}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=2)
        makePlot("zqq_hmumu_m", "zqq_hmumu_m", xMin=122, xMax=128, yMin=0, yMax=500, xLabel="m_{h}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=2)
        makePlot("zee_hmumu_m", "zee_hmumu_m", xMin=110, xMax=130, yMin=0, yMax=15, xLabel="m_{h}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=2)
        makePlot("zmumu_hmumu_m", "zmumu_hmumu_m", xMin=110, xMax=130, yMin=0, yMax=15, xLabel="m_{h}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=2)
        makePlot("znunu_hmumu_m", "znunu_hmumu_m", xMin=110, xMax=130, yMin=0, yMax=2000, xLabel="m_{h}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=2)

        # corresponding Z mass plots
        sig_scale = 10
        sig_legend = "ZH(#mu^{+}#mu^{#minus}) (#times 10)"
        makePlot("zqq_m", "zqq_m", xMin=50, xMax=150, yMin=0, yMax=400*2, xLabel="m_{Z}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zee_m", "zee_m", xMin=80, xMax=100, yMin=0, yMax=50*2, xLabel="m_{Z}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zmumu_m", "zmumu_m", xMin=80, xMax=100, yMin=0, yMax=50*2, xLabel="m_{Z}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=1)

        # Zqq plots
        makePlot("zqq_h_z_deltaR", "zqq_h_z_deltaR", xMin=0, xMax=5, yMin=0, yMax=100, xLabel="#DeltaR(#mu^{+},#mu^{#minus})", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_h_z_deltaTheta", "zqq_h_z_deltaTheta", xMin=0, xMax=5, yMin=0, yMax=100, xLabel="#Delta#Theta(#mu^{+},#mu^{#minus})", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_h_z_deltaPhi", "zqq_h_z_deltaPhi", xMin=0, xMax=5, yMin=0, yMax=100, xLabel="#Delta#Phi(#mu^{+},#mu^{#minus})", yLabel="Events", logY=False, rebin=1)

        makePlot("zqq_mumu_p_nOne", "zqq_mumu_p", xMin=20, xMax=70, yMin=0, yMax=500, xLabel="p_{#mu^{+}#mu^{#minus}} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_qq_p_nOne", "zqq_qq_p", xMin=20, xMax=70, yMin=0, yMax=500, xLabel="p_{#mu^{+}#mu^{#minus}} (GeV)", yLabel="Events", logY=False, rebin=1)

        makePlot("zqq_acoplanarity", "zqq_acoplanarity", xMin=0, xMax=1, yMin=0, yMax=100, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=10)
        makePlot("zqq_acolinearity", "zqq_acolinearity", xMin=0, xMax=1, yMin=0, yMax=100, xLabel="Acolinearity", yLabel="Events", logY=False, rebin=10)
        makePlot("zqq_missingEnergy", "zqq_missingEnergy", xMin=0, xMax=50, yMin=0, yMax=1000, xLabel="Missing energy (GeV)", yLabel="Events", logY=False, rebin=1)

        makePlot("zqq_jet1_p", "zqq_jet1_p", xMin=25, xMax=100, yMin=0, yMax=100, xLabel="Leading jet momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_jet2_p", "zqq_jet2_p", xMin=25, xMax=100, yMin=0, yMax=100, xLabel="Subleading jet momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_muon1_p", "zqq_muon1_p", xMin=25, xMax=100, yMin=0, yMax=100, xLabel="Leading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_muon2_p", "zqq_muon2_p", xMin=25, xMax=100, yMin=0, yMax=100, xLabel="Subleading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)

        makePlot("zqq_mass_tot_m", "zqq_mass_tot_m", xMin=200, xMax=250, yMin=0, yMax=1000, xLabel="Subleading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_mass_tot_p", "zqq_mass_tot_p", xMin=0, xMax=30, yMin=0, yMax=1000, xLabel="Subleading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)


        makePlot("zqq_hmumu_m_mvaCut", "zqq_hmumu_m_mvaCut", xMin=122, xMax=128, yMin=0, yMax=500, xLabel="m_{h}(#mu^{+}#mu^{#minus}) (GeV)", yLabel="Events", logY=False, rebin=2)
        makePlot("zqq_mva", "zqq_mva", xMin=0, xMax=1, yMin=0, yMax=1000, xLabel="MVA Score", yLabel="Events", logY=False, rebin=1)

    
    
    


   

        # Znunu plots
        sig_scale = 100
        sig_legend = "ZH(#mu^{+}#mu^{#minus}) (#times 100)"
        makePlot("znunu_muons_deltaR", "znunu_muons_deltaR", xMin=0, xMax=5, yMin=0, yMax=1000, xLabel="#DeltaR(#mu^{+},#mu^{#minus})", yLabel="Events", logY=False, rebin=1)
        makePlot("znunu_muons_deltaTheta", "znunu_muons_deltaTheta", xMin=0, xMax=5, yMin=0, yMax=1000, xLabel="#Delta#Theta(#mu^{+},#mu^{#minus})", yLabel="Events", logY=False, rebin=1)
        makePlot("znunu_muons_deltaPhi", "znunu_muons_deltaPhi", xMin=0, xMax=5, yMin=0, yMax=1000, xLabel="#Delta#Phi(#mu^{+},#mu^{#minus})", yLabel="Events", logY=False, rebin=1)

        makePlot("znunu_mll_Emiss_deltaR", "znunu_mll_Emiss_deltaR", xMin=0, xMax=5, yMin=0, yMax=1000, xLabel="#DeltaR(#slash{E}, p_{#mu^{+}#mu^{#minus}})", yLabel="Events", logY=False, rebin=1)
        makePlot("znunu_mll_Emiss_deltaTheta", "znunu_mll_Emiss_deltaTheta", xMin=0, xMax=5, yMin=0, yMax=1000, xLabel="#Delta#theta(#slash{E}, p_{#mu^{+}#mu^{#minus}})", yLabel="Events", logY=False, rebin=1)
        makePlot("znunu_mll_Emiss_deltaPhi", "znunu_mll_Emiss_deltaPhi", xMin=0, xMax=5, yMin=0, yMax=1000, xLabel="#Delta#phi(#slash{E}, p_{#mu^{+}#mu^{#minus}})", yLabel="Events", logY=False, rebin=1)

        makePlot("znunu_muon1_p", "znunu_muon1_p", xMin=25, xMax=150, yMin=0, yMax=10000, xLabel="Leading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("znunu_muon2_p", "znunu_muon2_p", xMin=25, xMax=150, yMin=0, yMax=10000, xLabel="Leading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("znunu_acoplanarity", "znunu_acoplanarity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=10)
        makePlot("znunu_acolinearity", "znunu_acolinearity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acolinearity", yLabel="Events", logY=False, rebin=10)
        makePlot("znunu_missingEnergy", "znunu_missingEnergy", xMin=0, xMax=150, yMin=0, yMax=10000, xLabel="Missing energy (GeV)", yLabel="Events", logY=False, rebin=1)



        makePlot("zmumu_muon1_h_p", "zmumu_muon1_h_p", xMin=25, xMax=150, yMin=0, yMax=100, xLabel="Leading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zmumu_muon2_h_p", "zmumu_muon2_h_p", xMin=25, xMax=150, yMin=0, yMax=100, xLabel="Subleading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zmumu_muon1_z_p", "zmumu_muon1_z_p", xMin=25, xMax=150, yMin=0, yMax=100, xLabel="Leading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zmumu_muon2_z_p", "zmumu_muon2_z_p", xMin=25, xMax=150, yMin=0, yMax=100, xLabel="Subleading muon momentum (GeV)", yLabel="Events", logY=False, rebin=1)



    if flavor == "aa":
        fIn = ROOT.TFile(f"output_h_gaga.root")
        outDir = f"/home/submit/jaeyserm/public_html/fccee/higgs_rare_aa/baseline/"

        labels = ["All events", "#geq 1 #mu^{#pm}", "#geq 2 #mu^{#pm}", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{T}^{#mu^{+}#mu^{#minus}} < 70", "|cos#theta_{missing}| < 0.98", "120 < m_{rec} < 140"]

        sigs = ["wzp6_ee_nunuH_Haa_ecm240", "wzp6_ee_eeH_Haa_ecm240", "wzp6_ee_tautauH_Haa_ecm240", "wzp6_ee_ccH_Haa_ecm240", "wzp6_ee_bbH_Haa_ecm240", "wzp6_ee_qqH_Haa_ecm240", "wzp6_ee_ssH_Haa_ecm240", "wzp6_ee_mumuH_Haa_ecm240"]
        sig_scale = 1
        sig_legend = "ZH(#gamma#gamma)"
    
        bkgs = ["gg", "qq"]

        bkgs_legends = ["#gamma#gamma", "Z/#gamma^{*} #rightarrow qq+#gamma(#gamma) (KKMC)"]
        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)]
        bgks_cfg = { 
            "gg"    : ["wzp6_ee_gammagamma_ecm240"],
            "qq"    : ["kkmcee_ee_uu_ecm240", "kkmcee_ee_dd_ecm240", "kkmcee_ee_cc_ecm240", "kkmcee_ee_ss_ecm240", "kkmcee_ee_bb_ecm240"]
        }

        # N-1 plots
        makePlot("zqq_hgaga_m_nOne", "zqq_hgaga_m_nOne", xMin=110, xMax=130, yMin=0, yMax=1000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)

        makePlot("zqq_hgaga_m", "zqq_hgaga_m", xMin=110, xMax=130, yMin=0, yMax=1000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zee_hgaga_m", "zee_hgaga_m", xMin=110, xMax=130, yMin=0, yMax=10, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zmumu_hgaga_m", "zmumu_hgaga_m", xMin=110, xMax=130, yMin=0, yMax=10, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("znunu_hgaga_m", "znunu_hgaga_m", xMin=110, xMax=130, yMin=0, yMax=100, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        quit()
        makePlot("acoplanarity", "acoplanarity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=10)
        makePlot("acolinearity", "acolinearity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acolinearity", yLabel="Events", logY=False, rebin=10)
        
        makePlot("cosThetaMiss_nOne", "cosThetaMiss_nOne", xMin=0, xMax=1, yMin=0, yMax=3000, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=50)
        makePlot("missingEnergy_nOne", "missingEnergy_nOne", xMin=0, xMax=150, yMin=0, yMax=2000, xLabel="Missing energy (GeV)", yLabel="Events", logY=False, rebin=1)
        
        
        makePlot("zqq_photons_p", "zqq_photons_p", xMin=0, xMax=150, yMin=0, yMax=2000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_photon_leading_p", "zqq_photon_leading_p", xMin=0, xMax=150, yMin=0, yMax=2000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_photons_p", "zqq_photons_p", xMin=0, xMax=150, yMin=0, yMax=2000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_photon_leading_costheta", "zqq_photon_leading_costheta", xMin=0, xMax=1, yMin=0, yMax=3000, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=50)
        makePlot("zqq_photons_costheta", "zqq_photons_costheta", xMin=0, xMax=1, yMin=0, yMax=3000, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=50)

        makePlot("zqq_acoplanarity", "zqq_acoplanarity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=10)
        makePlot("zqq_acolinearity", "zqq_acolinearity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acolinearity", yLabel="Events", logY=False, rebin=10)
        
        makePlot("zqq_m_nOne", "zqq_m_nOne", xMin=50, xMax=120, yMin=0, yMax=5000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)

        
        makePlot("photons_p", "photons_p", xMin=0, xMax=150, yMin=0, yMax=2000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        
        # zqq plots\\
        makePlot("zqq_gaga_p", "zqq_gaga_p", xMin=0, xMax=100, yMin=0, yMax=2000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("zqq_qq_p", "zqq_qq_p", xMin=0, xMax=100, yMin=0, yMax=2000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        
        makePlot("zqq_m", "zqq_m", xMin=0, xMax=120, yMin=0, yMax=2000, xLabel="m_{#gamma#gamma} (GeV)", yLabel="Events", logY=False, rebin=1)
        
        makePlot("zqq_acoplanarity", "zqq_acoplanarity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acoplanarity", yLabel="Events", logY=False, rebin=10)
        makePlot("zqq_acolinearity", "zqq_acolinearity", xMin=0, xMax=1, yMin=0, yMax=4000, xLabel="Acolinearity", yLabel="Events", logY=False, rebin=10)
        
        
        
        quit()
        makePlot("mumu_recoil_m_nOne", "mumu_recoil_m_nOne", xMin=0, xMax=150, yMin=0, yMax=10000, xLabel="m_{rec} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("mumu_p_nOne", "mumu_p_nOne", xMin=0, xMax=100, yMin=0, yMax=10000, xLabel="p_{ll} (GeV)", yLabel="Events", logY=False, rebin=1)
        makePlot("cosThetaMiss_nOne", "cosThetaMiss_nOne", xMin=0, xMax=1, yMin=0, yMax=10000, xLabel="|cos(#theta_{miss})|", yLabel="Events", logY=False, rebin=100)
        makePlot("missingEnergy_nOne", "missingEnergy_nOne", xMin=0, xMax=150, yMin=0, yMax=10000, xLabel="Missing energy (GeV)", yLabel="Events", logY=False, rebin=1)

