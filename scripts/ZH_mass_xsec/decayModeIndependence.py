
import ROOT


if __name__ == "__main__":
    
    # p8_ee_ZH_ecm240 wzp6_ee_mumuH_ecm240
    cuts = ["_cut0", "_cut1", "_cut2", "_cut3", "_cut4", ""]
    cuts = ["_cut0", "_cut1", "_cut2", "_cut3", "_cut4", "_cut5", "_cut6", "_cut7", "_cut8", ""]
    decay_pdgids = [4, 5, 13, 15, 21, 22, 23, 24]
    decay_names = ["cc", "bb", "mumu", "tautau", "gluon", "gamma", "Z", "W"]
    fIn = ROOT.TFile("output.root")
    
    #
    print("Branching ratios")
    for pdg in decay_names: print("%s\t" % pdg, end=" ")
    print()
    for cut in cuts:
        h = fIn.Get("wzp6_ee_mumuH_ecm240/higgs_decay%s" % cut)
        y = h.Integral()
        #y = h.GetBinContent(15+1)
        for pdg in decay_pdgids:
            print("%.3f\t" % (h.GetBinContent(pdg+1)*100./y), end=" ")
        print()


    print("")
    print("Selection efficiencies")
    print("\t", end=" ")
    for pdg in decay_names: print("%s\t" % pdg, end=" ")
    print()
    for cut in cuts:
        print("%s\t" % cut, end=" ")
        h_ref = fIn.Get("wzp6_ee_mumuH_ecm240/higgs_decay%s" % cuts[0])
        h = fIn.Get("wzp6_ee_mumuH_ecm240/higgs_decay%s" % cut)
        for pdg in decay_pdgids:
            print("%.3f\t" % (h.GetBinContent(pdg+1)*100./h_ref.GetBinContent(pdg+1)), end=" ")
        print()
    
    fIn.Close()