# -*- coding: utf-8 -*-
"""Bismillah.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19qv_KIG-QIWkO23PASykAlCm64K2T516
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
import warnings
warnings.filterwarnings("ignore")
import plotly as py
import plotly.graph_objs as go
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

#koneksi dari COLAB ke Gdrive
from google.colab import drive
drive.mount('/content/drive')

# Loading Data

path = '/content/drive/MyDrive/Dataset TA.xlsx'

df = pd.read_excel(path)
df

print(df.head)
print('__________')
print('Shape : ',df.shape)
print('__________')
print(df.dtypes)
print('__________')
print(df.describe())
print('__________')
print('Data Null ?')
print(df.isnull().sum())

plt.figure(figsize=(20,10))
df.boxplot(column=['Luas Wilayah (km2)','Jumlah Penduduk'])
plt.show()

fig, ax = plt.subplots(figsize=(15, 10))

# Title & Subtitle
fig.text(0.097, 1, 'Jumlah Penduduk Dan Luas Wilayah', fontfamily='serif', fontsize=15, fontweight='bold')

# Ax Spines
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('lightgray')

# Grid
ax.set_axisbelow(True)
ax.yaxis.grid(color='lightgray', linestyle='--')  # Choose a valid linestyle

# Plot
plt.scatter(x='Jumlah Penduduk', y='Luas Wilayah (km2)',
            data=df, color='#114a31', s=25, alpha=0.8)

# Tick Control
plt.yticks(fontsize=10, fontfamily='serif', fontweight='light')
plt.xticks(fontsize=10, fontfamily='serif', fontweight='light', rotation=90)

# Label Control
ax.set_ylabel('Luas Wilayah (km2)', fontfamily='serif', fontsize=12)
ax.set_xlabel('Jumlah Penduduk', fontfamily='serif', fontsize=12)

ax.set_ylim(0, 1800)
plt.axhline(y=0, color='black', linewidth=1.3, alpha=0.7)

plt.show()

# Menentukan input variabel

x = df[['Jumlah Penduduk','Luas Wilayah (km2)']]

# SSE Method
sse = []
index = range(1,10)
for i in index:
    kmeans = KMeans(n_clusters=i, random_state=30)
    kmeans.fit(x)  # Menggunakan fit, bukan fix
    sse_ = kmeans.inertia_
    sse.append(sse_)
    print("Jumlah Klaster =",i,"Nilai SSE =", sse_)

plt.plot(index, sse,  marker='o')
plt.xlabel('n_cluster')
plt.ylabel('SSE')
plt.show()

range_n_cluster = [3, 4, 5]
silhouette_scores = []

for n_clusters in range_n_cluster:
    clusterer = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    y_means = clusterer.fit_predict(x)
    silhouette_avg = silhouette_score(x, y_means)
    silhouette_scores.append(silhouette_avg)
    print("Jumlah Klaster =", n_clusters, "Nilai rata-rata Silhouette =", silhouette_avg)

# Elbow Method

# Inisialisasi range jumlah klaster yang akan diuji
cluster_range = range(1, 10)
cluster_wss = []

# Menghitung within-cluster sum of squares (WCSS) untuk setiap jumlah klaster
for num_cluster in cluster_range:
    cluster = KMeans(n_clusters=num_cluster)
    cluster.fit(x)
    cluster_wss.append(cluster.inertia_)

# Visualisasi dengan plot garis (elbow method)
plt.plot(cluster_range, cluster_wss, marker='o')
plt.xlabel('Jumlah Klaster')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.title('Metode Elbow untuk Menentukan Jumlah Klaster Optimal')
plt.show()

# Inisialisasi objek StandardScaler
scaler = StandardScaler()

# Melakukan standarisasi pada data
x_standardized = scaler.fit_transform(x)

#jumlah klaster optimal yang telah ditentukan adalah 3
optimal_num_clusters = 3

# Inisialisasi model K-Means dengan jumlah klaster optimal
kmeans_model = KMeans(n_clusters=optimal_num_clusters, random_state=0)

# Melakukan fitting model pada data yang sudah distandarisasi
kmeans_model.fit(x_standardized)

# Menambahkan kolom klaster ke dalam dataframe (atau dataset Anda)
df['Cluster'] = kmeans_model.labels_
df

fig, ax = plt.subplots(figsize=(20, 7))
fig.text(0.105, .98, '2D Visualisasi Klaster', fontfamily='serif', fontsize=15, fontweight='bold')
fig.text(0.105, .93, 'Klaster 2D : Jumlah Penduduk dan Luas Wilayah', fontfamily='serif', fontsize=15, fontweight='bold')

km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
y_means = km.fit_predict(x)

# Gunakan .iloc untuk memilih data
plt.scatter(x.iloc[y_means==0, 0], x.iloc[y_means==0, 1], s=100, c='green', label='Klaster 0')
plt.scatter(x.iloc[y_means==1, 0], x.iloc[y_means==1, 1], s=100, c='red', label='Klaster 1')
plt.scatter(x.iloc[y_means==2, 0], x.iloc[y_means==2, 1], s=100, c='salmon', label='Klaster 2')
plt.scatter(km.cluster_centers_[:3, 0], km.cluster_centers_[:3, 1], s=100, c='navy', label='Centroid')
plt.xlabel("Jumlah Penduduk")
plt.ylabel("Luas Wilayah (Km2)")
plt.legend()
plt.grid()
plt.show()

"""Berdasarkan grafik tersebut, dapat diketahui bahwa terdapat 3 cluster dan masing-masing memiliki nilai centroid, sehingga berdasarkan pembagian 3 cluster tersebut dapat dikategorikan bahwa :
 - 	Cluster 0 : Kepadatan jiwa/km2 yang rendah (<10.000 jiwa dengan luas wilayah <1.500 km2)
 - Cluster 1 : Kepadatan jiwa/km2 yang tinggi (<50.000 jiwa dengan luas wilayah <1250 km2)
 - Cluster 2 : Kepadatan jiwa/h yang menengah (<30.000 jiwa dengan luas wilayah <1250 km2)

Dapat diketahui bahwa Cluster 1 merupakan Cluster terpadat dari klaster lainnya, Cluster 0 merupakan CLuster rendah kepadatan penduduknya diantara ketiga Cluster tersebut. Dengan demikian, perlu kebijakan terkait kependudukan dari pemerintah agar perencanaan perkotaan Sulawesi Tengah dapat terus tertata dengan baik dan tingkat dari dampak kepadatan penduduk yang tinggi pada suatu titik akan terhindar pula.
"""

# Eksport to download if in colab
from google.colab import files

file_cluster = df.to_excel('TA Clustering.xlsx', sheet_name='predict')
files.download('TA Clustering.xlsx')