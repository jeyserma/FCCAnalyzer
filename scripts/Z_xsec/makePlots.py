
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter


def makePlot(hName, outName, xMin=0, xMax=100, yMin=1, yMax=1e5, xLabel="xlabel", yLabel="Events", logX=False, logY=True, rebin=1, legPos=[0.65, 0.75, 0.9, 0.9]):


    st = ROOT.THStack()
    st.SetName("stack")
        
    leg = ROOT.TLegend(legPos[0], legPos[1], legPos[2], legPos[3])
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)
    
    st = ROOT.THStack()
    st.SetName("stack")
    h_tot = None
    for i,proc in enumerate(procs):
		
        hist = plotter.getProc(fIn, hName, procs_cfg[proc])
        hist.SetName(proc)
        hist.SetFillColor(procs_colors[i])
        hist.SetLineColor(ROOT.kBlack)
        hist.SetLineWidth(1)
        hist.SetLineStyle(1)
        hist.Rebin(rebin)
		
        leg.AddEntry(hist, procs_legends[i], "F")
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
            
        'topRight'          : "#sqrt{s} = 91 GeV, 155 ab^{#minus1}",
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",

    }
        

    plotter.cfg = cfg
    canvas = plotter.canvas()
        
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

    canvas.SaveAs("%s/%s.png" % (outDir, outName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, outName))
    canvas.Close()


	
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
        
    
    makePlot("zll_m_cut4", "zll_m_cut4", xMin=73, xMax=109, yMin=1e6, yMax=1e10, xLabel="m_{ll} (GeV)", yLabel="Events / 10 MeV", logY=True, rebin=1)
    makePlot("zll_p_cut4", "zll_p_cut4", xMin=0, xMax=5, yMin=1e7, yMax=1e10, xLabel="p_{ll} (GeV)", yLabel="Events / 10 MeV", logY=True, rebin=1)
    makePlot("leps_p_cut4", "leps_p_cut4", xMin=0, xMax=80, yMin=1e5, yMax=1e11, xLabel="p leptons (GeV)", yLabel="Events / 10 MeV", logY=True, rebin=1)
