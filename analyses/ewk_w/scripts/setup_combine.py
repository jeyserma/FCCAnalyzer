
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


if __name__ == "__main__":
    fIn = ROOT.TFile("output_wmass_kinematic.root")
    outDir = f"combine/wmass_kinematic/" # directory must exist

    proc = "yfsww_ee_ww_noBES_ecm163"

    # get 
    hists = {}
    for charge in ["plus", "minus"]:
        h_base = fIn.Get(f"{proc}/w_{charge}_m")
        h_up = fIn.Get(f"{proc}/w_{charge}_m_plus_10MeV")
        h_dw = fIn.Get(f"{proc}/w_{charge}_m_minus_10MeV")
        hists[f"{charge}_nominal"] = copy.deepcopy(h_base)
        hists[f"{charge}_nominal_massShift10MeVUp"] = copy.deepcopy(h_up)
        hists[f"{charge}_nominal_massShift10MeVDown"] = copy.deepcopy(h_dw)
    fIn.Close()

    # write hists to a datacard.root
    fOut = ROOT.TFile(f"{outDir}/datacard.root", "RECREATE")
    for h in hists:
        hists[h].SetName(h)
        hists[h].Write()
    fOut.Close()

    # make datacard
    dc = ""
    dc += "imax *\n"
    dc += "jmax *\n"
    dc += "kmax *\n"
    dc += "####################\n"
    dc += "shapes *        * datacard.root $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n"
    dc += "shapes data_obs * datacard.root $CHANNEL_nominal\n"
    dc += "####################\n"
    dc += "bin                      plus      minus\n"
    dc += "observation              -1        -1\n"
    dc += "####################\n"
    dc += "bin                      plus      minus\n"
    dc += "process                  nominal   nominal\n"
    dc += "process                  1         1\n"
    dc += "rate                     -1        -1\n"
    dc += "####################\n"
    #dc += "dummy lnN                1.001    1.0001\n" # 0.1 % normalization uncertainty 
    dc += "massShift10MeV shapeNoConstraint  1   1\n" # uncertainty on the w mass, free floating

    f = open(f"{outDir}/datacard.txt", 'w')
    f.write(dc)
    f.close()

    print(dc)


