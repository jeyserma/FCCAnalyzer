
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)




def getHist(f, p, h):

    fIn = ROOT.TFile(f)
    hist = copy.deepcopy(fIn.Get("%s/%s" % (p, h)))
    fIn.Close()
    return hist


    
def makePlot(hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False, norm=True, yRatio=1.15):

    h1 = getHist(f1, p1, hName)
    h2 = getHist(f2, p2, hName)
    
    m1 = getHist(f1, p1, "meta")
    m2 = getHist(f2, p2, "meta")
    evc1 = m1.GetBinContent(1)
    evc2 = m2.GetBinContent(2)
    
    
    h1.Rebin(rebin)
    h2.Rebin(rebin)
    
    scale1 = h1.Integral()
    scale2 = h2.Integral()
    

    #scale1 = h1.GetBinContent(h1.GetXaxis().FindBin(125))
    #scale2 = h2.GetBinContent(h2.GetXaxis().FindBin(125))
    
    #print(scale1, scale2)
    
    if scale1 == 0: scale1 = h1.Integral()
    if scale2 == 0: scale2 = h2.Integral()



    
    h1.SetLineColor(ROOT.kRed)
    h1.SetLineWidth(2)
    if norm: h1.Scale(1./scale1)
    
    h2.SetLineColor(ROOT.kBlue)
    h2.SetLineWidth(2)
    if norm: h2.Scale(1./scale2)
    
    hRatio = h1.Clone("ratio")
    hRatio.Divide(h2)
    hRatio.SetLineColor(ROOT.kBlack)
    
    leg = ROOT.TLegend(.2, 0.75, 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetMargin(0.12)
    leg.SetTextSize(0.035)
    leg.AddEntry(h1, l1, "L")
    leg.AddEntry(h2, l2, "L")

    cfg = {

        'logy'              : logy,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else 1.3*max([h1.GetMaximum(), h2.GetMaximum()]),
            
        'xtitle'            : xTitle,
        'ytitle'            : yTitle,
            
        'topRight'          : "#sqrt{s} = 240 GeV", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
        
        'ratiofraction'     : 0.3,
        'ytitleR'           : "Ratio",
            
        'yminR'             : 1-(yRatio-1),
        'ymaxR'             : yRatio,
    }

    plotter.cfg = cfg
    canvas, padT, padB = plotter.canvasRatio()
    dummyT, dummyB, dummyL = plotter.dummyRatio()
    dummyB.SetTitleOffset(1) # necessary for unknown reason
    

    canvas.cd()
    padT.Draw()
    padT.cd()
    padT.SetGrid()
    dummyT.Draw("HIST")
    h1.Draw("SAME HIST")
    h2.Draw("SAME HIST")    
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
    hRatio.Draw("SAME HIST E")
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()
    
    canvas.SaveAs("%s/%s.png" % (outDir, hName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, hName))
    canvas.Close()




    
if __name__ == "__main__":

    
    f1, p1, l1 = "tmp/ZH_ISR_FSR_gen.root", "kkmc_noFSR", "KKMC (no FSR)"
    f2, p2, l2 = "tmp/ZH_ISR_FSR_gen.root", "whizard_noFSR", "WHIZARD (no FSR)"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass/ISR_FSR"
    

    #makePlot("gen_leptons_p_fsr", 0, 150, 0, 0.005, "Gen muon momentum (GeV)", "Events (normalized)", rebin=2, logy=False, norm=True)
    
    #f1, p1, l1 = "tmp/ZH_ISR_FSR_gen.root", "kkmc_noFSR", "KKMC"
    #f2, p2, l2 = "tmp/ZH_ISR_FSR_gen.root", "whizard_noFSR", "No FSR"
    makePlot("p_ll_sel", 0, 25, 0.0001, 1, "p(#mu^{#plus},#mu^{#minus}) (GeV)", "Events (normalized)", rebin=50, logy=True, norm=True)
    makePlot("gen_photons_no", 0, 5, 0, 1, "Number of gen-photons", "Events (normalized)", rebin=1, logy=False, norm=True)
    makePlot("gen_photons_p", 0, 150, 0.00001, 1, "Gen photon momentum (GeV)", "Events (normalized)", rebin=10, logy=True, norm=True)
    makePlot("gen_photons_sum_p", 0, 150, 0.00001, 1, "Gen photon momentum (GeV)", "Events (normalized)", rebin=1, logy=True, norm=True)
    
    #makePlot("gen_photons_p_sel", 0, 150, 0.00001, 1, "Gen photon momentum (GeV)", "Events (normalized)", rebin=1, logy=True, norm=True)
    makePlot("gen_photons_sum_p_sel", 0, 20, 0.0001, 1, "Gen photon momentum (GeV)", "Events (normalized)", rebin=5, logy=True, norm=True)
    
