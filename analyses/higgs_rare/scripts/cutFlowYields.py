
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

parser = argparse.ArgumentParser()
parser.add_argument("--flavor", type=str, help="Flavor (mumu or gaga)", default="mumu")
args = parser.parse_args()

def makePlot():

    totEntries = 1 + len(bkgs)
    #leg = ROOT.TLegend(.5, 1.0-totEntries*0.06, .92, .90)
    leg = ROOT.TLegend(.45, 0.99-(len(bkgs)+2)*0.055, .95, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.SetMargin(0.2)

    ret_hists = []
    h_sig = plotter.getProc(fIn, "cutFlow", sigs)
    '''
    h_sig = None
    for j,cut in enumerate(cuts):
        h = plotter.getProc(fIn, "cutFlow_%s" % cut, sigs)
        if h_sig == None: h_sig = h.Clone("sig")
        else: h_sig.Add(h)
    '''

    ret_hists.append(copy.deepcopy(h_sig))	
    h_sig.Scale(sig_scale)
    h_sig.SetLineColor(ROOT.TColor.GetColor("#BF2229"))
    h_sig.SetLineWidth(4)
    h_sig.SetLineStyle(1)
    leg.AddEntry(h_sig, sig_legend, "L")

    # Get all bkg histograms
    st = ROOT.THStack()
    st.SetName("stack")
    h_bkg_tot = None
    for i,bkg in enumerate(bkgs):
        h_bkg = plotter.getProc(fIn, "cutFlow", bgks_cfg[bkg])
        '''
        h_bkg = None
        for j,cut in enumerate(cuts):
            h = plotter.getProc(fIn, "cutFlow_%s" % cut, bgks_cfg[bkg])
            if h_bkg == None: h_bkg = h.Clone(bkg)
            else: h_bkg.Add(h)
        '''

        if h_bkg_tot == None: h_bkg_tot = h_bkg.Clone("h_bkg_tot")
        else: h_bkg_tot.Add(h_bkg)
        
        h_bkg.SetFillColor(bkgs_colors[i])
        h_bkg.SetLineColor(ROOT.kBlack)
        h_bkg.SetLineWidth(1)
        h_bkg.SetLineStyle(1)

        leg.AddEntry(h_bkg, bkgs_legends[i], "F")
        st.Add(h_bkg)
        ret_hists.append(h_bkg)	

    h_bkg_tot.SetLineColor(ROOT.kBlack)
    h_bkg_tot.SetLineWidth(2)



    ########### PLOTTING ###########
    cfg = {

        'logy'              : True,
        'logx'              : False,
        
        'xmin'              : 0,
        'xmax'              : len(cuts),
        'ymin'              : 1e2,
        'ymax'              : 1e9 ,
            
        'xtitle'            : "",
        'ytitle'            : "Events",
            
        'topRight'          : "#sqrt{s} = 240 GeV, 7.2 ab^{#minus1}", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
        }

    plotter.cfg = cfg

    canvas = plotter.canvas()
    canvas.SetGrid()
    canvas.SetTicks()
    dummy = plotter.dummy(len(cuts))
    dummy.GetXaxis().SetLabelSize(0.8*dummy.GetXaxis().GetLabelSize())
    dummy.GetXaxis().SetLabelOffset(1.3*dummy.GetXaxis().GetLabelOffset())
    for i,label in enumerate(labels): dummy.GetXaxis().SetBinLabel(i+1, label)
    dummy.GetXaxis().LabelsOption("u")
    dummy.Draw("HIST")

    st.Draw("SAME HIST")
    h_bkg_tot.Draw("SAME HIST")
    h_sig.Draw("SAME HIST")
    leg.Draw("SAME")

    plotter.aux()
    canvas.RedrawAxis()
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs("%s/cutFlow.png" % outDir)
    canvas.SaveAs("%s/cutFlow.pdf" % outDir)
    
    return ret_hists


if __name__ == "__main__":

    if args.flavor == "mumu":
        fIn = ROOT.TFile(f"output_h_mumu.root")
        outDir = f"/home/submit/jaeyserm/public_html/fccee/higgs_rare_mumu/baseline/"

        cuts = ["cut0", "cut1", "cut2", "cut3", "cut4", "cut5", "cut6", "cut7", "cut4"]

        labels = ["All events", "p_{#gamma} < 40 GeV", "#geq 2 #mu^{#pm}", "80 < m_{rec} < 120", "20 < p_{#mu^{+}#mu^{#minus}} < 65", "|cos#theta_{miss}| < 0.98", "Missing energy", "Acolinearity > 0.05", "110 < m_{#mu^{+}#mu^{#minus}} < 130"]

        sigs = ["wzp6_ee_nunuH_Hmumu_ecm240", "wzp6_ee_eeH_Hmumu_ecm240", "wzp6_ee_tautauH_Hmumu_ecm240", "wzp6_ee_ccH_Hmumu_ecm240", "wzp6_ee_bbH_Hmumu_ecm240", "wzp6_ee_qqH_Hmumu_ecm240", "wzp6_ee_ssH_Hmumu_ecm240", "wzp6_ee_mumuH_Hmumu_ecm240"]
        sig_scale = 1000
        sig_legend = "Z(#mu^{+}#mu^{#minus})H (#times 1000)"
        
        bkgs = ["WW", "ZZ", "Zg", "rare"]
        bkgs_legends = ["W^{+}W^{#minus}", "ZZ", "Z/#gamma^{*} #rightarrow #mu^{+}#mu^{#minus}, #tau^{+}#tau^{#minus}", "Rare (e(e)Z, #gamma#gamma #rightarrow #mu^{+}#mu^{#minus}, #tau^{+}#tau^{#minus})"]
        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
        bgks_cfg = { 
            "WW"        : ["p8_ee_WW_ecm240"],
            "ZZ"        : ["p8_ee_ZZ_ecm240"],
            "Zg"        : ["wzp6_ee_mumu_ecm240", "wzp6_ee_tautau_ecm240"],
            "rare"      : ["wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gaga_mumu_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]
        }

        hists = makePlot()
        quit()
        with open("%s/cutFlow.txt" % outDir, 'w') as f:
            sys.stdout = f

            formatted_row = '{:<10} {:<25} {:<25} {:<25} {:<25} {:<25}'
            print(formatted_row.format(*(["Cut", "Signal"]+bkgs)))
            print(formatted_row.format(*(["----------"]+["-----------------------"]*5)))
            for i,cut in enumerate(cuts):

                row = ["Cut %d"%i]
                for j,histProc in enumerate(hists):

                    yield_, err = histProc.GetBinContent(i+1), histProc.GetBinError(i+1)
                    row.append("%.2e +/- %.2e" % (yield_, err))

                print(formatted_row.format(*row))



    if args.flavor == "aa":
        fIn = ROOT.TFile(f"output_h_aa.root")
        outDir = f"/home/submit/jaeyserm/public_html/fccee/higgs_rare_aa/baseline/"

        cuts = ["cut0", "cut1", "cut2", "cut3", "cut4", "cut5", "cut6", "cut7"]

        labels = ["All events", "#geq 1 #gamma", "#geq 2 #gamma", "#geq 1 resonance", "80 < m_{rec} < 120", "20 < p_{#gamma#gamma} < 65", "Missing energy", "110 < m_{#gamma#gamma} < 130"]

        sigs = ["wzp6_ee_nunuH_Haa_ecm240", "wzp6_ee_eeH_Haa_ecm240", "wzp6_ee_tautauH_Haa_ecm240", "wzp6_ee_ccH_Haa_ecm240", "wzp6_ee_bbH_Haa_ecm240", "wzp6_ee_qqH_Haa_ecm240", "wzp6_ee_ssH_Haa_ecm240", "wzp6_ee_mumuH_Haa_ecm240"]
        sig_scale = 100
        sig_legend = "ZH(#gamma#gamma) (#times 100)"
    
        bkgs = ["gg", "qq"]

        bkgs_legends = ["#gamma#gamma", "Z/#gamma^{*} #rightarrow qq+#gamma(#gamma) (KKMC)"]
        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)]
        bgks_cfg = { 
            "gg"    : ["wzp6_ee_gammagamma_ecm240"],
            "qq"    : ["kkmcee_ee_uu_ecm240", "kkmcee_ee_dd_ecm240", "kkmcee_ee_cc_ecm240", "kkmcee_ee_ss_ecm240", "kkmcee_ee_bb_ecm240"]
        }

        hists = makePlot()
        quit()
        with open("%s/cutFlow.txt" % outDir, 'w') as f:
            sys.stdout = f

            formatted_row = '{:<10} {:<25} {:<25} {:<25} {:<25} {:<25}'
            print(formatted_row.format(*(["Cut", "Signal"]+bkgs)))
            print(formatted_row.format(*(["----------"]+["-----------------------"]*5)))
            for i,cut in enumerate(cuts):

                row = ["Cut %d"%i]
                for j,histProc in enumerate(hists):

                    yield_, err = histProc.GetBinContent(i+1), histProc.GetBinError(i+1)
                    row.append("%.2e +/- %.2e" % (yield_, err))

                print(formatted_row.format(*row))
