
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter


def recoil_plot(outName, files, hists, labels, colors, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False, norm=False, legLabel="", topRight=""):

    n = len(files) + (0 if legLabel=="" else 1)
    leg = ROOT.TLegend(.35, 0.9-0.05*n, 0.90, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.15)
    if legLabel != "":
        leg.SetHeader(legLabel)

    cfg = {

        'logy'              : logy,
        'logx'              : False,

        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax,

        'xtitle'            : xTitle,
        'ytitle'            : yTitle,

        'topRight'          : topRight, 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
    }

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")

    for i,h in enumerate(hists):
        lumi = lumi_240 if "ecm240" in hists[i] else lumi_365
        fIn = ROOT.TFile(files[i])
        hist = copy.deepcopy(fIn.Get(hists[i]))
        hist.Scale(lumi)
        if norm:
            x1, x2 = hist.FindBin(xMin), hist.FindBin(xMax)
            norm_ = hist.Integral(x1, x2)
            #norm_ = hist.Integral()
            hist.Scale(1./norm_)

        hist.Rebin(rebin)
        hist.SetLineColor(colors[i])
        hist.SetLineWidth(3)
        leg.AddEntry(hist, labels[i], "L")
        hist.Draw("SAME HIST C")
        #print(hist.Integral())


    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs(f"{outDir}/{outName}.png")
    canvas.SaveAs(f"{outDir}/{outName}.pdf")
    canvas.Close()



if __name__ == "__main__":

    tag = "test"
    lumi_240 = 10.8
    lumi_365 = 3

    if True: # Delphes vs FullSim
        topRight = "#sqrt{{s}} = 240 GeV, {} ab^{{#minus1}}".format(lumi_240)
        outDir = "/home/submit/jaeyserm/public_html/fccee/higgs_mass_xsec/plots/FastFullSim"
        colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1]

        files = ["output_ZH_mass_fast_fullsim.root", "output_ZH_mass_fast_fullsim.root", "output_ZH_mass_mumu_ecm240_sept20_scaleCorr.root"]
        hists = ["wzp6_ee_mumuH_ecm240_CLD/zll_recoil", "wzp6_ee_mumuH_ecm240_CLD_FullSim/zll_recoil", "wzp6_ee_mumuH_ecm240_CLD_FullSim/zll_recoil"]
        labels = ["IDEA Si Tracker (Delphes)", "CLD FullSim", "CLD FullSim (scale-corrected)"]
        #recoil_plot("CLD_recoil_scaleCorr", files, hists, labels, colors, 122, 132, 0, 0.015, "Recoil (GeV)", "Events", rebin=2, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H", norm=True, topRight=topRight)


        outDir = "/home/submit/jaeyserm/public_html/fccee/higgs_mass_xsec/plots/FastFullSim"
        colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1]

        files = ["output_ZH_mass_mumu_ecm240_test.root", "output_ZH_mass_mumu_ecm240_test.root"]
        hists = ["wzp6_ee_mumuH_ecm240_CLD/zll_recoil", "wzp6_ee_mumuH_ecm240_CLD_FullSim/zll_recoil"]
        labels = ["IDEA Si Tracker (Delphes)", "CLD (FullSim)"]
        recoil_plot("CLD_recoil", files, hists, labels, colors, 122, 132, 0, 0.015, "Recoil (GeV)", "Events", rebin=2, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H", norm=True, topRight=topRight)

    if False: # recoil for different ECM
        topRight = f"#sqrt{{s}} = 240/365 GeV"
        outDir = f"/home/submit/jaeyserm/public_html/fccee/higgs_mass_xsec/{tag}/plots/ecm_comparison"
        colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1]
        
        files = [f"output_ZH_mass_mumu_ecm365_{tag}.root", f"output_ZH_mass_mumu_ecm240_{tag}.root"]
        hists = ["wz3p6_ee_mumuH_ecm365/zll_recoil", "wzp6_ee_mumuH_ecm240/zll_recoil"]
        labels = ["365 GeV", "240 GeV"]
        recoil_plot("240_365GeV", files, hists, labels, colors, 122, 132, 0, 0.015, "Recoil (GeV)", "Events (a.u.)", rebin=2, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H", norm=True, topRight=topRight)
        

        files = ["output_ZH_mass_mumu_ecm365_compRec.root", "output_ZH_mass_mumu_ecm365_compRec.root", "output_ZH_mass_mumu_ecm365_compRec.root", "output_ZH_mass_mumu_ecm240_compRec.root"]
        hists = ["wz3p6_ee_mumuH_ecm365/zll_recoil", "wz3p6_ee_mumuH_noISR_ecm365/zll_recoil", "wz3p6_ee_mumuH_noBES_ecm365/zll_recoil", "wzp6_ee_mumuH_ecm240/zll_recoil"]
        labels = ["365 GeV", "365 GeV, noISR", "365 GeV, noBES", "240 GeV"]
        recoil_plot("240_365GeV_BES_ISR", files, hists, labels, colors, 122, 132, 0, 0.015, "Recoil (GeV)", "Events", rebin=2, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H", norm=True, topRight=topRight)

        quit()

        files = ["output_ZH_mass_mumu_ecm365_compRec_gen.root", "output_ZH_mass_mumu_ecm365_compRec_gen.root", "output_ZH_mass_mumu_ecm365_compRec_gen.root", "output_ZH_mass_mumu_ecm240_compRec_gen.root"]
        hists = ["wz3p6_ee_mumuH_ecm365/zll_recoil", "wz3p6_ee_mumuH_noISR_ecm365/zll_recoil", "wz3p6_ee_mumuH_noBES_ecm365/zll_recoil", "wzp6_ee_mumuH_ecm240/zll_recoil"]
        labels = ["365 GeV", "365 GeV, noISR", "365 GeV, noBES", "240 GeV"]
        recoil_plot("240_365GeV_BES_ISR_gen", files, hists, labels, colors, 122, 132, 0, 0.02, "Recoil (GeV)", "Events", rebin=2, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H (gen)", norm=True)


        files = ["output_ZH_mass_mumu_ecm365_compRec.root", "output_ZH_mass_mumu_ecm240_compRec.root"]
        hists = ["wz3p6_ee_mumuH_ecm365/zll_recoil", "wzp6_ee_mumuH_ecm240/zll_recoil"]
        labels = ["365 GeV", "240 GeV"]
        recoil_plot("240_365GeV", files, hists, labels, colors, 122, 132, 0, 0.01, "Recoil (GeV)", "Events", rebin=2, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H", norm=True)

        files = ["output_ZH_mass_mumu_ecm365_compRec.root", "output_ZH_mass_mumu_ecm240_compRec.root"]
        hists = ["wz3p6_ee_mumuH_ecm365/leps_reso_p_cut0", "wzp6_ee_mumuH_ecm240/leps_reso_p_cut0"]
        labels = ["365 GeV", "240 GeV"]
        recoil_plot("reso_240_365GeV", files, hists, labels, colors, 0.98, 1.02, 0, 0.005, "p(reco)/p(gen)", "Events", rebin=2, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H", norm=True)


    if False: # Recoil at 240 GeV
        outDir = f"/home/submit/jaeyserm/public_html/fccee/higgs_mass_xsec/{tag}/plots/recoil_comparison/"
        colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1]

        files = [f"output_ZH_mass_mumu_ecm240_{tag}.root", f"output_ZH_mass_mumu_ecm240_gen_{tag}.root", f"output_ZH_mass_mumu_ecm240_{tag}.root", f"output_ZH_mass_mumu_ecm240_{tag}.root"]
        hists = ["wzp6_ee_mumuH_ecm240/zll_recoil", "wzp6_ee_mumuH_ecm240/zll_recoil", "wzp6_ee_mumuH_ecm240_3T/zll_recoil", "wzp6_ee_mumuH_ecm240_CLD/zll_recoil"]
        labels = ["IDEA", "IDEA perfect resolution", "IDEA 3T", "IDEA CLD silicon tracker"]
        recoil_plot("IDEA_IDEAL_2T_3T_CLD_mumu", files, hists, labels, colors, 122, 132, 0, 2000, "Recoil (GeV)", "Events / 50 MeV", rebin=5, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H")

        files = [f"output_ZH_mass_ee_ecm240_{tag}.root", f"output_ZH_mass_ee_ecm240_gen_{tag}.root", f"output_ZH_mass_ee_ecm240_{tag}.root", f"output_ZH_mass_ee_ecm240_{tag}.root"]
        hists = ["wzp6_ee_eeH_ecm240/zll_recoil", "wzp6_ee_eeH_ecm240/zll_recoil", "wzp6_ee_eeH_ecm240_3T/zll_recoil", "wzp6_ee_eeH_ecm240_CLD/zll_recoil"]
        labels = ["IDEA", "IDEA perfect resolution", "IDEA 3T", "IDEA CLD silicon tracker"]
        recoil_plot("IDEA_IDEAL_2T_3T_CLD_ee", files, hists, labels, colors, 122, 132, 0, 2000, "Recoil (GeV)", "Events / 50 MeV", rebin=5, legLabel="Electron final state Z(e^{#plus}e^{#minus})H")

        files = [f"output_ZH_mass_mumu_ecm240_{tag}.root", f"output_ZH_mass_mumu_ecm240_{tag}.root", f"output_ZH_mass_ee_ecm240_{tag}.root", f"output_ZH_mass_ee_ecm240_{tag}.root"]
        hists = ["wzp6_ee_mumuH_ecm240/zll_recoil", "wzp6_ee_mumuH_ecm240_CLD/zll_recoil", "wzp6_ee_eeH_ecm240/zll_recoil", "wzp6_ee_eeH_ecm240_CLD/zll_recoil"]
        labels = ["IDEA 2T (#mu^{#plus}#mu^{#minus})", "CLD 2T (#mu^{#plus}#mu^{#minus})", "IDEA 2T (e^{#plus}e^{#minus})", "CLD 2T (e^{#plus}e^{#minus})"]
        recoil_plot("IDEA_CLD_mumu_ee", files, hists, labels, colors, 122, 132, 0, 2000, "Recoil (GeV)", "Events / 50 MeV", rebin=5)
