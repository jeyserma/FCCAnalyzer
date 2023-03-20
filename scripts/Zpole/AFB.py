
import sys,array,ROOT,math,os,copy

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)



if __name__ == "__main__":

    outDir = "/home/submit/jaeyserm/public_html/FCCee"
    
    fIn = ROOT.TFile("tmp/output_Zpole.root")
    proc = "wzp6_mumu"
    
    # sample/lumi
    xsec = 1692.4238 # pb
    lumi_lep = 35 # /pb
    lumi_fccee = 150e6 # /pb
    lumi = lumi_fccee

    # cuts
    costhetac_abs_min, costhetac_abs_max = 0.05, 0.8
    rebin = 1
    
    
    h_costhetac = fIn.Get(f"{proc}/cosThetac")
    h_costhetac.Rebin(rebin)
    h_meta = fIn.Get(f"{proc}/meta") # meta info: number of events in first bin
    nevents_sim = h_meta.GetBinContent(1) # number of simulated events
    h_costhetac.Scale(xsec*lumi/nevents_sim)
    
    
    # construct TGraph with errors sqrt(s) of the bin content
    N_F, N_B = 0, 0
    g_costhetac = ROOT.TGraphErrors()
    g_costhetac.SetLineColor(ROOT.kBlack)
    g_costhetac.SetMarkerStyle(20)
    g_costhetac.SetMarkerColor(ROOT.kBlack)
    g_costhetac.SetLineColor(ROOT.kBlack)
    for iBin in range(1, h_costhetac.GetNbinsX()+1):
    
        x, y = h_costhetac.GetBinCenter(iBin), h_costhetac.GetBinContent(iBin)
        if abs(x) > costhetac_abs_max or abs(x) < costhetac_abs_min: continue
        g_costhetac.SetPoint(iBin-1, x, y)
        g_costhetac.SetPointError(iBin-1, 0, y**0.5)
        print(x, y, y**0.5, h_costhetac.GetBinError(iBin))
        if x < 0: N_B += y
        else: N_F += y
    
    N_TOT = N_F + N_B
    A_FB = (N_F-N_B)/(N_F+N_B)
    
    A_FB_err = (4*N_F*N_B/(N_F+N_B)**3)**0.5
    
    # fit with parabola
    fit = ROOT.TF1("fit", "[0]*(3.*(1+x*x)/8. + [1]*x)", -costhetac_abs_max, costhetac_abs_max)
    fit.SetParameter(0, N_TOT)
    fit.SetParameter(1, 8.01962e-02)
    g_costhetac.Fit("fit", "NSE", "", -costhetac_abs_max, costhetac_abs_max)
    fit.SetLineColor(ROOT.kRed)
    
    A_FB_fit, A_FB_fit_err = fit.GetParameter(1), fit.GetParError(1)
    
    c = ROOT.TCanvas("c", "c", 1000, 1000)
    c.SetTopMargin(0.055)
    c.SetRightMargin(0.05)
    c.SetLeftMargin(0.15)
    c.SetBottomMargin(0.11)
    
    leg = ROOT.TLegend(.350, 0.5, .8, .9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.040)
    
    
    


    h_costhetac.GetXaxis().SetTitle("cos(#theta_{c}) (rad)")
    h_costhetac.GetXaxis().SetRangeUser(-1, 1)

    h_costhetac.GetXaxis().SetTitleFont(43)
    h_costhetac.GetXaxis().SetTitleSize(40)
    h_costhetac.GetXaxis().SetLabelFont(43)
    h_costhetac.GetXaxis().SetLabelSize(35)
    h_costhetac.GetXaxis().SetTitleOffset(1.2*h_costhetac.GetXaxis().GetTitleOffset())
    h_costhetac.GetXaxis().SetLabelOffset(1.2*h_costhetac.GetXaxis().GetLabelOffset())
    h_costhetac.GetYaxis().SetTitle("Events")

    h_costhetac.GetYaxis().SetTitleFont(43)
    h_costhetac.GetYaxis().SetTitleSize(40)
    h_costhetac.GetYaxis().SetLabelFont(43)
    h_costhetac.GetYaxis().SetLabelSize(35)

    h_costhetac.GetYaxis().SetTitleOffset(1.7*h_costhetac.GetYaxis().GetTitleOffset())
    h_costhetac.GetYaxis().SetLabelOffset(1.4*h_costhetac.GetYaxis().GetLabelOffset())
    
    
    h_costhetac.Draw("HIST")
    g_costhetac.Draw("SAME P")
    fit.Draw("SAME L")
    
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    if lumi == lumi_fccee: latex.DrawLatex(0.25, 0.85, "FCC-ee luminosity %d ab^{-1}" % (lumi/1e6))
    else: latex.DrawLatex(0.25, 0.85, "LEP luminosity %d pb^{-1}" % lumi)
    latex.DrawLatex(0.25, 0.78, "A_{FB} (int.) = %.3e #pm %.3e" % (A_FB, A_FB_err))
    latex.DrawLatex(0.25, 0.72, "A_{FB} (fit) = %.3e #pm %.3e" % (A_FB_fit, A_FB_fit_err))
    
    c.SaveAs(f"{outDir}/{proc}_cosThetac.png")
    
    
    print("##################")
    print(f"N_TOT:      {N_TOT}")
    print(f"N_F:        {N_F}")
    print(f"N_B:        {N_B}")
    print("A_FB:       %.3e +/- %.3e" % (A_FB, A_FB_err))
    print("A_FB_fit:   %.3e +/- %.3e" % (A_FB_fit, A_FB_fit_err))