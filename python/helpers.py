    
import ROOT

def defineCutFlowVars(df):

    for i in range(0, 20):
        df = df.Define("cut%d"%i, "%d"%i)
    return df
    


class JetClusteringHelper():
    
    def __init__(self, arg_radius, arg_exclusive, arg_cut, arg_sorted, arg_recombination, arg_exponent):
        self.clustering_helper = ROOT.FCCAnalyses.clustering_helper(arg_radius, arg_exclusive, arg_cut, arg_sorted, arg_recombination, arg_exponent, ROOT.GetThreadPoolSize())

    def run_clustering(self, df, input_col_name="pseudo_jets", output_col_name="clustered_jets"):
        df = df.Define(output_col_name, self.clustering_helper, [input_col_name])
        return df