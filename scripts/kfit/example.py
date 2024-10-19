import ROOT
from ROOT import TH1F, TFile,TLorentzVector, TLorentzRotation, TVector3, TProfile2D, TCanvas
from sympy import *
import numpy as np
from numpy.linalg import multi_dot, inv
import random
from math import sqrt, sin, cos, pi
from kfit import KinematicFit
ROOT.gROOT.SetBatch(True)

"""
- generate e+ e- -> Z H , H -> f f events
- smear energy to simulate Higgs decay product energy measurment
- perform kinematic fit to improve energy measurements using single constrain on the energy sum of decay products
"""

#_______________________________________________________________________________
""" various global definitions """
debug = True
debug = False

mh = 125.
mz = 91.18800354003906
mf = 0.#  fermion mass to be assumed for the H -> f fbar decay

sqrt_s = 240.
s = sqrt_s**2

l = (1 - mh**2/s - mz**2/s)**2 - (4*mh**2 * mz**2)/s**2
norm = l**2 * pi / 2 + 8 * mz**2 / s

Eh = 0.5 * (s + mh**2 - mz**2) / sqrt_s
Ez = sqrt_s - Eh

ph_mag = sqrt(Eh**2 - mh**2)
pz_mag = sqrt(Ez**2 - mz**2)

# energy resolution
sigmaOverE = 0.05

#_______________________________________________________________________________
""" generate random theta according to e+ e- -> Z H matrix element """
def sample_theta():
    while True:
        theta = random.uniform(0., pi)
        f_theta = 1/norm * l **2 * sin(theta) ** 2 + 8 * mz**2 / s
        y = random.random()
        if y<f_theta:
            return theta

#_______________________________________________________________________________
""" generate pseudo (e+ e- -> Z H , H -> f fbar) Montecarlo event """
def generate_event():

    # generate Higgs kinematics in lab frame
    theta = sample_theta()
    phi = random.uniform(0., 2*pi)
    ph_vec = ph_mag * TVector3( sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta))
    ph = TLorentzVector(ph_vec, Eh)

    # generate H-> f fbar in the Higgs rest frame
    theta_star = random.uniform(0., pi)
    phi_star = random.uniform(0., 2*pi)
    p1_star_vec = mh/2. * TVector3( sin(theta_star)*cos(phi_star), sin(theta_star)*sin(phi_star), cos(theta_star))
    p2_star_vec = - p1_star_vec
    e1_star = sqrt(p1_star_vec.Mag()**2 + mf**2)
    e2_star = e1_star
    p1_star = TLorentzVector(p1_star_vec, e1_star)
    p2_star = TLorentzVector(p2_star_vec, e2_star)

    # boost back in the lab frame
    boost_vec = (1./Eh ) * ph_vec
    ltr = TLorentzRotation(boost_vec)
    p1 = p1_star.Transform(ltr)
    p2 = p2_star.Transform(ltr)

    return p1, p2
#_______________________________________________________________________________
""" recompute 4-vector after energy update """
def updated_4vector(smeared_energy, p_in):
    scale = 1.
    if smeared_energy > p_in.M():
        scale = sqrt(smeared_energy**2 - p_in.M()**2) / p_in.Vect().Mag()
    p_reco_vec = scale * p_in.Vect()
    p_reco = TLorentzVector(p_reco_vec, smeared_energy)
    return p_reco

#_______________________________________________________________________________
""" recompute 4-vector after energy update """
def fill_covmatrix(covmatrix, histo):
    histo.Fill( 1., 0., covmatrix[0][0])
    histo.Fill( 0., 1., covmatrix[1][1])
    histo.Fill( 1., 1., covmatrix[0][1])
    histo.Fill( 0., 0., covmatrix[1][0])

#_______________________________________________________________________________
def main():

    """ histogram definition """
    nbins, lo, hi = 100, -5, 5
    hpull_e1 = TH1F('hpull_e1', 'hpull_e1', nbins, lo, hi)
    hpull_e2 = TH1F('hpull_e2', 'hpull_e2', nbins, lo, hi)

    nbins, lo, hi = 100, 100., 150
    hmass_before = TH1F('hmass_before', 'hmass_before', nbins, lo, hi)
    hmass_after = TH1F('hmass_after', 'hmass_after', nbins, lo, hi)

    hcov_before = TProfile2D('hcov_before', 'hcov_before', 2, -0.5, 1.5, 2, -0.5, 1.5)
    hcov_after = TProfile2D('hcov_after', 'hcov_after', 2, -0.5, 1.5, 2, -0.5, 1.5)

    hcovnorm_before = TProfile2D('hcovnorm_before', 'hcovnorm_before', 2, -0.5, 1.5, 2, -0.5, 1.5)
    hcovnorm_after = TProfile2D('hcovnorm_after', 'hcovnorm_after', 2, -0.5, 1.5, 2, -0.5, 1.5)

    """ define variables symbols """
    e1, e2 = symbols('e1 e2')
    variables = (e1, e2)

    """ define constraints here """
    constraints = []
    cnstr1 = e1 + e2 - Eh
    # cnstr2 = e1**2 + e2**3 - Eh
    # cnstr3 = ...
    constraints.append(cnstr1)
    # constraints.append(cnstr2)

    """ declare kinematic fit object """
    kin_fit = KinematicFit(variables, constraints)

    maxloops=100
    maxDeltaChiSq = 1.e-06
    weight = 1. # use weight = 1 when linear constraints
    options = (maxloops, maxDeltaChiSq, weight)

    ## event loop here
    for iev in range(100):
        print(iev)
        ## simulate Higgs decay kinematics
        p1_gen, p2_gen = generate_event()

        e1_gen = p1_gen.E()
        e2_gen = p2_gen.E()
        m_gen = (p1_gen + p2_gen).M()

        sigma1 = sigmaOverE * e1_gen
        sigma2 = sigmaOverE * e2_gen

        e1_reco = random.gauss(e1_gen, sigma1)
        e2_reco = random.gauss(e2_gen, sigma2)

        p1_reco = updated_4vector(e1_reco, p1_gen)
        p2_reco = updated_4vector(e2_reco, p2_gen)

        ## fill in parameters
        a0 = np.array([[e1_reco],
                      [e2_reco]])

        # and covariance matrix
        Va0 = np.array([[sigma1**2, 1.e-6],
                        [1.e-6, sigma2**2]])

        options = (maxloops, maxDeltaChiSq, weight)
        (a, Va, maxchisq, niter) = kin_fit.results(a0, Va0, options)
        #print(a, Va, maxchisq, niter)

        e1_fit = a[0][0]
        e2_fit = a[1][0]

        p1_fit = updated_4vector(e1_fit, p1_reco)
        p2_fit = updated_4vector(e2_fit, p2_reco)

        sigma1_post = sqrt(Va[0][0])
        sigma2_post = sqrt(Va[1][1])

        # fill histograms

        hpull_e1.Fill((e1_fit - e1_reco)/sqrt(sigma1**2 - sigma1_post**2))
        hpull_e2.Fill((e2_fit - e2_reco)/sqrt(sigma2**2 - sigma2_post**2))

        hmass_before.Fill( (p1_reco + p2_reco).M() )
        hmass_after.Fill( (p1_fit + p2_fit).M() )

        #print(e1_reco + e2_reco, e1_fit + e2_fit, e1_gen + e2_gen)

        Va0_norm = np.array([[sigma1**2 / e1_gen**2, 1.e-6],
                             [1.e-6, sigma2**2 / e2_gen**2]])

        Va_norm = np.array([[ Va[0][0]/e1_fit**2, Va[0][1]/(e1_fit*e2_fit)],
                             [Va[0][1]/(e2_fit*e1_fit), Va[1][1]/e2_fit**2]])

        fill_covmatrix(Va0, hcov_before)
        fill_covmatrix(Va0_norm, hcovnorm_before)
        fill_covmatrix(Va, hcov_after)
        fill_covmatrix(Va_norm, hcovnorm_after)

    out_root = TFile("output.root","RECREATE")
    hpull_e1.Write()
    hpull_e2.Write()
    hmass_before.Write()
    hmass_after.Write()
    hcov_before.Write()
    hcovnorm_before.Write()
    hcov_after.Write()
    hcovnorm_after.Write()

    quit()
    # Show resulting histograms
    cnv1 = TCanvas("pulls", "pulls", 50, 50, 800, 400)
    cnv1.Divide(2, 1)
    cnv1.cd(1)
    #ROOT.gStyle.SetOptStat(0)
    hpull_e1.Draw()
    cnv1.cd(2)
    #ROOT.gStyle.SetOptStat(0)
    hpull_e2.Draw()
    cnv1.Print("example_simple_pulls.png", "png")

    cnv2 = TCanvas("covariance matrix", "covariance matrix", 50, 50, 800, 400)
    cnv2.Divide(2, 1)
    cnv2.cd(1)
    #ROOT.gStyle.SetOptStat(0)
    hcovnorm_before.Draw("TEXT")
    cnv2.cd(2)
    #ROOT.gStyle.SetOptStat(0)
    hcovnorm_after.Draw("TEXT")
    cnv2.Print("example_simple_cov.png", "png")


    cnv3 = TCanvas("invariant mass", "invariant mass", 50, 50, 400, 400)
    ROOT.gStyle.SetOptStat(0)
    hmass_after.SetLineWidth(2)
    hmass_after.SetLineColor(ROOT.kRed)
    hmass_after.Draw()
    hmass_before.SetLineWidth(2)
    hmass_before.Draw("same")
    cnv3.Print("example_simple_mass.png", "png")

    input()

#_______________________________________________________________________________
if __name__ == "__main__":
    main()