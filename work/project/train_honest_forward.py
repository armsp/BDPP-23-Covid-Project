"""
warning: autogenerated by writefile2. do not edit!
"""


"""
trains a single weak learner.
cache node wrapper around honest_forward.py and train_weak_learner.py that caches the trained model
"""

import nodes
import require

@nodes.generic_node
def train_honest_forward( 
    
        subset = slice( None ), 
        n_estimators = 100,
        max_depth = 20,
        max_features = 1.0,
        n_jobs = -1,
        length_l = 100,
        lag = 50
    ):

    import numpy as np
    model = require.single( "honest_forward" )
    
    def main( weak_learner_node: nodes.find( "train_weak_learner" ).given( 
            
            subset = subset, 
            length_l = length_l, 
            lag = lag, 
            length_r = 1, 
            linear_operator = np.identity( 1 ),
            type = "forest",
            learner_kwargs = dict( n_estimators = n_estimators, max_depth = max_depth, max_features = max_features, n_jobs = n_jobs )
        )):

        m = model( )
        learner = weak_learner_node.result

        theory = ""
        theory += "\n### General\n"
        theory += f"""This model learns a function between two lagged sliding windows via a random forest 
        of ${ n_estimators }$ trees each with a maximum depth of ${ max_depth }$ and a feature ratio of 
        ${ int( max_features * 100 )}\\%$. Prediction is performed in an iterative forward fashion 
        (hence the name *honest*): the target dataframe on which we predict is only used for the necessary 
        burn-in period of the left window, the rest is predicted on its own prior output. This property makes it
        easy to validate against out-of-sample time series."""
        theory += "\n### Training dimensions\n"
        theory += learner.theory_info
        theory += f"In this case the linear operator corresponds to $M=I_{{1,1}}$, the $1 \\times 1$ identity matrix."
            
        m.__dict__.update( learner = learner, info = dict( table = learner.info_dict, theory = theory ))
        return m

    return main

node = train_honest_forward
