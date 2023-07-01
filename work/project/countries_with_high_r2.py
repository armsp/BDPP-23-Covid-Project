"""
countries which produced an acceptable (positive) per-time-series r2 score in the train set.
if a country is in the train set and produces a negative r2 score, we consider it harmful for the model.
this was tested on the honest_forward model with n_estimators = 100, max_depth = 20, max_features = 1.0,length_l = 100, lag = 50
trained on 80% of the dataset: list( set( owid_countries ).intersection( oxford_countries ).difference( broken_countries ))
"""

countries_with_high_r2 = [

 'Albania',
 'Andorra',
 'Argentina',
 'Austria',
 'Belgium',
 'Belize',
 'Bosnia and Herzegovina',
 'Brazil',
 'Bulgaria',
 'Colombia',
 'Croatia',
 'Chile',
 'Ecuador',
 'Estonia',
 'Finland',
 'France',
 'Georgia',
 'Germany',
 'Hungary',
 'Italy',
 'Kosovo',
 'Liechtenstein',
 'Luxembourg',
 'Malta',
 'Mexico',
 'Netherlands',
 'Paraguay',
 'Uruguay'
 'Peru',
 'Poland',
 'Portugal',
 'Romania',
 'Slovenia',
 'Sweden',
 'Trinidad and Tobago',
 'Ukraine',
 'United States',
 'Latvia',
 'Lithuania',
 'Moldova',
 'Serbia',
 'Switzerland',
 'Panama',
 'Spain',
 'United Kingdom',
 'Greece'
 ]