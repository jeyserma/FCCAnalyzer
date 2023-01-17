
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


import plotter



def makePlot():
	
    

    totEntries = 1 + len(bkgs)
    #leg = ROOT.TLegend(.5, 1.0-totEntries*0.06, .92, .90)
    leg = ROOT.TLegend(.45, 0.97-(len(bkgs)+2)*0.055, .95, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.03)
    leg.SetMargin(0.2)
    
    ret_hists = []
    h_sig = None
    for j,cut in enumerate(cuts):
        h = plotter.getProc(fIn, "cutFlow_%s" % cut, sigs)
        if h_sig == None: h_sig = h.Clone("sig")
        else: h_sig.Add(h)
	
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
        h_bkg = None
        for j,cut in enumerate(cuts):
            h = plotter.getProc(fIn, "cutFlow_%s" % cut, bgks_cfg[bkg])
            if h_bkg == None: h_bkg = h.Clone(bkg)
            else: h_bkg.Add(h)
		
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
        'ymin'              : 1e4,
        'ymax'              : 1e10 ,
            
        'xtitle'            : "",
        'ytitle'            : "Events",
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
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

    flavor = "ee"
    fIn = ROOT.TFile("tmp/output_mass_xsec_%s.root" % flavor)
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass_xsec/plots_%s/" % flavor
    
    cuts = ["cut0", "cut1", "cut2", "cut3", "cut4", "cut5", "cut6"]
    
    
    
    if flavor == "mumu":
    
        labels = ["All events", "#geq 1 #mu^{#pm} + ISO", "#geq 2 #mu^{#pm} + OS", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{T}^{#mu^{+}#mu^{#minus}} < 70", "|cos#theta_{miss}| < 0.98", "120 < m_{rec} < 140"]
    
        sigs = ["wzp6_ee_mumuH_ecm240"]
        sig_scale = 10
        sig_legend = "Z(#mu^{+}#mu^{#minus})H (10#times)"
    
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
    
        labels = ["All events", "#geq 1 e^{#pm} + ISO", "#geq 2 e^{#pm} + OS", "86 < m_{e^{+}e^{#minus}} < 96", "20 < p_{T}^{e^{+}e^{#minus}} < 70", "|cos#theta_{miss}| < 0.98", "120 < m_{rec} < 140"]
    
        sigs = ["wzp6_ee_eeH_ecm240"]
        sig_scale = 10
        sig_legend = "Z(e^{+}e^{#minus})H (10#times)"
    
        bkgs = ["WW", "ZZ", "Zg", "rare"] # this is the order of the plot
        bkgs_legends = ["W^{+}W^{#minus}", "ZZ", "Z/#gamma^{*} #rightarrow e^{+}e^{#minus}, #tau^{+}#tau^{#minus}", "Rare (e(e)Z, #gamma#gamma #rightarrow e^{+}e^{#minus}, #tau^{+}#tau^{#minus})"]
        
        bkgs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
        bgks_cfg = { 
            "WW"	    : ["p8_ee_WW_ecm240"],
            "ZZ"	    : ["p8_ee_ZZ_ecm240"],
            "Zg"        : ["wzp6_ee_ee_Mee_30_150_ecm240", "wzp6_ee_tautau_ecm240"],
            "rare"      : ["wzp6_egamma_eZ_Zee_ecm240", "wzp6_gammae_eZ_Zee_ecm240", "wzp6_gaga_ee_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]
        }
    
    
    hists = makePlot()
    
    
    
    rows = []
    for i,cut in enumerate(cuts):
        
        row = []
        row.append(cut)
        for j,histProc in enumerate(hists):
            
            #if j == 0: histProc.Scale(1./sig_scale)
            yield_, err = histProc.GetBinContent(i+1), histProc.GetBinError(i+1)
            row.append("%.2e %.2f" % (yield_, err))
            print(histProc, yield_, err)
        rows.append(row)
        
        
    def makeTable(rows, out, header=True):
    
        table = '''
<!DOCTYPE html>
<html>
<head>
<title>MathJax TeX Test Page</title>
<script type="text/x-mathjax-config">
    MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>
<script type="text/javascript"
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
</head>
<body>
<style>
            table, th, td {
              border: 1px solid black;
              border-collapse: collapse;
              padding: 10px;
              font: 16px Arial;
            }
</style>
        When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$
        '''
    
        table += '<table cellspcacing="" cellpadding="">\n'
        for row in rows:
            table += "    <tr>\n"
            for col in row:
                table += "        <td>%s</td>\n" % col
            table += "    </tr>\n"
        table += "</table>\n"
        
        fileout = open(out, "w")
        fileout.writelines(table)
        fileout.close()
    
    makeTable(rows, "%s/cutFlow.html" % outDir)
