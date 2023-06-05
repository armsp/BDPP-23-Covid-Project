"""
warning: autogenerated by writefile2. do not edit!
"""


import numpy as np
import pandas as pd
from IPython.display import display, HTML

def crop_to_valid_range( df, verbose = 1 ):

    if verbose == False:

        verbose = 0
    
    # find valid time range for this dataframe
    n, d = df.shape
    index_per_series = np.indices(( n, ), dtype = int ).T @ np.ones(( 1, d ), dtype = int )
    inf = np.iinfo( np.int64 ).max
    
    #for each column, get lowest non-nan index
    index_or_inf = np.ma.masked_array( index_per_series, mask = np.isnan( df.to_numpy( ))).filled( inf )
    start_per_column = index_or_inf.min( axis = 0 )
    
    #for each column, get highest non-nan index
    index_or_minus_inf = np.ma.masked_array( index_per_series, mask = np.isnan( df.to_numpy( ))).filled( - inf )
    last_per_column = index_or_minus_inf.max( axis = 0 )

    if verbose >= 2:

        display( HTML( f"<h3>valid intervals (exclusive)</h3>" ))

        for i in range( d ):

            display( HTML( f"<p>{ df.columns[ i ]} <b>{ start_per_column[ i ]}:{ last_per_column[ i ] + 1 }</b></p>" ))
    
    start = start_per_column.max( )
    end = last_per_column.min( ) + 1

    assert start != inf and end != -inf, "your data is completely unusable, see verbose = 2 for more info"

    if verbose >= 1:

        display( HTML( f"<p>all-valid interval (exclusive) <b>{ start }:{ end }</b></p>" ))
        display( HTML( f"<p>you retain <b>{ 100 * ( end - start ) / n :.1f}%</b> of your data</p>" ))

    df = df.iloc[ start: end, : ]
    
    # Check if DataFrame has any NaN values
    for col, sum in df.isna( ).sum( ).items( ):

        if sum > 0:

            if verbose >= 1:
                
                display( HTML( f"<p>warning '{ col }' has { sum } nan(s). performed forward fill.</p>" ))

    df = pd.DataFrame.fillna( df, axis = 0, method = "ffill" )
    assert not df.isna( ).any( ).any( )
    
    return df