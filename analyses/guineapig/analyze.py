import sys,os,re,glob
import ROOT
import numpy as np


if __name__ == "__main__":

    files = glob.glob("/data/submit/cms/store/fccee/guineapig/FullSim_IDEA/*.root")

    ch = ROOT.TChain("events")
    for f in files: ch.Add(f)

    #ch.Print()

    pairs_theta = ROOT.TH1D("pairs_theta", "", 100, 0, 4)
    pairs_phi = ROOT.TH1D("pairs_phi", "", 200, -4, 4)
    pairs_r_vs_z = ROOT.TH2D("pairs_r_vs_z", "", 400, -0.1, 0.1, 100, -0.1, 0.1)


    x_min, x_max = 1e-3, 1
    y_min, y_max = 1e-4, 10
    num_x_bins = 100
    num_y_bins = 100

    # Generate logarithmically spaced bin edges
    x_bins = np.logspace(np.log10(x_min), np.log10(x_max), num_x_bins + 1)
    y_bins = np.logspace(np.log10(y_min), np.log10(y_max), num_y_bins + 1)

    pairs_theta_pt = ROOT.TH2D("theta_pt", "", num_x_bins, x_bins, num_y_bins, y_bins)


    for iEv in range(0, ch.GetEntries()):
        print(iEv)
        ch.GetEntry(iEv)
        mc_particles = getattr(ch, "MCParticles")

        for iP, mc_p in enumerate(mc_particles):
            if abs(mc_p.PDG) != 11:
                continue

            mcp = mc_particles[iP]
            print(mc_particles[iP].vertex.x, mc_particles[iP].momentum.x)
            #db = mc_particles[iP].daughters_begin
            #de = mc_particles[iP].daughters_end
            #print(mc_p.PDG, db, de, mc_particles[daughters[db].index].PDG, mc_particles[daughters[de].index].PDG)
            


        

        continue
        for iP in range(0, nPairs):
            x = pairs.at(iP).vertex.x*1e-9
            y = pairs.at(iP).vertex.y*1e-9
            z = pairs.at(iP).vertex.z*1e-9
            px = pairs.at(iP).momentum.x
            py = pairs.at(iP).momentum.y
            pz = pairs.at(iP).momentum.z
            mass = pairs.at(iP).mass
            
            v = ROOT.TVector3(x, y, z)
            p = ROOT.Math.PxPyPzMVector(px, py, px, mass)
            #print(x, y, z)
            #print(v.Phi())
            pairs_theta.Fill(v.Theta())
            pairs_phi.Fill(v.Phi())
            pairs_r_vs_z.Fill(z, v.Mag() if y > 0 else -v.Mag())
            print(v.Theta(), p.Theta())
            pairs_theta_pt.Fill(v.Theta(), p.Pt())

        #print(len(pairs))
        #pairs_x = pairs.vertex.x
    
    
    # save output histograms
    fOut = ROOT.TFile("output_pairs.root", "RECREATE")
    pairs_theta.Write()
    pairs_phi.Write()
    pairs_r_vs_z.Write()
    pairs_theta_pt.Write()
    fOut.Close()


    c = ROOT.TCanvas("c", "", 800, 800)
    pairs_theta_pt.Draw("COLZ")
    c.SetLogx()
    c.SetLogy()
    c.SaveAs("/home/submit/jaeyserm/public_html/fccee/test.png")