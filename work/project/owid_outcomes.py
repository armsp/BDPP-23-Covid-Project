"""
the columns in OWID (our world in data) that are considered outcomes
"""

#we had to drop this because not enough countries have hospitalization data and estimates would severely overfit to a small number of countries
#owid_outcomes = [ "new_cases_smoothed_per_million", "new_deaths_smoothed_per_million", "weekly_hosp_admissions_per_million" ]

owid_outcomes = [ "new_cases_smoothed_per_million", "new_deaths_smoothed_per_million" ]