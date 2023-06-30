"""
Declares the indicators used from the Oxford dataset and their categorical value range.
If you change this file, make sure also to update the 'legend' directory, which
contains the descriptions for indicators (important for the frontend).
"""

import numpy as np
from types import SimpleNamespace as ns

indicators = [ 
    
    ns( name = "c6m_stay_at_home_requirements", range = np.arange( 4. )), 
    ns( name = "c8ev_internationaltravel", range = np.arange( 5. )), 
    ns( name = "h6m_facial_coverings", range = np.arange( 5. )), 
    ns( name = "c4m_restrictions_on_gatherings", range = np.arange( 5. )) 
]