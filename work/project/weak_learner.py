"""
warning: autogenerated by writefile2. do not edit!
source: train_weak_learner_h.ipynb
"""


"""
simple wrapper around the internal model's predict method with some additional checks
"""

class weak_learner:

    def predict( self, window ):
    
        assert window.shape == ( self.length_l, self.d )
        x = window.reshape( 1, -1, order = "C" )
        assert x.shape == ( 1, self.length_l * self.d )
        y = self.model.predict( x ).squeeze( 0 )
        assert y.shape == ( self.linear_operator.shape[ 0 ] * self.n_outcomes, )
        y = y.reshape( self.linear_operator.shape[ 0 ], self.n_outcomes )
        return y    
