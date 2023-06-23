"""
warning: autogenerated by writefile2. do not edit!
"""

import require
from tqdm import tqdm
import sys
import nodes
from IPython.display import display, HTML

"""
Note: by cropping here we loose some data (temporally), 
but we use the dataframe for window processing and need NaN-free series
"""

#TODO: can be replaced by cached nodes
compute_data_for_country = require.single( "compute_data_for_country" )
crop_to_valid_range = require.single( "crop_to_valid_range" )
verbose = require.untracked.single( "verbose" )

def compute_training_data( ):

    if verbose( ):

        display( HTML( f"<h1>Training data</h1>" ))
    
    dataframes = [ ]

    countries = [ 
        
        "Germany", 
        "Switzerland", 
        "Italy", 
        "France", 
        "Belgium", 
        "United States", 
        "Spain", 
        "United Kingdom", 
        "Malaysia", 
        "South Korea", 
        "Chile" 
    ]
    
    for country in tqdm( countries, file = sys.stdout, desc = "collecting data" ):

        if verbose( ):
        
            display( HTML( f"<h3>{ country }</h3>" ))

        df = compute_data_for_country( country )
        df = crop_to_valid_range( df ).copy( ) 
        dataframes.append( df )

    return dataframes
        