import numpy as np
from types import SimpleNamespace as ns

indicators = [ 
    
    ns( name = "c6m_stay_at_home_requirements", range = np.arange( 4. )), 
    ns( name = "c8ev_internationaltravel", range = np.arange( 5. )), 
    ns( name = "h6m_facial_coverings", range = np.arange( 5. )), 
    ns( name = "c4m_restrictions_on_gatherings", range = np.arange( 5. )) 
]