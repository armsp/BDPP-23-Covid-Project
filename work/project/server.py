"""
warning: autogenerated by writefile2. do not edit!
"""


"""
serve the implementation of this project over http.
client side files are contained in the 'static' directory.
for prediction, the server automatically (but also imperfectly) 
detects the necessary prediction start index. debugging for this algrithm is provided 
in the cumsum.png and cumsum_diff.png files. communication is realized
over websockets. data is transmitted as a dict of csvs per column.
"""


from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from io import StringIO
import os
import pandas as pd
import numpy as np
import require
import functools
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import nodes

categorical_to_dummy = require.single( "categorical_to_dummy" )
crop_to_valid_range = require.single( "crop_to_valid_range" )

app = Flask( __name__, static_folder = "static", static_url_path = '' )
socketio = SocketIO(app)

@functools.cache
def load_data( country ):

    log( f"loading data for { country }" )
    return nodes.find( "data_for_country" ).get_result( country, categorical_as_dummy = False )

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@functools.cache
def read_legend( column ):

    with open( f'legend/{ column }', "r" ) as file: 
        
        text = file.read( )

    data = {}
    lines = text.strip().split('\n')
    for line in lines:
        if '-' in line:
            key, value = line.split('-', 1)  # 1 is the maxsplit parameter.
            data[key.strip()] = value.strip()
    return data
    

@socketio.event
def get_columns( ):
    
    outcomes = require.single( "owid_outcomes" )
    n_outcomes = len( outcomes )
    owid_measures = require.single( "owid_measures" )
    n_numerical = n_outcomes + len( owid_measures )
    indicators = require.single( "indicators" )

    columns = [ * outcomes, * owid_measures, * [ i.name for i in indicators ]]
    assert columns == load_data( "Germany" ).columns.tolist( )
    
    return [ dict( 
        name = name, 
        is_measure = i >= n_outcomes,
        is_categorical = i >= n_numerical,
        n_categories = len( indicators[ i - n_numerical ].range ) if i >= n_numerical else 0,
        legend = read_legend( name ) if i >= n_numerical else { }) for i, name in enumerate( columns )]

@socketio.event
def get_countries( ):
    
    return require.single( "countries_with_hospitalization_data" )

@socketio.event
def get_methods( ):
    
    return [ "belief_ensemble", "honest_forward" ]

@socketio.event
@functools.cache
def get_data( country ):

    df = load_data( country ).copy( )
    fill_df( df )
    return df_to_csvs( df )

def df_to_csvs( df ):

    def to_csv( s ):

        s.name = "close"
        return s.to_csv( )

    return { c: to_csv( df[ c ]) for c in df.columns }

def csvs_to_df( csvs ):

    df = pd.DataFrame( )
    for col in csvs:

        parsed = pd.read_csv(StringIO(csvs[ col ]), index_col = "date", parse_dates = True, low_memory = False )
        df[ col ] = parsed[ "close" ]
        df.index = parsed.index

    return df



@functools.cache
def train_model( method ):

    log( f"training { method }" )
    
    if method == "belief_ensemble":

        train_ensemble_node = require.single( "train_ensemble" )
        return train_ensemble_node.get_result( )

    if method == "honest_forward":

        return nodes.find( "train_honest_forward" ).get_result( )

def find_first_different_index( df1, df2 ):

    scaler = MinMaxScaler( )
    scaler.fit( df1 )
    df1 = pd.DataFrame( scaler.transform( df1 ), columns = df1.columns )
    df2 = pd.DataFrame( scaler.transform( df2 ), columns = df2.columns )
    
    # create a dataframe of True/False values
    diff = ( df1 - df2 ).abs( ).to_numpy( )
    cumsum = diff.sum( axis = 1 ).cumsum( )
    cumsum_diff = np.pad(np.diff( cumsum ), (0, 1), 'constant') 
    changed_too_much = ( cumsum > 10 )
    
    # Find the first index where they differ too much
    first_diff_index = changed_too_much.argmax( ) if changed_too_much.any( ) else None

    plt.clf( )
    plt.plot( cumsum )
    
    if first_diff_index:
        
        plt.axvline( x = first_diff_index, color = "r" )
        
    plt.savefig( "cumsum.png" )

    plt.clf( )
    plt.plot( cumsum_diff )

    if first_diff_index:
        
        plt.axvline( x = first_diff_index, color = "r" )
        
    plt.savefig( "cumsum_diff.png" )

    if first_diff_index:
        
        log( f"change detected at index { first_diff_index }" )
        
    return first_diff_index

def fill_df( df ):

    df.fillna( axis = 0, method = "ffill", inplace = True )
    df.fillna( axis = 0, method = "bfill", inplace = True )
    assert not df.isna( ).any( ).any( )

last_sent_message = None

def prediction_callback( progress ):

    global last_sent_message
    message = f"prediction progress { int( progress * 100 )}%"

    if last_sent_message != message:

        log( message )
        last_sent_message = message

@socketio.event
def predict( args ):

    csvs, country, method = args
    
    df = categorical_to_dummy( csvs_to_df( csvs ))
    assert not df.isna( ).any( ).any( )
        
    reference = categorical_to_dummy( csvs_to_df( get_data( country )))
    assert not reference.isna( ).any( ).any( )
    assert df.columns.tolist( ) == reference.columns.tolist( )
    
    log( f"{ method } making predictions..." )
    model = train_model( method )
    start = find_first_different_index( df, reference )

    # no prediction necessary
    if start is None:

        log( "nothing to be done" )
        return [ df_to_csvs( df ), None ]

    else:

        df_pred = model.predict_replace( df, start = start, callback = prediction_callback )
        assert df_pred.shape == df.shape
        assert df_pred.columns.tolist( ) == reference.columns.tolist( )
        assert not df_pred.isna( ).any( ).any( )
        
        log( "done" )
        return [ df_to_csvs( df_pred ), str( start )]

def log( * args ):

    print( * args )
    socketio.emit( "log", * args )
    socketio.sleep( 0 ) #force immediate send

def main( ):

    # preheat
    for m in get_methods( ):
        
        train_model( m )
    
    load_data( "Germany" )
    
    try:

        log( "running..." )
        log( "http://localhost:8080" )
        socketio.run( app, port = 8080, host = "0.0.0.0" )    

    except:
        
        print( "done." )

if "is_server" in os.environ:

    main( )
    
