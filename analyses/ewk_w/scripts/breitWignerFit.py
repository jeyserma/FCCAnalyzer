
import ROOT

ROOT.gROOT.SetBatch()

def rel_bwFunc(x, par):
    #return par[0] * ROOT.TMath.BreitWignerRelativistic(x[0], par[1], par[2])
    return par[0] * ROOT.TMath.BreitWigner(x[0], par[1], par[2])
if __name__ == "__main__":
    
    fIn = ROOT.TFile("output_wmass_kinematic.root")
    h = fIn.Get("yfsww_ee_ww_noBES_ecm163/w_plus_m") # p8_ee_WW_ecm240 yfsww_ee_ww_noBES_ecm163
    xMin, xMax = 70, 80
    
    #rel_bwFunc = ROOT.TF1("rel_bwFunc", "[0]*((0.5*[1]) / (TMath::Pi()*TMath::Max(1.e-20, (x-[2])*(x-[2]) + 0.25*[1]*[1])))", xMin, xMax)
    #rel_bwFunc = ROOT.TF1("rel_bwFunc", "[0] / ((x**2 - [1]**2)**2 + [1]**2 * [2]**2)", xMin, xMax)
    #rel_bwFunc.SetParameters(h.Integral(), 80., 2.)  # Amplitude, mean, width
    rel_bwTF1 = ROOT.TF1("rel_bwTF1", rel_bwFunc, xMin, xMax, 3)
    rel_bwTF1.SetParameters(h.Integral(), 80.379, 2.085)  # Amplitude, mean, width
    rel_bwTF1.FixParameter(1, 80.379);
    #rel_bwTF1.FixParameter(2, 2.085);
    #h.GetXaxis().SetRangeUser(82, 90)
    h.Fit("rel_bwTF1", "R")
    
    canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)
    h.Draw()
    rel_bwTF1.Draw("same")
    
    canvas.SaveAs("/home/submit/jaeyserm/public_html/fccee/bw.png")