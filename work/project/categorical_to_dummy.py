import require
indicators = require.single( "indicators" )

def categorical_to_dummy( df ):

    df = df.copy( )

    for indicator in indicators:

        nnz_values = indicator.range[ 1: ]

        for v in nnz_values:

            df[ f"{ indicator.name }=={ v }" ] = ( df[ indicator.name ] == v ).astype( int )

        df.drop( indicator.name, axis = 1, inplace = True )
                
    return df