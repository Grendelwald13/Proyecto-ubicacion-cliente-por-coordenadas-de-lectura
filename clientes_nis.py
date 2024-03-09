import pandas as pd
import numpy as np
import folium

class Ubicacion_cliente():
    def __init__(self, nis, df_original, df_clustering):
        self.nis = nis
        self.df_original = df_original
        self.df_clustering = df_clustering

    def calcular_centroides(self):
        coordenada_inicial = df_original[df_original['nis'] == self.nis][['LATITUDE', 'LONGITUDE']].iloc[0]
        
        return coordenada_inicial
    
    def definir_nis(self):
        imp_coordendas = df_clustering[df_clustering['NIS'] == self.nis]
        imp_coordendas = imp_coordendas[imp_coordendas['cluster_label'] != -1]
        return imp_coordendas

    def calcular_centroides_cluster_sin_ruido(self):
        imp_coordendas = self.definir_nis()
        centroides = []
        for cluster_label in imp_coordendas['cluster_label'].unique():
            datos_cluster = imp_coordendas[imp_coordendas['cluster_label'] == cluster_label][['LATITUDE', 'LONGITUDE']]
            centroide = np.mean(datos_cluster, axis=0)
            centroides.append(centroide)
        return centroide
    
    def crear_mapa(self):
        coordenada_inicial = self.calcular_centroides()
        # Crear un mapa centrado en la coordenada inicial
        mapa = folium.Map(location=[coordenada_inicial['LATITUDE'], coordenada_inicial['LONGITUDE']], zoom_start=15)

        # Agregar marcador para la coordenada inicial
        folium.Marker(
            location=[coordenada_inicial['LATITUDE'], coordenada_inicial['LONGITUDE']],
            popup='Coordenada Inicial',
            icon=folium.Icon(color='green')
        ).add_to(mapa)
        return mapa
    
    #agrupa las coordenadas y las grafica en el mapa creado anteriormente
    def agrupar_cargar_mapa(self):
        mapa = self.crear_mapa()
        for cluster_label, cluster_data in df_clustering[df_clustering['NIS'] == self.nis].groupby('cluster_label'):
            cluster_group = folium.FeatureGroup(name=f'Cluster {cluster_label}')
            for idx, row in cluster_data.iterrows():
                folium.CircleMarker(
                    location=[row['LATITUDE'], row['LONGITUDE']],
                    radius=5,
                    color='blue' if cluster_label == -1 else 'red',  # Color azul para ruido, rojo para otros clusters
                    fill=True,
                    fill_color='blue' if cluster_label == -1 else 'red'
                ).add_to(cluster_group)
            cluster_group.add_to(mapa)
        folium.LayerControl().add_to(mapa)
        return mapa



c1 = Ubicacion_cliente(363707, df_original, df_clustering)

centroide_origen = c1.calcular_centroides()
centroides_cluster = c1.calcular_centroides_cluster_sin_ruido()
mapa = c1.agrupar_cargar_mapa( )
print(centroide_origen)
print(centroides_cluster)
mapa
