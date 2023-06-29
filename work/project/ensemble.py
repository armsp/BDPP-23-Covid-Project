"""
warning: autogenerated by writefile2. do not edit!
source: train_ensemble_h.ipynb
"""


"""
train a belief ensemble of weak learners.
beliefs are combined by manually selected weight in a least-squares sense.
this model is not an honest/forward model in the sense that it modifies the original
data rather than predicting it (counterfactual). validation must be inferred
from the weak learners, as the predict_replace method works on the unseen
data that would be passed in for validation. it is possible to have
a forward-predicting version of this belief ensemble, but since the weak learners 
vary in structure (window lengths and lag), the implementation is rather involved.
"""

import numpy as np
from IPython.display import display, HTML
from types import SimpleNamespace as ns
from tqdm import tqdm
import sys
import require
train_weak_learner = require.single( "train_weak_learner" )
verbose = require.untracked.single( "verbose" )
n_outcomes = len( require.single( "owid_outcomes" ))

class ensemble:

    def train( self, train_set ):

        if verbose( ):

            display( HTML( f"<h1>Ensemble Training</h1>" ))
        
        def first_last( l ):
    
            M = np.zeros(( 2, l ))
            M[ 0, 0 ] = 1
            M[ 1, l - 1 ] = 1
            return M
        
        def mean( l ):
    
            return np.ones(( 1, l )) / l
    
        def gradient( l ):
        
            grad = np.zeros(( l, l ))
            #grad[ np.arange( l - 1 ) + 1, ( np.arange( l - 1 )) % l ] = -1 # for left diagonal
            grad[ np.arange( l ), np.arange( l )] = -1
            grad[ np.arange( l - 1 ), ( np.arange( l - 1 ) + 1 ) % l ] = 1
            return grad
        
        ensemble = [ ]
        length_r = 100
        
        learner = train_weak_learner( train_set, length_l = length_r, lag = 50, length_r = length_r, linear_operator = mean( length_r ) @ gradient( length_r ) @ gradient( length_r ))    
        ensemble.append( learner )
        
        learner = train_weak_learner( train_set, length_l = length_r, lag = 50, length_r = length_r, linear_operator = mean( length_r ) @ gradient( length_r ))    
        ensemble.append( learner )
    
        self.__dict__.update( ensemble = ensemble )

    def predict_replace( self, df, start = None, length = None, callback = None ):

        callback = ( lambda * _: None ) if callback is None else callback
        ensemble = self.ensemble
        # for predicted time range
        
        min_start = max([ l.length_l + l.lag for l in ensemble ])
        min_length = max([ l.length_r for l in ensemble ])
        
        start = min_start if start is None else start
        start = max( start, min_start )
        length = df.shape[ 0 ] - start if length is None else length
        assert length >= min_length
        assert start + length <= df.shape[ 0 ]
        
        lhs_chunks = [ ]
        rhs_chunks = [ ]
        weight_chunks = [ ]

        n_predictions_total = sum([ 1 + length - learner.length_r for learner in ensemble ])
        n_predictions_done = 0
        
        for learner in tqdm( ensemble, file = sys.stdout, desc = "training ensemble" ):
        
            n_predictions = 1 + length - learner.length_r
            M = learner.linear_operator
            n_rows_total = M.shape[ 0 ] * n_predictions
            lag = learner.lag
        
            for i in range( n_predictions ):
        
                chunk = np.zeros(( M.shape[ 0 ], length ))
                chunk[ :, i : i + M.shape[ 1 ]] = M
                lhs_chunks.append( chunk )
        
                window = df.iloc[ start - lag - learner.length_l + i: start - lag + i, : ].to_numpy( )
                y = learner.predict( window )
                rhs_chunks.append( y )
        
                # each weak learner is now regarded equally important, independent of total rows occupied
                # otherwise learners with smaller windows and larger operators are favoured
                weight_chunks.append( np.ones( M.shape[ 0 ], ) * ( learner.weight / n_rows_total ))

                n_predictions_done += 1
                callback( n_predictions_done / n_predictions_total )
    
        lhs = np.concatenate( lhs_chunks, axis = 0 )
        rhs = np.concatenate( rhs_chunks, axis = 0 )
        weight = np.concatenate( weight_chunks, axis = 0 )
        
        lhs = np.diag( weight ) @ lhs
        rhs = np.diag( weight ) @ rhs
        
        assert lhs.shape == ( rhs.shape[ 0 ], length )
    
        if verbose( ):
        
            print( f"lhs shape = { lhs.shape }" )
            print( f"lhs rank = { np.linalg.matrix_rank( lhs )}" )
            print( f"degrees of freedom = { length }" )
    
        prediction, *_ = np.linalg.lstsq( lhs, rhs, rcond = None )
    
        df_pred = df.copy( )
        df_pred.iloc[ start : start + length, :n_outcomes ] = prediction
    
        return df_pred
