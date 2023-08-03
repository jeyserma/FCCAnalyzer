
import sys,copy,array,os,subprocess,math
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--flavor", type=str, choices=["ee", "mumu", "qq"], help="Flavor (ee, mumu, qq)", default="mumu")
args = parser.parse_args()

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import plotter


datacard_template_ll = """
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

datacard_template_qq = """
imax *
jmax *
kmax *
---------------
shapes Zqq          * datacard.root Zqq
shapes bkg          * datacard.root bkg
shapes data_obs     * datacard.root Zqq
---------------
---------------
#bin            bin1
observation     -1
------------------------------
bin          bin1   bin1
process      Zqq    bkg
process      0      1
rate         -1     -1
--------------------------------
dummy lnN    1.00    1.00001
"""

 
def doFitDiagnostics(runDir, rMin=0, rMax=2, combineOptions = ""):
    cmd = "combine -M FitDiagnostics -t -1 --setParameterRanges r=%f,%f ws.root --expectSignal=1 -m 125  -v 10 %s" % (rMin, rMax, combineOptions)
    subprocess.call(cmd, shell=True, cwd=runDir)
    
def text2workspace(cardName, combineDir):
    cmd = "text2workspace.py %s -o ws.root  -v 10 --X-allow-no-background" % cardName
    subprocess.call(cmd, shell=True, cwd=combineDir)
  
if __name__ == "__main__":

    flavor = args.flavor
    combineDir = "combine/run_z_xsec_%s" % flavor # make directory if it does not exist
    if not os.path.exists(combineDir): os.makedirs(combineDir)

    if flavor == "mumu":
        rootFile = "tmp/output_z_xsec_%s.root" % flavor # analysis output ROOT file
        cardName = "datacard.txt" # datacard name, as written in the combineDir
        signalName = "p8_ee_Zmumu_ecm91"
        tauName = "p8_ee_Ztautau_ecm91"
        histName = "zll_m_cut4" # fit on the Z mass peak
        
        # Step 1: make datacard
        datacard = datacard_template_ll.format(rootFile=os.path.abspath(rootFile), sig=signalName, Ztautau=tauName, hName=histName)
        cardFile = open("%s/%s" % (combineDir, cardName), "w")
        cardFile.write(datacard)
        cardFile.close()
    
    
        # Step 2: run text2workspace (make the model in Combine from the input histograms)
        text2workspace(cardName, combineDir)
        
        
        # Step 3: run the fit
        combineOptions = ""
        rMin, rMax = 0.95, 1.05
        doFitDiagnostics(combineDir, rMin=rMin, rMax=rMax, combineOptions=combineOptions)
        
    if flavor == "qq":
        
        # Step 1: first we need to merge all hadronic processes to 1 histogram, write to datacard.root in the combineDir
        # as we don't have backgrounds here, make a fake background with tiny yields
        
        fIn = ROOT.TFile("tmp/output_z_xsec_qq.root")
        z_bb = fIn.Get("p8_ee_Zbb_ecm91/dijet_m_final")
        z_cc = fIn.Get("p8_ee_Zcc_ecm91/dijet_m_final")
        z_uds = fIn.Get("p8_ee_Zuds_ecm91/dijet_m_final")
        z_bb.Add(z_cc)
        z_cc.Add(z_uds)
        z_bb.SetName("Zqq")
        #z_bb.Scale(1./10000)
        
        bkg = z_bb.Clone("bkg")
        for k in range(1, bkg.GetNbinsX()+1): 
            bkg.SetBinContent(k, 0.1)
            bkg.SetBinError(k, 0.001)
            
        fOut = ROOT.TFile("%s/datacard.root" % combineDir, "RECREATE")
        z_bb.Write()
        bkg.Write()
        fOut.Close()

        fIn.Close()
        
        
        # Step 2: prepare the text combine card
        cardFile = open("%s/datacard.txt" % combineDir, "w")
        cardFile.write(datacard_template_qq)
        cardFile.close()
        
        # Step 3: run text2workspace (make the model in Combine from the input histograms)
        #text2workspace("datacard.txt", combineDir)
        
        # Step 4: run the fit
        combineOptions = "" #  --skipBOnlyFit justFit --skipBOnlyFit
        rMin, rMax = 0.99, 1.01
        #doFitDiagnostics(combineDir, rMin=rMin, rMax=rMax, combineOptions=combineOptions) # need combinedTF...