
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


#sys.path.insert(0, '/afs/cern.ch/work/j/jaeyserm/pythonlibs')
import plotter




def getHist(f, p, h):

    fIn = ROOT.TFile(f)
    fIn.ls()
    hist = copy.deepcopy(fIn.Get("%s/%s" % (p, h)))
    fIn.Close()
    return hist

    



def recoil_plot(outName, files, hists, labels, colors, xMin, xMax, yMin, yMax, xTitle, yTitle, rebin=1, logy=False, norm=False, legLabel=""):

    n = len(files) + (0 if legLabel=="" else 1)
    leg = ROOT.TLegend(.45, 0.9-0.05*n, 0.90, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.1)
    if legLabel != "":
        leg.SetHeader(legLabel)
    
    
    cfg = {

        'logy'              : logy,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax,
            
        'xtitle'            : xTitle,
        'ytitle'            : yTitle,
            
        'topRight'          : "#sqrt{s} = 240 GeV, 10 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",
    }
    
        
    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")
    
    for i,h in enumerate(hists):
        fIn = ROOT.TFile(files[i])
        hist = copy.deepcopy(fIn.Get(hists[i]))
        if norm:
            hist.Scale(1./hist.Integral())
        hist.Rebin(rebin)
        hist.SetLineColor(colors[i])
        hist.SetLineWidth(3)
        leg.AddEntry(hist, labels[i], "L")
        hist.Draw("SAME HIST C")
        
    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs("%s/%s.png" % (outDir, outName))
    canvas.SaveAs("%s/%s.pdf" % (outDir, outName))
    canvas.Close()


  
    
if __name__ == "__main__":

    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass/recoil_comparison/"
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1]

    files = ["tmp/output_ZH_mass_mumu_reco.root", "tmp/output_ZH_mass_mumu_mc.root", "tmp/output_ZH_mass_mumu_reco.root", "tmp/output_ZH_mass_mumu_reco.root"]
    hists = ["p_wzp6_ee_mumuH_ecm240/zll_recoil", "p_wzp6_ee_mumuH_ecm240/zll_recoil", "p_wzp6_ee_mumuH_ecm240_3T/zll_recoil", "p_wzp6_ee_mumuH_ecm240_CLD/zll_recoil"]
    labels = ["IDEA", "IDEA perfect resolution", "IDEA 3T", "IDEA CLD silicon tracker"]
    recoil_plot("IDEA_IDEAL_2T_3T_CLD_mumu", files, hists, labels, colors, 122, 132, 0, 700, "Recoil (GeV)", "Events / 20 MeV", rebin=2, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H")

    files = ["tmp/output_ZH_mass_ee_reco.root", "tmp/output_ZH_mass_ee_mc.root", "tmp/output_ZH_mass_ee_reco.root", "tmp/output_ZH_mass_ee_reco.root"]
    hists = ["p_wzp6_ee_eeH_ecm240/zll_recoil", "p_wzp6_ee_eeH_ecm240/zll_recoil", "p_wzp6_ee_eeH_ecm240_3T/zll_recoil", "p_wzp6_ee_eeH_ecm240_CLD/zll_recoil"]
    labels = ["IDEA", "IDEA perfect resolution", "IDEA 3T", "IDEA CLD silicon tracker"]
    recoil_plot("IDEA_IDEAL_2T_3T_CLD_ee", files, hists, labels, colors, 122, 132, 0, 700, "Recoil (GeV)", "Events / 20 MeV", rebin=2, legLabel="Electron final state Z(e^{#plus}e^{#minus})H")

    files = ["tmp/output_ZH_mass_mumu_reco.root", "tmp/output_ZH_mass_mumu_reco.root", "tmp/output_ZH_mass_ee_reco.root", "tmp/output_ZH_mass_ee_reco.root"]
    hists = ["p_wzp6_ee_mumuH_ecm240/zll_recoil", "p_wzp6_ee_mumuH_ecm240_CLD/zll_recoil", "p_wzp6_ee_eeH_ecm240/zll_recoil", "p_wzp6_ee_eeH_ecm240_CLD/zll_recoil"]
    labels = ["IDEA 2T (#mu^{#plus}#mu^{#minus})", "CLD 2T (#mu^{#plus}#mu^{#minus})", "IDEA 2T (e^{#plus}e^{#minus})", "CLD 2T (e^{#plus}e^{#minus})"]
    recoil_plot("IDEA_CLD_mumu_ee", files, hists, labels, colors, 122, 132, 0, 700, "Recoil (GeV)", "Events / 20 MeV", rebin=2)


    files = [f"tmp/output_ZH_mass_mumu_reco.root", f"tmp/output_ZH_mass_ee_reco.root", f"tmp/output_ZH_mass_mumu_mc.root"]
    hists = [f"p_wzp6_ee_mumuH_ecm240/zll_recoil", f"p_wzp6_ee_eeH_ecm240/zll_recoil", f"p_wzp6_ee_mumuH_ecm240_3T/zll_recoil"]
    labels = ["IDEA 2T (#mu^{#plus}#mu^{#minus})", "IDEA 2T (e^{#plus}e^{#minus})", "IDEA, perfect resolution (#mu^{#plus}#mu^{#minus})"]
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue]

    
    recoil_plot("IDEA_MU_E_IDEAL", files, hists, labels, colors, 122, 132, 0, 700, "Recoil (GeV)", "Events (normalized)", rebin=2)






    files = [f"tmp/output_ZH_mass_mumu_reco.root", f"tmp/output_ZH_mass_mumu_reco.root", f"tmp/output_ZH_mass_mumu_reco.root"]
    hists = [f"p_wzp6_ee_mumuH_ecm240/zll_recoil", f"p_wzp6_ee_mumuH_ecm240_3T/zll_recoil", f"p_wzp6_ee_mumuH_ecm240_CLD/zll_recoil"]
    labels = ["IDEA 2T (#mu^{#plus}#mu^{#minus})", "IDEA 3T (#mu^{#plus}#mu^{#minus})", "CLD 2T (#mu^{#plus}#mu^{#minus})"]
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue]

    outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass/recoil_comparison/"
    recoil_plot("IDEA_MU_3T_CLD", files, hists, labels, colors, 122, 132, 0, 700, "Recoil (GeV)", "Events (normalized)", rebin=2)
