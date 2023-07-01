import nodes

subset = dict( 

    random_state = 22, 
    shuffle = True, 
    test_size = 0.2, 
    train_size = 0.8
)

model = nodes.find( "train_honest_forward" ).given( 
    
    subset = { ** subset, "type": "train_split" }, 
    length_l = 100,
    lag = 50,
    n_estimators = 100, 
    max_depth = 20,
    max_features = 1.0,
    n_jobs = -1
)

top_level_nodes = [ model ]