
import sys,copy,array,os,subprocess,math
import ROOT
import argparse

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter


parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, help="Detector mode", choices=["IDEA", "IDEA_MC", "IDEA_3T", "CLD", "IDEA_noBES", "IDEA_2E", "IDEA_BES6pct"], default="IDEA")
parser.add_argument("--lumi", type=str, help="Luminosity (2p5, 5, 7p2, 10 or 15)", choices=["1", "2p5", "5", "7p2", "10", "15", "20"], default="7p2")
parser.add_argument("--statOnly", action='store_true', help="Stat-only fit")
args = parser.parse_args()


def findCrossing(xv, yv, left=True, flip=125, cross=1.):

    closestPoint, idx = 1e9, -1
    for i in range(0, len(xv)):
        if left and xv[i] > flip: continue
        if not left and xv[i] < flip: continue
        dy = abs(yv[i]-cross)
        if dy < closestPoint: 
            closestPoint = dy
            idx = i
    # find correct indices around crossing
    if left: 
        if yv[idx] > cross: idx_ = idx+1
        else: idx_ = idx-1
    else:
        if yv[idx] > cross: idx_ = idx-1
        else: idx_ = idx+1

    # do interpolation
    omega = (yv[idx]-yv[idx_])/(xv[idx]-xv[idx_])
    return (cross-yv[idx])/omega + xv[idx]

def analyzeMass(runDir, outDir, xMin=-1, xMax=-1, yMin=0, yMax=2, label="label"):

    if not os.path.exists(outDir): os.makedirs(outDir)

    fIn = ROOT.TFile("%s/higgsCombinemass.MultiDimFit.mH125.root" % runDir, "READ")
    t = fIn.Get("limit")

    str_out = ""

    xv, yv = [], []
    for i in range(0, t.GetEntries()):

        t.GetEntry(i)
        
        if t.quantileExpected < -1.5: continue
        if t.deltaNLL > 1000: continue
        if t.deltaNLL > 20: continue
        xv.append(getattr(t, "MH"))
        yv.append(t.deltaNLL*2.)

    xv, yv = zip(*sorted(zip(xv, yv)))
    g = ROOT.TGraph(len(xv), array.array('d', xv), array.array('d', yv))

    # bestfit = minimum
    mass = 1e9
    for i in xrange(g.GetN()):
        if g.GetY()[i] == 0.: mass = g.GetX()[i]

    # extract uncertainties at crossing = 1
    unc_m = findCrossing(xv, yv, left=True, flip=mass)
    unc_p = findCrossing(xv, yv, left=False, flip=mass)
    unc = 0.5*(abs(mass-unc_m) + abs(unc_p-mass))

    ########### PLOTTING ###########
    cfg = {

        'logy'              : False,
        'logx'              : False,

        'xmin'              : min(xv) if xMin < 0 else xMin,
        'xmax'              : max(xv) if xMax < 0 else xMax,
        'ymin'              : yMin,
        'ymax'              : yMax , # max(yv)

        'xtitle'            : "m_{h} (GeV)",
        'ytitle'            : "-2#DeltaNLL",

        'topRight'          : topRight, 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Internal}}",
        }

    plotter.cfg = cfg

    canvas = plotter.canvas()
    canvas.SetGrid()
    dummy = plotter.dummy()

    dummy.GetXaxis().SetNdivisions(507)
    dummy.Draw("HIST")

    g.SetMarkerStyle(20)
    g.SetMarkerColor(ROOT.kRed)
    g.SetMarkerSize(1)
    g.SetLineColor(ROOT.kRed)
    g.SetLineWidth(2)
    g.Draw("SAME LP")

    line = ROOT.TLine(float(cfg['xmin']), 1, float(cfg['xmax']), 1)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(2)
    line.Draw("SAME")

    leg = ROOT.TLegend(.20, 0.825, 0.90, .9)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.15)
    leg.SetBorderSize(1)
    leg.AddEntry(g, "%s, #delta(m_{h}) = %.2f MeV" % (label, unc*1000.), "LP")
    leg.Draw()

    plotter.aux()
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs("%s/mass%s.png" % (outDir, suffix))
    canvas.SaveAs("%s/mass%s.pdf" % (outDir, suffix))


    # write values to text file
    str_out = "%f %f %f %f\n" % (unc_m, unc_p, unc, mass)
    for i in range(0, len(xv)): str_out += "%f %f\n" % (xv[i], yv[i])
    tFile = open("%s/mass%s.txt" % (outDir, suffix), "w")
    tFile.write(str_out)
    tFile.close()
    tFile = open("%s/mass%s.txt" % (runDir, suffix), "w")
    tFile.write(str_out)
    tFile.close()

def analyzeXsec(runDir, outDir, xMin=-1, xMax=-1, yMin=0, yMax=2, label="label"):

    fIn = ROOT.TFile("%s/higgsCombinexsec.MultiDimFit.mH125.root" % runDir, "READ")
    t = fIn.Get("limit")

    ref_xsec = 0.201868 # pb, for pythia
    ref_xsec = 0.0067656 # whizard, Z->mumu
    ref_xsec = 1

    xv, yv = [], []
    for i in range(0, t.GetEntries()):
        t.GetEntry(i)
        xv.append(getattr(t, "r")*ref_xsec)
        yv.append(t.deltaNLL*2.)

    xv, yv = zip(*sorted(zip(xv, yv)))        
    g = ROOT.TGraph(len(xv), array.array('d', xv), array.array('d', yv))

    # bestfit = minimum
    xsec = 1e9
    for i in xrange(g.GetN()):
        if g.GetY()[i] == 0.: xsec = g.GetX()[i]

    # extract uncertainties at crossing = 1
    unc_m = findCrossing(xv, yv, left=True, flip=ref_xsec)
    unc_p = findCrossing(xv, yv, left=False, flip=ref_xsec)
    unc = 0.5*(abs(xsec-unc_m) + abs(unc_p-xsec))

    ########### PLOTTING ###########
    cfg = {

        'logy'              : False,
        'logx'              : False,
        
        'xmin'              : min(xv),
        'xmax'              : max(xv),
        'ymin'              : min(yv),
        'ymax'              : 2 , # max(yv)

        'xtitle'            : "#sigma(ZH, Z#rightarrow#mu#mu)/#sigma_{ref}",
        'ytitle'            : "-2#DeltaNLL",

        'topRight'          : topRight, 
        'topLeft'           : "#bf{FCCee} #scale[0.7]{#it{Internal}}",
    }

    plotter.cfg = cfg

    canvas = plotter.canvas()
    canvas.SetGrid()
    dummy = plotter.dummy()

    dummy.GetXaxis().SetNdivisions(507)
    dummy.Draw("HIST")

    g.SetMarkerStyle(20)
    g.SetMarkerColor(ROOT.kRed)
    g.SetMarkerSize(1)
    g.SetLineColor(ROOT.kRed)
    g.SetLineWidth(2)
    g.Draw("SAME LP")

    line = ROOT.TLine(float(cfg['xmin']), 1, float(cfg['xmax']), 1)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(2)
    line.Draw("SAME")

    leg = ROOT.TLegend(.20, 0.825, 0.90, .9)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.15)
    leg.SetBorderSize(1)
    leg.AddEntry(g, "%s, #delta(#sigma) = %.2f %%" % (label, unc*100.), "LP")
    leg.Draw()

    plotter.aux()
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs("%s/xsec%s.png" % (outDir, suffix))
    canvas.SaveAs("%s/xsec%s.pdf" % (outDir, suffix))

    # write values to text file
    str_out = "%f %f %f %f\n" % (unc_m, unc_p, unc, xsec)
    for i in range(0, len(xv)): str_out += "%f %f\n" % (xv[i], yv[i])
    tFile = open("%s/xsec%s.txt" % (outDir, suffix), "w")
    tFile.write(str_out)
    tFile.close()
    tFile = open("%s/xsec%s.txt" % (runDir, suffix), "w")
    tFile.write(str_out)
    tFile.close()



def doFit_xsec(runDir, rMin=0.98, rMax=1.02, npoints=50, combineOptions = ""):

    # scan for signal strength (= xsec)
    cmd = "combine -M MultiDimFit -t -1 --setParameterRanges r=%f,%f --points=%d --algo=grid ws.root --expectSignal=1 -m 125 --X-rtd TMCSO_AdaptivePseudoAsimov -v 10 --X-rtd ADDNLL_CBNLL=0 -n xsec %s" % (rMin, rMax, npoints, combineOptions)

    subprocess.call(cmd, shell=True, cwd=runDir)

def doFit_mass(runDir, mhMin=124.99, mhMax=125.01, npoints=50, combineOptions = ""):

    # scan for signal mass
    exe = "%s/HiggsAnalysis/CombinedLimit/build/bin/combine" % os.environ['WDIR']
    cmd = "%s -M MultiDimFit -t -1 --setParameterRanges MH=%f,%f --points=%d --algo=grid ws.root --expectSignal=1 -m 125 --redefineSignalPOIs MH --X-rtd TMCSO_AdaptivePseudoAsimov -v 10 --X-rtd ADDNLL_CBNLL=0 -n mass %s" % (exe, mhMin, mhMax, npoints, combineOptions)

    subprocess.call(cmd, shell=True, cwd=runDir)

def doFitDiagnostics_mass(runDir, mhMin=124.99, mhMax=125.01, combineOptions = ""):

    # scan for signal mass
    exe = "%s/HiggsAnalysis/CombinedLimit/build/bin/combine" % os.environ['WDIR']
    cmd = "%s -M FitDiagnostics -t -1 --setParameterRanges MH=%f,%f ws.root --expectSignal=1 -m 125 --redefineSignalPOIs MH --X-rtd TMCSO_AdaptivePseudoAsimov -v 10 --X-rtd ADDNLL_CBNLL=0 -n mass %s" % (exe, mhMin, mhMax, combineOptions)

    # ,shapeBkg_bkg_bin1__norm
    subprocess.call(cmd, shell=True, cwd=runDir)

    # get the uncertainty
    fIn = ROOT.TFile("%s/fitDiagnosticsmass.root"%runDir)
    fIn.ls()
    tt = fIn.Get("tree_fit_sb")
    tt.GetEntry(0)
    mh_err = tt.MHErr
    fIn.Close()
    return mh_err



def plotMultiple(tags, labels, fOut, xMin=-1, xMax=-1, yMin=0, yMax=2, legLabel="", forceStat=[]):

    global suffix
    best_mass, best_xsec = [], []
    unc_mass, unc_xsec = [], []
    g_mass, g_xsec = [], []
    statOnly = False
    if len(forceStat) == 0:
        statOnly = True
        forceStat = [False]*len(tags)

    for i, tag in enumerate(tags):
        xv, yv = [], []
        fIn = open("%s/mass%s.txt" % (tag, suffix+"_stat" if forceStat[i] else suffix), "r")
        for i,line in enumerate(fIn.readlines()):

            line = line.rstrip()
            if i == 0: 
                best_mass.append(float(line.split(" ")[3]))
                unc_mass.append(float(line.split(" ")[2]))
            else:
                xv.append(float(line.split(" ")[0]))
                yv.append(float(line.split(" ")[1]))

        g = ROOT.TGraph(len(xv), array.array('d', xv), array.array('d', yv))    
        g_mass.append(g)


    ########### PLOTTING ###########
    cfg = {

        'logy'              : False,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax,

        'xtitle'            : "m_{h} (GeV)",
        'ytitle'            : "-2#DeltaNLL",

        'topRight'          : topRight, 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
        }

    plotter.cfg = cfg

    canvas = plotter.canvas()
    canvas.SetGrid()
    dummy = plotter.dummy()

    dummy.GetXaxis().SetNdivisions(507)  
    dummy.Draw("HIST")

    n = len(g_mass) + (0 if legLabel=="" else 1)
    leg = ROOT.TLegend(.20, 0.9-n*0.05, 0.90, .9)
    leg.SetBorderSize(0)
    #leg.SetFillStyle(0) 
    leg.SetTextSize(0.03)
    leg.SetMargin(0.15)
    leg.SetBorderSize(1)
    if legLabel != "":
        leg.SetHeader(legLabel)

    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1]
    for i,g in enumerate(g_mass):
        g.SetMarkerStyle(20)
        g.SetMarkerColor(colors[i])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[i])
        g.SetLineWidth(4)
        g.Draw("SAME L")
        leg.AddEntry(g, "%s #delta(m_{h}) = %.2f MeV" % (labels[i], unc_mass[i]*1000.), "L")

    leg.Draw()
    line = ROOT.TLine(float(cfg['xmin']), 1, float(cfg['xmax']), 1)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(2)
    line.Draw("SAME")

    plotter.aux()
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    if statOnly:
        canvas.SaveAs("%s%s.png" % (fOut, suffix))
        canvas.SaveAs("%s%s.pdf" % (fOut, suffix))
    else:
        canvas.SaveAs("%s%s_stat.png" % (fOut, suffix))
        canvas.SaveAs("%s%s_stat.pdf" % (fOut, suffix))

def plotMultiple_xsec(tags, labels, fOut, xMin=-1, xMax=-1, yMin=0, yMax=2):

    best_xsec, unc_xsec, g_xsec = [], [], []
    for tag in tags:
        xv, yv = [], []
        fIn = open("%s/xsec.txt" % (tag), "r")
        for i,line in enumerate(fIn.readlines()):

            line = line.rstrip()
            if i == 0: 
                best_xsec.append(float(line.split(" ")[3]))
                unc_xsec.append(float(line.split(" ")[2]))
            else:
                xv.append(float(line.split(" ")[0]))
                yv.append(float(line.split(" ")[1]))

        g = ROOT.TGraph(len(xv), array.array('d', xv), array.array('d', yv))    
        g_xsec.append(g)

    cfg = {

        'logy'              : False,
        'logx'              : False,
        
        'xmin'              : xMin,
        'xmax'              : xMax,
        'ymin'              : yMin,
        'ymax'              : yMax,

        'xtitle'            : "#sigma(ZH#rightarrowl^{#plus}l^{#minus})/#sigma_{ref}",
        'ytitle'            : "-2#DeltaNLL",

        'topRight'          : topRight, 
        'topLeft'           : "#bf{FCC-ee} #scale[0.7]{#it{Simulation}}",
        }

    plotter.cfg = cfg

    canvas = plotter.canvas()
    canvas.SetGrid()
    dummy = plotter.dummy()

    dummy.GetXaxis().SetNdivisions(507)
    dummy.Draw("HIST")

    totEntries = len(g_xsec)
    leg = ROOT.TLegend(.20, 0.9-totEntries*0.05, 0.90, .9)
    leg.SetBorderSize(0)
    #leg.SetFillStyle(0) 
    leg.SetTextSize(0.03)
    leg.SetMargin(0.15)
    leg.SetBorderSize(1)

    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1]
    for i,g in enumerate(g_xsec):
        g.SetMarkerStyle(20)
        g.SetMarkerColor(colors[i])
        g.SetMarkerSize(1)
        g.SetLineColor(colors[i])
        g.SetLineWidth(4)
        g.Draw("SAME L")
        leg.AddEntry(g, "%s #delta(#sigma) = %.2f %%" % (labels[i], unc_xsec[i]*100.), "L")

    leg.Draw()
    line = ROOT.TLine(float(cfg['xmin']), 1, float(cfg['xmax']), 1)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineWidth(2)
    line.Draw("SAME")

    plotter.aux()
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs("%s.png" % (fOut))
    canvas.SaveAs("%s.pdf" % (fOut))


def breakDown(fitCfg):
    def getUnc(fitCfg, tag, type_):

        xv, yv = [], []
        fIn = open("%s/%s/%s%s.txt" % (outDir, fitCfg, type_, tag), "r")
        for i,line in enumerate(fIn.readlines()):

            line = line.rstrip()
            if i == 0: 
                best = float(line.split(" ")[3])
                unc = float(line.split(" ")[2])
                break
                
        if type_ == "mass": unc*= 1000. # convert to MeV
        if type_ == "xsec": unc*= 100. # convert to %
        return best, unc

    ############# mass
    canvas = ROOT.TCanvas("c", "c", 800, 800)
    canvas.SetTopMargin(0.08)
    canvas.SetBottomMargin(0.1)
    canvas.SetLeftMargin(0.25)
    canvas.SetRightMargin(0.05)
    canvas.SetFillStyle(4000) # transparency?
    canvas.SetGrid(1, 0)
    canvas.SetTickx(1)


    xMin, xMax = -3, 3
    xTitle = "#sigma_{syst.}(m_{h}) (MeV)"

    ref = ""
    best_ref, unc_ref = getUnc(fitCfg, "_stat", "mass")
    params = ["_BES", "_SQRTS", "_LEPSCALE_MU", "_LEPSCALE_EL", ""]
    labels = ["BES 6%", "#sqrt{s} #pm 2 MeV", "Muon scale (~10^{-5})", "El. scale (~10^{-5})", "Syst. combined"]

    n_params = len(params)
    h_pulls = ROOT.TH2F("pulls", "pulls", 6, xMin, xMax, n_params, 0, n_params)
    g_pulls = ROOT.TGraphAsymmErrors(n_params)

    i = n_params
    for p in xrange(n_params):
        i -= 1
        best, unc = getUnc(fitCfg, params[p], "mass")
        #unc = math.sqrt(unc_ref**2 - unc**2)
        print(unc_ref, unc)
        unc = math.sqrt(unc**2 - unc_ref**2)
        g_pulls.SetPoint(i, 0, float(i) + 0.5)
        g_pulls.SetPointError(i, unc, unc, 0., 0.)
        h_pulls.GetYaxis().SetBinLabel(i + 1, "#splitline{%s}{(%.2f MeV)}" % (labels[p], unc))


    h_pulls.GetXaxis().SetTitleSize(0.04)
    h_pulls.GetXaxis().SetLabelSize(0.03)
    h_pulls.GetXaxis().SetTitle(xTitle)
    h_pulls.GetXaxis().SetTitleOffset(1)
    h_pulls.GetYaxis().SetLabelSize(0.045)
    h_pulls.GetYaxis().SetTickLength(0)
    h_pulls.GetYaxis().LabelsOption('v')
    h_pulls.SetNdivisions(506, 'XYZ')
    h_pulls.Draw("HIST")


    g_pulls.SetMarkerSize(0.8)
    g_pulls.SetMarkerStyle(20)
    g_pulls.SetLineWidth(2)
    g_pulls.Draw('P SAME')
    
    
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.045)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(30) # 0 special vertical aligment with subscripts
    latex.DrawLatex(0.95, 0.925, topRight)

    latex.SetTextAlign(13)
    latex.SetTextFont(42)
    latex.SetTextSize(0.045)
    latex.DrawLatex(0.25, 0.96, "#bf{FCCee} #scale[0.7]{#it{Simulation}}")

    canvas.SaveAs("%s/%s/mass_breakdown.png" % (outDir, fitCfg))
    canvas.SaveAs("%s/%s/mass_breakdown.pdf" % (outDir, fitCfg))
    del canvas, g_pulls, h_pulls


def text2workspace(runDir):

    cmd = "text2workspace.py datacard.txt -o ws.root  -v 10"
    subprocess.call(cmd, shell=True, cwd=runDir)

def combineCards(runDir, input_=[]):

    if not os.path.exists(runDir): os.makedirs(runDir)
    
    input_ = ["%s/%s" % (os.getcwd(), i) for i in input_]
    cards = ' '.join(input_)

    cmd = "combineCards.py %s > datacard.txt" % cards
    subprocess.call(cmd, shell=True, cwd=runDir)
    text2workspace(runDir)


if __name__ == "__main__":

    mode = args.mode
    lumi = args.lumi

    lumi_suffix = "_LUMI_%s"%lumi
    combineDir = "combine/h_mass/%s%s" % (mode, lumi_suffix)
    #outDir = "/eos/user/j/jaeyserm/www/FCCee/ZH_mass/combine/%s%s/" % (mode, lumi_suffix) # CERN
    outDir = "/work/submit/jaeyserm/public_html/fccee/ZH_mass/combine_out/%s%s/" % (mode, lumi_suffix) # MIT
    topRight = "#sqrt{s} = 240 GeV, %s ab^{#minus1}" % lumi.replace('p', '.')

    def mHrange(mh_err):
        if 1.5*mh_err > 0.05: # bound to 50 MeV
            return 124.95, 125.05
        return 125-1.5*mh_err, 125+1.5*mh_err

    combineOptions = ""
    freezeParameters = []
    setParameters = []
    suffix=""

    doSyst = not args.statOnly
    if not doSyst:
        suffix = "_stat"
        freezeParameters.extend(["BES", "ISR", "SQRTS", "LEPSCALE_MU", "LEPSCALE_EL"])

    freezeBkg = False
    if freezeBkg:
        suffix = "_freezeBkg%s"%suffix
        freezeParameters.extend(["bkg_norm"])

    noBkg = False
    if noBkg:
        suffix = "_noBkg%s"%suffix
        freezeParameters.extend(["bkg_norm"])
        setParameters.extend(["bkg_norm=0"])

    ## systematic variations, unfreeze them
    systs = ["BES", "SQRTS", "LEPSCALE_MU", "LEPSCALE_EL"]

    #suffix+="_BES"
    #systs.remove("BES")

    #suffix+="_SQRTS"
    #systs.remove("SQRTS")

    #suffix+="_LEPSCALE_MU"
    #systs.remove("LEPSCALE_MU")

    #suffix+="_LEPSCALE_EL"
    #systs.remove("LEPSCALE_EL")

    #freezeParameters.extend(systs)


    doBreakDown = False
    if doBreakDown:
        breakDown("mumu_ee_combined_categorized")
        breakDown("mumu_ee_combined_inclusive")
        breakDown("mumu_cat0")
        breakDown("mumu_cat1")
        breakDown("mumu_cat2")
        breakDown("mumu_cat3")
        breakDown("mumu_combined")
        breakDown("ee_cat0")
        breakDown("ee_cat1")
        breakDown("ee_cat2")
        breakDown("ee_cat3")
        breakDown("ee_combined")
        quit()

    doSummary = False
    if doSummary:
        outDir__ = "/work/submit/jaeyserm/public_html/fccee/ZH_mass/combine_out/"
        plotMultiple(["%s/IDEA_LUMI_7p2/mumu_combined/"%outDir__, "%s/IDEA_MC_LUMI_7p2/mumu_combined/"%outDir__, "%s/IDEA_3T_LUMI_7p2/mumu_combined/"%outDir__, "%s/CLD_LUMI_7p2/mumu_combined/"%outDir__], ["IDEA", "IDEA perfect resolution", "IDEA 3T", "IDEA CLD silicon tracker"], "%s/IDEA_IDEAL_2T_3T_CLD_mumu"%outDir__, xMin=124.99, xMax=125.01, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H (stat. + syst.)")
        plotMultiple(["%s/IDEA_LUMI_7p2/mumu_combined/"%outDir__, "%s/IDEA_MC_LUMI_7p2/mumu_combined/"%outDir__, "%s/IDEA_3T_LUMI_7p2/mumu_combined/"%outDir__, "%s/CLD_LUMI_7p2/mumu_combined/"%outDir__], ["IDEA", "IDEA perfect resolution", "IDEA 3T", "IDEA CLD silicon tracker"], "%s/IDEA_IDEAL_2T_3T_CLD_mumu"%outDir__, xMin=124.99, xMax=125.01, legLabel="Muon final state Z(#mu^{#plus}#mu^{#minus})H (stat. only)", forceStat=[True, True, True, True])
        plotMultiple(["%s/IDEA_LUMI_7p2/mumu_ee_combined_categorized/"%outDir__, "%s/IDEA_LUMI_7p2/mumu_ee_combined_categorized/"%outDir__], ["Statistical", "Statistical+systematic"], "%s/IDEA_stat_syst"%outDir__, xMin=124.995, xMax=125.005, legLabel="Combined muon and electron final states", forceStat=[True, False])
        quit()


    ##################################
    if len(freezeParameters) > 0:
        combineOptions += " --freezeParameters " + ",".join(freezeParameters)
    if len(setParameters) > 0:
        combineOptions += " --setParameters " + ",".join(setParameters)


    ############### MUON
    if True:
        tag, label = "mumu_cat0", "#mu^{#plus}#mu^{#minus}, inclusive"
        rMin, rMax = 0.98, 1.02
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)
        #doFit_xsec("%s/%s" % (combineDir, tag), rMin=rMin, rMax=rMax, npoints=50, combineOptions=combineOptions)
        #analyzeXsec("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=rMin, xMax=rMax)
        #doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, combineOptions=combineOptions)

        tag, label = "mumu_cat1", "#mu^{#plus}#mu^{#minus}, central-central"
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)

        tag, label = "mumu_cat2", "#mu^{#plus}#mu^{#minus}, central-forward"
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)

        tag, label = "mumu_cat3", "#mu^{#plus}#mu^{#minus}, forward-forward"
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)

        tag, label = "mumu_combined", "#mu^{#plus}#mu^{#minus}, combined"
        combineCards("%s/%s" % (combineDir, tag), [combineDir+"/mumu_cat1/datacard_parametric.txt", combineDir+"/mumu_cat2/datacard_parametric.txt", combineDir+"/mumu_cat3/datacard_parametric.txt"])
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)


    ############### ELECTRON
    if True:
        tag, label = "ee_cat0", "e^{#plus}e^{#minus}, inclusive"
        rMin, rMax = 0.98, 1.02
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)
        
        tag, label = "ee_cat1", "e^{#plus}e^{#minus}, central-central"
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)

        tag, label = "ee_cat2", "e^{#plus}e^{#minus}, central-forward"
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)

        tag, label = "ee_cat3", "e^{#plus}e^{#minus}, forward-forward"
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)

        tag, label = "ee_combined", "e^{#plus}e^{#minus}, combined"
        combineCards("%s/%s" % (combineDir, tag), [combineDir+"/ee_cat1/datacard_parametric.txt", combineDir+"/ee_cat2/datacard_parametric.txt", combineDir+"/ee_cat3/datacard_parametric.txt"])
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)


    ############### MUON+ELECTRON
    if True:

        tag, label = "mumu_ee_combined_inclusive", "#mu^{#plus}#mu^{#minus}+e^{#plus}e^{#minus}, inclusive"
        combineCards("%s/%s" % (combineDir, tag), [combineDir+"/mumu_cat0/datacard_parametric.txt", combineDir+"/ee_cat0/datacard_parametric.txt"])
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)


        tag, label = "mumu_ee_combined_categorized", "#mu^{#plus}#mu^{#minus}+e^{#plus}e^{#minus}, categorized"
        combineCards("%s/%s" % (combineDir, tag), [combineDir+"/mumu_combined/datacard.txt", combineDir+"/ee_combined/datacard.txt"])
        mh_err = doFitDiagnostics_mass("%s/%s" % (combineDir, tag), mhMin=124.95, mhMax=125.05, combineOptions=combineOptions)
        mhMin, mhMax = mHrange(mh_err)
        doFit_mass("%s/%s" % (combineDir, tag), mhMin=mhMin, mhMax=mhMax, npoints=50, combineOptions=combineOptions)
        analyzeMass("%s/%s" % (combineDir, tag), "%s/%s/" % (outDir, tag), label=label, xMin=mhMin, xMax=mhMax)

        plotMultiple(["%s/mumu_cat0/"%outDir, "%s/ee_cat0/"%outDir, "%s/mumu_ee_combined_inclusive/"%outDir], ["#mu^{#plus}#mu^{#minus}, inclusive", "e^{#plus}e^{#minus}, inclusive", "#mu^{#plus}#mu^{#minus} + e^{#plus}e^{#minus}, inclusive"], "%s/mumu_ee_inclusive"%outDir, xMin=124.99, xMax=125.01)
        plotMultiple(["%s/mumu_combined/"%outDir, "%s/ee_combined/"%outDir, "%s/mumu_ee_combined_categorized/"%outDir], ["#mu^{#plus}#mu^{#minus}, categorized", "e^{#plus}e^{#minus}, categorized", "#mu^{#plus}#mu^{#minus} + e^{#plus}e^{#minus}, categorized"], "%s/mumu_ee_categorized"%outDir, xMin=124.99, xMax=125.01)
        plotMultiple(["%s/mumu_cat0/"%outDir, "%s/mumu_combined/"%outDir, "%s/ee_cat0/"%outDir, "%s/ee_combined/"%outDir], ["#mu^{#plus}#mu^{#minus}, inclusive", "#mu^{#plus}#mu^{#minus}, categorized", "e^{#plus}e^{#minus}, inclusive", "e^{#plus}e^{#minus}, categorized"], "%s/mumu_ee_inclusive_categorized"%outDir, xMin=124.99, xMax=125.01)
