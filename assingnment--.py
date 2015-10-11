# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 16:02:32 2015

@author: architgupta
"""

import sqlite3
import pandas as pd
import math
conn = sqlite3.connect('renewable.db') # create a "connection"
c = conn.cursor()
location = pd.read_sql_query("SELECT * FROM location;",conn)
ports = pd.read_sql_query("SELECT * FROM ports;",conn)

print location
print ports
 
def dist(lat1, long1, lat2, long2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    R = 6378.1 #Radius of the Earth
    return arc*R

def cost(dist , produc): # create a cost function
    box_capacity = 500 
    boxes = math.ceil(produc/box_capacity)
    cost_per_box_per_km = 10
    return dist*cost_per_box_per_km*boxes



cost_list_full=[]
cost_list_port_full=[]
min_cost_port=[]
index_min_cost_port=[]

total_production = sum(location.production)

for i in range(0,len(location.long)):
    cost_list=[]
    cost_list_port=[]    
    
    for j in range(0,len(location.long)):
      d=dist(location.lat[i], location.long[i], location.lat[j], location.long[j])
      
      cost_list.append(cost(d, location.production[j]))
      
    cost_list_full.append(cost_list)
    
    for k in range(0,len(ports.long)):
        
      d_port=dist(location.lat[i], location.long[i], ports.lat[k], ports.long[k])
      
      cost_list_port.append(cost(d_port, total_production))
      
    cost_list_port_full.append(cost_list_port)
    
    min_cost_port.append(min(cost_list_port_full[i]))
    
    index_min_cost_port.append(cost_list_port_full[i].index(min(cost_list_port_full[i])))

sum_cost=[]

for i in range(0,len(location.long)):    
    sum_cost.append(sum(cost_list_full[i]))
    
final_cost=[]    
for i in range(0,len(location.long)):     
    final_cost.append(sum_cost[i]+min_cost_port[i])

min_location = final_cost.index(min(final_cost))    
min_port_location = index_min_cost_port[min_location]   
print "location:",min_location,"port:",min_port_location 


    