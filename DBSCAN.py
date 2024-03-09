#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from coordenadas_importar import df_latitude
#from coordenadas_importar import df_original

# Inicializar el modelo DBSCAN
epsilon = 0.0001  # Ajusta según tus datos
min_samples = 10  # Ajusta según tus datos
dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)

# Iterar sobre cada cliente
for cliente in df_latitude['NIS'].unique():
    # Filtrar los datos del cliente actual
    datos_cliente = df_latitude[df_latitude['NIS'] == cliente][['LATITUDE', 'LONGITUDE']]
    
    # Aplicar DBSCAN al cliente actual
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(datos_cliente)
    
    # Agregar los resultados de DBSCAN al DataFrame original
    df_latitude.loc[df_latitude['NIS'] == cliente, 'cluster_label'] = cluster_labels


df_clustering = df_latitude

clientes_con_ruido_exclusivo = df_clustering.groupby('NIS').filter(lambda x: (x['cluster_label'] == -1).all())

num_clientes_con_ruido_exclusivo = len(clientes_con_ruido_exclusivo['NIS'].unique())
clientes_totales = df_clustering['NIS'].nunique()
#df_latitude.head(150)

print(num_clientes_con_ruido_exclusivo, ", ",clientes_totales)

