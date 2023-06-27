"""
warning: autogenerated by writefile2. do not edit!
source: data_for_country_h.ipynb
"""


import pandas as pd
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import numpy as np
from types import SimpleNamespace as ns
import math
import require
get_oxford_categorical_flagged = require.single( "get_oxford_categorical_flagged" )
categorical_to_dummy = require.single( "categorical_to_dummy" )
indicators = require.single( "indicators" )
verbose = require.untracked.single( "verbose" )
owid_outcomes = require.single( "owid_outcomes" )
owid_measures = require.single( "owid_measures" )

def compute_data_for_country( country, categorical_as_dummy = True ):

    def plot_all( df, columns = None ):

        if columns is None:

            columns = df.columns

        n_cols = min( 4, len( columns ))
        n_rows = math.ceil( len( columns ) / 4 )
        fig, axs = plt.subplots( n_rows, n_cols, figsize = ( 4 * n_cols, 4 * n_rows ))

        if len( columns ) > 1:
        
            axs = axs.ravel( )
            
        fig.subplots_adjust( hspace = 0.5 )
        
        for i, c in enumerate( columns ):
        
            df[ c ].plot( title = c.replace( '_', ' ' ), ax = axs[ i ])

        #remove unwanted grid cells
        if n_rows > 1:

            for ax in axs[ -(( n_cols * n_rows ) - len( columns )) : ]:

                ax.remove( )

        plt.show( )
    
    if verbose( ):

        display( HTML( f"<h1>{ country }</h1>" ))
    
    df = pd.read_csv( "data/owid-covid-data.csv", index_col = "date", parse_dates = True, low_memory = False )
    df = df[ df.location == country ]

    # outcomes

    columns = owid_outcomes
    outcome_df = df[ columns ].copy( )

    for c in columns:

        pass
        #outcome_df[ np.isnan( outcome_df[ c ])] = 0

    if verbose( ):

        display( HTML( f"<h3>outcomes</h3>" ))
        plot_all( outcome_df )

    # OWID measures

    columns = owid_measures
    measure_df = df[ columns ].copy( )

    for c in columns:

        measure_df[ c ][ np.isnan( measure_df[ c ])] = 0

    # Oxford measures

    series_per_indicator = { indicator.name: get_oxford_categorical_flagged( country, indicator.name, verbose = False ) for indicator in indicators }

    for indicator in indicators:

        date_offset = 2 # oxford data starts 2 days earlier, just discard it
        measure_df[ indicator.name ] = series_per_indicator[ indicator.name ][ date_offset: ]

    if categorical_as_dummy:

        measure_df = categorical_to_dummy( measure_df )

    if verbose( ):

        url = "https://github.com/OxCGRT/covid-policy-tracker/blob/master/documentation/codebook.md#containment-and-closure-policies"
        display( HTML( f"<h3>measures</h3><p><a href={ url }>see here</a> for an explanation of categorical values</p>" ))
        plot_all( measure_df )

    full_df = pd.concat([ outcome_df, measure_df ], axis = 1 )
    return full_df
