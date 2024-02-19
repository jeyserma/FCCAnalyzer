import sys
import json
import functions
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.EnableThreadSafety()

"""
this configuration file contains the:
- list of flavors to be considered
- reconstruction sequence stored as two dicts: definition and alias
- the list of variables used in the tagger as well as their range for validation plotting
"""

## name of collections in EDM root files
collections = {
    "GenParticles": "Particle",
    "PFParticles": "ReconstructedParticles",
    "PFTracks": "EFlowTrack",
    "PFPhotons": "EFlowPhoton",
    "PFNeutralHadrons": "EFlowNeutralHadron",
    "TrackState": "EFlowTrack_1",
    "TrackerHits": "TrackerHits",
    "CalorimeterHits": "CalorimeterHits",
    "dNdx": "EFlowTrack_2",
    "PathLength": "EFlowTrack_L",
    "Bz": "magFieldBz",
}

#### list of flavors f = g, q, c, s, ...(will look for input file name ccontaining "[Hff]")
flavors = ["g", "q", "s", "c", "b", "tau"]

class JetFlavourHelper:
    def __init__(self, jet, jetc, tag=""):

        self.jet = jet
        self.const = jetc

        self.tag = tag
        if tag != "":
            self.tag = "_{}".format(tag)

        self.particle = collections["GenParticles"]
        self.pfcand = collections["PFParticles"]
        self.pftrack = collections["PFTracks"]
        self.pfphoton = collections["PFPhotons"]
        self.pfnh = collections["PFNeutralHadrons"]
        self.trackstate = collections["TrackState"]
        self.trackerhits = collections["TrackerHits"]
        self.calohits = collections["CalorimeterHits"]
        self.dndx = collections["dNdx"]
        self.l = collections["PathLength"]
        self.bz = collections["Bz"]

        self.definition = dict()

        # ===== VERTEX
        # MC primary vertex
        self.definition["pv{}".format(self.tag)] = "FCCAnalyses::MCParticle::get_EventPrimaryVertexP4()( {} )".format(
            self.particle
        )

        # build jet constituents lists
        self.definition["pfcand_isMu{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_isMu({})".format(self.const)
        self.definition["pfcand_isEl{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_isEl({})".format(self.const)
        self.definition["pfcand_isChargedHad{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_isChargedHad({})".format(
            self.const
        )
        self.definition["pfcand_isGamma{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_isGamma({})".format(
            self.const
        )
        self.definition["pfcand_isNeutralHad{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_isNeutralHad({})".format(
            self.const
        )

        # kinematics, displacement, PID
        self.definition["pfcand_e{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_e({})".format(self.const)
        self.definition["pfcand_p{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_p({})".format(self.const)
        self.definition["pfcand_theta{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_theta({})".format(self.const)
        self.definition["pfcand_phi{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_phi({})".format(self.const)
        self.definition["pfcand_charge{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_charge({})".format(self.const)
        self.definition["pfcand_type{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_type({})".format(self.const)
        self.definition["pfcand_erel{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_erel_cluster({}, {})".format(
            jet, self.const
        )

        self.definition[
            "pfcand_erel_log{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_erel_log_cluster({}, {})".format(jet, self.const)

        self.definition[
            "pfcand_thetarel{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_thetarel_cluster({}, {})".format(jet, self.const)

        self.definition["pfcand_phirel{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_phirel_cluster({}, {})".format(
            jet, self.const
        )

        self.definition[
            "pfcand_dndx{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_dndx({}, {}, {}, pfcand_isChargedHad{})".format(
            self.const, self.dndx, self.pftrack, self.tag
        )

        self.definition[
            "pfcand_mtof{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_mtof({}, {}, {}, {}, {}, {}, {}, pv{})".format(
            self.const, self.l, self.pftrack, self.trackerhits, self.pfphoton, self.pfnh, self.calohits, self.tag
        )

        self.definition["Bz{}".format(self.tag)] = "{}[0]".format(self.bz)

        self.definition[
            "pfcand_dxy{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::XPtoPar_dxy({}, {}, pv{}, Bz{})".format(
            self.const, self.trackstate, self.tag, self.tag
        )

        self.definition["pfcand_dz{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::XPtoPar_dz({}, {}, pv{}, Bz{})".format(
            self.const, self.trackstate, self.tag, self.tag
        )

        self.definition[
            "pfcand_phi0{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::XPtoPar_phi({}, {}, pv{}, Bz{})".format(
            self.const, self.trackstate, self.tag, self.tag
        )

        self.definition["pfcand_C{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::XPtoPar_C({}, {}, Bz{})".format(
            self.const, self.trackstate, self.tag
        )

        self.definition["pfcand_ct{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::XPtoPar_ct({}, {}, Bz{})".format(
            self.const, self.trackstate, self.tag
        )

        self.definition["pfcand_dptdpt{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_omega_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dxydxy{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_d0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dzdz{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_z0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dphidphi{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_phi0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition[
            "pfcand_detadeta{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_tanlambda_cov({}, {})".format(self.const, self.trackstate)

        self.definition["pfcand_dxydz{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_d0_z0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dphidxy{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_phi0_d0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_phidz{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_phi0_z0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition[
            "pfcand_phictgtheta{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_tanlambda_phi0_cov({}, {})".format(self.const, self.trackstate)

        self.definition[
            "pfcand_dxyctgtheta{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_tanlambda_d0_cov({}, {})".format(self.const, self.trackstate)

        self.definition[
            "pfcand_dlambdadz{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_tanlambda_z0_cov({}, {})".format(self.const, self.trackstate)

        self.definition[
            "pfcand_cctgtheta{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_omega_tanlambda_cov({}, {})".format(self.const, self.trackstate)

        self.definition["pfcand_phic{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_omega_phi0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_dxyc{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_omega_d0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition["pfcand_cdz{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::get_omega_z0_cov({}, {})".format(
            self.const, self.trackstate
        )

        self.definition[
            "pfcand_btagSip2dVal{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_Sip2dVal_clusterV({}, pfcand_dxy{}, pfcand_phi0{}, Bz{})".format(
            jet, self.tag, self.tag, self.tag
        )

        self.definition[
            "pfcand_btagSip2dSig{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_Sip2dSig(pfcand_btagSip2dVal{}, pfcand_dxydxy{})".format(self.tag, self.tag)

        self.definition[
            "pfcand_btagSip3dVal{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_Sip3dVal_clusterV({}, pfcand_dxy{}, pfcand_dz{}, pfcand_phi0{}, Bz{})".format(
            jet, self.tag, self.tag, self.tag, self.tag
        )

        self.definition[
            "pfcand_btagSip3dSig{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_Sip3dSig(pfcand_btagSip3dVal{}, pfcand_dxydxy{}, pfcand_dzdz{})".format(
            self.tag, self.tag, self.tag
        )

        self.definition[
            "pfcand_btagJetDistVal{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_JetDistVal_clusterV({}, {}, pfcand_dxy{}, pfcand_dz{}, pfcand_phi0{}, Bz{})".format(
            jet, self.const, self.tag, self.tag, self.tag, self.tag
        )

        self.definition[
            "pfcand_btagJetDistSig{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::get_JetDistSig(pfcand_btagJetDistVal{}, pfcand_dxydxy{}, pfcand_dzdz{})".format(
            self.tag, self.tag, self.tag
        )

        self.definition["jet_nmu{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::count_type(pfcand_isMu{})".format(
            self.tag
        )
        self.definition["jet_nel{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::count_type(pfcand_isEl{})".format(
            self.tag
        )
        self.definition[
            "jet_nchad{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::count_type(pfcand_isChargedHad{})".format(self.tag)
        self.definition["jet_ngamma{}".format(self.tag)] = "FCCAnalyses::JetConstituentsUtils::count_type(pfcand_isGamma{})".format(
            self.tag
        )
        self.definition[
            "jet_nnhad{}".format(self.tag)
        ] = "FCCAnalyses::JetConstituentsUtils::count_type(pfcand_isNeutralHad{})".format(self.tag)

    def define_and_inference(self, df):

        for var, call in self.definition.items():
            df = df.Define(var, call)

        # run inference and cast scores
        df = df.Define("MVAVec_{}".format(self.tag), self.get_weight_str)

        for i, scorename in enumerate(self.scores):
            df = df.Define(scorename, "FCCAnalyses::JetFlavourUtils::get_weight(MVAVec_{}, {})".format(self.tag, i))

        return df

    def load(self, jsonCfg, onnxCfg):

        ## extract input variables/score name and ordering from json file
        initvars, self.variables, self.scores = [], [], []
        f = open(jsonCfg)
        data = json.load(f)

        for varname in data["pf_features"]["var_names"]:
            initvars.append(varname)
            self.variables.append("{}{}".format(varname, self.tag))

        for varname in data["pf_vectors"]["var_names"]:
            initvars.append(varname)
            self.variables.append("{}{}".format(varname, self.tag))

        for scorename in data["output_names"]:
            # self.scores.append(scorename)
            # self.scores.append(scorename.replace("jet", "jet{}".format(self.tag)))
            self.scores.append("{}{}".format(scorename, self.tag))

        f.close()
        # convert to tuple
        initvars = tuple(initvars)

        # then funcs
        for varname in self.variables:
            matches = [obs for obs in self.definition.keys() if obs == varname]
            if len(matches) != 1:
                print("ERROR: {} variables was not defined.".format(varname))
                sys.exit()

        self.get_weight_str = "FCCAnalyses::JetFlavourUtils::get_weights(rdfslot_, "
        for var in self.variables:
            self.get_weight_str += "{},".format(var)
        self.get_weight_str = "{})".format(self.get_weight_str[:-1])

        weaver = ROOT.FCCAnalyses.JetFlavourUtils.setup_weaver(
            onnxCfg,  # name of the trained model exported
            jsonCfg,  # .json file produced by weaver during training
            initvars,
            ROOT.GetThreadPoolSize() if ROOT.GetThreadPoolSize() > 0 else 1,
        )

    def outputBranches(self):

        out = self.scores
        out += [obs for obs in self.definition.keys() if "jet_" in obs]
        return out