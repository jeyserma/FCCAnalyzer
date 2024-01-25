
import sys,array,ROOT,math,os,copy
import argparse
import plotter

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

parser = argparse.ArgumentParser()
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", default="mumu")
args = parser.parse_args()


if __name__ == "__main__":

    if args.flavor == "mumu":
        fIn = ROOT.TFile(f"output_h_mumu.root") # zqq_hmumu_m_mvaCut
        outDir = f"combine/h_mumu/"

        cats = ["zqq", "zee", "zmumu", "znunu"]
        cats = ["zqq"]
        procs_dict = {
            "hmumu"     : ["wzp6_ee_nunuH_Hmumu_ecm240", "wzp6_ee_eeH_Hmumu_ecm240", "wzp6_ee_tautauH_Hmumu_ecm240", "wzp6_ee_ccH_Hmumu_ecm240", "wzp6_ee_bbH_Hmumu_ecm240", "wzp6_ee_qqH_Hmumu_ecm240", "wzp6_ee_ssH_Hmumu_ecm240", "wzp6_ee_mumuH_Hmumu_ecm240"],
            #"ww"        : ["p8_ee_WW_ecm240"], # combine ww with rares
            "zz"        : ["p8_ee_ZZ_ecm240", "p8_ee_ZZ_ecm240_ext"],
            "zg"        : ["wzp6_ee_mumu_ecm240", "wzp6_ee_tautau_ecm240"],
            "rare"      : ["wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gaga_mumu_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240", "p8_ee_WW_ecm240"]
        }
        procs = procs_dict.keys()

        hists = {}
        for cat in cats:
            for proc in procs_dict:
                h = None
                for i,p in enumerate(procs_dict[proc]):
                    h_ = copy.deepcopy(fIn.Get(f"{p}/{cat}_hmumu_m_nOne")) # zqq_mva
                    if h == None: h = h_.Clone()
                    else: h.Add(h_)
                hists[f"{cat}_{proc}"] = copy.deepcopy(h)

        fIn.Close()
        fOut = ROOT.TFile(f"{outDir}/datacard.root", "RECREATE")
        for h in hists:
            hists[h].Rebin(2) # 1 GeV
            if h=="zqq_zz":
                hists[h].Scale(.5)
            #hists[h].Scale(5./7.2)
            hists[h].SetName(h)
            hists[h].Write()
        fOut.Close()
        
        # make datacard
        dc = ""
        dc += "imax *\n"
        dc += "jmax *\n"
        dc += "kmax *\n"
        dc += "####################\n"
        dc += "shapes *        * datacard.root $CHANNEL_$PROCESS\n"
        dc += "shapes data_obs * datacard.root $CHANNEL_hmumu\n"
        dc += "####################\n"
        dc += "bin          {}\n".format('\t'.join(cats))
        dc += "observation  {}\n".format('\t'.join(["-1  "]*len(cats)))
        dc += "####################\n"
        dc += "bin          {}\n".format('\t'.join([ '\t'.join([cat]*len(procs)) for cat in cats]))
        dc += "process      {}\n".format('\t'.join([ '\t'.join(procs) for cat in cats]))
        dc += "process      {}\n".format('\t'.join([ '\t'.join([str(i*(-1))+"  " for i in range(0, len(procs))]) for cat in cats]))
        dc += "rate         {}\n".format('\t'.join(["-1  "]*(len(cats)*len(procs))))
        dc += "####################\n"
        dc += "dummy lnN    {}\n".format('\t'.join(["1.0001"]*(len(cats)*len(procs))))
        #dc += "norm_ww lnN    {}\n".format('\t'.join( [ '\t'.join(["1.2" if p=="ww" else "1.0" for p in procs]) for cat in cats] ))
        #dc += "norm_zz lnN    {}\n".format('\t'.join( [ '\t'.join(["1.2" if p=="zz" else "1.0" for p in procs]) for cat in cats] ))
        #dc += "norm_zg lnN    {}\n".format('\t'.join( [ '\t'.join(["1.2" if p=="zg" else "1.0" for p in procs]) for cat in cats] ))
        #dc += "norm_rare lnN  {}\n".format('\t'.join( [ '\t'.join(["1.2" if p=="rare" else "1.0" for p in procs]) for cat in cats] ))

        f = open(f"{outDir}/datacard.txt", 'w')
        f.write(dc)
        f.close()

        print(dc)



    if args.flavor == "aa":
        fIn = ROOT.TFile(f"output_h_aa_ctp95.root") # zqq_hmumu_m_mvaCut
        outDir = f"combine/h_aa/"

        cats = ["zqq", "zee", "zmumu", "znunu"]
        
        procs_dict = {
            "haa"       : ["wzp6_ee_nunuH_Haa_ecm240", "wzp6_ee_eeH_Haa_ecm240", "wzp6_ee_tautauH_Haa_ecm240", "wzp6_ee_ccH_Haa_ecm240", "wzp6_ee_bbH_Haa_ecm240", "wzp6_ee_qqH_Haa_ecm240", "wzp6_ee_ssH_Haa_ecm240", "wzp6_ee_mumuH_Haa_ecm240"],
            "aa"        : ["wzp6_ee_gammagamma_ecm240", ],
            "qq"        : ["kkmcee_ee_uu_ecm240", "kkmcee_ee_dd_ecm240", "kkmcee_ee_cc_ecm240", "kkmcee_ee_ss_ecm240", "kkmcee_ee_bb_ecm240"],
        }
        procs = procs_dict.keys()

        hists = {}
        for cat in cats:
            for proc in procs_dict:
                h = None
                for i,p in enumerate(procs_dict[proc]):
                    h_ = copy.deepcopy(fIn.Get(f"{p}/{cat}_haa_m"))
                    if h == None: h = h_.Clone()
                    else: h.Add(h_)
                hists[f"{cat}_{proc}"] = copy.deepcopy(h)

        fIn.Close()
        fOut = ROOT.TFile(f"{outDir}/datacard.root", "RECREATE")
        for h in hists:
            hists[h].Rebin(2) # 1 GeV
            #hists[h].Scale(5./7.2)
            hists[h].SetName(h)
            hists[h].Write()
        fOut.Close()
        
        # make datacard
        dc = ""
        dc += "imax *\n"
        dc += "jmax *\n"
        dc += "kmax *\n"
        dc += "####################\n"
        dc += "shapes *        * datacard.root $CHANNEL_$PROCESS\n"
        dc += "shapes data_obs * datacard.root $CHANNEL_haa\n"
        dc += "####################\n"
        dc += "bin          {}\n".format('\t'.join(cats))
        dc += "observation  {}\n".format('\t'.join(["-1  "]*len(cats)))
        dc += "####################\n"
        dc += "bin          {}\n".format('\t'.join([ '\t'.join([cat]*len(procs)) for cat in cats]))
        dc += "process      {}\n".format('\t'.join([ '\t'.join(procs) for cat in cats]))
        dc += "process      {}\n".format('\t'.join([ '\t'.join([str(i*(-1))+"  " for i in range(0, len(procs))]) for cat in cats]))
        dc += "rate         {}\n".format('\t'.join(["-1  "]*(len(cats)*len(procs))))
        dc += "####################\n"
        dc += "dummy lnN    {}\n".format('\t'.join(["1.0001"]*(len(cats)*len(procs))))
        #dc += "norm_ww lnN    {}\n".format('\t'.join( [ '\t'.join(["1.2" if p=="ww" else "1.0" for p in procs]) for cat in cats] ))
        #dc += "norm_zz lnN    {}\n".format('\t'.join( [ '\t'.join(["1.2" if p=="zz" else "1.0" for p in procs]) for cat in cats] ))
        #dc += "norm_zg lnN    {}\n".format('\t'.join( [ '\t'.join(["1.2" if p=="zg" else "1.0" for p in procs]) for cat in cats] ))
        #dc += "norm_rare lnN  {}\n".format('\t'.join( [ '\t'.join(["1.2" if p=="rare" else "1.0" for p in procs]) for cat in cats] ))

        f = open(f"{outDir}/datacard.txt", 'w')
        f.write(dc)
        f.close()

        print(dc)