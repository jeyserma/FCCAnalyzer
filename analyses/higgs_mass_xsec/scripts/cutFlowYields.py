
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
parser.add_argument("--mode", type=str, help="Simulation/detector mode", choices=["IDEA", "CLD", "CLD_FullSim"], default="IDEA")
parser.add_argument("--tag", type=str, help="Analysis tag", default="july24")
args = parser.parse_args()

mode_map = {}
mode_map['IDEA'] = "IDEA detector"
mode_map['CLD'] = "IDEA CLD silicon tracker"
mode_map['CLD_FullSim'] = "CLD detector (FullSim)"

def makePlot():

    totEntries = 1 + len(bkgs)
    leg = ROOT.TLegend(.45, 0.93-(len(bkgs)+3)*0.0425, .95, .93)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.SetMargin(0.2)
    leg.SetHeader(f"#bf{{{mode_map[args.mode]}}}")

    ret_hists = []
    h_sig = plotter.getProc(fIn, "cutFlow", sigs, lumiScale)
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
        h_bkg = plotter.getProc(fIn, "cutFlow", bgks_cfg[bkg], lumiScale)
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
        'ymin'              : 1e4 if args.ecm == 240 else 1e3,
        'ymax'              : 1e10 if args.ecm == 240 else 1e9,
            
        'xtitle'            : "",
        'ytitle'            : "Events",
            
        'topRight'          : lumi, 
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
    canvas.SaveAs(f"{outDir}/cutFlow_{args.mode}.png")
    canvas.SaveAs(f"{outDir}/cutFlow_{args.mode}.pdf")
    
    return ret_hists


if __name__ == "__main__":

    flavor = args.flavor
    ecm = args.ecm
    fIn = ROOT.TFile(f"output_ZH_{args.type}_{flavor}_ecm{ecm}_{args.tag}.root")
    outDir = f"/work/submit/jaeyserm/public_html/fccee/higgs_mass_xsec/{args.tag}/plots/{args.type}_{flavor}_{ecm}/"
    os.makedirs(outDir, exist_ok=True)

    lumiScale = 10.8 if ecm == 240 else 3
    lumi = "#sqrt{s} = 240 GeV, 10.8 ab^{#minus1}" if ecm == 240 else "#sqrt{s} = 365 GeV, 3 ab^{#minus1}"

    cuts = ["cut0", "cut1", "cut2", "cut3", "cut4", "cut5", "cut6"]

    if flavor == "mumu":

        labels = ["All events", "#geq 1 #mu^{#pm} + ISO", "#geq 2 #mu^{#pm} + OS", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{#mu^{+}#mu^{#minus}} < 70", "120 < m_{rec} < 140", "|cos#theta_{miss}| < 0.98"]
        if args.ecm == 365:
            labels = ["All events", "#geq 1 #mu^{#pm} + ISO", "#geq 2 #mu^{#pm} + OS", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "50 < p_{#mu^{+}#mu^{#minus}} < 150", "120 < m_{rec} < 140", "|cos#theta_{miss}| < 0.98"]

        if args.mode == "IDEA":
            sigs = [f"wzp6_ee_mumuH_ecm{ecm}"]
        elif args.mode == "CLD":
            sigs = [f"wzp6_ee_mumuH_ecm240_CLD"]
        elif args.mode == "CLD_FullSim":
            sigs = [f"wzp6_ee_mumuH_ecm240_CLD_FullSim"]
        sig_scale = 10
        sig_legend = "Z(#mu^{+}#mu^{#minus})H (10#times)"
    
        bkgs = ["WW", "ZZ", "Z/g", "Rare"] # this is the order of the plot
        bkgs_legends = ["W^{+}W^{#minus}", "ZZ", "Z/#gamma^{*} #rightarrow #mu^{+}#mu^{#minus}, #tau^{+}#tau^{#minus}", "Rare (e(e)Z, #gamma#gamma #rightarrow #mu^{+}#mu^{#minus}, #tau^{+}#tau^{#minus})"]
        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
        bgks_cfg = { 
            "WW"        : [f"p8_ee_WW_ecm{ecm}"],
            "ZZ"        : [f"p8_ee_ZZ_ecm{ecm}"],
            "Z/g"       : [f"wzp6_ee_mumu_ecm{ecm}", f"wzp6_ee_tautau_ecm{ecm}"],
            "Rare"      : [f"wzp6_egamma_eZ_Zmumu_ecm{ecm}", f"wzp6_gammae_eZ_Zmumu_ecm{ecm}", f"wzp6_gaga_mumu_60_ecm{ecm}", f"wzp6_gaga_tautau_60_ecm{ecm}", f"wzp6_ee_nuenueZ_ecm{ecm}"]
        }

    if flavor == "ee":

        labels = ["All events", "#geq 1 e^{#pm} + ISO", "#geq 2 e^{#pm} + OS", "86 < m_{e^{+}e^{#minus}} < 96", "20 < p_{e^{+}e^{#minus}} < 70", "120 < m_{rec} < 140", "|cos#theta_{miss}| < 0.98"]
        if args.ecm == 365:
            labels = ["All events", "#geq 1 e^{#pm} + ISO", "#geq 2 e^{#pm} + OS", "86 < m_{e^{+}e^{#minus}} < 96", "50 < p_{e^{+}e^{#minus}} < 150", "120 < m_{rec} < 140", "|cos#theta_{miss}| < 0.98"]

        sigs = [f"wzp6_ee_eeH_ecm{ecm}"]
        sig_scale = 10
        sig_legend = "Z(e^{+}e^{#minus})H (10#times)"

        bkgs = ["WW", "ZZ", "Z/g", "Rare"] # this is the order of the plot
        bkgs_legends = ["W^{+}W^{#minus}", "ZZ", "Z/#gamma^{*} #rightarrow e^{+}e^{#minus}, #tau^{+}#tau^{#minus}", "Rare (e(e)Z, #gamma#gamma #rightarrow e^{+}e^{#minus}, #tau^{+}#tau^{#minus})"]

        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
        bgks_cfg = { 
            "WW"        : [f"p8_ee_WW_ecm{ecm}"],
            "ZZ"        : [f"p8_ee_ZZ_ecm{ecm}"],
            "Z/g"       : [f"wzp6_ee_ee_Mee_30_150_ecm{ecm}", f"wzp6_ee_tautau_ecm{ecm}"],
            "Rare"      : [f"wzp6_egamma_eZ_Zee_ecm{ecm}", f"wzp6_gammae_eZ_Zee_ecm{ecm}", f"wzp6_gaga_ee_60_ecm{ecm}", f"wzp6_gaga_tautau_60_ecm{ecm}", f"wzp6_ee_nuenueZ_ecm{ecm}"]
        }

    hists = makePlot()

    with open(f"{outDir}/cutFlow_{args.mode}.txt", 'w') as f:
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
