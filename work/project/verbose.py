def level( ):

	with open( "verbose.txt", "r" ) as file:

		return int( file.read( ))

def verbose( ):

	return level( )

def set_level( level ):

	with open( "verbose.txt", "w" ) as file:

		file.write( f"{ level }" )

set_level( 0 )