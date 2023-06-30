"""
warning: autogenerated by writefile2. do not edit!
"""

"""
train a weak learner using given right/left window lengths and lag.
for learning a (rank-deficient) linear function of the right window use the linear operator.
the weak learner can be a linear model or a random forest.
trigger this node with verbose settings to see some diagnostic and theory output in LaTeX.
"""

import nodes
import require

@nodes.store_in_tmp
@nodes.generic_node
def train_weak_learner( 

        subset = slice( None ), 
        length_l = 1, 
        lag = 0, 
        length_r = 1, 
        linear_operator = None, 
        weight = 1, 
        type = "lm",
        learner_kwargs = { }
    ):

    import numpy as np
    import pandas as pd
    from IPython.display import display, HTML, Markdown as md
    from tqdm import tqdm
    import sys
    from types import SimpleNamespace as ns
    import os
    import math
        
    weak_learner = require.single( "weak_learner" )
    get_number_of_window_samples = require.single( "get_number_of_window_samples" )
    display_dict = require.untracked.single( "display_dict" )
    verbose = require.untracked.single( "verbose" )
    n_outcomes = len( require.single( "owid_outcomes" ))

    if linear_operator is None:

        #average
        linear_operator = np.ones(( 1, length_r )) / length_r
    
    patch_args = dict( 

        subset = subset,
        length_l = length_l, 
        lag = lag, 
        length_r = length_r, 
        linear_operator = linear_operator 
    )
    
    def main( 
        
            patches_node: nodes.find( "window_patches" ).given( ** patch_args ),
            training_data_node: nodes.find( "training_data" ).given( )
        ):

        self = weak_learner( )
        X = patches_node.result.X
        Y = patches_node.result.Y
        
        dataframes = training_data_node.result[ subset ] #currently simple slice indexing

        #number of time series
        d = dataframes[ 0 ].shape[ 1 ]
        get_n_samples = lambda df: get_number_of_window_samples( df, length_l, lag, length_r )
        n_samples_total = sum([ get_n_samples( df ) for df in dataframes ])

        print( "training..." )
            
        if type == "lm":
            
            from sklearn.linear_model import LinearRegression as lm
            return lm( ** learner_kwargs ).fit( X, Y )

        if type == "forest":

            from sklearn.ensemble import RandomForestRegressor as rf

            kwargs = learner_kwargs
            args = ns( ** kwargs )
            
            if not hasattr( args, "n_jobs" ): 
                
                args.n_jobs = 1
            
            if args.n_jobs < 0:

                args.n_jobs = os.cpu_count( ) + 1 + args.n_jobs

            if not hasattr( args, "n_estimators" ):

                args.n_estimators = 100

            n_estimators = args.n_estimators
            n_jobs = args.n_jobs
            kwargs = args.__dict__
            print( kwargs )
            model = rf( warm_start = True, oob_score = True, ** kwargs )
            
            n_steps = int( math.ceil( n_estimators / n_jobs ))
            for i in tqdm( range( n_steps ), file = sys.stdout, desc = "training estimators" ):

                model.set_params( n_estimators = n_jobs * ( i + 1 ), oob_score = i == n_steps - 1 )
                model.fit( X, Y )    

        print( "done" )
            
        info_dict = {
                
            "number of dataframes": len( dataframes ),
            ** { f"samples from dataframe { i }": get_n_samples( dataframes[ i ]) for i in range( len( dataframes ))},
            "total number of samples": n_samples_total,
            "number of time series": d,
            "number of outcome series": n_outcomes,
            "length of left/predictor window": length_l, 
            "lag/spacing between windows": lag, 
            "length of right/response window": length_r,
            "shape of linear operator M": linear_operator.shape,
            "least squares weight": weight,
            "score": model.oob_score_,
            "score type": "r2",
            ** kwargs
        }
            
        if verbose( ):
    
            display( HTML( f"<h1>Weak Learner Training</h1>" ))
            display( HTML( f"<h3>Parameters</h3>" ))
            display_dict( info_dict )
            display( HTML( f"<h3>Theory</h3>" ))
            display( md( patches_node.result.info ))            
    
        self.__dict__.update( 

            model = model,
            length_l = length_l, 
            lag = lag,
            length_r = length_r,
            linear_operator = linear_operator,
            weight = weight,
            d = d,
            n_outcomes = n_outcomes,
            theory_info = patches_node.result.info,
            info_dict = info_dict
        )

        return self

    return main

node = train_weak_learner
