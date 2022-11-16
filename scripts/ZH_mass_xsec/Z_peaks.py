
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


#sys.path.insert(0, '/afs/cern.ch/work/j/jaeyserm/pythonlibs')
import plotter






def plot_m():

    outDir_ = "/eos/user/j/jaeyserm/www/FCCee/ZH/test/"
    fIn = ROOT.TFile("output.root")

        
    
    
    colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen+1, ROOT.kMagenta, ROOT.kCyan, ROOT.kGray, ROOT.kYellow]
    decay_pdgids = [4, 5, 13, 15, 21, 22, 23, 24]
    decay_names = ["cc", "bb", "mumu", "tautau", "gluon", "gamma", "Z", "W"]
    decay_pdgids = [4, 5, 15, 21, 22, 23, 24]
    decay_names = ["cc", "bb", "tautau", "gluon", "gamma", "Z", "W"]
    
    decay_pdgids = [5, 15]
    decay_names = ["bb", "tautau"]
    
    th2 = fIn.Get("wzp6_ee_mumuH_ecm240/higgs_decay_zed_leptonic_m_cut4")

    leg = ROOT.TLegend(.3, 0.75, 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(2)
    leg.SetTextSize(0.035)
    
    cfg = {

        'logy'              : False,
        'logx'              : False,
        
        'xmin'              : 70,
        'xmax'              : 120,
        'ymin'              : 0,
        'ymax'              : 0.01,
            
        'xtitle'            : "m_{#mu^{+},#mu^{#minus}} (GeV)",
        'ytitle'            : "Events / 0.5 GeV",
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",

    }
        

    plotter.cfg = cfg
    canvas = plotter.canvas()
        
    dummy = plotter.dummy()
    dummy.Draw("HIST")
    
    for i,pdgid in enumerate(decay_pdgids):
    
        h = th2.ProjectionY(decay_names[i], pdgid+1, pdgid+1)
        h.SetLineColor(colors[i])
        h.SetLineWidth(1)
        h.Rebin(2)
        h.Scale(1./h.Integral())
        h.Draw("HIST SAME")
        leg.AddEntry(h, decay_names[i], "L")

    leg.Draw("SAME")
    canvas.SetGrid()
    canvas.Modify()
    canvas.Update()

    plotter.aux()
    ROOT.gPad.SetTicks()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs("%s/mll.png" % (outDir_))
    canvas.SaveAs("%s/mll.pdf" % (outDir_))
    canvas.Close()
    
    
    
def plot_p():
    outDir_ = "/eos/user/j/jaeyserm/www/FCCee/ZH/test/"
    fIn = ROOT.TFile("output.root")

        
    
    
    colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen+1, ROOT.kMagenta, ROOT.kCyan, ROOT.kGray, ROOT.kYellow]
    decay_pdgids = [4, 5, 13, 15, 21, 22, 23, 24]
    decay_names = ["cc", "bb", "mumu", "tautau", "gluon", "gamma", "Z", "W"]
    decay_pdgids = [4, 5, 15, 21, 22, 23, 24]
    decay_names = ["cc", "bb", "tautau", "gluon", "gamma", "Z", "W"]
    
    decay_pdgids = [5, 15]
    decay_names = ["bb", "tautau"]
    
    th2 = fIn.Get("wzp6_ee_mumuH_ecm240/higgs_decay_zed_leptonic_p_cut4")

    leg = ROOT.TLegend(.6, 0.55, 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    
    cfg = {

        'logy'              : True,
        'logx'              : False,
        
        'xmin'              : 0,
        'xmax'              : 150,
        'ymin'              : 0.0001,
        'ymax'              : 1,
            
        'xtitle'            : "p_{#mu^{+},#mu^{#minus}} (GeV)",
        'ytitle'            : "Events / 0.5 GeV",
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",

    }
        

    plotter.cfg = cfg
    canvas = plotter.canvas()
        
    dummy = plotter.dummy()
    dummy.Draw("HIST")
    
    for i,pdgid in enumerate(decay_pdgids):
    
        h = th2.ProjectionY(decay_names[i], pdgid+1, pdgid+1)
        h.SetLineColor(colors[i])
        h.SetLineWidth(2)
        h.Scale(1./h.Integral())
        h.Draw("HIST SAME")
        leg.AddEntry(h, decay_names[i], "L")

    leg.Draw("SAME")
    canvas.SetGrid()
    canvas.Modify()
    canvas.Update()

    plotter.aux()
    ROOT.gPad.SetTicks()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs("%s/pll.png" % (outDir_))
    canvas.SaveAs("%s/pll.pdf" % (outDir_))
    canvas.Close()
    
    
    
if __name__ == "__main__":

    #plot_m()
    plot_p()
