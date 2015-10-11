# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 16:02:32 2015

@author: architgupta
"""

import sqlite3 
import pandas as pd
import math
conn = sqlite3.connect('renewable.db') # create a "connection"
c = conn.cursor() # link a connection
location = pd.read_sql_query("SELECT * FROM location;",conn) #assign database "location" and "ports" to pandas data frame
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
    box_capacity = 500 # Considersing total capacity of box 
    boxes = math.ceil(produc/box_capacity) #calculating total no. of boxes
    cost_per_box_per_km = 10 # Calculating cost per box per km.
    return dist*cost_per_box_per_km*boxes # cost


#creating empty lists 
cost_list_full=[]
cost_list_port_full=[]
min_cost_port=[]
index_min_cost_port=[]

total_production = sum(location.production) # calculating total production. considering no damage

for i in range(0,len(location.long)): #creating a for to go through all the locations
    cost_list=[]
    cost_list_port=[]    
    
    for j in range(0,len(location.long)):# creating another for to go through all the locations
      d=dist(location.lat[i], location.long[i], location.lat[j], location.long[j])# calculating distance between location i and j
      
      cost_list.append(cost(d, location.production[j]))# calculating cost for each location i and j
      
    cost_list_full.append(cost_list) #calculating fulll cost and appending it to another list
    
    for k in range(0,len(ports.long)):# creating a for loop to go through all the ports
        
      d_port=dist(location.lat[i], location.long[i], ports.lat[k], ports.long[k])# loc i and port k
      
      cost_list_port.append(cost(d_port, total_production)) #calculating all the cost of moving from i to k
      
    cost_list_port_full.append(cost_list_port) # creating list and putting all the list in to it
    
    min_cost_port.append(min(cost_list_port_full[i])) # getting minimum cost at port
    
    index_min_cost_port.append(cost_list_port_full[i].index(min(cost_list_port_full[i])))# getting minimumal index for each location

sum_cost=[]

for i in range(0,len(location.long)):    
    sum_cost.append(sum(cost_list_full[i])) #Summing up all the cost:moving all the production to single location
    
final_cost=[]    
for i in range(0,len(location.long)):     
    final_cost.append(sum_cost[i]+min_cost_port[i]) # final cost by adding sum of all the cost cost to the minimum cost of the port

min_location = final_cost.index(min(final_cost))   # min location with mini cost of list
min_port_location = index_min_cost_port[min_location] # min index for the port
print "location:",min_location,"port:",min_port_location 


    git add assingnment--.py
    git commit -m "First version - Nocomments