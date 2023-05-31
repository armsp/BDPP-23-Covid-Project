"""
warning: autogenerated by writefile2. do not edit!
"""

from types import SimpleNamespace as ns
import numpy as np
import pandas as pd
from IPython.display import display, Markdown as md
import require
display_dict = require.single( "display_dict" )

def train_weak_learner( dataframes, length_l = 1, lag = 0, length_r = 1, linear_operator = None, verbose = True ):

    if linear_operator is None:

        linear_operator = np.ones(( 1, length_r )) / length_r
    
    # number of outcomes
    n_outcomes = 3
    
    #number of time series
    d = dataframes[ 0 ].shape[ 1 ]

    def get_n_samples( df ):

        return df.shape[ 0 ] - length_r + 1 - lag - length_r

    n_samples_total = sum([ get_n_samples( df ) for df in dataframes ])

    if verbose:

        display( HTML( f"<h1>Weak Learner Training</h1>" ))
        display( HTML( f"<h3>Parameters</h3>" ))
        
        display_dict({
            
            "number of dataframes": len( dataframes ),
            ** { f"samples from dataframe { i }": get_n_samples( dataframes[ i ]) for i in range( len( dataframes ))},
            "total number of samples": n_samples_total,
            "number of time series": d,
            "number of outcome series": n_outcomes,
            "length of left/predictor window": length_l, 
            "lag/spacing between windows": lag, 
            "length of right/response window": length_r,
            "shape of linear operator M": linear_operator.shape,
        })
    
    for i, df in enumerate( dataframes ):

        assert get_n_samples( df ) >= 1, f"dataframe { df } at index { i } is too short"    

    assert linear_operator.shape[ 1 ] == length_r, f"linear_operator of shape { linear_operator.shape } cannot be applied to a window of shape { length_r, n_outcomes }"

    def get_patch( df, i, length_l, lag, length_r ):

        # number of outcomes
        n_outcomes = 3 
        
        left = df.iloc[ i : i + length_l, : ]
        right = df.iloc[ i + length_l + lag : i + length_l + lag + length_r, :n_outcomes ] # assume outcomes are the first columns
        
        assert ( length_l, d ) == left.shape, f"got { left.shape } but expected { length_l, d }"
        assert ( length_r, n_outcomes ) == right.shape, f"got { right.shape } but expected { length_r, n_outcomes }"
        return left, right
    
    L = np.zeros(( n_samples_total, length_l, d ))
    R = np.zeros(( n_samples_total, length_r, n_outcomes ))

    start_index = 0
    for df in dataframes:

        n_samples = get_n_samples( df )
        
        for t in range( n_samples ):
    
            L[ start_index + t ], R[ start_index + t ] = get_patch( df, t, length_l, lag, length_r )

        # offset for next data frame
        start_index += n_samples

    X = L.reshape( L.shape[ 0 ], -1, order = "C" )
    Z = R.reshape( R.shape[ 0 ], -1, order = "C" )
    M = np.kron( linear_operator, np.identity( n_outcomes ))
    Y = Z @ M.T

    if verbose:

        s = [
            "### Theory\n",
            f"Consider the predictor windows $L \in \mathbb{{R}}^{{{ L.shape }}}$ and response windows $R \in \mathbb{{R}}^{{{ R.shape }}}$.",
            f"Let $X \in \mathbb{{R}}^{{{ X.shape }}}$ be a reshaping of $L$ which is directly passed into the model as predictor sample matrix.",
            f"Let latent response $Z \in \mathbb{{R}}^{{{ Z.shape }}}$ be a reshaping of $R$. As the name suggests, this is not given to the model.",
            f"Instead, the model observes a linear transformation of $Z$: We have $Y \in \mathbb{{R}}^{{{ Y.shape }}}=Z (M \otimes I_{{{ n_outcomes }}})^\\top$.",
            f"This applies the linear operator $M \in \mathbb{{R}}^{{{ linear_operator.shape }}}$ to every outcome time series window.",
            f"Hence, the weak learner learns a function $f: \mathbb{{R}}^{{{ L.shape[ 1: ]}}} \\rightarrow \mathbb{{R}}^{{{( linear_operator.shape[ 0 ], n_outcomes )}}}$,",
            f"where $f(x)=y=Mz$."
        ]
        
        display( md( " ".join( s )))

    def get_weak_learner( X, Y ):

        from sklearn.linear_model import LinearRegression as lm
        return lm( ).fit( X, Y )

    model = get_weak_learner( X, Y )

    def predict( window ):

        assert window.shape == ( length_l, d )
        x = window.reshape( 1, -1, order = "C" )
        assert x.shape == ( 1, length_l * d )
        y = model.predict( x ).squeeze( 0 )
        assert y.shape == ( linear_operator.shape[ 0 ] * n_outcomes, )
        y = y.reshape( linear_operator.shape[ 0 ], n_outcomes )
        return y

    # avoid excessive memory usage
    del dataframes, L, R, X, Z, M, Y

    return ns( 
    
        predict = predict, 
        length_l = length_l, 
        lag = lag,
        length_r = length_r,
        linear_operator = linear_operator
    )