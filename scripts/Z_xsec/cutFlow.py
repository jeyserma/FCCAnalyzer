
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter


def makePlot():
	
    leg = ROOT.TLegend(.5, 0.97-(len(procs)+2)*0.055, .8, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)

    st = ROOT.THStack()
    st.SetName("stack")
    h_tot = None
    for i,proc in enumerate(procs):
        h = None
        for j,cut in enumerate(cuts):
            h_ = plotter.getProc(fIn, "cutFlow_%s" % cut, procs_cfg[proc])
            if h == None: h = h_.Clone(proc)
            else: h.Add(h_)
		
        if h_tot == None: h_tot = h.Clone("h")
        else: h_tot.Add(h)
        
        h.SetFillColor(procs_colors[i])
        h.SetLineColor(ROOT.kBlack)
        h.SetLineWidth(1)
        h.SetLineStyle(1)
		
        leg.AddEntry(h, procs_legends[i], "F")
        st.Add(h)
        
    h_tot.SetLineColor(ROOT.kBlack)
    h_tot.SetLineWidth(2)
	


    ########### PLOTTING ###########
    cfg = {

        'logy'              : True,
        'logx'              : False,
        
        'xmin'              : 0,
        'xmax'              : len(cuts),
        'ymin'              : 1e10,
        'ymax'              : 1e12 ,
            
        'xtitle'            : "",
        'ytitle'            : "Events",
            
        'topRight'          : "#sqrt{s} = 91 GeV, 150 ab^{#minus1}", 
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
    h_tot.Draw("SAME HIST")
    leg.Draw("SAME")
      
    plotter.aux()
    canvas.RedrawAxis()
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs("%s/cutFlow.png" % outDir)
    canvas.SaveAs("%s/cutFlow.pdf" % outDir)
    

	
if __name__ == "__main__":

    flavor = "mumu"
    fIn = ROOT.TFile("tmp/output_z_xsec_%s.root" % flavor)
    outDir = "/eos/user/j/jaeyserm/www/FCCee/Z_xsec/plots_%s/" % flavor
    
    cuts = ["cut0", "cut1", "cut2", "cut3", "cut4"]

    if flavor == "mumu":
    
        labels = ["All events", "#geq 1 #mu^{#pm}", "#geq 2 #mu^{#pm}", "#mu^{+}#mu^{#minus} pair", "73 < m_{#mu^{+}#mu^{#minus}} < 109"]
    
        procs = ["Zmumu", "Ztautau"] # this is the order of the plot
        procs_legends = ["Z #rightarrow #mu^{+}#mu^{#minus}", "Z #rightarrow #tau^{+}#tau^{#minus}"]
        procs_colors = [ROOT.TColor.GetColor(248, 206, 104), ROOT.TColor.GetColor(222, 90, 106), ROOT.TColor.GetColor(100, 192, 232), ROOT.TColor.GetColor(155, 152, 204)] # from
        procs_cfg = { 
            "Zmumu"	        : ["p8_ee_Zmumu_ecm91"],
            "Ztautau"	    : ["p8_ee_Ztautau_ecm91"],
            "Zbb"           : ["p8_ee_Zbb_ecm91"],
            "Zcc"           : ["p8_ee_Zcc_ecm91"]
        }
        
    
    hists = makePlot()
    
    
  