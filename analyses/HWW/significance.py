

import ROOT


fIn = ROOT.TFile("output_HWW.root")


h_ww = fIn.Get("p8_ee_WW_ecm240/muons_from_w_p_min")
h_zz = fIn.Get("p8_ee_ZZ_ecm240/muons_from_w_p_min")
h_sig = fIn.Get("wzp6_ee_nunuH_HWW_ecm240/muons_from_w_p_min")


h_ww.Add(h_zz)



for i in range(1, 30):

    h_sig.SetBinContent(i-1, 0)
    h_ww.SetBinContent(i-1, 0)

    if h_sig.GetBinContent(i) + h_ww.GetBinContent(i) <= 0:
        continue
    significance = h_sig.Integral() / (h_sig.Integral() + h_ww.Integral())**0.5
    
    print(h_sig.GetBinCenter(i), h_sig.GetBinContent(i),  h_ww.GetBinContent(i), significance)