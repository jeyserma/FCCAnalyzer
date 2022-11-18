
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


#sys.path.insert(0, '/afs/cern.ch/work/j/jaeyserm/pythonlibs')
import plotter




def getHist(f, p, h):

    fIn = ROOT.TFile(f)
    hist = copy.deepcopy(fIn.Get("%s/%s" % (p, h)))
    fIn.Close()
    return hist

    
def makePlot(hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False, norm=True):

    h1 = getHist(f1, p1, hName)
    h2 = getHist(f2, p2, hName)
    
    m1 = getHist(f1, p1, "meta")
    m2 = getHist(f2, p2, "meta")
    evc1 = m1.GetBinContent(1)
    evc2 = m2.GetBinContent(2)
    
    print(evc1, evc2, m1.Integral(), m2.Integral())
    
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
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
    }

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")
        
    h1.Draw("SAME HIST")
    h2.Draw("SAME HIST")    
    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs("%s/%s.png" % (outDir, hName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, hName))
    canvas.Close()




def makeResolutionPlot(hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False):

    h1 = getHist(f1, p1, hName)
    h2 = getHist(f2, p2, hName)
    
    h1.Rebin(rebin)
    h2.Rebin(rebin)
    
    h1.SetLineColor(ROOT.kRed)
    h1.SetLineWidth(2)
    #h_old.Scale(1./h_old.Integral(h_old.FindBin(0.9925/2.), h_old.FindBin(1.0025/2.)))
    #h1.Scale(1./h1.Integral())
    
    h2.SetLineColor(ROOT.kBlue)
    h2.SetLineWidth(2)
    #h_new.Scale(1./h_new.Integral(h_new.FindBin(0.9925/2.), h_new.FindBin(1.0025/2.)))
    #h2.Scale(1./h2.Integral())

    leg = ROOT.TLegend(.2, 0.75, 0.85, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.1)
    leg.AddEntry(h1, "%s (RMS=%.5f)" % (l1, h1.GetRMS()), "L")
    leg.AddEntry(h2, "%s (RMS=%.5f)" % (l2, h2.GetRMS()), "L")
    
    cfg = {

        'logy'              : logy,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else 1.3*max([h1.GetMaximum(), h2.GetMaximum()]),
            
        'xtitle'            : xTitle,
        'ytitle'            : yTitle,
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
    }

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")
        
    h1.Draw("SAME HIST")
    h2.Draw("SAME HIST")    
    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs("%s/%s.png" % (outDir, hName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, hName))
    canvas.Close()


    
    
    
if __name__ == "__main__":

    
    f1, p1, l1 = "tmp/output_higgs_gaga.root", "wzp6_ee_mumuH_ecm240", "Spring 2021"
    f2, p2, l2 = "tmp/output_higgs_gaga.root", "wz2p6_ee_mumuH_ecm240_winter_v2", "Winter 2023"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_higgs_gaga/sampleComparison/spring2021_prewinter2023"
    
    
    f1, p1, l1 = "tmp/output_higgs_gaga.root", "wzp6_ee_mumuH_ecm240", "Spring 2021, WZ2"
    f2, p2, l2 = "tmp/output_higgs_gaga.root", "wz3p6_ee_mumuH_ecm240_winter_v2", "Winter 2023, WZ3"
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_higgs_gaga/sampleComparison/spring2021_prewinter2023_wz3"
    
    
    makePlot("photons_p", 0, 100, 0, -1, "Photon p (GeV)", "Events (normalized)", rebin=1)
    makePlot("photons_no", 0, 15, 0, -1, "Photon multiplicity", "Events (normalized)", rebin=1)
    makePlot("photons_phi", -5, 5, 0, -1, "Photon #phi", "Events (normalized)", rebin=1)
    makePlot("photons_theta", 0, 3.14, 0, -1, "Photon #theta", "Events (normalized)", rebin=1)
    

    makePlot("selected_photons_p", 0, 100, 0, -1, "Selected photon p (GeV)", "Events (normalized)", rebin=1)
    makePlot("selected_photons_no", 0, 15, 0, -1, "Selected photon multiplicity", "Events (normalized)", rebin=1)
    makePlot("selected_photons_phi", -5, 5, 0, -1, "Selected photon #phi", "Events (normalized)", rebin=1)
    makePlot("selected_photons_theta", 0, 3.14, 0, -1, "Selected photon #theta", "Events (normalized)", rebin=1)
 
    makePlot("resonance_m", 100, 150, 0, -1, "m_{#gamma#gamma} (Gev)", "Events (normalized)", rebin=2)
    makePlot("resonance_p", 0, 100, 0, -1, "p_{#gamma#gamma} (Gev)", "Events (normalized)", rebin=4)
    makePlot("resonance_recoil", 50, 150, 0, -1, "Recoil #gamma#gamma (GeV)", "Events (normalized)", rebin=4)
 

    
    