"""
warning: autogenerated by writefile2. do not edit!
source: crop_to_valid_range_h.ipynb
"""


"""
extract the range from the first non-nan (inclusive) to the first again nan (exclusive).
this is a heuristic to get a mostly-valid data range for a country data frame, so
we can train our models on them.
also used to discard/warn for countries which have no usable data (e.g. entire column is nan)
"""

import require
import numpy as np
from IPython.display import display, HTML
verbose = require.untracked.single( "verbose" )

def get_valid_range( df ):
    
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

    if verbose( ) >= 2:

        display( HTML( f"<h3>valid intervals (exclusive)</h3>" ))

        for i in range( d ):

            display( HTML( f"<p>{ df.columns[ i ]} <b>{ start_per_column[ i ]}:{ last_per_column[ i ] + 1 }</b></p>" ))
    
    start = start_per_column.max( )
    end = last_per_column.min( ) + 1

    assert start != inf and end != -inf, "your data is completely unusable, see verbose = 2 for more info"

    if verbose( ) >= 1:

        display( HTML( f"<p>all-valid interval (exclusive) <b>{ start }:{ end }</b></p>" ))
        display( HTML( f"<p>you retain <b>{ 100 * ( end - start ) / n :.1f}%</b> of your data</p>" ))

    return slice( start, end )
