"""Script used to calculate projected water needs for different population growth scenarios"""

# required packages
import pandas as pd
import numpy as np

# conversion factors
millions = 1000000
billions = 1000000000

# import historical water data
water_data = pd.read_csv("water_data.csv", 
                         index_col = 0)

# get water data from natural sources
water_data['natural_prod'] = water_data.iloc[:,[3,4,5,8,9]].sum(axis=1)

# get treated wastewater
water_data['tww'] = water_data.iloc[:,[6,10]].sum(axis=1)

# focus on last 10 years
recent_water_data=water_data[-11:]

# calculate average per capita use based on last 10 years
total_per_cap = np.mean(recent_water_data.Total_Consump*millions/recent_water_data.Population)
domstic_per_cap = np.mean(recent_water_data.Domestic*millions/recent_water_data.Population)
total_natural = np.mean(recent_water_data.natural_prod)*millions
tww_dom_ratio = np.mean(recent_water_data.tww/recent_water_data.Domestic)

# create new dataframes for different growth scenarios
columns = ['population',
           'total_demand', 
           'domestic', 
           'natural', 
           'tww',
           'desal',
           'total_supply']
new_index=np.arange(2021, 2066)

low_growth = pd.DataFrame(index=new_index,
                          columns = columns,
                          dtype=object)

med_growth = pd.DataFrame(index=new_index,
                          columns = columns,
                          dtype=object)

high_growth = pd.DataFrame(index=new_index,
                          columns = columns,
                          dtype=object)

# add future population
future_df = pd.read_csv("future_populations.csv", index_col=0)
future_df=future_df.loc[2021:2066]

low_growth['population'] = future_df.low_pop
med_growth['population'] = future_df.med_pop
high_growth['population'] = future_df.high_pop

# rate of decline for natural production
nat_decline = np.linspace(1, 0.8, len(new_index))
    
# calculate demand and expected desal capacity
scenarios = [low_growth, med_growth, high_growth]

for scen in scenarios:
    # demand
    scen['total_demand'] = scen['population']*total_per_cap
    scen['domestic'] = scen['population']*domstic_per_cap
    
    
    # supply
    scen['natural'] = total_natural*nat_decline
    scen['tww'] = scen['domestic']*tww_dom_ratio
    scen['desal'] = scen['total_demand'] - scen['natural'] - scen['tww']
    
    scen['new_desal'] = scen.desal.diff()/millions
    scen['plants'] = np.floor(scen['desal']/(millions*100))
    


        
        
    
    

    


