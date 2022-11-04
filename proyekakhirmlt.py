# -*- coding: utf-8 -*-
"""ProyekAkhirMLT

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EFo-kdgVSLtPk1dy5NY6mA3DNygLPL6l

# Pendahuluan

Tema dari analisis ini adalah hiburan dimana hasilnya akan berupa model machine learning yang nanti dapat digunakan untuk dijadikan sebuah sistem rekomendasi film

# Data Loading
## Import Library
"""

# Commented out IPython magic to ensure Python compatibility.
import zipfile
import pandas as pd
import numpy as np
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.callbacks import EarlyStopping

import matplotlib.pyplot as plt
# %matplotlib inline

from google.colab import files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""## Extract Data"""

local_zip = '/content/movielens.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content')
zip_ref.close()

"""## Data Understanding

Dataset ini bersumber dari kaggle dimana memiliki 4 file data yaitu:

- links.csv
- ratings.csv
- movies.csv
- tags.csv

Dari keempat file diatas data yang akan kita gunakan hanya dua yaitu data pada file ratings.csv dan juga movies.csv

## Read Dataset
"""

ratings = pd.read_csv('/content/ml-latest-small/ratings.csv')
movies = pd.read_csv('/content/ml-latest-small/movies.csv')

movies.head()

ratings.head()

"""# Exploratory Data Analysis
## Univariate Analysis
### Deskripsi Variabel
- Variabel file movies.csv:
  - movieId = ID dari film
  - title = Judul dari film
  - genres = Genre dari film

- Variabel file ratings.csv:
  - userId = ID pengguna
  - movieId = ID film yang diberi rating
  - rating = Skor dari rating yang diberikan
  - timestamp = Waktu rating terekam
  
### Melihat Infromasi Data
"""

movies.info()

ratings.info()

ratings.rating.value_counts()

"""Terlihat dari informasi data rating diatas bahwa rating memiliki maksimal 5 bintang dengan skala 0.5

### Menghitung Total Data
"""

print(f'Jumlah data Movie sebanyak {movies.shape[0]}, dan memiliki {movies.shape[1]} kolom')
print(f'Jumlah data Rating sebanyak {ratings.shape[0]}, dan memiliki {ratings.shape[1]} kolom')

"""### Mengecek Missing Value"""

movies.isnull().sum()
#movies.isna().sum()

ratings.isnull().sum()
#ratings.isna().sum()

"""Terlihat diatas bahwasannya tidak terdapat missing value pada kedua dataframe diatas, baik data film maupun data rating.

### Mengecek Data Duplikat
"""

movies.duplicated().sum()

ratings.duplicated().sum()

"""Terlihat dari hasil diatas tidak terdapat data duplikat pada kedua dataframe diatas, baik data film maupun data rating.

### Menghitung Total Data Unik
"""

movies.nunique()

"""Terlihat dari hasil diatas, terdapat 9742 data unik pada variabel movieId, 9737 data unik pada variabel title dan 951 data unik pada variabel genres"""

ratings.nunique()

"""Terlihat dari hasil diatas, terdapat 610 data unik pada variabel userId, 9724 data unik pada variabel movieId, 10 data unik pada variabel rating dan 85043 data unik pada variabel timestamp

### Menganalisa Distribusi Sebaran Tahun Rilis Film
"""

movies_year = movies.copy()
movies_year['year'] = movies['title'].str.extract('(\d+)').astype(float)
movies_year.year.dropna(inplace=True)

"""Melakukan deklarasi variabel baru bernama movies_year, lalu melakukan konversi pada variabel title dari bertipe data object menjadi tipe data string dan mengektrak tahun yang terdapat kurung didalamnya dan merubah tahun tersebut menjadi bentuk float, setelah itu melakukan drop missing value pada film yang tidak memiliki tahun"""

new_movies_year = movies_year[movies_year['year'] > 1000.0]
new_movies_year.year.astype(int)
data = new_movies_year

"""Membuat variabel baru lalu menyaring variabel year (diatas 1000) yang diekstrak menggunakan kurung tadi untuk mengantisipasi lolosnya variabel lain selain variabel tahun. lalu merubah tipe datanya menjadi integer."""

plt.figure(figsize=(12,6))
sns.histplot(data=data, x='year',bins=50)
plt.title('Distribusi Sebaran Tahun Rilis Film', fontsize=15, pad=15)
plt.tight_layout()
plt.show()

"""Hasil analisis dari grafik diatas ialah distribusi terbanyak terjadi diatas tahun 2000, dimana distribusi film cenderung mengalami kenaikan secara signifkan setiap berjalannya waktu.

### Menganalisa Distribusi Sebaran Genre Film
"""

movies_genres = movies.copy()
genres=[]
for i in range(len(movies.genres)):
    for x in movies.genres[i].split('|'):
        if x not in genres:
            genres.append(x)
genres

"""Karena sebuah film memiliki banyak genre, maka untuk memisahkannya kita dapat menggunakan fungsi split yang tersedia pada python, dimana jika kita lihat preview data diatas bahwasannya variabel genres film yang memiliki lebih dari satu dipisahkan dengan "|", lalu kita masukkan dalam sebuah list.

"""

for x in genres:
    movies_genres[x] = 0

for i in range(len(movies.genres)):
    for x in movies.genres[i].split('|'):
        movies_genres[x][i]=1

movies_genres.head()

"""Menambahkan setiap genres untuk menjadi variabel/kolom pada dataframe agar mempermudah proses selanjutnya nantinya."""

data = movies_genres.iloc[:,3:].sum().reset_index()
data.columns = ['title','total']

plt.figure(figsize=(14,10))
sns.barplot(y='title', x='total', data=data)
plt.title('Distribusi Sebaran Genre Film', fontsize=30, pad=30)
plt.tight_layout()
plt.show()

"""Dari hasil analisa pada grafik diatas didapat bahwasannya genre paling diminati dalam film ialah drama diikuti dengan genre komedi setelahnya dimana kedua genre tersebut hampir menguasai setengah data yang kita miliki

### Menganalisa Distribusi Sebaran Rating Film Tertinggi
"""

print(f'Jumlah pengguna yang memberikan rating: {ratings.userId.nunique()}')
print(f'Jumlah film yang diberi rating oleh pengguna: {ratings.movieId.nunique()}')

rating_movies = pd.merge(ratings, movies, on='movieId', how='inner')
rating_movies.drop(['timestamp','genres'],axis=1, inplace=True)
rating_movies.head()

"""Melakukan pendeklarasian variabel baru, lalu melakukan merge dataframe movies dan ratings berdasarkan relasi variabel movieId yang dimiliki kedua dataframe. Setelah itu melakukan drop untuk kolom/variabel genres dan timestamp yang tidak diperlukan pada analisa distribusi ini"""

rating_movies_count = rating_movies.groupby('title')['rating'].count()
rating_movies_count = pd.DataFrame(rating_movies_count).reset_index().rename(columns={'rating':'total_rating'})
rating_movies_count.head()

"""Melakukan perhitungan total rating berdasarkan title film agar tidak terjadi duplikasi data"""

data = rating_movies_count.sort_values(by ='total_rating')

plt.figure(figsize=(15,10))
sns.barplot(data=data.iloc[-10:,:], 
            y='title', x='total_rating',
            palette="Blues_d")
plt.title('Distribusi Sebaran Rating dari 10 Film Tertinggi', pad=30, fontsize=30)
plt.tight_layout()
plt.show()

"""Terlihat pada grafik bahwasannya film yang memiliki rating tertinggi adalah Forrest Gump yang rilis pada tahun 1994

# Data Preparation
## Melakukan Pembersihan Data Missing Value
"""

movies.dropna(axis=0, inplace=True)
ratings.dropna(axis=0, inplace=True)

"""## Melakukan Sorting Data Rating berdasarkan ID Pengguna"""

ratings = ratings.sort_values('userId').astype('int')

"""Merubah data rating menjadi integer

## Menghapus Data Duplikat
"""

movies.drop_duplicates(subset=['title'], keep='first', inplace=True)
ratings.drop_duplicates(subset=['userId','movieId'], keep='first', inplace=True)

"""Menghapus data duplikat berdasarkan title pada dataframe movies dan juga userId dan movieId pada dataframe ratings dan membiarkan satu data tersisa

## Melakukan penggabungan Data
"""

merge_df = pd.merge(ratings, movies, how='left', on='movieId')
df = merge_df.copy().drop('timestamp', axis=1)
df.head()

df = df[~pd.isnull(df['genres'])]
df.shape

"""Menghapus data yang memiliki missing value pada variabel genres dan melihat jumlah data setelah digabungkan, terlihat data memiliki 100830 baris dengan 5 kolom

# Model Development
## Content Based Filtering
### TF-IDF Vectorizer
"""

tfid = TfidfVectorizer(stop_words='english')
tfid.fit(movies['genres'])
tfid.get_feature_names()

"""Melakukan inisialisasi TfidfVectorizer, lalu melakukan perhitungan idf pada data film dan melakukan mapping array dari fitur index integer ke fitur nama

### Transform Data ke Matriks
"""

tfidf_matrix = tfid.fit_transform(movies['genres']) 
tfidf_matrix.shape

"""Melakukan transform data ke matriks berdasarkan genre

### Menghitung Cosine Similarity
"""

cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

"""### Membuat dataframe baru berdasarkan Cosine Similarity"""

cosine_sim_df = pd.DataFrame(cosine_sim, index=movies['title'],
                             columns=movies['title'])
print('Shape:', cosine_sim_df.shape)

cosine_sim_df.sample(10, axis=1).sample(10, axis=0)

"""Terlihat diatas hasil dari similarity matrix pada setiap film

### Uji Coba Model Content Based Filtering
#### Membuat Function untuk Merekomendasikan 10 Film yang Mirip
"""

def MovieRecommendations(movies_title, similarity_data=cosine_sim_df, 
                         items=movies[['movieId','title','genres']], k=10):
  
    ''' Mengambil data menggunakan argpartition untuk partisi secara tidak langsung,
    sepanjang sumbu yang diberikan, kemudian dataframe diubah menjadi numpy Range 
    dengan parameter sebagai berikut (start, stop, step) '''
    index = similarity_data.loc[:, movies_title].to_numpy().argpartition(
        range(-1, -k, -1)
    )

    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    closest = closest.drop(movies_title, errors='ignore')

    return pd.DataFrame(closest).merge(items).head(k)

"""Mengambil data dengan similarity terbesar dari index yang ada, lalu melakukan drop movie_title agar nama movie yang dicari tidak muncul dalam daftar rekomendasi

#### Melakukan Pengecekan Data Film
"""

find_title = movies[movies['title'] == 'Daddy Day Care (2003)']
find_title

"""Melakukan pengecekan data film berdasarkan title. Dapat dilihat bahwa judul film Daddy Day Care (2003) memiliki genre Children dan Family

#### Mengujicoba Model Rekomendasi Content Based Filtering
"""

movie_title = 'Daddy Day Care (2003)'
movie_recomend = MovieRecommendations(movie_title)
movie_recomend

"""Dari 10 rekomendasi yang sistem berikan, 10 judul film tersebut memiliki genre yang sama dengan yaitu Children dan Family

## Collaborative Filtering
### Melakukan Encoding pada ID Pengguna
"""

user_id = df['userId'].unique().tolist()
print(f'list userId: {user_id}')
 
user_to_user_encoded = {x: i for i, x in enumerate(user_id)}
print(f'\nencoded userId: {user_to_user_encoded}')
 
user_encoded_to_user = {i: x for i, x in enumerate(user_id)}
print(f'\nencoded number to userId: {user_encoded_to_user}')

"""Mengubah unique userId menjadi list, lalu melakukan encoding userId, dan terakhir mengubah encoding angka ke userId

### Melakukan Encoding pada ID Film
"""

movie_id = df['movieId'].unique().tolist()
print(f'list movieId: {movie_id}')
 
movie_to_movie_encoded = {x: i for i, x in enumerate(movie_id)}
print(f'\nencoded movieId: {movie_to_movie_encoded}')
 
movie_encoded_to_movie = {i: x for i, x in enumerate(movie_id)}
print(f'\nencoded number to movieId: {movie_encoded_to_movie}')

"""Mengubah unique movieId menjadi list, lalu melakukan encoding movieId, dan terakhir mengubah encoding angka ke movieId

### Melakukan Mapping pada ID Pengguna dan ID Film
"""

df['user'] = df['userId'].map(user_to_user_encoded)
df['movie'] = df['movieId'].map(movie_to_movie_encoded)
df.head()

"""Melakukan mapping userId ke dataframe user dan melakukan mapping movie_id ke dataframe movie

"""

num_users = len(user_to_user_encoded)
num_movie = len(movie_encoded_to_movie)
df['rating'] = df['rating'].values.astype(np.float32)
min_rating = min(df['rating'])
max_rating = max(df['rating'])

print(f'Number of User: {num_users}')
print(f'Number of Movie: {num_movie}')
print(f'Min rating: {min_rating}')
print(f'Max rating: {max_rating}')

"""Mendapatkan jumlah pengguna dan film, lalu merubah tipe data variabel rating menjadi float, lalu melihat nilai maksimum dan nilai minimum pada rating

### Melakukan Pembagian Data untuk Training dan Validasi
#### Mengacak Dataset
"""

df = df.sample(frac=1, random_state=42)
df.head()

"""#### Membuat Variabel Training dan Validasi"""

x = df[['user', 'movie']].values
y = df['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

"""Mendeklarasikan variabel x untuk mencocokkan data pengguna dan film menjadi satu value, lalu membuat variabel y untuk rating dari hasil, dan selanjutnya ialah membagi data train sebesar 80% dan data validasi sebesar 20%

### Pelatihan Model
#### Pembuatan kelas dan Inisialisasi Fungsi
"""

class RecommenderNet(tf.keras.Model):
  def __init__(self, num_users, num_movie, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_movie = num_movie
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding(
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(5e-7)
    )
    self.user_bias = layers.Embedding(num_users, 1)
    self.movie_embedding = layers.Embedding(
        num_movie,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(5e-7)
    )
    self.movie_bias = layers.Embedding(num_movie, 1)
 
  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0])
    user_bias = self.user_bias(inputs[:, 0])
    movie_vector = self.movie_embedding(inputs[:, 1])
    movie_bias = self.movie_bias(inputs[:, 1])
 
    dot_user_movie = tf.tensordot(user_vector, movie_vector, 2) 
 
    x = dot_user_movie + user_bias + movie_bias
    
    return tf.nn.sigmoid(x)

"""#### Memanggil Kelas, Mengcompile Model dan Membuat Callback"""

model = RecommenderNet(num_users, num_movie, 50) # inisialisasi model

model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[[tf.keras.metrics.MeanAbsoluteError(),tf.keras.metrics.RootMeanSquaredError()]]
)
callbacks = EarlyStopping(
    min_delta=0.0001,
    patience=7,
    restore_best_weights=True,
)

"""#### Melakukan Pelatihan Model"""

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 8,
    epochs = 100,
    validation_data = (x_val, y_val),
    callbacks=[callbacks]
)

"""### Uji Coba Model Collaborative Filtering
#### Mengambil Data Sample Pengguna
"""

user_ID = df.userId.sample(1).iloc[0]
movie_watched_by_user = df[df.userId == user_ID]
 
movie_not_watched = movies[~movies['movieId'].isin(movie_watched_by_user.movieId.values)]['movieId'] 
movie_not_watched = list(
    set(movie_not_watched)
    .intersection(set(movie_to_movie_encoded.keys()))
)

 
movie_not_watched = [[movie_to_movie_encoded.get(x)] for x in movie_not_watched]
user_encoder = user_to_user_encoded.get(user_ID)
user_movie_array = np.hstack(
    ([[user_encoder]] * len(movie_not_watched), movie_not_watched)
)

"""#### Mengujicoba Model Rekomendasi Collaborative Filtering"""

ratings = model.predict(user_movie_array).flatten()
 
top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_movie_ids = [
    movie_encoded_to_movie.get(movie_not_watched[x][0]) for x in top_ratings_indices
]
 
print('Showing recommendations for users: {}'.format(user_ID))
print('====' * 10)
print('movie with high ratings from user')
print('----' * 8)
 
top_movie_user = (
    movie_watched_by_user.sort_values(
        by = 'rating',
        ascending=False
    )
    .head(5)
    .movieId.values
)
 
movie_df_rows = movies[movies['movieId'].isin(top_movie_user)]
for row in movie_df_rows.itertuples():
    print(row.title)
 
print('----' * 8)
print('Top 10 movie recommendation')
print('----' * 8)
 
recommended_movie = movies[movies['movieId'].isin(recommended_movie_ids)]
for row in recommended_movie.itertuples():
    print(row.title)

"""# Evaluation
Evaluasi yang akan saya lakukan disini yaitu evaluasi dengan Mean Absolute Error (MAE) dan Root Mean Squared Error (RMSE) pada Collaborative Filtering dan Precision Content Based Filtering
## Metrik Precision
"""

find_title = movies[movies['title'] == 'Outbreak (1995)']
find_title

"""Melakukan pengecekan data film berdasarkan title. Dapat dilihat bahwa judul film Outbreak (1995) memiliki genre 4 genre yaitu Action, Drama, Sci-Fi, dan Thriller"""

movie_title = 'Outbreak (1995)'
movie_recomend = MovieRecommendations(movie_title)
movie_recomend

"""Dari hasil rekomendasi di atas, diketahui bahwa Outbreak (1995) memiliki 4 genre. Dari 10 item yang direkomendasikan, 8 item memiliki kategori 4 genre yang sama (similar). Artinya, precision sistem kita sebesar 8/10 atau sebesar 80%.

Precision = #of recommendation that are relevant/#of item we recommend.
Pada contoh rekomendasi di atas:
Precision = 8/10.
Jadi presisinya = 80%

## Mean Absolute Error Plot
"""

plt.plot(history.history['mean_absolute_error'])
plt.plot(history.history['val_mean_absolute_error'])
plt.title('model_metrics')
plt.ylabel('mean_absolute_error')
plt.xlabel('epoch')
plt.legend(['mean_absolute_error', 'val_mean_absolute_error'])
plt.show()

"""Berdasarkan hasil _fitting_ nilai konvergen metrik MAE berada sedikit dibawah 0.135 untuk training dan sedikit diatas 0.1450 untuk validasi.

## Root Mean Squared Error Plot
"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['root_mean_squared_error', 'val_root_mean_squared_error'])
plt.show()

"""Berdasarkan hasil _fitting_ nilai konvergen metrik RMSE berada sedikit diatas 0.170 untuk training dan sedikit dibawah 0.190 untuk validasi.

NAMA : MUHAMMAD ALBAR

EMAIL : m502X1057@dicoding.org / albardirman@gmail.com

KELAS : MLFE (M08)

KAMPUS : UNIVERSITAS MEGAREZKY

ALAMAT : MAKASSAR
"""