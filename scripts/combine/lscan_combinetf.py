
'''
Script to plot the likelihood scan and extract uncertainties using combinetf

How to run CombineTF:

combinetf.py datacard.hdf5 -t -1 --fitverbose 10 --scan zhss_mu --scanRange 2 --postfix zhss_mu --scanPoints 8 --allowNegativePOI

--scan: the parameter of interest (POI), as defined in the card
--scanRange: the range in number of sigma's, computed based on the Hessian uncertainty
--scanPoints: the number of points to be computed for the likelihood scan
'''

import sys
import os
import ROOT
import array
import argparse 
import numpy as np
from scipy import interpolate, optimize

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default="", help="ROOT input file")
parser.add_argument("-l", "--label", type=str, default="", help="Label")
parser.add_argument("-o", "--outName", type=str, default="", help="Output name")
parser.add_argument("--outFolder", type=str, default="./", help='Output dir')
parser.add_argument("-p", "--poi", type=str, default="zhss_mu", help='Parameter of interest')
args = parser.parse_args()


def findCrossing(xv, yv, x_min_hess, unc_hess):
    x = np.array(xv)
    y = np.array(yv)
    minx = x[np.argmin(y)]
    interp_fn = interpolate.interp1d(x, y, 'quadratic')
    interp_fn2 = lambda x: interp_fn(x)-1 # 68% CL = crossing at 1
    unc_m, unc_p = optimize.newton(interp_fn2, x_min_hess-unc_hess), optimize.newton(interp_fn2, x_min_hess+unc_hess)
    unc_avg = 0.5*(abs(minx-unc_m) + abs(unc_p-minx))
    return unc_m, unc_p, unc_avg, minx

def main(args):
    if not os.path.exists(args.outFolder): os.makedirs(args.outFolder)

    fIn = ROOT.TFile(args.input, "READ")
    t = fIn.Get("fitresults")

    # TF1 for Hessian unc - plot parabola
    t.GetEntry(0) # first entry is Hessian
    x_min_hess = getattr(t, args.poi)
    unc_hess = getattr(t, f"{args.poi}_err")
    a_ = 1./(unc_hess**2)
    g_nll_hess = ROOT.TF1("parabola_func", f"{a_}*(x-{x_min_hess})*(x-{x_min_hess})", x_min_hess-3*unc_hess, x_min_hess+3*unc_hess)
    g_nll_hess.SetLineColor(ROOT.kBlue)
    g_nll_hess.SetLineWidth(2)

    xv, yv = [], []
    yMin_, xMin_ = 1e9, 1e9
    for i in range(1, t.GetEntries()): 
        t.GetEntry(i)
        mu = getattr(t, args.poi)

        xv.append(mu)
        deltaNLL = t.dnllval*2.
        if deltaNLL < yMin_:
            yMin_ = deltaNLL
            xMin_ = mu
        yv.append(deltaNLL)
        #print(mu, deltaNLL, t.nllval, t.nllvalfull)
    yv = [k - yMin_ for k in yv] # DeltaNLL
    xv, yv = zip(*sorted(zip(xv, yv)))
    g_nll = ROOT.TGraph(len(xv), array.array('d', xv), array.array('d', yv))

    # find the crossing at 68% CL, i.e. DeltaNLL=1
    unc_m, unc_p, unc, x_min = findCrossing(xv, yv, x_min_hess, unc_hess)

    #############################################
    c = ROOT.TCanvas("c", "c", 1000, 1000)
    c.SetTopMargin(0.055)
    c.SetRightMargin(0.05)
    c.SetLeftMargin(0.15)
    c.SetBottomMargin(0.11)
    c.SetGrid()

    g_nll.GetXaxis().SetTitle("Signal Strength #mu")
    
    g_nll.SetMarkerStyle(20)
    g_nll.SetMarkerColor(ROOT.kRed)
    g_nll.SetMarkerSize(1)
    g_nll.SetLineColor(ROOT.kRed)
    g_nll.SetLineWidth(2)

    g_nll.GetXaxis().SetTitleFont(43)
    g_nll.GetXaxis().SetTitleSize(40)
    g_nll.GetXaxis().SetLabelFont(43)
    g_nll.GetXaxis().SetLabelSize(35)
    g_nll.GetXaxis().SetTitleOffset(1.2*g_nll.GetXaxis().GetTitleOffset())
    g_nll.GetXaxis().SetLabelOffset(1.2*g_nll.GetXaxis().GetLabelOffset())
    g_nll.GetYaxis().SetTitle("-2#DeltaNLL")

    g_nll.GetYaxis().SetTitleFont(43)
    g_nll.GetYaxis().SetTitleSize(40)
    g_nll.GetYaxis().SetLabelFont(43)
    g_nll.GetYaxis().SetLabelSize(35)

    g_nll.GetYaxis().SetTitleOffset(1.7*g_nll.GetYaxis().GetTitleOffset())
    g_nll.GetYaxis().SetLabelOffset(1.4*g_nll.GetYaxis().GetLabelOffset())

    g_nll.Draw("ALP")
    g_nll_hess.Draw("L SAME")

    leg = ROOT.TLegend(.20, 0.78, 0.85, .92)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.03)
    leg.SetMargin(0.15)
    leg.SetBorderSize(1)
    leg.SetHeader(args.label)
    leg.AddEntry(g_nll, "Likelihood scan #delta#mu = %.2f %%" % (unc*100.), "LP")
    leg.AddEntry(g_nll_hess, "Hessian #delta#mu = %.2f %%" % (unc_hess*100.), "LP")
    leg.Draw()

    c.Modify()
    c.Update()
    c.Draw()
    c.SaveAs(f"{args.outFolder}/{args.outName}.png")
    c.SaveAs(f"{args.outFolder}/{args.outName}.pdf")


if __name__ == "__main__":
    main(args)
