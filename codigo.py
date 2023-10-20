def CrearDataSet():
    # Cargar el dataset
    data = pd.read_csv("flights_final.csv")

    # Obtener los códigos únicos de aeropuertos
    codigos_aeropuertos_unicos_Source = data['Source Airport Code']
    codigos_aeropuertos_unicos_Destination = data['Destination Airport Code']

    # Inicializar un nuevo DataFrame vacío
    nuevo_data = pd.DataFrame(columns=data.columns)
    conexiones = []
    filas_cumplen = []

    # Crear un grafo completo
    G = nx.Graph()

    # Iterar a través de las filas del DataFrame
    for index, row in data.iterrows():
        valor1 = row['Source Airport Code']
        valor2 = row['Destination Airport Code']

        # Asegurarte de que los dos valores no sean iguales a los de otra sublista
        if (valor1, valor2) not in conexiones and (valor2, valor1) not in conexiones:
            filas_cumplen.append(row)
            conexiones.append((valor1, valor2))

    cantidad_de_sublistas = sum(1 for sublista in conexiones if len(sublista) == 2)

    print("Cantidad de sublistas con exactamente dos elementos:", cantidad_de_sublistas)
    nuevo_data = pd.DataFrame(filas_cumplen)

    nuevo_data.to_csv("flights_clean.csv", index=False)

    nuevo_data
CrearDataSet()
import folium
import pandas as pd
import networkx as nx
from geopy.distance import geodesic


def CrearDataSet():
    # Cargar el dataset
    data = pd.read_csv("flights_final.csv")

    # Obtener los códigos únicos de aeropuertos
    codigos_aeropuertos_unicos_Source = data['Source Airport Code']
    codigos_aeropuertos_unicos_Destination = data['Destination Airport Code']

    # Inicializar un nuevo DataFrame vacío
    nuevo_data = pd.DataFrame(columns=data.columns)
    conexiones = []
    filas_cumplen = []

    # Crear un grafo completo
    G = nx.Graph()

    # Iterar a través de las filas del DataFrame
    for index, row in data.iterrows():
        valor1 = row['Source Airport Code']
        valor2 = row['Destination Airport Code']

        # Asegurarte de que los dos valores no sean iguales a los de otra sublista
        if (valor1, valor2) not in conexiones and (valor2, valor1) not in conexiones:
            filas_cumplen.append(row)
            conexiones.append((valor1, valor2))

    cantidad_de_sublistas = sum(1 for sublista in conexiones if len(sublista) == 2)

    print("Cantidad de sublistas con exactamente dos elementos:", cantidad_de_sublistas)
    nuevo_data = pd.DataFrame(filas_cumplen)

    nuevo_data.to_csv("flights_clean.csv", index=False)

    nuevo_data


# Cargar el dataset en un DataFrame
data = pd.read_csv("flights_clean.csv")

# Crear un grafo vacío
G = nx.Graph()

    # Crear un diccionario para almacenar la información de los aeropuertos
aeropuertosS = {}
aeropuertosD = {}

 # Diccionario con todos los aeropuertos y su respectiva información
aeropuertos = {}

# Itera a través de las filas del DataFrame para agregar información de aeropuertos al diccionario
for index, row in data.iterrows():
    codigo = row['Source Airport Code']
    latitud = row['Source Airport Latitude']
    longitud = row['Source Airport Longitude']
    name = row['Source Airport Name']
    city = row['Source Airport City']
    country = row['Source Airport Country']
    aeropuertos[codigo] = {'latitud': latitud, 'longitud': longitud, 'nombre': name,
                           'ciudad': city, 'pais': country}

    codigo2 = row['Destination Airport Code']
    latitud2 = row['Destination Airport Latitude']
    longitud2 = row['Destination Airport Longitude']
    name2 = row['Destination Airport Name']
    city2 = row['Destination Airport City']
    country2 = row['Destination Airport Country']

    if codigo2 not in aeropuertos:
        aeropuertos[codigo2] = {'latitud': latitud2, 'longitud': longitud2, 'nombre': name2,
                                'ciudad': city2, 'pais': country2}

# Itera a través de las claves y valores del diccionario para agregar nodos al grafo
for codigo_aeropuerto, atributos in aeropuertos.items():
    G.add_node(codigo_aeropuerto, **atributos)

# lista que contendra los aeropuertos en los que hay vuelos
conexiones = []

# Iterar a través de las filas del DataFrame para agregar aristas ponderadas al grafo
for index, row in data.iterrows():
    codigo = row['Source Airport Code']
    codigo2 = row['Destination Airport Code']
    latitud = row['Source Airport Latitude']
    longitud = row['Source Airport Longitude']
    latitudD = row['Destination Airport Latitude']
    longitudD = row['Destination Airport Longitude']

        # Almacenar la información del aeropuerto en el diccionario
    aeropuertosS[codigo] = (latitud, longitud)
    aeropuertosD[codigo2] = (latitudD, longitudD)

    conexiones.append((codigo, codigo2))

    # Iterar a través de las sublistas que representan las conexiones y agregar aristas al grafo
for sublist in conexiones:
    origen, destino = sublist  # Suponiendo que cada sublista contiene dos códigos de aeropuerto

    # Calcular la distancia entre los aeropuertos usando sus coordenadas de latitud y longitud
    distancia = geodesic(aeropuertosS[origen], aeropuertosD[destino]).kilometers

        # Agregar una arista con el peso igual a la distancia
    G.add_edge(origen, destino, weight=distancia)

    # El grafo G contiene la información de los aeropuertos y las conexiones con el peso de distancia.

#Crear mapa
mapa = folium.Map()

def DibujarAristas():
    for u, v in G.edges():
        latitud_u = G.nodes[u]['latitud']
        longitud_u = G.nodes[u]['longitud']
        latitud_v = G.nodes[v]['latitud']
        longitud_v = G.nodes[v]['longitud']
        peso = G[u][v]['weight']

        # Agregar una línea entre las ubicaciones con un popup que muestra el peso (distancia)
        folium.PolyLine([(latitud_u, longitud_u), (latitud_v, longitud_v)],
                        color='blue', weight=2.5,
                        popup=f'Distancia: {peso} km').add_to(mapa)

#Agrega al mapa todas las ubicaciones incluendo las conexiones (muy lento)
def MostrarNodosMapa():
    for nodo in G.nodes():
        latitud = G.nodes[nodo]['latitud']
        longitud = G.nodes[nodo]['longitud']

        # Agregar un marcador para cada ubicación
        folium.Marker([latitud, longitud], popup=nodo).add_to(mapa)

        #DibujarAristas()

    mapa.save("mapa.html")

#Ejemplo de prueba para la variable que recibe el codigo del aeropuerto

def Crear10Caminos(code):
    # Utiliza el algoritmo de Dijkstra para encontrar los caminos mínimos desde el vértice de inicio
    longitudes_caminos = nx.single_source_dijkstra_path_length(G, code)

    # Ordena el diccionario por las longitudes de los caminos
    longitudes_caminos_ordenadas = dict(sorted(longitudes_caminos.items(), key=lambda item: item[1], reverse=True))

    # Obtiene los 10 aeropuertos más lejanos
    aeropuertos_mas_lejanos = list(longitudes_caminos_ordenadas.keys())[:10]

    # Crear un mapa centrado en una ubicación
    mapa = folium.Map(location=[aeropuertos[code]['latitud'], aeropuertos[code]['longitud']], zoom_start=6)
    folium.Marker(location=[aeropuertos[code]['latitud'], aeropuertos[code]['longitud']],
                      popup=f'Código: {code}\n Nombre: {aeropuertos[code]["nombre"]}\n Ciudad: {aeropuertos[code]["ciudad"]}\n País: {aeropuertos[code]["pais"]}\n Latitud: {aeropuertos[code]["latitud"]}\n Longitud: {aeropuertos[code]["longitud"]}').add_to(mapa)
    # Itera a través de los 10 aeropuertos más lejanos
    for aeropuerto in aeropuertos_mas_lejanos:
        # Agrega un marcador para cada aeropuerto
        folium.Marker(location=[aeropuertos[aeropuerto]['latitud'], aeropuertos[aeropuerto]['longitud']], popup=f'Código: {aeropuerto}').add_to(mapa)

        # Calcula la distancia en kilómetros entre el aeropuerto de inicio y el aeropuerto actual
        distancia_km = longitudes_caminos_ordenadas[aeropuerto]

        latitud = float(aeropuertos[codigo]['latitud'])
        longitud = float(aeropuertos[codigo]['longitud'])

         # Luego, en folium.PolyLine
        folium.PolyLine(locations=[(aeropuertos[code]['latitud'], aeropuertos[code]['longitud']),
                                 (aeropuertos[aeropuerto]['latitud'], aeropuertos[aeropuerto]['longitud'])],
                        color='darkcyan', weight=2.5, popup=f'Distancia: {distancia_km} km').add_to(mapa)

    # Guarda el mapa en un archivo HTML
    mapa.save("mapa1.html")

def MostrarCaminoMinimo(origen, destino):
    # Calcular el camino mínimo desde el aeropuerto de origen al destino
    camino_minimo = nx.shortest_path(G, source=origen, target=destino, weight='weight')

    # Crear un mapa centrado en la ubicación del aeropuerto de origen
    mapa = folium.Map(location=[aeropuertos[origen]['latitud'], aeropuertos[origen]['longitud']], zoom_start=6)

    # Agregar un marcador para el aeropuerto de origen
    folium.Marker(location=[aeropuertos[origen]['latitud'], aeropuertos[origen]['longitud']],
                      popup=f'Código: {origen}\n Nombre: {aeropuertos[origen]["nombre"]}\n Ciudad: {aeropuertos[origen]["ciudad"]}\n País: {aeropuertos[origen]["pais"]}\n Latitud: {aeropuertos[origen]["latitud"]}\n Longitud: {aeropuertos[origen]["longitud"]}').add_to(mapa)

    # Iterar a través de los aeropuertos en el camino mínimo
    for aeropuerto in camino_minimo:
        # Agregar un marcador para cada aeropuerto en el camino
        folium.Marker(location=[aeropuertos[aeropuerto]['latitud'], aeropuertos[aeropuerto]['longitud']],
                                popup=f'Código: {aeropuerto}\n Nombre: {aeropuertos[aeropuerto]["nombre"]}\n Ciudad: {aeropuertos[aeropuerto]["ciudad"]}\n País: {aeropuertos[aeropuerto]["pais"]}\n Latitud: {aeropuertos[aeropuerto]["latitud"]}\n Longitud: {aeropuertos[aeropuerto]["longitud"]}').add_to(mapa)


        # Calcular la distancia en kilómetros entre el aeropuerto actual y el siguiente en el camino
        if aeropuerto != destino:
            siguiente_aeropuerto = camino_minimo[camino_minimo.index(aeropuerto) + 1]
            distancia_km = geodesic((aeropuertos[aeropuerto]['latitud'], aeropuertos[aeropuerto]['longitud']),
                                    (aeropuertos[siguiente_aeropuerto]['latitud'], aeropuertos[siguiente_aeropuerto]['longitud'])).kilometers

            # Dibujar una línea entre el aeropuerto actual y el siguiente en el camino
            folium.PolyLine(locations=[(aeropuertos[aeropuerto]['latitud'], aeropuertos[aeropuerto]['longitud']),
                                      (aeropuertos[siguiente_aeropuerto]['latitud'], aeropuertos[siguiente_aeropuerto]['longitud'])],
                            color='darkcyan', weight=2.5, popup=f'Distancia: {distancia_km} km').add_to(mapa)

    # Guardar el mapa en un archivo HTML
    mapa.save("mapa2.html")






while True:
    print("Menú:")
    print("0. Mostrar todos los aeropuertos")
    print("1. Crear 10 caminos")
    print("2. Crear camino mínimo")
    print("3. Salir")

    opcion = input("Selecciona una opción (1/2/3): ")

    if opcion == "0":
      MostrarNodosMapa()


    elif opcion == '1':
        codigo_aeropuerto = input("Ingresa el código del aeropuerto: ")
        Crear10Caminos(codigo_aeropuerto)
        # Abre el archivo HTML para mostrar el mapa

    elif opcion == '2':
        origen = input("Código del aeropuerto de origen: ")
        destino = input("Código del aeropuerto de destino: ")
        MostrarCaminoMinimo(origen, destino)
        # Abre el archivo HTML para mostrar el mapa

    elif opcion == '3':
        print("Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, selecciona una opción válida (1/2/3).")
