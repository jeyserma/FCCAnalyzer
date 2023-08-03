
import sys,array,ROOT,math,os,copy,ctypes

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


import plotter

def getYield(proc, sel):

    hName = "cosTheta_miss" # take an event variable, always filled regardless the cut
    
    xMin=-1e6
    xMax=1e6
        
    fIn = ROOT.TFile("%s/%s_hists.root" % (histDir, proc))
    h = fIn.Get("%s_%s" % (hName, sel))
    h.Scale(lumi*ds.datasets[proc]['xsec']*1e6/ds.datasets[proc]['nevents'])


    xbinMin = h.GetXaxis().FindBin(xMin)
    xbinMax = h.GetXaxis().FindBin(xMax)
    
 
    evYield, err = 0, 0
    for i in range(xbinMin, xbinMax):
    
        evYield += h.GetBinContent(i) 
        err += h.GetBinError(i)**2
    
    err = err**0.5

    y = h.Integral()
    fIn.Close()
    
    return y, err

def makePlot():
	
    

    totEntries = 1 + len(bkgs)
    #leg = ROOT.TLegend(.5, 1.0-totEntries*0.06, .92, .90)
    leg = ROOT.TLegend(.5, 0.97-(len(bkgs)+2)*0.055, .8, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)
    
    h_sig = None
    for j,cut in enumerate(cuts):
        h = plotter.getProc(fIn, "cutFlow_%s" % cut, sigs)
        if h_sig == None: h_sig = h.Clone("sig")
        else: h_sig.Add(h)
		
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
        
    h_bkg_tot.SetLineColor(ROOT.kBlack)
    h_bkg_tot.SetLineWidth(2)
	


    ########### PLOTTING ###########
    cfg = {

        'logy'              : True,
        'logx'              : False,
        
        'xmin'              : 0,
        'xmax'              : 7,
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
    
	
	
	
if __name__ == "__main__":

    flavor = "mumu"
    fIn = ROOT.TFile("tmp/output_mass_xsec_%s.root" % flavor)
    outDir = "/eos/user/j/jaeyserm/www/FCC-ee/ZH_mass_xsec/plots_%s/" % flavor
    
    
    h = fIn.Get("wzp6_ee_%sH_ecm240/zll_leps_from_higgs_cut6" % flavor)
    
    totEvts = h.Integral()
    
    
    totEvts_err = ctypes.c_double(1.)
    totEvts = h.IntegralAndError(0, h.GetNbinsX() + 1, totEvts_err)
    totEvts_err = totEvts_err.value
    
    
    
    goodPairs = h.GetBinContent(1)
    goodPairs_err = h.GetBinError(1)
    pairEfficiency = goodPairs / totEvts
    pairEfficiency_err = pairEfficiency*((totEvts_err/totEvts)**2 + (goodPairs_err/goodPairs)**2)**0.5
    
    print(pairEfficiency*100.)
    print(pairEfficiency_err*100.)
    
    