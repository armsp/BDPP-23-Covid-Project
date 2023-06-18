"""
warning: autogenerated by writefile2. do not edit!
"""


from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import os
import require
import functools
get_data_for_country = require.single( "get_data_for_country" )

app = Flask( __name__, static_folder = "static", static_url_path = '' )
socketio = SocketIO(app)

@functools.cache
def load_data( country ):

    print( f"loading data for { country }" )
    return get_data_for_country( country, verbose = False, categorical_as_dummy = False )

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@socketio.event
def my_event(json):
    print('received json: ' + str(json))
    return "OK", 200

@socketio.event
def get_outcome_columns( ):
    
    return ['new_cases_smoothed_per_million', 'new_deaths_smoothed_per_million', 'weekly_hosp_admissions_per_million', ]

@socketio.event
def get_measure_columns( ):
    
    return ['new_vaccinations_smoothed_per_million',
       'new_tests_smoothed_per_thousand', 'c6m_stay_at_home_requirements',
       'c8ev_internationaltravel', 'h6m_facial_coverings',
       'c4m_restrictions_on_gatherings']

@socketio.event
def get_columns( ):

    df = load_data( "Germany" )
    return [ dict( 
        name = c, 
        is_measure = i >= 3,
        is_categorical = i >= 3 and not c.startswith( "new" ),
        n_categories = [ 3, 4, 4, 4 ][ i - 5 ] if i >= 3 and not c.startswith( "new" ) else 0 ) for i, c in enumerate( df.columns )]

@socketio.event
def get_countries( ):
    
    return [ "Germany", "Switzerland", "Italy", "France", "Belgium", "United States", "Spain", "United Kingdom", "Malaysia", "South Korea", "Chile" ]

@socketio.event
def get_data( country ):

    def to_csv( s ):

        s.name = "close"
        return s.to_csv( )

    df = load_data( country )
    return { c: to_csv( df[ c ]) for c in df.columns }

def main( ):

    try:

        print( "running..." )
        print( "http://localhost:8080" )
        socketio.run( app, port = 8080, host = "0.0.0.0" )    

    except:
        
        print( "done." )

if "is_server" in os.environ:

    main( )
