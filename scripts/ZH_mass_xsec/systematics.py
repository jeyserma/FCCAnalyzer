
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

parser = argparse.ArgumentParser()
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", default="mumu")
parser.add_argument("--type", type=str, help="Run type (mass or xsec)", choices=["mass", "xsec"], default="mass")
args = parser.parse_args()



def getHist(f, p, h):

    fIn = ROOT.TFile(f)
    hist = copy.deepcopy(fIn.Get("%s/%s" % (p, h)))
    fIn.Close()
    return hist

    
def makePlot(outName, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False, norm=True, yRatio=1.15, hNames=[], labels=[]):

    colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed]
    
    leg = ROOT.TLegend(.5, 0.9-len(labels)*0.08, 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetMargin(0.12)
    leg.SetTextSize(0.040)

    hists = []
    hists_ratio = []
    for i,hName in enumerate(hNames):
        h = fIn.Get(hName)
        h.SetName(hName.replace("/", "_"))
        h.Rebin(rebin)
        if norm: h.Scale(1./h.Integral())
        h.SetLineColor(colors[i])
        h.SetLineWidth(2)
        leg.AddEntry(h, labels[i], "L")
        hists.append(h)

        if i > 0:
            hRatio = hists[0].Clone("ratio_%d"%i)
            hRatio.Divide(h)
            hRatio.SetLineColor(colors[i])
            hists_ratio.append(hRatio)
    

    cfg = {

        'logy'              : logy,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax if yMax > 0 else 1.3*max([h.GetMaximum() for h in hists]),
            
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

    canvas.cd()
    padT.Draw()
    padT.cd()
    padT.SetGrid()
    dummyT.Draw("HIST")
        
    for h in hists:
        h.Draw("SAME HIST")
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
    for h in hists_ratio:
        h.Draw("SAME HIST E")
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs("%s/%s.png" % (outDir, outName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, outName))
    canvas.Close()




if __name__ == "__main__":

    f = args.flavor
    fIn = ROOT.TFile(f"tmp/output_ZH_mass_{f}_reco.root")
    outDir = f"/eos/user/j/jaeyserm/www/FCCee/ZH_mass/plots_systs_{f}/"
    
    #makePlot("field_2T_3T_noBES", 120, 140, 0, -1, "m_{rec} (GeV)", "Events (normalized)", rebin=10, hNames=[f"p_wzp6_ee_{f}H_noBES_ecm240/zll_recoil", f"p_wzp6_ee_{f}H_noBES_ecm240_3T/zll_recoil"], labels=["2T noBES", "3T no BES"], yRatio=1.15)
    
    makePlot("BES_noBES", 120, 140, 0, -1, "m_{rec} (GeV)", "Events (normalized)", rebin=10, hNames=[f"p_wzp6_ee_{f}H_ecm240/zll_recoil", f"p_wzp6_ee_{f}H_noBES_ecm240/zll_recoil"], labels=["Nominal BES", "No BES"], yRatio=1.8)
    
    makePlot("BES_syst_6pct", 120, 140, 0, -1, "m_{rec} (GeV)", "Events (normalized)", rebin=20, hNames=[f"p_wzp6_ee_{f}H_ecm240/zll_recoil", f"p_wzp6_ee_{f}H_BES-higher-6pc_ecm240/zll_recoil", f"p_wzp6_ee_{f}H_BES-lower-6pc_ecm240/zll_recoil"], labels=["Nominal BES", "BES #plus 6%", "BES #minus 6%"], yRatio=1.35)
    
    makePlot("BES_syst_1pct", 120, 140, 0, -1, "m_{rec} (GeV)", "Events (normalized)", rebin=20, hNames=[f"p_wzp6_ee_{f}H_ecm240/zll_recoil", f"p_wzp6_ee_{f}H_BES-higher-1pc_ecm240/zll_recoil", f"p_wzp6_ee_{f}H_BES-lower-1pc_ecm240/zll_recoil"], labels=["Nominal BES", "BES #plus 1%", "BES #minus 1%"], yRatio=1.15)
    
    
    makePlot("field_2T_3T", 120, 140, 0, -1, "m_{rec} (GeV)", "Events (normalized)", rebin=10, hNames=[f"p_wzp6_ee_{f}H_ecm240/zll_recoil", f"p_wzp6_ee_{f}H_ecm240_3T/zll_recoil"], labels=["2T magnetic field (nom.)", "3T magnetic field"], yRatio=1.15)

    #makePlot("mumu_ee", 120, 140, 0, -1, "m_{rec} (GeV)", "Events (normalized)", rebin=10, hNames=[f"p_wzp6_ee_mumuH_ecm240/zll_recoil", f"p_wzp6_ee_eeH_ecm240_3T/zll_recoil"], labels=["Z(#mu^{#plus}#mu^{#minus})H", "Z(e^{#plus}e^{#minus})H"], yRatio=1.75)