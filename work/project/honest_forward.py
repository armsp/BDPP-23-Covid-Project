"""
warning: autogenerated by writefile2. do not edit!
source: train_honest_forward.ipynb
"""


"""
trains a single weak learner. the prediction scheme is an honest forward-prediction
where the sliding window eventually operates on its on predictions after a 
burn-in phase.
"""

import require
import numpy as np
train_weak_learner = require.single( "train_weak_learner" )
n_outcomes = len( require.single( "owid_outcomes" ))

class honest_forward:

    def train( self, train_set ):

        length_r = 1
        learner = train_weak_learner( 
        
            train_set, 
            length_l = 100, 
            lag = 50, 
            length_r = length_r, 
            linear_operator = np.identity( 1 ),
            type = "forest"
        )    
    
        self.__dict__.update( learner = learner )

    def predict_replace( self, df, start = None, length = None, callback = None ):

        callback = ( lambda * _: None ) if callback is None else callback
        learner = self.learner
        
        min_start = learner.length_l + learner.lag
        min_length = learner.length_r
        
        start = min_start if start is None else start
        start = max( start, min_start )
        length = df.shape[ 0 ] - start if length is None else length
        assert length >= min_length
        assert start + length <= df.shape[ 0 ]
        
        n_predictions = 1 + length - learner.length_r
        M = learner.linear_operator
        n_rows_total = M.shape[ 0 ] * n_predictions
        lag = learner.lag

        df_pred = df.copy( )
        df_pred.iloc[ start:, :n_outcomes ] = np.nan
    
        for i in range( n_predictions ):
    
            window = df_pred.iloc[ start - lag - learner.length_l + i: start - lag + i, : ].to_numpy( )
            y = learner.predict( window )
            assert y.shape == ( learner.length_r, n_outcomes )
            df_pred.iloc[ start + i: start + i + learner.length_r, :n_outcomes ] = y
            callback(( i + 1 ) / n_predictions )
    
        return df_pred
