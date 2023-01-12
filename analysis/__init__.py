
import sys
import ROOT
import pathlib

ROOT.gROOT.SetBatch()
ROOT.gInterpreter.ProcessLine(".O3")
sys.path.insert(0, "analysis/datasets/")

# load fcc libraries
print ("Load default cxx analyzers ... ")
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

# load c++ macros
ROOT.gInterpreter.ProcessLine(".O3")
ROOT.gInterpreter.AddIncludePath(f"{pathlib.Path(__file__).parent}/include/")
ROOT.gInterpreter.Declare('#include "defines.h"')
ROOT.gInterpreter.Declare('#include "utils.h"')
ROOT.gInterpreter.Declare('#include "gen.h"')
ROOT.gInterpreter.Declare('#include "zh_mass_xsec.h"')
ROOT.gInterpreter.Declare('#include "zh_mass_xsec_gen.h"')
ROOT.gInterpreter.Declare('#include "photon.h"')
ROOT.gInterpreter.Declare('#include "z_xsec.h"')
ROOT.gInterpreter.Declare('#include "xsec_example.h"')