
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


def semileptonic(hName, cat):
    procNameUp = procName.replace("noBES", "mw50MeVplus_noBES")
    procNameDw = procName.replace("noBES", "mw50MeVminus_noBES")

    fIn = ROOT.TFile(fName)
    h_base = fIn.Get(f"{procName}/{hName}")
    h_bkg = fIn.Get(f"{bkgName}/{hName}")
    h_up = fIn.Get(f"{procNameUp}/{hName}")
    h_dw = fIn.Get(f"{procNameDw}/{hName}")

    hists = {}
    hists[f"{cat}_nominal"] = copy.deepcopy(h_base)
    hists[f"{cat}_bkg"] = copy.deepcopy(h_bkg)
    hists[f"{cat}_nominal_massShift50MeVUp"] = copy.deepcopy(h_up)
    hists[f"{cat}_nominal_massShift50MeVDown"] = copy.deepcopy(h_dw)
    fIn.Close()

    # write hists to a datacard.root
    fOut = ROOT.TFile(f"{outDir}/datacard_{cat}.root", "RECREATE")
    for h in hists:
        hists[h].SetName(h)
        hists[h].Write()
    fOut.Close()

    # make datacard
    dc = ""
    dc += f"imax *\n"
    dc += f"jmax *\n"
    dc += "kmax *\n"
    dc += f"####################\n"
    dc += f"shapes *        * datacard_{cat}.root $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n"
    dc += f"shapes data_obs * datacard_{cat}.root $CHANNEL_nominal\n"
    dc += f"####################\n"
    dc += f"bin                      {cat}\n"
    dc += f"observation              -1\n"
    dc += f"####################\n"
    dc += f"bin                      {cat}     {cat}\n"
    dc += f"process                  nominal   bkg\n"
    dc += f"process                  1         2\n"
    dc += f"rate                     -1        -1\n"
    dc += f"####################\n"
    #dc += "dummy lnN                1.001    1.0001\n" # 0.1 % normalization uncertainty 
    dc += f"massShift50MeV shapeNoConstraint  1        -\n" # uncertainty on the w mass, free floating

    f = open(f"{outDir}/datacard_{cat}.txt", 'w')
    f.write(dc)
    f.close()

    print(dc)



def hadronic(hName1, hName2):
    procNameUp = procName.replace("noBES", "mw50MeVplus_noBES")
    procNameDw = procName.replace("noBES", "mw50MeVminus_noBES")

    fIn = ROOT.TFile(fName)
    h1_base = fIn.Get(f"{procName}/{hName1}")
    h1_bkg = fIn.Get(f"{bkgName}/{hName1}")
    h1_up = fIn.Get(f"{procNameUp}/{hName1}")
    h1_dw = fIn.Get(f"{procNameDw}/{hName1}")

    h2_base = fIn.Get(f"{procName}/{hName2}")
    h2_bkg = fIn.Get(f"{bkgName}/{hName2}")
    h2_up = fIn.Get(f"{procNameUp}/{hName2}")
    h2_dw = fIn.Get(f"{procNameDw}/{hName2}")

    hists = {}
    hists[f"qqqq_w1_nominal"] = copy.deepcopy(h1_base)
    hists[f"qqqq_w1_bkg"] = copy.deepcopy(h1_bkg)
    hists[f"qqqq_w1_nominal_massShift50MeVUp"] = copy.deepcopy(h1_up)
    hists[f"qqqq_w1_nominal_massShift50MeVDown"] = copy.deepcopy(h1_dw)
    hists[f"qqqq_w2_nominal"] = copy.deepcopy(h2_base)
    hists[f"qqqq_w2_bkg"] = copy.deepcopy(h2_bkg)
    hists[f"qqqq_w2_nominal_massShift50MeVUp"] = copy.deepcopy(h2_up)
    hists[f"qqqq_w2_nominal_massShift50MeVDown"] = copy.deepcopy(h2_dw)
    fIn.Close()


    # write hists to a datacard.root
    fOut = ROOT.TFile(f"{outDir}/datacard_qqqq.root", "RECREATE")
    for h in hists:
        hists[h].SetName(h)
        hists[h].Write()
    fOut.Close()

    # make datacard
    dc = ""
    dc += f"imax *\n"
    dc += f"jmax *\n"
    dc += f"kmax *\n"
    dc += f"####################\n"
    dc += f"shapes *        * datacard_qqqq.root $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n"
    dc += f"shapes data_obs * datacard_qqqq.root $CHANNEL_nominal\n"
    dc += f"####################\n"
    dc += f"bin                      qqqq_w1   qqqq_w2\n"
    dc += f"observation              -1        -1\n"
    dc += f"####################\n"
    dc += f"bin                      qqqq_w1   qqqq_w2    qqqq_w1   qqqq_w2\n"
    dc += f"process                  nominal   nominal    bkg       bkg\n"
    dc += f"process                  1         1          2         2\n"
    dc += f"rate                     -1        -1         -1        -1\n"
    dc += f"####################\n"
    #dc += "dummy lnN                1.001    1.0001\n" # 0.1 % normalization uncertainty 
    dc += f"massShift50MeV shapeNoConstraint  1   1       -         -\n" # uncertainty on the w mass, free floating

    f = open(f"{outDir}/datacard_qqqq.txt", 'w')
    f.write(dc)
    f.close()

    print(dc)




if __name__ == "__main__":
    fName = "output_wmass_kinematic.root"
    outDir = f"combine/wmass_kinematic/" # directory must exist
    procName = "yfsww_ee_ww_noBES_ecm163"
    bkgName = "p8_ee_Z_noBES_ecm163"

    semileptonic("enuqq_dijet_m", "enu")
    semileptonic("munuqq_dijet_m", "munu")
    hadronic("qqqq_w1_m", "qqqq_w2_m")

