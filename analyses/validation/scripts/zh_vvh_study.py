
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

#sys.path.insert(0, '/afs/cern.ch/work/j/jaeyserm/pythonlibs')
import plotter


if __name__ == "__main__":

    outDir = "/home/submit/jaeyserm/public_html/fccee/zh_vvh_study/"

    hName = "missingMass_gen"
    fIn = ROOT.TFile("zh_vvh_study.root")

    # cross-sections in fb
    #wzp6_ee_nunuH_Haa_ecm365        5.3969995E+01
    #wzp6_ee_nuenueH_Haa_ecm365      3.7446425E+01
    #wzp6_ee_numunumuH_Haa_ecm365    8.2609609E+00

    h_nue = fIn.Get(f"wzp6_ee_nuenueH_Haa_ecm365/{hName}")
    h_numu = fIn.Get(f"wzp6_ee_numunumuH_Haa_ecm365/{hName}")
    h_incl = fIn.Get(f"wzp6_ee_nunuH_Haa_ecm365/{hName}")

    h_nue.Scale(1./h_nue.Integral())
    h_numu.Scale(1./h_numu.Integral())
    h_incl.Scale(1./h_incl.Integral())

    h_nue.Scale(3.7446425E+01)
    h_numu.Scale(8.2609609E+00)
    h_incl.Scale(5.3969995E+01)

    h_zh = h_numu.Clone("h_zh")
    h_zh.Scale(3.)

    h_vbf = h_nue.Clone("h_vbf")
    h_vbf.Add(h_numu, -1)

    #h_vbf = h_incl - h_zh # remove z(nuenue)h component
    
    # normalize for now till xsecs arrive
    #h_incl.Scale(1./h_incl.Integral())
    ##h_zh.Scale(1./h_zh.Integral())
    #h_vbf = h_incl - h_zh # remove z(nuenue)h component
    
    h_incl.SetLineColor(ROOT.kBlack)
    h_incl.SetLineWidth(2)
    
    h_zh.SetLineColor(ROOT.kRed)
    h_zh.SetLineWidth(2)
    
    h_vbf.SetLineColor(ROOT.kBlue)
    h_vbf.SetLineWidth(2)


    ############### RMS
    cfg = {

        'logy'              : False,
        'logx'              : False,

        'xmin'              : 50,
        'xmax'              : 250,
        'ymin'              : -0.5,
        'ymax'              : 5,

        'xtitle'            : "Gen-level missing mass (GeV)",
        'ytitle'            : "Events (a.u.)",
                
        'topRight'          : "#sqrt{s} = 365 GeV", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
    }

    leg = ROOT.TLegend(.4, 0.7, 0.90, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.15)

    leg.AddEntry(h_vbf, "VBF + interference", "L")
    leg.AddEntry(h_zh, "ZH", "L")
    leg.AddEntry(h_incl, "Inclusive", "L")

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")

    h_vbf.Draw("SAME HIST")
    h_zh.Draw("SAME HIST")
    h_incl.Draw("SAME HIST")

    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs(f"{outDir}/missing_mass_gen.png")
    canvas.SaveAs(f"{outDir}/missing_mass_gen.pdf")
    canvas.Close()


    # RECO level plot

    hName = "missingMass_reco"
    fIn = ROOT.TFile("zh_vvh_study.root")

    # cross-sections in fb
    #wzp6_ee_nunuH_Haa_ecm365        5.3969995E+01
    #wzp6_ee_nuenueH_Haa_ecm365      3.7446425E+01
    #wzp6_ee_numunumuH_Haa_ecm365    8.2609609E+00

    h_nue = fIn.Get(f"wzp6_ee_nuenueH_Haa_ecm365/{hName}")
    h_numu = fIn.Get(f"wzp6_ee_numunumuH_Haa_ecm365/{hName}")
    h_incl = fIn.Get(f"wzp6_ee_nunuH_Haa_ecm365/{hName}")

    h_nue.Scale(1./h_nue.Integral())
    h_numu.Scale(1./h_numu.Integral())
    h_incl.Scale(1./h_incl.Integral())

    h_nue.Scale(3.7446425E+01)
    h_numu.Scale(8.2609609E+00)
    h_incl.Scale(5.3969995E+01)

    h_zh = h_numu.Clone("h_zh")
    h_zh.Scale(3.)

    h_vbf = h_nue.Clone("h_vbf")
    h_vbf.Add(h_numu, -1)

    #h_vbf = h_incl - h_zh # remove z(nuenue)h component
    
    # normalize for now till xsecs arrive
    #h_incl.Scale(1./h_incl.Integral())
    ##h_zh.Scale(1./h_zh.Integral())
    #h_vbf = h_incl - h_zh # remove z(nuenue)h component
    
    h_incl.SetLineColor(ROOT.kBlack)
    h_incl.SetLineWidth(2)
    
    h_zh.SetLineColor(ROOT.kRed)
    h_zh.SetLineWidth(2)
    
    h_vbf.SetLineColor(ROOT.kBlue)
    h_vbf.SetLineWidth(2)


    ############### RMS
    cfg = {

        'logy'              : False,
        'logx'              : False,

        'xmin'              : 50,
        'xmax'              : 250,
        'ymin'              : -0.5,
        'ymax'              : 5,

        'xtitle'            : "Reco-level missing mass (GeV)",
        'ytitle'            : "Events (a.u.)",
                
        'topRight'          : "#sqrt{s} = 365 GeV", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
    }

    leg = ROOT.TLegend(.4, 0.7, 0.90, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.15)

    leg.AddEntry(h_vbf, "VBF + interference", "L")
    leg.AddEntry(h_zh, "ZH", "L")
    leg.AddEntry(h_incl, "Inclusive", "L")

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")

    h_vbf.Draw("SAME HIST")
    h_zh.Draw("SAME HIST")
    h_incl.Draw("SAME HIST")

    leg.Draw("SAME") 
    plotter.aux()
    canvas.SetGrid()  
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()  

    canvas.SaveAs(f"{outDir}/missing_mass_reco.png")
    canvas.SaveAs(f"{outDir}/missing_mass_reco.pdf")
    canvas.Close()
