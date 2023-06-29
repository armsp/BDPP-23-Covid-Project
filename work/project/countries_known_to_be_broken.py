"""
these are manually filtered (by visual inspection) using the training_data_h.ipynb notebook.

reasons for making it into this list include:
 - missing outcomes
 - no or very little testing data
 - sketchy/ erroneuous looking data (extreme spikes, gaps, plateaus, discontinous data)

note: some of these countries could be recovered merely by smoothing

hospitalization data is NOT considered a requirement to stay off this list.
there is a separate file listing all the countries that have sufficient hospitalilization data:
countries_with_hospitalization_data.py

"""

countries_known_to_be_broken = [

   "Macao",
   "Turkmenistan",
   "Burundi",
   "Tajikistan",
   "Taiwan",
   "South Sudan",
   "Oman",
   "Venezuela",
   "Kiribati",
   "Greenland",
   "Qatar",
   "Monaco",
   "Brunei",
   "Bermuda",
   "Hong Kong",
   "Central African Republic",
   "Burkina Faso",
   "Lesotho",
   "Guinea",
   "Gambia",
   "Barbados",
   "Syria",
   "Congo",
   "San Marino",
   "Yemen",
   "Honduras",
   "Egypt",
   "Gabon",
   "Sudan",
   "Benin",
   "Liberia",
   "Eswatini",
   "Djibouti",
   "Somalia",
   "Papua New Guinea",
   "Libya",
   "Grenada",
   "Faroe Islands"
   "Chile",
   "Niger",
   "Nicaragua",
   "Comoros",
   "Angola",
   "Algeria",
   "Dominica",
   "Eritrea",
   "Mauritius",
   "Aruba",
   "Tonga",
   "Sierra Leone",
   "Vanuatu",
   "Singapore",
   "Uzbekistan",
   "Mali",
   "Chad",
   "Seychelles",
   "Solomon Islands",
   "Lebanon",
   "Guam",
   "Tanzania",
   "Cape Verde",
   "Afghanistan"

]