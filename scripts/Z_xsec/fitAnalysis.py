
import sys,copy,array,os,subprocess,math
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter


datacard_template = """
imax *
jmax *
kmax *
---------------
shapes Zmumu        * {rootFile} {sig}/{hName}
shapes Ztautau      * {rootFile} {Ztautau}/{hName}
shapes data_obs     * {rootFile} {sig}/{hName}
---------------
---------------
#bin            bin1
observation     -1
------------------------------
bin          bin1           bin1
process      Zmumu          Ztautau 
process      0              1
rate         -1             -1
--------------------------------
"""


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
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
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
    canvas.SaveAs("%s/mass.png" % outDir)
    canvas.SaveAs("%s/mass.pdf" % outDir)
    
    
    # write values to text file
    str_out = "%f %f %f %f\n" % (unc_m, unc_p, unc, mass)
    for i in range(0, len(xv)): str_out += "%f %f\n" % (xv[i], yv[i])
    tFile = open("%s/mass.txt" % outDir, "w")
    tFile.write(str_out)
    tFile.close()
    tFile = open("%s/mass.txt" % runDir, "w")
    tFile.write(str_out)
    tFile.close()
        
def analyzeXsec(tag):

    fIn = ROOT.TFile("%s/higgsCombine%s_xsec.MultiDimFit.mH125.root" % (runDir, tag), "READ")
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
            
        'topRight'          : "#sqrt{s} = 240 GeV, 5 ab^{#minus1}", 
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
    
    leg = ROOT.TLegend(.20, 0.82, 0.90, .9)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.035)
    leg.SetMargin(0.15)
    leg.SetBorderSize(1)
    leg.AddEntry(g, "#sigma = %.5f #pm  %.5f" % (xsec, unc), "L")
    leg.Draw()
              
    plotter.aux()
    canvas.Modify()
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs("%s/xsec_%s.png" % (outDir, tag))
    canvas.SaveAs("%s/xsec_%s.pdf" % (outDir, tag))
    
    
    # write values to text file
    str_out = "%f %f %f %f\n" % (unc_m, unc_p, unc, xsec)
    for i in range(0, len(xv)): str_out += "%f %f\n" % (xv[i], yv[i])
    tFile = open("%s/xsec_%s.txt" % (outDir, tag), "w")
    tFile.write(str_out)
    tFile.close()
    tFile = open("%s/xsec_%s.txt" % (runDir, tag), "w")
    tFile.write(str_out)
    tFile.close()

def calculateXsec(tag, combineOptions = "", rMin=0.95, rMax=1.05, npoints=50):

    # scan for signal strength (= xsec)
    cmd = "combine -M MultiDimFit -t -1 --setParameterRanges r=%f,%f --points=%d --algo=grid ws.root --expectSignal=1 -m 125 --X-rtd TMCSO_AdaptivePseudoAsimov -v 10 --X-rtd ADDNLL_CBNLL=0 -n %s_xsec %s" % (rMin, rMax, npoints, tag, combineOptions)
    
    subprocess.call(cmd, shell=True, cwd=runDir)
     
def doFit_mass(runDir, mhMin=124.99, mhMax=125.01, npoints=50, combineOptions = ""):

    # scan for signal mass
    cmd = "combine -M MultiDimFit -t -1 --setParameterRanges MH=%f,%f --points=%d --algo=grid ws.root --expectSignal=1 -m 125 --redefineSignalPOIs MH --X-rtd TMCSO_AdaptivePseudoAsimov -v 10 --X-rtd ADDNLL_CBNLL=0 -n mass %s" % (mhMin, mhMax, npoints, combineOptions)
    
    subprocess.call(cmd, shell=True, cwd=runDir)
    
def doFitDiagnostics(runDir, rMin=0, rMax=2, combineOptions = ""):


    cmd = "combine -M FitDiagnostics -t -1 --setParameterRanges r=%f,%f ws.root --expectSignal=1 -m 125  -v 10 %s" % (rMin, rMax, combineOptions)
    subprocess.call(cmd, shell=True, cwd=runDir)
    

    

def text2workspace(cardName, combineDir):

    cmd = "text2workspace.py %s -o ws.root  -v 10" % cardName
    subprocess.call(cmd, shell=True, cwd=combineDir)
    
def combineCards(runDir, input_=[]):

    if not os.path.exists(runDir): os.makedirs(runDir)
    
    input_ = ["%s/%s" % (os.getcwd(), i) for i in input_]
    cards = ' '.join(input_)
    
    cmd = "combineCards.py %s > datacard.txt" % cards
    subprocess.call(cmd, shell=True, cwd=runDir)
    text2workspace(runDir)


def makeCard(cardName, combineDir, rootFile, signalName, procName_Ztautau, histName):

    datacard = datacard_template.format(rootFile=os.path.abspath(rootFile), sig=signalName, Ztautau=procName_Ztautau, hName=histName)
    print(datacard)
    cardFile = open("%s/%s" % (combineDir, cardName), "w")
    cardFile.write(datacard)
    cardFile.close()
    
    
  
if __name__ == "__main__":

    flavor = "mumu"
    combineDir = "combine/run_z_xsec" # make directory if it does not exist


    
    rootFile = "tmp/output_z_xsec_%s.root" % flavor # analysis output ROOT file
    cardName = "datacard.txt" # datacard name, as written in the combineDir
    signalName = "p8_ee_Z%s_ecm91" % flavor # electrons or muons
    histName = "zll_m_cut4" # fit on the Z mass peak
    
    makeCard(cardName, combineDir, rootFile=rootFile, signalName=signalName, procName_Ztautau="p8_ee_Ztautau_ecm91", histName=histName)
    text2workspace(cardName, combineDir)
    
    combineOptions = ""
    rMin, rMax = 0, 2
    doFitDiagnostics(combineDir, rMin=rMin, rMax=rMax, combineOptions=combineOptions)
    
 