import pandas as pd


def createstr(site_coord):

    df = pd.read_excel("subbase.xlsx", dtype=str)
    dbcoord = df[["Coord"]]
    #print(dbcoord)
    
    #  Get lat long
    df[["Coord"]] = df[["Coord"]].map(lambda x : x.replace(" ", ""))
    #print(df[["Coord"]])
    df[['lat', 'long']] = df['Coord'].str.split(',', expand=True)
    dbcoord = df['long'].astype(str) +","+df['lat'].astype(str)

    # Inicialización var
    strcoord = '' 
    nstrcoord = [] # Cantidad de pares de coordenadas por elemento 
    listcoord = [] # Lista de elementos nstrcoord
    matrixcoord = [] # Matrix que contiene las listas de list coord

    coords = dbcoord.values.tolist()
    coords.insert(0,site_coord)   
    counta = 0

    # Acá se saca adresses ---
    


    #------

    #print(f"coord: {coords}")
    # Cordenada fija para iterar
    ncoord = len(coords)
    print(f"Number of coordinates: {ncoord}")
    
    for coordy in range(len(coords)): # for columns 
        coordfix =  coords[coordy] #dbcoord.iloc[coordy]['Coord']
        #print(f"columna: {coordy}")
        #print(f"Coordenada fija out: {coordfix}")
        counta = 0
        listcoord = [] 
        strcoord = ''    
        for coordx in coords:
            #print(coordx)
            #print(test1[coord].values)
            #print(f"Coordenada fija in: {coordfix}") # Check
            twoaddresses = coordfix + ";" + coordx +";" # example: 13.388860,52.517037;13.397634,52.529407;
            #print(f"twoaddresses: {twoaddresses}") #Check 
            counta += 1
            if ( counta %100 == 0 or ncoord == counta ): #counta % 100 == 0
                #print(f"Acá entra counta {counta}")
                strcoord += twoaddresses
                strcoord=strcoord[0:-1]
                listcoord.append(strcoord)
                nstrcoord.append(counta)
                strcoord = ''
            else:
                strcoord += twoaddresses
                #print(f"strcoord: {strcoord}")
        #print(strcoord) # cada elemento
        ##print(listcoord) # lista de elementos
        #print(f"Packs a enviar: {len(listcoord)}")
        matrixcoord.append(listcoord)
    #print(matrixcoord) # matrix de elementos
    #print(f"pares de coordenadas por elemento: {nstrcoord}")
    #print(f"Packs a enviar: {len(listcoord)}")
    ##print(listcoord)
    #print(f"Columns a enviar: {len(matrixcoord)}")
    #print(f"coord: {coords}")
    return  ncoord, matrixcoord # retorna número coordenadas y matrix coords,

def export_matrixcoord(matrixcoord):
    with open('bu_matrixcoord.txt', 'w') as f:
        f.write(str(matrixcoord))    

def createAddress(site_coord): # pendinete arreglar
    df = pd.read_excel("subbase.xlsx", dtype = str)

    #  Get lat long
    site_coord = site_coord.split(',')
    lat=site_coord[1]
    long=site_coord[0]
    site_list = []
    site_list.extend(["0",float(lat),float(long)])
    #print(site_list)
    site_add_list = []
    df[["Coord"]] = df[["Coord"]].map(lambda x : x.replace(" ", ""))
    df[['lat', 'long']] = df['Coord'].str.split(',', expand=True)
    df['CCMS'] = df['CCMS'].astype(str)
    #df['CCMS'] = df['CCMS'].map(lambda x : round(x,0))
    df['lat'] = df['lat'].astype(float)
    df['long'] = df['long'].astype(float)
    adresses = df[['CCMS','lat','long']].values.tolist()
    #print(adresses)
    site_add_list.append(site_list)
    adresses.insert(0,site_list)
    #print(f"Address: {adresses}")
    return adresses

def routesStr_main(site_coord): #site_coord
    #site_coord = '-74.119482000000000,4.684755000000000'

    ncoord , matrixcoord = createstr(site_coord) #, matrixcoord  
    adresses = createAddress(site_coord)
    
    #export_matrixcoord(matrixcoord)
    
    # Check the matrixcoord len 
    #print(matrixcoord[1])
    return ncoord , matrixcoord, adresses #, matrixcoord

if __name__ == "__main__":
    routesStr_main()

