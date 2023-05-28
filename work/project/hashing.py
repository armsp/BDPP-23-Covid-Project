from hashlib import md5
import pickle
import importlib
import inspect

def md5_hash( x ):
    
    return md5( x.encode( "utf-8" ) if type( x ) is str else pickle.dumps( x )).hexdigest( )[ :7 ]

def code_hash_by_name( name ):
    
    return md5_hash( importlib.util.find_spec( name ).loader.get_source( name ))

def hash_deps( * deps ):
    
    hash_v = ""
    
    for dep in [ * deps, __name__ ]:
        
        hash_v = md5_hash( hash_v + code_hash_by_name( dep ))
        
    return hash_v
        
