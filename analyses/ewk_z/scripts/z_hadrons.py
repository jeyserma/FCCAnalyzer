
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


def makePlot_compare(procs, hName, xMin=0, xMax=100, yMin=0, yMax=-1, xLabel="xlabel", yLabel="Events", rebin=1, logX=False, logY=False, norm=False, yRatio=1.15, normRange=[]):

    hists, rhists = [], []
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1]

    leg = ROOT.TLegend(.2, 0.9-0.07*len(procs), 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetMargin(0.12)
    leg.SetTextSize(0.035)

    for i,proc in enumerate(procs):
        print(proc, hName)
        hist = plotter.getProc(fIn, hName, procDict[proc]['procs'])
        hist.Rebin(rebin)

        scale = hist.Integral()
        if len(normRange) > 0:
            scale = hist.Integral(hist.FindBin(normRange[0]), hist.FindBin(normRange[1])+1)
        scale = scale if scale > 0 else 1
        

        hist.SetLineColor(colors[i])
        hist.SetLineWidth(2)
        if norm:
            hist.Scale(1./scale)

        leg.AddEntry(hist, procDict[proc]['label'], "L")
        hists.append(hist)
        if i > 0:
            rhist = hist.Clone(f"rhist_{proc}")
            rhist.Divide(hists[0])
            rhists.append(rhist)

    cfg = {
        'logy'              : logY,
        'logx'              : logX,

        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else 1.3*max([h.GetMaximum() for h in hists]),

        'xtitle'            : xLabel,
        'ytitle'            : yLabel,

        'topRight'          : "#sqrt{s} = 91.2 GeV", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",

        'ratiofraction'     : 0.3,
        'ytitleR'           : "Ratio",

        'yminR'             : 1-(yRatio-1),
        'ymaxR'             : yRatio,
    }

    ## top panel
    plotter.cfg = cfg
    canvas, padT, padB = plotter.canvasRatio()
    dummyT, dummyB, dummyL = plotter.dummyRatio()

    ## top panel
    canvas.cd()
    padT.Draw()
    padT.cd()
    padT.SetGrid()
    dummyT.Draw("HIST")

    for hist in hists:
        hist.Draw("SAME HIST")
    leg.Draw("SAME")
    plotter.auxRatio()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    ## bottom panel
    canvas.cd()
    padB.Draw()
    padB.SetFillStyle(0)
    padB.cd()
    dummyB.Draw("HIST")
    dummyL.Draw("SAME")

    for hist in rhists:
        hist.Draw("PE0 SAME")

    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs(f"{outDir}/{hName}.png")
    canvas.SaveAs(f"{outDir}/{hName}.pdf")
    canvas.Close()


def makePlot(hName, outName, xMin=0, xMax=100, yMin=1, yMax=1e5, xLabel="xlabel", yLabel="Events", logX=False, logY=True, rebin=1):

    st = ROOT.THStack()
    st.SetName("stack")

    leg = ROOT.TLegend(0.4, 0.92-0.04*len(procs), 0.9, 0.92)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.SetMargin(0.2)


    st = ROOT.THStack()
    st.SetName("stack")
    h_tot = None
    for i,proc in enumerate(procs):
        print(proc)
        hist = plotter.getProc(fIn, hName, procDict[proc]['procs'])
        if "TH2" in hist.ClassName(): hist = hist.ProjectionX()
        hist.SetName(proc)
        hist.SetFillColor(procDict[proc]['fillcolor'])
        hist.SetLineColor(ROOT.kBlack)
        hist.SetLineWidth(1)
        hist.SetLineStyle(1)
        hist.Rebin(rebin)

        leg.AddEntry(hist, procDict[proc]['label'], "F")
        st.Add(hist)
        if h_tot == None:
            h_tot = copy.deepcopy(hist)
            h_tot.SetName("h_tot")
        else: h_tot.Add(hist)

    cfg = {

        'logy'              : logY,
        'logx'              : logX,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else ath.ceil(h_tot.GetMaximum()*100)/10.,
            
        'xtitle'            : xLabel,
        'ytitle'            : yLabel,
            
        'topRight'          : "#sqrt{s} = 91.2 GeV, 44.84 pb^{#minus1}",
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",

    }

    plotter.cfg = cfg
    canvas = plotter.canvas(width=850, height=1200)
    dummy = plotter.dummy()
    dummy.Draw("HIST") 
    st.Draw("HIST SAME")


    h_tot.SetLineColor(ROOT.kBlack)
    h_tot.SetFillColor(0)
    h_tot.SetLineWidth(2)
    h_tot.Draw("HIST SAME")
    leg.Draw("SAME")
    
    canvas.SetGrid()
    canvas.Modify()
    canvas.Update()

    plotter.aux()
    ROOT.gPad.SetTicks()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs(f"{outDir}/{outName}.png")
    canvas.SaveAs(f"{outDir}/{outName}.pdf")
    canvas.Close()



if __name__ == "__main__":

    procDict = {}
    procDict['kkmcee_ee_qq_ecm91p2'] = {
        'procs': ['kkmcee_ee_uu_ecm91p2', 'kkmcee_ee_dd_ecm91p2', 'kkmcee_ee_ss_ecm91p2', 'kkmcee_ee_cc_ecm91p2', 'kkmcee_ee_bb_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow hadrons (#gamma) (KKMCee)",
        'fillcolor': ROOT.kWhite,
    }
    procDict['wzp6_ee_qq_ecm91p2'] = {
        'procs': ['wzp6_ee_qq_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow hadrons (#gamma) (Whizard)",
        'fillcolor': ROOT.kWhite,
    }
    procDict['wzp6_ee_tautau_ecm91p2'] = {
        'procs': ['wzp6_ee_tautau_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow #tau^{#plus}#tau^{#minus}(#gamma) (Whizard)",
        'fillcolor': ROOT.TColor.GetColor(222, 90, 106),
    }
    procDict['p8_ee_Ztautau_ecm91'] = {
        'procs': ['p8_ee_Ztautau_ecm91'],
        'label': "e^{#plus}e^{#minus} #rightarrow #tau^{#plus}#tau^{#minus}(#gamma) (Pythia8)",
        'fillcolor': ROOT.TColor.GetColor(222, 90, 106),
    }
    procDict['kkmcee_ee_ee_ecm91p2'] = {
        'procs': ['kkmcee_ee_ee_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow e^{#plus}e^{#minus}(#gamma) (KKMCee)",
        'fillcolor': ROOT.TColor.GetColor(155, 152, 204),
    }
    procDict['kkmcee_ee_mumu_ecm91p2'] = {
        'procs': ['kkmcee_ee_mumu_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow #mu^{#plus}#mu^{#minus}(#gamma) (KKMCee)",
        'fillcolor': ROOT.TColor.GetColor(100, 192, 232),
    }
    procDict['kkmcee_ee_tautau_ecm91p2'] = {
        'procs': ['kkmcee_ee_tautau_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow #tau^{#plus}#tau^{#minus}(#gamma) (KKMCee)",
        'fillcolor': ROOT.TColor.GetColor(222, 90, 106),
    }
    procDict['wz3p6_ee_gaga_qq_ecm91p2'] = {
        'procs': ['wz3p6_ee_gaga_qq_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow e^{#plus}e^{#minus} + hadrons (Whizard)",
        'fillcolor': ROOT.TColor.GetColor(248, 206, 104),
    }
    procDict['p8_ee_gaga_qq_ecm91p2'] = {
        'procs': ['p8_ee_gaga_qq_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow e^{#plus}e^{#minus} + hadrons (Pythia8)",
        'fillcolor': ROOT.TColor.GetColor(248, 206, 104),
    }
    
    procDict['p8_ee_uu_ecm91p2'] = {
        'procs': ['p8_ee_uu_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow e^{#plus}e^{#minus} + u#bar{u} (Pythia8)",
        'fillcolor': ROOT.TColor.GetColor(248, 206, 104),
    }
    procDict['wz3p6_ee_uu_ALEPH_ecm91p2'] = {
        'procs': ['wz3p6_ee_uu_ALEPH_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow e^{#plus}e^{#minus} + u#bar{u} (Whizard + Pythia6 ALEPH)",
        'fillcolor': ROOT.TColor.GetColor(248, 206, 104),
    }
    procDict['wz3p6_ee_uu_ecm91p2'] = {
        'procs': ['wz3p6_ee_uu_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow e^{#plus}e^{#minus} + u#bar{u} (Whizard + Pythia6 OPAL)",
        'fillcolor': ROOT.TColor.GetColor(248, 206, 104),
    }
    procDict['kkmcee_ee_mumu_ecm91p2'] = {
        'procs': ['kkmcee_ee_mumu_ecm91p2'],
        'label': "e^{#plus}e^{#minus} #rightarrow e^{#plus}e^{#minus} + u#bar{u} (KKMCee + Pythia8)",
        'fillcolor': ROOT.TColor.GetColor(248, 206, 104),
    }


    if False: # acceptance
        fIn = ROOT.TFile(f"output_z_hadrons.root")
        fIn.ls()
        h_wzp6 = fIn.Get("wzp6_ee_qq_ecm91p2/cutFlow")
        h_kkmcee_uu = fIn.Get("kkmcee_ee_uu_ecm91p2/cutFlow")
        h_kkmcee_dd = fIn.Get("kkmcee_ee_dd_ecm91p2/cutFlow")
        h_kkmcee_cc = fIn.Get("kkmcee_ee_cc_ecm91p2/cutFlow")
        h_kkmcee_ss = fIn.Get("kkmcee_ee_ss_ecm91p2/cutFlow")
        h_kkmcee_bb = fIn.Get("kkmcee_ee_bb_ecm91p2/cutFlow")
        
        h_kkmcee = fIn.Get("kkmcee_ee_uu_ecm91p2/cutFlow")
        h_kkmcee.Add(h_kkmcee_dd)
        h_kkmcee.Add(h_kkmcee_cc)
        h_kkmcee.Add(h_kkmcee_ss)
        h_kkmcee.Add(h_kkmcee_bb)
        
        print("h_wzp6", h_wzp6.GetBinContent(1), h_wzp6.GetBinContent(2), h_wzp6.GetBinContent(2)/h_wzp6.GetBinContent(1))
        print("h_kkmcee", h_kkmcee.GetBinContent(1), h_kkmcee.GetBinContent(2), h_kkmcee.GetBinContent(2)/h_kkmcee.GetBinContent(1))
        
        print("h_kkmcee_uu", h_kkmcee.GetBinContent(1), h_kkmcee_uu.GetBinContent(2), h_kkmcee_uu.GetBinContent(2)/h_kkmcee_uu.GetBinContent(1))
        print("h_kkmcee_dd", h_kkmcee.GetBinContent(1), h_kkmcee_dd.GetBinContent(2), h_kkmcee_dd.GetBinContent(2)/h_kkmcee_dd.GetBinContent(1))
        print("h_kkmcee_cc", h_kkmcee.GetBinContent(1), h_kkmcee_cc.GetBinContent(2), h_kkmcee_cc.GetBinContent(2)/h_kkmcee_cc.GetBinContent(1))
        print("h_kkmcee_ss", h_kkmcee_ss.GetBinContent(1), h_kkmcee_ss.GetBinContent(2), h_kkmcee_ss.GetBinContent(2)/h_kkmcee_ss.GetBinContent(1))
        print("h_kkmcee_bb", h_kkmcee_bb.GetBinContent(1), h_kkmcee_bb.GetBinContent(2), h_kkmcee_bb.GetBinContent(2)/h_kkmcee_bb.GetBinContent(1))
        
    if False:
        procs = ["p8_ee_Ztautau_ecm91", "wzp6_ee_tautau_ecm91p2", "kkmcee_ee_tautau_ecm91p2"]
        outDir = f"/home/submit/jaeyserm/public_html/fccee/z_hadrons/plots_comparison_tautau/"
        fIn = ROOT.TFile(f"output_z_hadrons_tautau.root")
        
        procs = ["p8_ee_gaga_qq_ecm91p2", "wz3p6_ee_gaga_qq_ecm91p2"]
        outDir_c = f"/home/submit/jaeyserm/public_html/fccee/z_hadrons/plots_comparison_gaga/"
        fIn = ROOT.TFile(f"output_z_hadrons_gaga.root")
        
        makePlot_compare(procs, "visible_energy_norm_nCut", xMin=0, xMax=1.5, yMin=1e-1, yMax=1e6, xLabel="E_{vis}/#sqrt{s}", rebin=1, logY=True)
        makePlot_compare(procs, "visible_energy_norm_nOne", xMin=0, xMax=1.5, yMin=1e-1, yMax=1e6, xLabel="E_{vis}/#sqrt{s}", rebin=1, logY=True)

    if False: # RECO/GEN particles
        procs = ["kkmcee_ee_qq_ecm91p2", "wzp6_ee_qq_ecm91p2"]
        outDir = f"/home/submit/jaeyserm/public_html/fccee/z_hadrons/plots_comparison_qq/"
        fIn = ROOT.TFile(f"output_z_hadrons.root")
        
        makePlot_compare(procs, "RP_theta", xMin=0, xMax=3.15, yMin=0, yMax=0.01, yRatio=1.01, xLabel="#theta reco particles (rad)", yLabel="Events (normalized)", rebin=1, logY=False, norm=True)
        makePlot_compare(procs, "GP_theta", xMin=0, xMax=3.15, yMin=0, yMax=0.01, xLabel="#theta gen particles (rad)", yLabel="Events (normalized)", rebin=1, logY=False, norm=True)

    if True: # uu plots
        procs = ["p8_ee_uu_ecm91p2", "wz3p6_ee_uu_ALEPH_ecm91p2", "wz3p6_ee_uu_ecm91p2"]
        outDir = f"/home/submit/jaeyserm/public_html/fccee/z_hadrons/plots_comparison_uu/"
        fIn = ROOT.TFile(f"output_z_hadrons_uu.root")

        makePlot_compare(procs, "visible_energy_norm_nCut", xMin=0, xMax=1.2, yMin=1e-6, yMax=1e0, xLabel="E_{vis}/#sqrt{s}", yLabel="Events (normalized)", rebin=1, logY=True, norm=True)
        makePlot_compare(procs, "RP_no", xMin=0, xMax=100, yMin=1e-6, yMax=1e2, xLabel="Number of reco particles", yLabel="Events (normalized)", rebin=1, logY=True, norm=True, yRatio=1.3)
        makePlot_compare(procs, "GP_no", xMin=0, xMax=100, yMin=1e-6, yMax=1e2, xLabel="Number of gen particles", yLabel="Events (normalized)", rebin=1, logY=True, norm=True)

        makePlot_compare(procs, "RP_theta", xMin=0, xMax=3.15, yMin=0, yMax=0.01, yRatio=1.01, xLabel="#theta reco particles (rad)", yLabel="Events (normalized)", rebin=1, logY=False, norm=True, normRange=[0.1, 3.1])
        makePlot_compare(procs, "GP_theta", xMin=0, xMax=3.15, yMin=0, yMax=0.01, xLabel="#theta gen particles (rad)", yLabel="Events (normalized)", rebin=1, logY=False, norm=True, normRange=[0.1, 3.1])


    if False: # tau plots
        procs = ["p8_ee_Ztautau_ecm91", "wzp6_ee_tautau_ecm91p2", "kkmcee_ee_tautau_ecm91p2"]
        outDir = f"/home/submit/jaeyserm/public_html/fccee/z_hadrons/plots_comparison_tautau/"
        fIn = ROOT.TFile(f"output_z_hadrons.root")

        makePlot_compare(procs, "visible_energy_norm_nCut", xMin=0, xMax=1.5, yMin=1e-6, yMax=1e0, xLabel="E_{vis}/#sqrt{s}", yLabel="Events (normalized)", rebin=1, logY=True, norm=True)
        makePlot_compare(procs, "RP_no", xMin=0, xMax=25, yMin=1e-6, yMax=1e2, xLabel="Number of reco particles", yLabel="Events (normalized)", rebin=1, logY=True, norm=True, yRatio=1.3)
        makePlot_compare(procs, "GP_no", xMin=0, xMax=25, yMin=1e-6, yMax=1e2, xLabel="Number of gen particles", yLabel="Events (normalized)", rebin=1, logY=True, norm=True)

    if False:

        
        procs = ["p8_ee_gaga_qq_ecm91p2", "wz3p6_ee_gaga_qq_ecm91p2"]
        outDir_c = f"/home/submit/jaeyserm/public_html/fccee/z_hadrons/plots_comparison_gaga/"
        fIn = ROOT.TFile(f"output_z_hadrons_gaga.root")
        
        makePlot_compare(procs, "visible_energy_norm_nCut", xMin=0, xMax=1.5, yMin=1e-1, yMax=1e6, xLabel="E_{vis}/#sqrt{s}", rebin=1, logY=True)
        makePlot_compare(procs, "visible_energy_norm_nOne", xMin=0, xMax=1.5, yMin=1e-1, yMax=1e6, xLabel="E_{vis}/#sqrt{s}", rebin=1, logY=True)
        
        makePlot_compare(procs, "RP_no_barrel_nCut", xMin=0, xMax=50, yMin=1e-1, yMax=1e6, xLabel="Number of particles (barrel)", rebin=1, logY=True)
        makePlot_compare(procs, "RP_no_endcap_nCut", xMin=0, xMax=50, yMin=1e-1, yMax=1e6, xLabel="Number of particles (endcap)", rebin=1, logY=True)
        
        makePlot_compare(procs, "RP_no_barrel_nOne", xMin=0, xMax=50, yMin=1e-1, yMax=1e6, xLabel="Number of particles (barrel)", rebin=1, logY=True)
        makePlot_compare(procs, "RP_no_endcap_nOne", xMin=0, xMax=50, yMin=1e-1, yMax=1e6, xLabel="Number of particles (endcap)", rebin=1, logY=True)

        makePlot_compare(procs, "energy_imbalance_long_nCut", xMin=0, xMax=1, yMin=0.1, yMax=1e6, xLabel="energy_imbalance_long_nOne", logY=True, rebin=2)
        makePlot_compare(procs, "energy_imbalance_trans_nCut", xMin=0, xMax=1, yMin=0.1, yMax=1e6, xLabel="energy_imbalance_trans_nOne", logY=True, rebin=2)

        makePlot_compare(procs, "energy_imbalance_long_nOne", xMin=0, xMax=1, yMin=0.1, yMax=1e6, xLabel="energy_imbalance_long_nOne", logY=True, rebin=2)
        makePlot_compare(procs, "energy_imbalance_trans_nOne", xMin=0, xMax=1, yMin=0.1, yMax=1e6, xLabel="energy_imbalance_trans_nOne", logY=True, rebin=2)


    if False:
        fIn = ROOT.TFile(f"output_z_hadrons.root")
        outDir = f"/home/submit/jaeyserm/public_html/fccee/z_hadrons/plots/"
        
        procs = ["wz3p6_ee_gaga_qq_ecm91p2", "wzp6_ee_tautau_ecm91p2", "wzp6_ee_qq_ecm91p2"]
        procs = ["p8_ee_gaga_qq_ecm91p2", "kkmcee_ee_tautau_ecm91p2", "kkmcee_ee_qq_ecm91p2"]
        #procs = ["wzp6_ee_tautau_ecm91p2",  "wz3p6_ee_gaga_qq_ecm91p2", "wzp6_ee_qq_ecm91p2"]
        fIn.ls()
        # no cut plots
        makePlot("visible_energy_norm_nCut", "visible_energy_norm_nCut", xMin=0.2, xMax=2.4, yMin=0.1, yMax=1e7, xLabel="E_{vis}/#sqrt{s}", yLabel="Events", logY=True, rebin=1)
        makePlot("visible_energy_norm_nOne", "visible_energy_norm_nOne", xMin=0.2, xMax=2.4, yMin=0.1, yMax=1e7, xLabel="E_{vis}/#sqrt{s}", yLabel="Events", logY=True, rebin=1)


        makePlot("thrust_costheta_nCut", "thrust_costheta_nCut", xMin=0, xMax=1, yMin=0, yMax=1e5, xLabel="|cos(#theta_{t})|", yLabel="Events", logY=False, rebin=1)
        makePlot("thrust_magn_nCut", "thrust_magn_nCut", xMin=0, xMax=1, yMin=0, yMax=1e5, xLabel="Thrust magnitude", yLabel="Events", logY=False, rebin=1)
        
        #makePlot("thrust_costheta", "thrust_costheta", xMin=0, xMax=1, yMin=0, yMax=1e5, xLabel="|cos(#theta_{t})|", yLabel="Events", logY=False, rebin=1)
        #makePlot("thrust_magn", "thrust_magn", xMin=0, xMax=1, yMin=0, yMax=1e5, xLabel="Thrust magnitude", yLabel="Events", logY=False, rebin=1)


        makePlot("energy_imbalance_long_nCut", "energy_imbalance_long_nCut", xMin=0, xMax=1, yMin=0.1, yMax=1e7, xLabel="E_{long}/E_{vis}", yLabel="Events", logY=True, rebin=2)
        makePlot("energy_imbalance_trans_nCut", "energy_imbalance_trans_nCut", xMin=0, xMax=1, yMin=0.1, yMax=1e7, xLabel="E_{trans}/E_{vis}", yLabel="Events", logY=True, rebin=2)

        makePlot("energy_imbalance_long_nOne", "energy_imbalance_long_nOne", xMin=0, xMax=1, yMin=0.1, yMax=1e7, xLabel="E_{long}/E_{vis}", yLabel="Events", logY=True, rebin=2)
        makePlot("energy_imbalance_trans_nOne", "energy_imbalance_trans_nOne", xMin=0, xMax=1, yMin=0.1, yMax=1e7, xLabel="E_{trans}/E_{vis}", yLabel="Events", logY=True, rebin=2)
        

        # N-1 plots
        
        # check ncut with all MC

        
        procs = ["kkmcee_ee_mumu_ecm91p2", "kkmcee_ee_ee_ecm91p2", "p8_ee_gaga_qq_ecm91p2", "kkmcee_ee_tautau_ecm91p2", "kkmcee_ee_qq_ecm91p2"]

        makePlot("visible_energy_norm_nCut", "visible_energy_norm_nCut", xMin=0.0, xMax=1.5, yMin=0.1, yMax=1e8, xLabel="E_{vis}/#sqrt{s}", yLabel="Events", logY=True, rebin=1)

        makePlot("thrust_costheta_nCut", "thrust_costheta_nCut", xMin=0, xMax=1, yMin=0, yMax=1e5, xLabel="|cos(#theta_{t})|", yLabel="Events", logY=False, rebin=1)
        makePlot("thrust_magn_nCut", "thrust_magn_nCut", xMin=0, xMax=1, yMin=0, yMax=1e5, xLabel="Thrust magnitude", yLabel="Events", logY=False, rebin=1)

        makePlot("energy_imbalance_long_nCut", "energy_imbalance_long_nCut", xMin=0, xMax=1, yMin=0.1, yMax=1e6, xLabel="E_{long}/E_{vis}", yLabel="Events", logY=True, rebin=2)
        makePlot("energy_imbalance_trans_nCut", "energy_imbalance_trans_nCut", xMin=0, xMax=1, yMin=0.1, yMax=1e6, xLabel="E_{trans}/E_{vis}", yLabel="Events", logY=True, rebin=2)

        makePlot("RP_no_barrel_nCut", "RP_no_barrel_nCut", xMin=0, xMax=120, yMin=0.1, yMax=1e7, xLabel="Number of particles (barrel)", yLabel="Events", logY=True, rebin=1)
        makePlot("RP_no_endcap_nCut", "RP_no_endcap_nCut", xMin=0, xMax=120, yMin=0.1, yMax=1e7, xLabel="Number of particles (endcap)", yLabel="Events", logY=True, rebin=1)
        makePlot("RP_no_barrel_nOne", "RP_no_barrel_nOne", xMin=0, xMax=120, yMin=0.1, yMax=1e7, xLabel="Number of particles (barrel)", yLabel="Events", logY=True, rebin=1)
        makePlot("RP_no_endcap_nOne", "RP_no_endcap_nOne", xMin=0, xMax=120, yMin=0.1, yMax=1e7, xLabel="Number of particles (endcap)", yLabel="Events", logY=True, rebin=1)


