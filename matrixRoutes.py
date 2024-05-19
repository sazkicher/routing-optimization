"""
Requests matrixcoord to OSRM to get the distance_matrix and JSON maker.

"""

import itertools
import json
from datetime import datetime

import pandas as pd
import requests

from routesStr import routesStr_main


def calculate_distance(route_str):
    
    server = "http://router.project-osrm.org/route/v1/driving/"

    coordexamp = "13.388860,52.517037;13.397634,52.529407;13.428555,52.523219"
    coordinates = route_str
    url = server+coordinates+"?overview=false"
    #print(url)
    response = requests.post(url) 
    distances = []

    try:
        data = response.json()
        legs = data['routes'][0]['legs']
        #print(len(legs))
        
        for distance in range(len(legs)):
            #print(legs[distance]['distance'])
            distances.append(legs[distance]['distance'])
        distances = distances[0::2] # Return only odd distances

    except requests.exceptions.JSONDecodeError as e:
        print(e.args[0])        
      
    #print(distances)
    return distances


def calculate_matrix(ncoords, matrixcoord):
    distance_matrix = []
    counta = 0
    for route_str in matrixcoord:
        counta += 1
        print(f"{counta} of {ncoords}")
        distancex_i = [] 
        for route_substr in route_str:
            distancex = calculate_distance(route_substr)
            distancex_i.append(distancex)
        #print(f"Len str routes{len(route_str[0])}") #Check
        #print(f"str routes {route_str[0]}") #Check
        distance_matrix.append(distancex_i)

    return distance_matrix

def join_matrix(distance_matrix):
    f_distance_matrix=[]
    for elem in distance_matrix:
        joinlist = []
        for i in elem:
            joinlist.extend(i)
        f_distance_matrix.append(joinlist)
    #print(f_distance_matrix)
    return f_distance_matrix 

def insert_site(distance_matrix):
    new_distance_matrix = []
    for route_str in distance_matrix:
        route_str[0] = 0
        new_distance_matrix.append(route_str)
    return new_distance_matrix


def json_maker(ncoords, distance_matrix,  vehicle_cap, adresses, max_distance):
    demands = list(itertools.repeat(1, ncoords))
    demands[0] = 0
    vehicle_capacities = list(itertools.repeat(int(vehicle_cap), ncoords))
    
    json_routes = json.dumps({
        'Addresses' : adresses,
        'distance_matrix' : distance_matrix,
        'demands': demands,
        'vehicle_capacities': vehicle_capacities,
        'num_vehicles': ncoords,
        'depot': 0,
        'max_distance' : int(max_distance)*1000
        })
    #print(f"JSON: {json_routes}")
    return json_routes

def matrixRoutes_main (): 

    ## SITE COORD
    print("Routing WPA Model.")
    while True: 
        site = input("site(cnt/txt/mdn): ")
        if site == "cnt" or site == "txt" or site == "mdn": 
            break 

    while True: 
        vehicle_cap = input("vehicle_capacity: ")
        if vehicle_cap.isdigit(): 
            break 
        
    while True: 
        max_distance = input("max_distance (20-40 km): ")
        if max_distance.isdigit(): 
            break 
    
    now = datetime.now()
    print(f"Start at: {now}")
    sites = {
    "cnt" : '-74.119482000000000,4.684755000000000',
    "txt" : '-74.113022849155100,4.625909598848730',
    "mdn" : '-75.569532084982700,6.219800359800670',
    }

    site_coord = sites[site]
    print(f"Site: {site}, coord: {site_coord}")


    ## CALCULATE DISTANCE MATRIX AGENTS

    # Strings to calculate distance
    ncoords, matrixcoord, adresses = routesStr_main(site_coord) #Given a set of coordinates return that matrix of nxn coordinates 
    #print(f"ncoords: {ncoords}")
    #print(f"matrixcoord: {matrixcoord}")
    
    # Distance matrix chopped by 100
    print("Requesting matrix data information...")
    distance_matrix = calculate_matrix(ncoords, matrixcoord)
    
    # Distance matrix
    distance_matrix = join_matrix(distance_matrix)
    #print(f"Matriz de distancias: {distance_matrix}")

    # Insert
    distance_matrix = insert_site(distance_matrix)


    #JSON maker
    json_routes =  json_maker(ncoords, distance_matrix, vehicle_cap, adresses, max_distance) #ccms, coords, 
    
    # Save distance_matrix
    with open('bu_distance_matrix.txt', 'w') as f:
        f.write(str(distance_matrix))
     # Save JSON maker
    with open('bu_json_routes.txt', 'w') as f:
        f.write(str(json_routes))

    return json_routes

if __name__ == "__main__":
    matrixRoutes_main()






