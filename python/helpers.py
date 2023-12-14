    
import ROOT

def defineCutFlowVars(df):

    for i in range(0, 20):
        df = df.Define("cut%d"%i, "%d"%i)
    return df
    

class TMVAHelper():

    def __init__(self, model_input, model_name, variables):
    
        self.variables = variables
        self.nvars = len(self.variables)
        self.model_input = model_input
        self.model_name = model_name
        self.nthreads = ROOT.GetThreadPoolSize() 
        
        self.tmva_helper = ROOT.FCCAnalyses.tmva_helper(self.model_input, self.model_name, self.nvars, self.nthreads)
        self.var_col = f"tmva_vars_{self.model_name}"
    
    def run_inference(self, df, col_name = "mva_score"):
    
        # check if columns exist
        cols = df.GetColumnNames()
        for var in self.variables:
            if not var in cols:
                raise Exception(f"Variable {var} not defined in dataframe.")
        
        vars_str = ', '.join(self.variables)
        df = df.Define(self.var_col, f"ROOT::VecOps::RVec<float>{{{vars_str}}}")
        df = df.Define(col_name, self.tmva_helper, [self.var_col])
        return df



class JetClusteringHelper():
    
    def __init__(self, arg_radius, arg_exclusive, arg_cut, arg_sorted, arg_recombination, arg_exponent):
        self.clustering_helper = ROOT.FCCAnalyses.clustering_helper(arg_radius, arg_exclusive, arg_cut, arg_sorted, arg_recombination, arg_exponent, ROOT.GetThreadPoolSize())

    def run_clustering(self, df, input_col_name="pseudo_jets", output_col_name="clustered_jets"):
        df = df.Define(output_col_name, self.clustering_helper, [input_col_name])
        return df