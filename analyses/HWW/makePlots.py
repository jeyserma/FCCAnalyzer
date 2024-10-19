
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

parser = argparse.ArgumentParser()
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", default="mumu")
parser.add_argument("--ecm", type=int, help="Center-of-mass energy", choices=[240, 365], default=240)
parser.add_argument("--type", type=str, help="Run type (mass or xsec)", choices=["mass", "xsec"], default="mass")
parser.add_argument("--tag", type=str, help="Analysis tag", default="july24")
args = parser.parse_args()



def makePlot(hName, outName, xMin=0, xMax=100, yMin=1, yMax=1e5, xLabel="xlabel", yLabel="Events", logX=False, logY=True, rebin=1, legPos=[0.4, 0.65, 0.9, 0.9]):


    st = ROOT.THStack()
    st.SetName("stack")

    leg = ROOT.TLegend(legPos[0], legPos[1], legPos[2], legPos[3])
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.SetMargin(0.2)

    h_sig = plotter.getProc(fIn, hName, sigs, lumiScale)
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

        hist = plotter.getProc(fIn, hName, bgks_cfg[bkg], lumiScale)
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
        'ymax'              : yMax if yMax > 0 else math.ceil(h_bkg_tot.GetMaximum()*100)/1.,
            
        'xtitle'            : xLabel,
        'ytitle'            : yLabel,
            
        'topRight'          : lumi,
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





if __name__ == "__main__":

    fIn = ROOT.TFile(f"output_HWW.root")
    outDir = f"/work/submit/jaeyserm/public_html/fccee/HWW/plots/"
    os.makedirs(outDir, exist_ok=True)

    lumi = "#sqrt{s} = 240 GeV, 10.8 ab^{#minus1}"
    lumiScale = 1

    #sigs = ["wzp6_ee_mumuH_HWW_ecm240", "wzp6_ee_ssH_HWW_ecm240", "wzp6_ee_eeH_HWW_ecm240", "wzp6_ee_bbH_HWW_ecm240", "wzp6_ee_ccH_HWW_ecm240", "wzp6_ee_nunuH_HWW_ecm240", "wzp6_ee_qqH_HWW_ecm240", "wzp6_ee_tautauH_HWW_ecm240"]
    sigs = ["wzp6_ee_ssH_HWW_ecm240", "wzp6_ee_bbH_HWW_ecm240", "wzp6_ee_ccH_HWW_ecm240", "wzp6_ee_qqH_HWW_ecm240"]
    #sigs = ["wzp6_ee_nunuH_HWW_ecm240"]

    sig_scale = 1
    sig_legend = "Z(qq)H(W^{+}W^{#minus})"

    bkgs = ["WW", "ZZ"]
    bkgs_legends = ["W^{+}W^{#minus}", "ZZ"]
    bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
    bgks_cfg = { 
        "WW"        : [f"p8_ee_WW_ecm240"],
        "ZZ"        : [f"p8_ee_ZZ_ecm240"],
    }



    #makePlot("qq_mumu_muons_p", "qq_mumu_muons_p", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Muon momentum (GeV)", yLabel="Events", logY=True, rebin=1)
    #makePlot("qq_mumu_leading_muon_p", "qq_mumu_leading_muon_p", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Leading muon momentum (GeV)", yLabel="Events", logY=True, rebin=1)
    #makePlot("qq_mumu_subleading_muon_p", "qq_mumu_subleading_muon_p", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Subleading muon momentum (GeV)", yLabel="Events", logY=True, rebin=1)
    #quit()


    makePlot("qq_mumu_missingEnergy_pre", "qq_mumu_missingEnergy_pre", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Missing energy (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_cosThetaMiss_pre", "qq_mumu_cosThetaMiss_pre", xMin=0.95, xMax=1, yMin=1, yMax=-1, xLabel="cos(#theta_{miss})", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_dimuon_m_pre", "qq_mumu_dimuon_m_pre", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="m(#mu#mu) (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_dimuon_p_pre", "qq_mumu_dimuon_p_pre", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="p(#mu#mu) (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_dijet_m_pre", "qq_mumu_dijet_m_pre", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="m(qq) (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_dijet_p_pre", "qq_mumu_dijet_p_pre", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="p(qq) (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_recoil_m_pre", "qq_mumu_recoil_m_pre", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Recoil (GeV)", yLabel="Events", logY=True, rebin=1)

    makePlot("qq_mumu_jet1_p_pre", "qq_mumu_jet1_p_pre", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Jet 1 momentum (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_jet2_p_pre", "qq_mumu_jet2_p_pre", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Jet 2 momentum (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_dijet_dr_pre", "qq_mumu_dijet_dr_pre", xMin=0, xMax=10, yMin=1, yMax=-1, xLabel="Recoil (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_dimuon_dr_pre", "qq_mumu_dimuon_dr_pre", xMin=0, xMax=10, yMin=1, yMax=-1, xLabel="Recoil (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("qq_mumu_dimuon_dijet_dr_pre", "qq_mumu_dimuon_dijet_dr_pre", xMin=0, xMax=10, yMin=1, yMax=-1, xLabel="Recoil (GeV)", yLabel="Events", logY=True, rebin=1)

    makePlot("higgs_cand_m", "higgs_cand_m", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Recoil (GeV)", yLabel="Events", logY=True, rebin=1)
    makePlot("higgs_cand_p", "higgs_cand_p", xMin=0, xMax=240, yMin=1, yMax=-1, xLabel="Recoil (GeV)", yLabel="Events", logY=True, rebin=1)



    quit()
    makePlot("mumu_missingEnergy", "mumu_missingEnergy", xMin=140, xMax=240, yMin=1e0, yMax=-1, xLabel="Missing energy", yLabel="Events", logY=True, rebin=1)
    makePlot("ee_missingEnergy", "ee_missingEnergy", xMin=140, xMax=240, yMin=1e0, yMax=-1, xLabel="Missing energy", yLabel="Events", logY=True, rebin=1)
    makePlot("emu_missingEnergy", "emu_missingEnergy", xMin=140, xMax=240, yMin=1e0, yMax=-1, xLabel="Missing energy", yLabel="Events", logY=True, rebin=1)

    makePlot("mumu_m", "mumu_m", xMin=0, xMax=200, yMin=1e0, yMax=-1, xLabel="mll", yLabel="Events", logY=True, rebin=1)
    makePlot("ee_m", "ee_m", xMin=0, xMax=200, yMin=1e0, yMax=-1, xLabel="mll", yLabel="Events", logY=True, rebin=1)

