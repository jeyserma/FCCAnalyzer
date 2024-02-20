
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter


def massVariations(hName, charge="plus"):

    ecm = float(hName.split("_")[-1].replace("ecm", ""))
    h_base = fIn.Get(f"{hName}/w_{charge}_m")
    h_up = fIn.Get(f"{hName}/w_{charge}_m_plus_10MeV")
    h_dw = fIn.Get(f"{hName}/w_{charge}_m_minus_10MeV")

    h_base.SetLineColor(ROOT.kBlack)
    h_base.SetLineWidth(2)

    h_up.SetLineColor(ROOT.kBlue)
    h_up.SetLineWidth(2)

    h_dw.SetLineColor(ROOT.kRed)
    h_dw.SetLineWidth(2)

    h_up_ratio = h_up.Clone("rup")
    h_dw_ratio = h_dw.Clone("rdw")
    h_up_ratio.Divide(h_base)
    h_dw_ratio.Divide(h_base)

    leg = ROOT.TLegend(.2, 0.65, 0.9, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetMargin(0.12)
    leg.SetTextSize(0.040)
    leg.AddEntry(h_base, "Nominal mass", "L")
    leg.AddEntry(h_up, "#plus 10 MeV", "L")
    leg.AddEntry(h_dw, "#minus 10 MeV", "L")

    yRatio=1.05
    cfg = {
        'logy'              : False,
        'logx'              : False,

        'xmin'              : 70,
        'xmax'              : 90,
        'ymin'              : 0,
        'ymax'              : 1.3*h_base.GetMaximum(),

        'xtitle'            : f"m(W)",
        'ytitle'            : "Events",

        'topRight'          : f"#sqrt{{s}} = {ecm} GeV, 5 ab^{{#minus1}}", 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Simulation}}",

        'ratiofraction'     : 0.3,
        'ytitleR'           : "Data/MC",

        'yminR'             : 1-(yRatio-1),
        'ymaxR'             : yRatio,
    }


    ## top panel
    plotter.cfg = cfg
    canvas, padT, padB = plotter.canvasRatio()
    dummyT, dummyB, dummyL = plotter.dummyRatio()

    ## top panel
    canvas.cd()
    padT.Draw()
    padT.cd()
    padT.SetGrid()
    dummyT.Draw("HIST")

    h_up.Draw("SAME HIST")
    h_dw.Draw("SAME HIST")
    h_base.Draw("SAME HIST")
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

    h_up_ratio.Draw("PE0 SAME")
    h_dw_ratio.Draw("PE0 SAME")

    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs(f"{outDir}/{hName}_{charge}.png")
    canvas.SaveAs(f"{outDir}/{hName}_{charge}.pdf")
    canvas.Close()


if __name__ == "__main__":

    outDir = "/work/submit/jaeyserm/public_html/fccee/wmass/kinematic/"
    fIn = ROOT.TFile("output_wmass_kinematic.root")
    massVariations("yfsww_ee_ww_noBES_ecm163")
    massVariations("yfsww_ee_ww_noBES_ecm163", charge="minus")

    massVariations("yfsww_ee_ww_noBES_ecm157")
    massVariations("yfsww_ee_ww_noBES_ecm157", charge="minus")

    massVariations("yfsww_ee_ww_noBES_Born_ecm163")
    massVariations("yfsww_ee_ww_noBES_Born_ecm163", charge="minus")