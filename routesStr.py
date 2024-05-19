"""
Coordinate string maker to feed OSRM server.

"""
import pandas as pd


def createstr(site_coord):

    df = pd.read_excel("subbase.xlsx", dtype=str)
    dbcoord = df[["Coord"]]
    
    #  Get lat long
    df[["Coord"]] = df[["Coord"]].map(lambda x : x.replace(" ", ""))
    df[['lat', 'long']] = df['Coord'].str.split(',', expand=True)
    dbcoord = df['long'].astype(str) +","+df['lat'].astype(str)

    # Inits vars
    strcoord = '' 
    nstrcoord = [] # Number of coordinate pairs per element
    listcoord = [] # List of nstrcoord elements
    matrixcoord = [] # Matrix containing lists of list coord

    coords = dbcoord.values.tolist()
    coords.insert(0,site_coord)   
    counta = 0

    # Fixed coordinate to iterate
    ncoord = len(coords)
    print(f"Number of coordinates: {ncoord}")
    
    for coordy in range(len(coords)): # for columns 
        coordfix =  coords[coordy] 
        #print(f"column: {coordy}")
        #print(f"Fixed coord out: {coordfix}")
        counta = 0
        listcoord = [] 
        strcoord = ''    
        for coordx in coords:
            #print(f"Fixed coord in: {coordfix}") # Check
            twoaddresses = coordfix + ";" + coordx +";" # example: 13.388860,52.517037;13.397634,52.529407;
            #print(f"twoaddresses: {twoaddresses}") #Check 
            counta += 1
            if ( counta %100 == 0 or ncoord == counta ): #counta % 100 == 0
                strcoord += twoaddresses
                strcoord=strcoord[0:-1]
                listcoord.append(strcoord)
                nstrcoord.append(counta)
                strcoord = ''
            else:
                strcoord += twoaddresses
        matrixcoord.append(listcoord)
    #print(f"coordinate pairs per element: {nstrcoord}")
    #print(f"Packs to send: {len(listcoord)}")
    #print(f"Columnsto send: {len(matrixcoord)}")
    return  ncoord, matrixcoord 

def export_matrixcoord(matrixcoord):
    with open('bu_matrixcoord.txt', 'w') as f:
        f.write(str(matrixcoord))    

def createAddress(site_coord): 
    df = pd.read_excel("subbase.xlsx", dtype = str)

    #  Get lat long
    site_coord = site_coord.split(',')
    lat=site_coord[1]
    long=site_coord[0]
    site_list = []
    site_list.extend(["0",float(lat),float(long)])
    site_add_list = []
    df[["Coord"]] = df[["Coord"]].map(lambda x : x.replace(" ", ""))
    df[['lat', 'long']] = df['Coord'].str.split(',', expand=True)
    df['CCMS'] = df['CCMS'].astype(str)
    df['lat'] = df['lat'].astype(float)
    df['long'] = df['long'].astype(float)
    adresses = df[['CCMS','lat','long']].values.tolist()
    site_add_list.append(site_list)
    adresses.insert(0,site_list)

    return adresses

def routesStr_main(site_coord): 
    #site_coord = '-74.119482000000000,4.684755000000000' 

    ncoord , matrixcoord = createstr(site_coord) #, matrixcoord  
    adresses = createAddress(site_coord)
    
    #export_matrixcoord(matrixcoord)
    
    # Check the matrixcoord len 
    #print(matrixcoord[1])
    return ncoord , matrixcoord, adresses #, matrixcoord

if __name__ == "__main__":
    routesStr_main()

