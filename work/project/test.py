import require

get_training_data = require.single( "get_training_data" )
dataframes = get_training_data( )

train_ensemble = require.single( "train_ensemble" )
ensemble = train_ensemble( dataframes[ :-1 ])

import matplotlib.pyplot as plt
predict_replace = require.single( "predict_replace" )

time_range = slice( 0, 1000 )
column = 1
df = dataframes[ 1 ]

df_pred = predict_replace( df, ensemble )
df.iloc[ time_range, column ].plot( color = "blue" )
df_pred.iloc[ time_range, column ].plot( color = "orange" )

line = lambda color, label: plt.Line2D([ ], [ ], color = color, label = label )
h = [ line( "blue", "true" ), line( "orange", "predicted" )]

plt.legend( handles = h )
print( df_pred.columns[ column ])