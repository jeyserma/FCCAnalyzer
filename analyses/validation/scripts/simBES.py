

import ROOT
import math
import random

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)



# Box–Muller transform

bes = 0.001
ecm = 91.2e0
m_PI = 3.14259265

h1 = ROOT.TH1D("h1", "", 1000, 44.5, 46.5)
h2 = ROOT.TH1D("h2", "", 1000, 44.5, 46.5)

for i in range(0, 10000):
    
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)

    E1    = ecm/2.
    E2    = ecm/2.
    '''
    corho = 0
    x1 = math.sqrt(-2.*math.log(r1)) * math.cos(2.*m_PI*r2)
    x2 = math.sqrt(-2.*math.log(r1)) * math.sin(2.*m_PI*r2)
    y1 = x1
    y2 = corho * x1 + math.sqrt(1.-corho*corho) * x2
    rr1= y1 * bes
    rr2= y2 * bes
    rr1= bes
    rr2= bes
    Ebeam1 = E1 * (1.0 + y1 * rr1)
    Ebeam2 = E2 * (1.0 + y2 * rr2)
    
    #print(Ebeam1, Ebeam2)
    '''
    Ebeam1 = random.gauss(E1, bes*E1)

    h1.Fill(Ebeam1)
    #h2.Fill(Ebeam2)


canvas = ROOT.TCanvas("", "", 600, 600)



h1.Draw("HIST")
h1.Fit("gaus")

myfunc = h1.GetFunction("gaus")
myfunc.Draw("L SAME")

canvas.SaveAs("/eos/user/j/jaeyserm/www/FCCee/testBES.png")

