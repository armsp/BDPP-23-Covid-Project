import pickle
import os
import json
import time
from types import SimpleNamespace as namespace
import shutil
from hashing import hash_deps, md5_hash

def create_cache( cache_dir, version = None, alt_get_file_name = None ):
    
    cache_log_file = f"{ cache_dir }/log.jsonl"
    cache_version_file = f"{ cache_dir }/version.txt"
    prev_version = None
    
    if os.path.exists( cache_version_file ):
        
        with open( cache_version_file, "r" ) as file:

            prev_version = file.read( )

    if version:
        
        version = md5_hash( version + hash_deps( __name__ ))
            
    if prev_version is None or version is None or prev_version != version:
        
        if os.path.exists( cache_dir ):
        
            shutil.rmtree( cache_dir )

        os.makedirs( cache_dir )
    
    if version:
        
        with open( cache_version_file, "w" ) as file:

            file.write( version )

    def log( ** kwargs ):

        with open( cache_log_file, "a" ) as file:

            file.write( json.dumps( dict( ** kwargs, time_ms = int( time.time( ) * 1000 ))) + "\n" )
    
    def get_path( suffix ):
        
        return f"{ cache_dir }/{ suffix }"
        
    def get_file_name( key ):
        
        return  f"{ get_path( key )}.pkl"
    
    def get_meta_key( file_rel ):
        
        #must be in the same directory
        dirname = os.path.dirname( file_rel )
        prefix = f"{ dirname }/" if len( dirname ) else ""
        return f"{ prefix }{ md5_hash( file_rel )}"
    
    def is_cached( key ):
        
        is_hit = os.path.exists( get_file_name( key ))
        log( action = "hit" if is_hit else "miss", key = key )
        return is_hit
    
    def is_cached_file( file_rel ):
        
        is_hit = is_cached( get_meta_key( file_rel )) and os.path.exists( get_path( file_rel ))
        log( action = "hit_file" if is_hit else "miss_file", file = file_rel )
        return is_hit
    
    def load( key ):
            
        with open( get_file_name( key ), "rb" ) as file:

            log( action = "load", key = key )
            return pickle.load( file )
        
    def load_file( file_rel ):
        
        log( action = "load_file", file = file_rel )
        return get_path( file_rel )
        
    def save( key, data ):

        os.makedirs( os.path.dirname( get_file_name( key )), exist_ok = True )
        with open( get_file_name( key ), "wb" ) as file:

            log( action = "save", key = key )
            pickle.dump( data, file )
            
    def save_file( file_rel ):
        
        save( get_meta_key( file_rel ), { })
        log( action = "save_file", file = file_rel )
            
    def get( key, get_raw ):
        
        if not is_cached( key ):
            
            save( key, get_raw( ))
            
        return load( key )
    
    def get_file( file_rel, get_raw_file ):
        
        if not is_cached_file( file_rel ):
            
            get_raw_file( )
            save_file( file_rel )
            
        return load_file( file_rel )
    
    def delete_dir( key ):
        
        if os.path.exists( get_path( key )) and os.path.isdir( get_path( key )):
        
            shutil.rmtree( get_path( key ))
            log( action = "delete_dir", key = key )
    
    def delete( key ):
        
        delete_dir( key )
        
        if is_cached( key ):

            os.remove( get_file_name( key ))                    
            log( action = "delete", key = key )
            
    def delete_file( file_rel ):
        
        delete_dir( file_rel )
        
        if is_cached_file( file_rel ):
            
            delete( get_meta_key( file_rel ))
            os.remove( get_path( file_rel ))
            log( action = "delete_file", file = file_rel )
    
    files = namespace( 
        
        get_path = get_path,
        is_cached = is_cached_file,
        load = load_file,
        save = save_file,
        get = get_file,
        delete = delete_file
    )
            
    return namespace( 
        
        is_cached = is_cached,
        load = load,
        save = save,
        get = get,
        delete = delete,
        files = files
    )
