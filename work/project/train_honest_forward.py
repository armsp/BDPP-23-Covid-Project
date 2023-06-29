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
def train_honest_forward( subset = slice( None )):

    import numpy as np
    model = require.single( "honest_forward" )
    
    def main( weak_learner_node: nodes.find( "train_weak_learner" ).given( 
            
            subset = subset, 
            length_l = 100, 
            lag = 50, 
            length_r = 1, 
            linear_operator = np.identity( 1 ),
            type = "forest",
            learner_kwargs = dict( max_depth = 2, max_features = 1.0, n_jobs = 1, n_estimators = 1 )
        )):

        m = model( )
        learner = weak_learner_node.result
        m.__dict__.update( learner = learner, info = dict( table = learner.info_dict, theory = learner.theory_info ))
        return m

    return main

node = train_honest_forward
