# Laporan Proyek Machine Learning - Muhammad Albar

## Project Overview
Domain proyek yang dipilih dalam proyek _machine learning_ ini adalah mengenai hiburan dengan judul proyek _"Movie Recommendation System"_.

**Latar Belakang**

Hiburan merupakan kebutuhan terbelakang manusia, mengapa demikian? Karena hiburan bukanlah sebuah kebutuhan pokok yang wajib dipenuhi oleh setiap manusia, begitulah pikir orang terdahulu. Seiring berjalannya waktu orang-orang mulai menganggap hiburan merupakan sebuah kebutuhan yang wajib dipenuhi oleh setiap orang. Terutama semenjak memasuki abad 21, di mana terjadi perkembangan yang pesat pada dunia hiburan. Khususnya pada dunia pertelevisian dan film. Dari era televisi hitam putih, hingga menginjak ke era warna-warni. Bahkan mulai bermunculan televisi hologram dan layanan _streaming_ yang disesuaikan dengan kesukaan pengguna. Penggunaan layanan _streaming_ saat ini meningkat cukup pesat. Dan baru-baru ini pun semakin meningkat akibat pandemi yang berkepanjangan ini.

Dari latar belakang itulah penulis mengambil topik ini sebagai domain proyek _machine learning_ yang penulis kerjakan. Selain dari latar belakang diatas, tujuan lain dibuatnya proyek _machine learning_ ini ialah membuat sebuah model untuk proyek aplikasi yang sedang penulis kembangkan. Diharapkan model ini nantinya akan berguna pada aplikasi yang penulis kembangkan dan mendapatkan hasil keluaran berupa aplikasi yang berkualitas sesuai dengan yang penulis harapkan.

## Business Understanding
Sistem rekomendasi adalah suatu aplikasi yang digunakan untuk memberikan rekomendasi dalam membuat suatu keputusan yang diinginkan pengguna. Untuk meningkatkan _user experience_ dalam menemukan judul film yang menarik dan yang sesuai dengan yang pengguna inginkan, maka sistem rekomendasi adalah pilihan yang tepat untuk diterapkan. Dengan adanya sistem rekomendasi, _user experience_ tentu akan lebih baik karena pengguna bisa mendapatkan rekomendasi judul film yang ingin diharapkan.

### Problem Statement
Berdasarkan pada latar belakang di atas, permasalahan yang dapat diselesaikan pada proyek ini adalah sebagai berikut:
-   Bagaimana cara melakukan pengolahan data yang baik sehingga dapat digunakan untuk membuat model sistem rekomendasi yang baik?
-   Bagaimana cara membangun model _machine learning_ untuk merekomendasikan sebuah film yang mungkin disukai pengguna?

### Goal
Tujuan dibuatnya proyek ini adalah sebagai berikut:
-   Melakukan pengolahan data yang baik agar dapat digunakan dalam membangun model sistem rekomendasi yang baik.
-   Membangun model _machine learning_ untuk merekomendasikan sebuah film yang kemungkinan disukai pengguna.


### Solution
Untuk menyelesaikan masalah ini, penulis akan menggunakan 2 solusi algoritma yaitu _content-based filtering_ dan _collaborative filtering_. Berikut adalah penjelasan teknik-teknik yang akan digunakan untuk masalah ini:
* _Content-Based Filtering_ merupakan cara untuk memberi rekomendasi bedasarkan genre atau fitur pada item yang disukai oleh pengguna. _Content-based filtering_ mempelajari profil minat pengguna baru berdasarkan data dari objek yang telah dinilai pengguna.
* _Collaborative Filtering_ merupakan cara untuk memberi rekomendasi bedasarkan penilaian komunitas pengguna atau biasa disebut dengan *rating*. _Collaborative filtering_ tidak memerlukan atribut untuk setiap itemnya seperti pada sistem berbasis konten.

## Data Understanding

- **Informasi Dataset**
  <br> Dataset yang digunakan pada proyek ini yaitu dataset film lengkap dengan genre dan rating, informasi lebih lanjut mengenai dataset tersebut dapat lihat pada tabel berikut:

  | Jenis                   | Keterangan                                                                              |
  | ----------------------- | --------------------------------------------------------------------------------------- |
  | Sumber                  | Dataset: [Kaggle](https://www.kaggle.com/sunilgautam/movielens) |
  | Dataset Owner           | Sunil Gautam                                                                           |
  | Lisensi                 | -                                                                                       |
  | Kategori                | Movies & TV Shows                                                                     |
  | Usability               | 5.3                                                                                       |
  | Jenis dan Ukuran Berkas | ZIP (3.3 MB)                                                                           |
  | Jumlah File Dataset     | 4 File (CSV)                                                                           |

  <br> Berikut ini file dataset
  * links.csv
  * ratings.csv
  * movies.csv
  * tags.csv

  Pada proyek ini penulis hanya menggunakan 2 file dataset yaitu:
  1. *movies.csv*
      <br> *Jumlah Data 9742, dan memiliki 3 kolom*
      <br> Untuk penjelasan mengenai variabel-variabel pada dataset dapat dilihat pada poin-poin berikut ini:
      * `movieId`: ID dari film
        <br>movieId memiliki 9742 data unik.
      * `title`: Judul dari film
        <br>title memiliki 9737 data unik.
      * `genres`: Genre dari film
        <br>genres memiliki 951 data unik.

  2. *ratings.csv*
      <br> *Jumlah Data 100836, dan memiliki 4 kolom*
      <br> Untuk penjelasan mengenai variabel-variabel pada dataset dapat dilihat pada poin-poin berikut ini:
      * `userId`: ID pengguna pemberi rating
        <br>userId  memiliki 610 data unik.   
      * `movieId`: ID film yang di rating
        <br>movieId memiliki 9724 data unik.
      * `rating`: Rating dari film
        <br>rating memiliki 10 data unik. dengan range 0 - 5 dan skala 0.5
      * `timestamp` = Waktu rating terekam
        <br>timestamp memiliki 85043 data unik.
      
- **Sebaran atau Distribusi Data pada Fitur yang Digunakan**

  Berikut merupakan visualisasi data yang menunjukkan sebaran/distribusi data pada beberapa variabel yang akan penulis gunakan nanti:
  
  Distribusi tahun rilis film:

  ![Distribusi Tahun Rilis](https://raw.githubusercontent.com/barbarianking88/ProyekAkhirMLT/main/images/tahun_rilis.png)
  Gambar 1. Distribusi sebaran Tahun Rilis film

  Dapat dilihat pada grafik di atas rata-rata rilis sebuah film berkisar antara tahun 1990-2000 ke atas, distribusi terbanyak terjadi di atas tahun 2000, di mana distribusi film cenderung mengalami kenaikan secara signifikan setiap berjalannya waktu.

  Distribusi total jumlah genre:

  ![Distribusi Genre](https://raw.githubusercontent.com/barbarianking88/ProyekAkhirMLT/main/images/genre.png)
  Gambar 2. Distribusi sebaran genre film

  Terlihat pada gambar di atas ada 20 kategori atau genre di dalam data ini. genre `Drama` yang paling banyak dan diikuti oleh genre `Comedy` lalu ada beberapa film yang tidak memiliki genre `no genres listed`
  
  10 film yang memiliki _rating_ tertinggi:

  ![Top Rating](https://raw.githubusercontent.com/barbarianking88/ProyekAkhirMLT/main/images/top_ten.png)
  Gambar 3. Distribusi Sebaran rating dari 10 film tertinggi

  Terlihat pada grafik, bahwa film yang memiliki _rating_ tertinggi adalah **Forrest Gump** yang rilis pada tahun 1994

## Data Preparation
Data preparation diperlukan untuk mempersiapkan data agar ketika nanti dilakukan proses pengembangan model diharapkan akurasi model akan semakin baik dan meminimalisir terjadinya bias pada data. Berikut ini merupakan tahapan-tahapan dalam melakukan pra-pemrosesan data:
 - **Melakukan Penanganan _Missing Value_**
    <br> Penanganan yang penulis lakukan pada _missing value_ yaitu dengan melakukan drop data. Tetapi karena dataset yang digunakan cukup bersih, _missing value_ hanya terdapat ketika proses penggabungan dataset.
 
 - **Melakukan _Sorting_ Data Rating berdasarkan ID Pengguna**
    <br> Melakukan pengurutan data _rating_ berdasarkan ID Pengguna agar mempermudah dalam melakukan penghapusan data duplikat nantinya.

 - **Menghapus Data Duplikat**
    <br> Melakukan penghapusan data duplikat agar tidak terjadi bias pada data nantinya.

 - **Melakukan penggabungan Data**
    <br> Melakukan penggabungan data yang sudah diolah sebelumnya untuk membangun model. lalu menghapus data yang memiliki _missing value_ pada variabel genre dan melihat jumlah data setelah digabungkan, terlihat data memiliki 100830 baris dengan 5 kolom.
    
 - **Melakukan Normalisasi Nilai Rating**
    <br> Untuk menghasilkan rekomendasi yang sesuai dan akurat maka pada tahap ini diperlukan sebuah normalisasi pada data nilai _rating_ dengan menggunakan formula MinMax pada data rating sebelum memasuki tahap modelling.
    
 - **Melakukan Splitting Dataset**
    <br> Untuk melatih model maka penulis perlu melakukan pembagian dataset latih dan juga dataset validasi, untuk dataset latih penulis berikan 80% dari total keseluruhan jumlah data sedangkan dataset validasi sebesar 20% dari keseluruhan data. Hal ini diperlukan untuk pengembangan pada model _Collaborative Filtering_ nantinya.

## Modeling and Result
Pada proyek ini, Proses modeling dalam proyek ini menggunakan metode *Neural Network* dan *Cosine Similarity*. Model *Deep Learning* akan penulis gunakan untuk Sistem Rekomendasi berbasis `Collaborative Filtering` yang mana model ini akan menghasilkan rekomendasi untuk satu pengguna. *Cosine Similarity* akan penulis gunakan untuk Sistem Rekomendasi berbasis `Content-Based Filtering` yang akan menghitung kemiripan antara satu film dengan lainnya berdasarkan fitur yang terdapat pada satu film. Berikut penjelasan tahapannya:

### Content Based Filtering
Pada modeling `Content Based Filtering`, langkah pertama yang dilakukan ialah penulis menggunakan TF-IDF Vectorizer untuk menemukan representasi fitur penting dari setiap genre film. Fungsi yang penulis gunakan adalah tfidfvectorizer() dari library sklearn. Selanjutnya penulis melakukan fit dan transformasi ke dalam bentuk matriks. Keluarannya adalah matriks berukuran (9737, 23). Nilai 9737 merupakan ukuran data dan 23 merupakan matriks genre film.

Untuk menghitung derajat kesamaan (_similarity degree_) antar movie, penulis menggunakan teknik _cosine similarity_ dengan fungsi _cosine_similarity_ dari _library_ sklearn. Berikut dibawah ini adalah rumusnya:

![Rumus Cosine Similarity](https://camo.githubusercontent.com/8d30a8f1b354dfa7fab96839c43c2288d5640f651d822eaca2a430e1fd716fdb/68747470733a2f2f69302e77702e636f6d2f68656e64726f707261736574796f2e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032302f30342f696d6167652d332e706e673f726573697a653d3430372532433131302673736c3d31)
Gambar 4. Rumus Cosine Similarity

Langkah selanjutnya yaitu menggunakan _argpartition_ untuk mengambil sejumlah nilai k tertinggi dari _similarity_ data kemudian mengambil data dari bobot (tingkat kesamaan) tertinggi ke terendah. Kemudian menguji akurasi dari sistem rekomendasi ini untuk menemukan rekomendasi movies yang mirip dari film yang ingin dicari.

- Kelebihan
  - Semakin banyak informasi yang diberikan pengguna, semakin baik akurasi sistem rekomendasi.

- Kekurangan
  - Hanya dapat digunakan untuk fitur yang sesuai, seperti film, dan buku.
  - Tidak mampu menentukan profil dari user baru.

Berikut ini adalah konten yang dijadikan referensi untuk menentukan 10 rekomendasi film tertinggi yang memiliki kesamaan genre yang sama:

| movieId |                 title |           genres |
|--------:|----------------------:|-----------------:|
| 6338    | Daddy day care (2003) | Children\|Comedy |

Terlihat pada tabel diatas bahwasannya saya akan menguji coba model berdasarkan judul film "Daddy Day Care (2003)" dengan genre Children & Comedy.

Berikut ini adalah hasil rekomendasi tertinggi dari model _Content Based Filtering_ berdasarkan referensi film diatas:

|                                 title | movieId |           genres |
|--------------------------------------:|--------:|-----------------:|
| Cat in the Hat, The (2003)            | 6951    | Children\|Comedy |
| Blank Check (1994)                    | 2036    | Children\|Comedy |
| Home Alone 2: Lost in New York (1992) | 2953    | Children\|Comedy |
| Air Bud: Golden Receiver (1998)       | 2152    | Children\|Comedy |
| Blackbeard's Ghost (1968)             | 2035    | Children\|Comedy |
| Madeline (1998)                       | 1919    | Children\|Comedy |
| Paddington (2014)                     | 117887  | Children\|Comedy |
| Love Bug, The (1969)                  | 1010    | Children\|Comedy |
| Ernest Rides Again (1993)             | 69227   | Children\|Comedy |
| Son of Flubber (1963)                 | 2098    | Children\|Comedy |

### Collaborative Filtering
Pada modeling `Collaborative Filtering` penulis menggunakan data hasil gabungan dari dua datasets yaitu *movies.csv* & *ratings.csv*. Langkah pertama adalah melakukan _encode_ data `userId` & `movieId` setelah di _encode_ lakukan _mapping_ ke dalam data yang digunakan dan juga mengubah nilai _rating_ menjadi _float_. Selanjutnya ialah membagi data untuk _training_ sebesar 80% dan validasi sebesar 20%.

Lakukan proses _embedding_ terhadap data film dan pengguna. Lalu lakukan operasi perkalian _dot product_ antara _embedding_ pengguna dan film. Selain itu, penulis juga menambahkan bias untuk setiap pengguna dan film. Skor kecocokan ditetapkan dalam skala [0,1] dengan fungsi aktivasi _sigmoid_. Untuk mendapatkan rekomendasi film, penulis mengambil sampel user secara acak dan mendefinisikan variabel _movie_not_watched_ yang merupakan daftar film yang belum pernah ditonton oleh pengguna.

- Kelebihan
  - Tidak memerlukan atribut untuk setiap itemnya.
  - Dapat membuat rekomendasi tanpa harus selalu menggunakan dataset yang lengkap.
  - Unggul dari segi kecepatan dan skalabilitas.
  - Rekomendasi tetap akan berkerja dalam keadaan dimana konten sulit dianalisi sekalipun

- Kekurangan
  - Membutuhkan parameter rating, sehingga jika ada item baru sistem tidak akan merekomendasikan item tersebut.

Berikut ini adalah hasil rekomendasi film tertinggi terhadap user 606:

| Showing recommendations for users: 606            |
|---------------------------------------------------|
| Movie with high ratings from user                 |
| ------------------------------------------------- |
| Pulp Fiction (1994)                               |
| Manhattan (1979)                                  |
| Metropolis (1927)                                 |
| All About My Mother (Todo sobre mi madre) (1999)  |
| Guess Who's Coming to Dinner (1967)               |
| ------------------------------------------------- |
| Top 10 movie recommendation                       |
| ------------------------------------------------- |
| Raging Bull (1980)                                |
| Boot, Das (Boat, The) (1981)                      |
| Sevent Seal, The (Sjunde inseglet, Det) (1957)    |
| Glory (1989)                                      |
| Touch of Evil (1958)                              |
| Chinatown (1974)                                  |
| Evil Dead II (Dead by Dawn) (1987)                |
| Great Escape, The (1963)                          |
| Unforgiven (1992)                                 |
| Manchurian Candidate, The (1962)                  |

## Evaluation
Evaluasi yang akan penulis lakukan disini yaitu evaluasi dengan Mean Absolute Error (MAE) dan Root Mean Squared Error (RMSE) pada Collaborative Filtering dan Precision Content Based Filtering

### Content Based Filtering
Pada evaluasi model ini penulis menggunakan metrik precision content based filtering untuk menghitung precision model sistem telah dibuat sebelumnya. Berikut ini adalah hasil analisisnya:

Precision Metric Formula:

![Precision Formula](https://raw.githubusercontent.com/barbarianking88/ProyekAkhirMLT/main/images/precision_formula.png)
Gambar 5. Precision Metric Formula

Precision Metric Test:

| movieId |           title |                         genres |
|--------:|----------------:|-------------------------------:|
| 292     | Outbreak (1995) | Action\|Drama\|Sci-Fi-Thriller |

![MovieRecommendation](https://raw.githubusercontent.com/barbarianking88/ProyekAkhirMLT/main/images/MovieRecommendation.PNG)
Gambar 6. MovieRecommendation

|                                 title | movieId |                          genres |
|--------------------------------------:|--------:|--------------------------------:|
| Core, The (2003)                      |   6264  | Action\|Drama\|Sci-Fi\|Thriller |
| 2012 (2009)                           |  72378  | Action\|Drama\|Sci-Fi\|Thriller |
| Doomsday (2008)                       |  58297  | Action\|Drama\|Sci-Fi\|Thriller |
| Star Trek: Nemesis (2002)             |   5944  | Action\|Drama\|Sci-Fi\|Thriller |
| Omega Man, The (1971)                 |   3032  | Action\|Drama\|Sci-Fi\|Thriller |
| Impostor (2002)                       |   5046  | Action\|Drama\|Sci-Fi\|Thriller |
| Rise of the Planet of the Apes (2011) |  88744  | Action\|Drama\|Sci-Fi\|Thriller |
| Battlestar Galactica: Razor (2007)    |  56921  | Action\|Drama\|Sci-Fi\|Thriller |
| X-Men: The Last Stand (2006)          |  45499  | Action\|Drama\|Sci-Fi\|Thriller |
| Paycheck (2003)                       |   7163  | Action\|Drama\|Sci-Fi\|Thriller |

Langkah pertama adalah melakukan pengecekan data film berdasarkan title. Dapat dilihat bahwa judul film Outbreak (1995) memiliki 4 genre yaitu Action, Drama, Sci-Fi, dan Thriller. Lalu dari hasil rekomendasi di atas, diketahui bahwa Outbreak (1995) memiliki 4 genre. Dari 10 item yang direkomendasikan, 8 item memiliki kategori 4 genre yang sama (similar). Artinya, precision sistem kita sebesar 8/10 atau sebesar 80%.

### Collaborative Filtering
| _Mean Absolute Error (MAE)_ | _Root Mean Squared Error (RMSE)_ |
| --------------------------- | -------------------------------- |
| Mengukur besarnya rata-rata kesalahan dalam serangkaian prediksi yang sudah dilatih kepada data yang akan dites, tanpa mempertimbangkan arahnya. Semakin rendah nilai MAE (_Mean Absolute Error_) maka semakin baik dan akurat model yang dibuat. | Adalah aturan penilaian kuadrat yang juga mengukur besarnya rata-rata kesalahan. Sama seperti MAE, semakin rendahnya nilai _root mean square error_ juga menandakan semakin baik model tersebut dalam melakukan prediksi. |
| Formula _Mean Absolute Error (MAE)_ | Formula _Root Mean Squared Error (RMSE)_ |
| ![MAE](https://gisgeography.com/wp-content/uploads/2014/08/mae-formula.png) | ![RMSE](https://1.bp.blogspot.com/-MM7g3UQjW9s/X8JzKPlxfQI/AAAAAAAACX0/zNDQCP4CJWANa1Bh_zBoLBCCOuUnCXKigCPcBGAYYCw/s16000/Rumus%2BRMSE.jpg) |
| Visualisasi _Mean Absolute Error (MAE)_ | Visualisasi _Root Mean Squared Error (RMSE)_ |
| ![Plot MAE](https://raw.githubusercontent.com/barbarianking88/ProyekAkhirMLT/main/images/mae.png)
Gambar 7. Plot MAE | 
![Plot RMSE](https://raw.githubusercontent.com/barbarianking88/ProyekAkhirMLT/main/images/rmse.png) |
Gambar 8. Plot RMSE
| Berdasarkan hasil _fitting_ nilai konvergen metrik MAE berada sedikit dibawah 0.135 untuk training dan sedikit diatas 0.1450 untuk validasi. | Berdasarkan hasil _fitting_ nilai konvergen metrik RMSE berada sedikit diatas 0.170 untuk training dan sedikit dibawah 0.190 untuk validasi. |

Untuk menghasilkan nilai yang konvergen proses `fitting` memerlukan 15 _epoch_. Dari hasil perhitungan kedua metrik diatas dapat disimpulkan bahwa model ini memiliki tingkat eror di bawah 20%.
