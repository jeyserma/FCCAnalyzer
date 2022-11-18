
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter

    
def makePlot(proc, hName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False):

    h1 = fIn.Get("%s/%s" % (proc, hName))
    h1.Rebin(rebin)
    
    h1.SetLineColor(ROOT.kRed)
    h1.SetLineWidth(2)
    h1.Scale(1./h1.Integral())

    cfg = {

        'logy'              : logy,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : 1.2*h1.GetMaximum(),
            
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
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs("%s/%s.png" % (outDir, hName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, hName))
    canvas.Close()

    
    
    
if __name__ == "__main__":
    
    fIn = ROOT.TFile("tmp/output_higgs_gaga.root")
    proc = "wzp6_ee_mumuH_ecm240"
  
    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_higgs_gaga/plots/"


    makePlot(proc, "photons_p", 0, 100, 0, 0.05, "Photon p (GeV)", "Events (normalized)", rebin=1)
    makePlot(proc, "photons_no", 0, 15, 0, 1, "Photon multiplicity", "Events (normalized)", rebin=1)
    makePlot(proc, "photons_phi", -5, 5, 0, 0.005, "Photon #phi", "Events (normalized)", rebin=1)
    makePlot(proc, "photons_theta", 0, 3.14, 0, 0.015, "Photon #theta", "Events (normalized)", rebin=1)
    

    makePlot(proc, "selected_photons_p", 0, 100, 0, 0.05, "Selected photon p (GeV)", "Events (normalized)", rebin=1)
    makePlot(proc, "selected_photons_no", 0, 15, 0, 1, "Selected photon multiplicity", "Events (normalized)", rebin=1)
    makePlot(proc, "selected_photons_phi", -5, 5, 0, 0.005, "Selected photon #phi", "Events (normalized)", rebin=1)
    makePlot(proc, "selected_photons_theta", 0, 3.14, 0, 0.015, "Selected photon #theta", "Events (normalized)", rebin=1)
 
    makePlot(proc, "resonance_m", 100, 150, 0, 0.1, "m_{#gamma#gamma} (Gev)", "Events (normalized)", rebin=2)
    makePlot(proc, "resonance_p", 0, 100, 0, 0.015, "p_{#gamma#gamma} (Gev)", "Events (normalized)", rebin=4)
    makePlot(proc, "resonance_recoil", 50, 150, 0, 0.015, "Recoil #gamma#gamma (GeV)", "Events (normalized)", rebin=4)
 
