
import sys,array,ROOT,math,os,copy
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

#sys.path.insert(0, '/afs/cern.ch/work/j/jaeyserm/pythonlibs')
import plotter


def compute_res(hist, outName, param, plotGauss=False):


    if param == "p":
        rebin = 4
        xTitle = "(p_{reco} #minus p_{gen})/p_{gen}"
        probabilities = np.array([0.001, 0.999, 0.84, 0.16], dtype='d')
    if param == "theta":
        rebin = 1
        xTitle = "(#theta_{reco} #minus #theta_{gen})/#theta_{gen}"
        probabilities = np.array([0.002, 0.998, 0.84, 0.16], dtype='d')
    if param == "phi":
        rebin = 1
        xTitle = "(#phi_{reco} #minus #phi_{gen})/#phi_{gen}"
        probabilities = np.array([0.01, 0.99, 0.84, 0.16], dtype='d')

    # compute quantiles
    quantiles = np.array([0.0, 0.0, 0.0, 0.0], dtype='d')
    hist.GetQuantiles(4, quantiles, probabilities)
    xMin, xMax = min([quantiles[0], -quantiles[1]]), max([-quantiles[0], quantiles[1]])
    res = 100.*0.5*(quantiles[2] - quantiles[3])

    rms, rms_err = hist.GetRMS()*100., hist.GetRMSError()*100.

    hist = hist.Rebin(rebin)
    gauss = ROOT.TF1("gauss2", "gaus", xMin, xMax)
    gauss.SetParameter(0, hist.Integral())
    gauss.SetParameter(1, hist.GetMean())
    gauss.SetParameter(2, hist.GetRMS())
    hist.Fit("gauss2", "R")

    sigma, sigma_err = gauss.GetParameter(2)*100., gauss.GetParError(2)*100.

    gauss.SetLineColor(ROOT.kRed)
    gauss.SetLineWidth(3)

    ## plot
    cfg = {

        'logy'              : False,
        'logx'              : False,

        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : 0,
        'ymax'              : 1.3*hist.GetMaximum(),

        'xtitle'            : xTitle,
        'ytitle'            : "Events / bin",
                
        'topRight'          : "#sqrt{s} = 240 GeV", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
    }

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")

    hist.Draw("SAME HIST")
    if plotGauss:
        gauss.Draw("SAME")

    plotter.aux()
    canvas.SetGrid()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.DrawLatex(0.2, 0.9, f"Mean/RMS(#times 100) = {hist.GetMean():.4f}/{rms:.4f}")
    latex.DrawLatex(0.2, 0.85, f"Resolution = {res:.4f} %")
    if plotGauss:
        latex.DrawLatex(0.2, 0.80, f"Gauss #mu/#sigma(#times 100) = {gauss.GetParameter(1):.4f}/{sigma:.4f}")

    canvas.SaveAs(f"{outDir_fits}/{outName}.png")
    canvas.SaveAs(f"{outDir_fits}/{outName}.pdf")
    canvas.Close()

    del gauss
    return rms, rms_err, sigma, sigma_err, res


def resolution(rFile, outDir, xVar="theta", yVar="p", yMax=1, coll=""):

    fIn = ROOT.TFile(rFile)

    if xVar == "theta":
        guns = ["mu_theta_10_p_20-80", "mu_theta_20_p_20-80", "mu_theta_30_p_20-80", "mu_theta_40_p_20-80", "mu_theta_50_p_20-80", "mu_theta_60_p_20-80", "mu_theta_70_p_20-80", "mu_theta_75_p_20-80", "mu_theta_80_p_20-80", "mu_theta_81_p_20-80", "mu_theta_82_p_20-80", "mu_theta_83_p_20-80", "mu_theta_84_p_20-80", "mu_theta_85_p_20-80", "mu_theta_90_p_20-80"]
        guns = ["mu_theta_10_p_20-80", "mu_theta_20_p_20-80", "mu_theta_30_p_20-80", "mu_theta_40_p_20-80", "mu_theta_50_p_20-80", "mu_theta_60_p_20-80", "mu_theta_70_p_20-80", "mu_theta_75_p_20-80", "mu_theta_80_p_20-80", "mu_theta_85_p_20-80", "mu_theta_90_p_20-80"]
    else:
        guns = ["mu_theta_10-90_p_3", "mu_theta_10-90_p_4", "mu_theta_10-90_p_5", "mu_theta_10-90_p_10", "mu_theta_10-90_p_20", "mu_theta_10-90_p_30", "mu_theta_10-90_p_40", "mu_theta_10-90_p_50", "mu_theta_10-90_p_75", "mu_theta_10-90_p_100"] # "mu_theta_10-90_p_2",


    dets = ["delphes", "fullsim"]
    legends = ["IDEA Si Tracker (Delphes)", "CLD (FullSim)"]
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kBlack]

    graphs_res = []
    for i,det in enumerate(dets):
        g_res = ROOT.TGraphErrors()
        g_res.SetName(f"res_{det}")
        g_res.SetLineColor(colors[i])
        g_res.SetLineWidth(2)
        g_res.SetMarkerStyle(22)
        g_res.SetMarkerSize(1.5)
        g_res.SetMarkerColor(colors[i])
        graphs_res.append(g_res)



        
    for i,det in enumerate(dets):
        iPoint = 0
        for j, gun in enumerate(guns):
            xVal = float(gun.split("_")[2]) if xVar=="theta" else float(gun.split("_")[4])
            hist = fIn.Get(f"{gun}_{det}/muons{coll}_reso_{yVar}")
            #rms, rms_err, sigma, sigma_err, res = compute_res(hist, f"{gun}_{det}_{param}{coll}", param=yVar)
            rms, rms_err, sigma, sigma_err, res = compute_res(hist, f"{det}_{yVar}_xVal_{xVal}", param=yVar)
            graphs_res[i].SetPoint(iPoint, xVal, res)
            graphs_res[i].SetPointError(iPoint, 0, 0)
            iPoint += 1


    if yVar == "p": yTitle = "Momentum Resolution (%)"
    if yVar == "theta": yTitle = "#theta Resolution (%)"
    if yVar == "phi": yTitle = "#phi Resolution (%)"

    if xVar == "p": xTitle = "Momentum (GeV)"
    if xVar == "theta": xTitle = "Polar angle #theta (deg)"

    ############### SIGMA
    cfg = {

        'logy'              : False,
        'logx'              : False,

        'xmin'              : 0,
        'xmax'              : 100,
        'ymin'              : 0,
        'ymax'              : yMax,

        'xtitle'            : xTitle,
        'ytitle'            : yTitle,
                
        'topRight'          : "#sqrt{s} = 240 GeV", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
    }

    leg = ROOT.TLegend(.4, 0.7, 0.90, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.15)
    leg.SetHeader("Muon gun")

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")

    for i,det in enumerate(dets):
        leg.AddEntry(graphs_res[i], legends[i], "LP")
        graphs_res[i].Draw("SAME LP")

    leg.Draw("SAME")
    plotter.aux()
    canvas.SetGrid()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs(f"{outDir}/resolution_{yVar}_vs_{xVar}{coll}.png")
    canvas.SaveAs(f"{outDir}/resolution_{yVar}_vs_{xVar}{coll}.pdf")
    canvas.Close()


def resolution_zh(rFile, outDir, xVar="theta", yVar="p", yMax=1):

    fIn = ROOT.TFile(rFile)

    dets = ["wzp6_ee_mumuH_ecm240_CLD", "wzp6_ee_mumuH_ecm240_CLD_FullSim"]
    legends = ["IDEA Si Tracker (Delphes)", "CLD (FullSim)"]
    colors = [ROOT.kRed, ROOT.kBlue]

    graphs_res = []
    for i,det in enumerate(dets):
        g_res = ROOT.TGraphErrors()
        g_res.SetName(f"res_{det}")
        g_res.SetLineColor(colors[i])
        g_res.SetLineWidth(2)
        g_res.SetMarkerStyle(22)
        g_res.SetMarkerSize(1.5)
        g_res.SetMarkerColor(colors[i])
        graphs_res.append(g_res)

    for i,det in enumerate(dets):
        hist_2d = fIn.Get(f"{det}/leps_reso_{yVar}_vs_{xVar}_cut0")
        hist_proj_var = hist_2d.ProjectionY(f"hist_theta")

        iPoint = 0
        for iBin in range(hist_proj_var.GetNbinsX()):
            xVal = hist_proj_var.GetBinCenter(iBin)
            if xVar == "theta":
                xVal *= 180/math.pi
                if xVal > 90 or xVal < 8:
                    continue
            if xVar == "p":
                if xVal < 20:
                    continue
            hist = hist_2d.ProjectionX(f"hist_{iBin}", iBin, iBin)
            rms, rms_err, sigma, sigma_err, res = compute_res(hist, f"{det}_{yVar}_xVal_{xVal}", param=yVar)
            graphs_res[i].SetPoint(iPoint, xVal, res)
            graphs_res[i].SetPointError(iPoint, 0, 0)
            iPoint += 1

    if yVar == "p": yTitle = "Momentum Resolution (%)"
    if yVar == "theta": yTitle = "#theta Resolution (%)"
    if yVar == "phi": yTitle = "#phi Resolution (%)"

    if xVar == "p": xTitle = "Momentum (GeV)"
    if xVar == "theta": xTitle = "Polar angle #theta (deg)"

    cfg = {

        'logy'              : False,
        'logx'              : False,

        'xmin'              : 0,
        'xmax'              : 100,
        'ymin'              : 0,
        'ymax'              : yMax,

        'xtitle'            : xTitle,
        'ytitle'            : yTitle,
                
        'topRight'          : "#sqrt{s} = 240 GeV", 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
    }

    leg = ROOT.TLegend(.4, 0.7, 0.90, .90)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(1)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.15)
    leg.SetHeader("Z(#mu^{#plus}#mu^{#minus})H events")

    plotter.cfg = cfg
    canvas = plotter.canvas()
    dummy = plotter.dummy()
    dummy.Draw("HIST")

    for i,det in enumerate(dets):
        leg.AddEntry(graphs_res[i], legends[i], "LP")
        graphs_res[i].Draw("SAME LP")

    leg.Draw("SAME")
    plotter.aux()
    canvas.SetGrid()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    canvas.SaveAs(f"{outDir}/resolution_{yVar}_vs_{xVar}.png")
    canvas.SaveAs(f"{outDir}/resolution_{yVar}_vs_{xVar}.pdf")
    canvas.Close()



if __name__ == "__main__":

    if False: # muon guns
        outDir = "/home/submit/jaeyserm/public_html/fccee/fast_fullsim/muon_resolution_CLD_gun/"
        outDir_fits = "/home/submit/jaeyserm/public_html/fccee/fast_fullsim/muon_resolution_CLD_gun/fits/"

        resolution("particlegun.root", outDir, xVar="theta", yVar="p", yMax=2.5)
        resolution("particlegun.root", outDir, xVar="p", yVar="p", yMax=2.5)

        resolution("particlegun.root", outDir, xVar="theta", yVar="p", yMax=2.5, coll="_plus")
        resolution("particlegun.root", outDir, xVar="p", yVar="p", yMax=2.5, coll="_plus")

        resolution("particlegun.root", outDir, xVar="theta", yVar="p", yMax=2.5, coll="_minus")
        resolution("particlegun.root", outDir, xVar="p", yVar="p", yMax=2.5, coll="_minus")

        resolution("particlegun.root", outDir, xVar="theta", yVar="theta", yMax=0.05)
        resolution("particlegun.root", outDir, xVar="p", yVar="theta", yMax=0.1)

        resolution("particlegun.root", outDir, xVar="theta", yVar="phi", yMax=0.05)
        resolution("particlegun.root", outDir, xVar="p", yVar="phi", yMax=0.1)

    if True: # ZH events
        outDir = "/home/submit/jaeyserm/public_html/fccee/fast_fullsim/muon_resolution_CLD_ZH/"
        outDir_fits = "/home/submit/jaeyserm/public_html/fccee/fast_fullsim/muon_resolution_CLD_ZH/fits/"

        resolution_zh("output_ZH_mass_mumu_ecm240_test.root", outDir, xVar="theta", yVar="p", yMax=2.5)
        resolution_zh("output_ZH_mass_mumu_ecm240_test.root", outDir, xVar="p", yVar="p", yMax=2.5)
        
        resolution_zh("output_ZH_mass_mumu_ecm240_test.root", outDir, xVar="theta", yVar="theta", yMax=0.05)
        resolution_zh("output_ZH_mass_mumu_ecm240_test.root", outDir, xVar="theta", yVar="phi", yMax=0.05)