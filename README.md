# My Portofolio

Nama: Adinda Pika Fauziah  
NPM: 2506533646  
Kelas: PBP F  

## Deskripsi

Website ini merupakan portfolio pribadi yang dibuat sebagai bagian dari pembelajaran mata kuliah
Pemrograman Berbasis Platform (PBP). 

Portfolio ini menampilkan informasi pribadi, pendidikan, dan pengalaman organisasi
serta kepanitiaan yang pernah saya tempuh atau ikuti. Pada Individual Assignment 1, saya mengembangkan website dari hasil Tutorial 01 dengan menambahkan section Education dan Experience yang masing-masing
menampilkan beberapa item dalam bentuk card.


### Tugas 1
1. Pada website ini saya menggunakan elemen semantik HTML5 seperti <main>, <section>, <article>, dan <footer> Elemen <section> digunakan untuk memisahkan bagian-bagian utama portfolio (Profile, Education, dan Experience). Sementara itu, <article> digunakan untuk menampilkan setiap item pendidikan dan pengalaman secara individual. Penggunaan elemen semantik membantu saya membuat struktur static web menjadi lebih jelas dan juga terorganisir. 


2. Tantangan utama dalam membuat responsive design adalah memastikan layout yang terlihat baik pada layar desktop & tetap nyaman digunakan pada layar yang lebih kecil. Pada desktop, bagian Profile menggunakan grid dengan dua kolom sehingga informasi dan foto dapat ditampilkan berdampingan. Namun, layout tersebut tidak cocok jika digunakan pada layar smartphone yang sempit. Untuk mengatasinya, saya menggunakan CSS Grid dan media query. Pada ukuran layar maksimal 600px, layout Profile diubah menjadi satu kolom dengan urutan identity, photo, kemudian details. Saya juga menggunakan auto-fit pada card grid agar jumlah kolom Education dan Experience dapat menyesuaikan lebar layar. Dalam mengevaluasi responsive design, saya memprioritaskan keterbacaan teks, ukuran foto, jarak antar elemen, serta memastikan card tidak melebihi lebar layar.


3. Karena website yang dibuat saat ini merupakan static web, informasi di dalamnya masih ditulis secara langsung pada HTML. Salah satu keterbatasannya adalah ketika saya ingin mengubah atau menambahkan banyak data, perubahan harus dilakukan secara manual pada file HTML. Pada iterasi berikutnya, saya ingin menambahkan untuk mengelola data portfolio, misalnya data pendidikan, pengalaman, dan proyek dapat disimpan dalam database dan ditampilkan secara dinamis menggunakan Django. Saya juga ingin mengembangkan bagian Projects sehingga proyek-proyek yang pernah dikerjakan dapat ditambahkan dan diperbarui tanpa harus mengubah struktur HTML secara manual.


### AI Disclosure
Dalam pengerjaan Individual Assignment 1 ini, saya menggunakan ChatGPT untuk membantu memahami instruksi tugas dan juga membantu mengidentifikasi dan memperbaiki beberapa masalah pada kode.

Saya tetap mengerjakan tugas dan menambahkan isi portfolio saya sendiri, termasuk menentukan informasi pendidikan dan pengalaman yang saya tmpilkan serta tampilan visual seperti warna, font, dan bentuk card.

Saya menggunakan AI terutama melalui percakapan bertahap seperti saya memberikan kode, hasil command pada terminal, atau masalah yang saya temukan, kemudian menggunakan saran yang diberikan untuk menentukan langkah berikutnya. 

Penggunaan AI membantu mempercepat proses debugging dan memberi pemahaman mengenai struktur HTML, CSS responsive, serta workflow Git. Namun, saya tetap perlu memeriksa hasil yang diberikan karena AI dapat memberikan saran yang tidak selalu sesuai dengan kondisi project saya. Contohnya, dalam proses pengerjaan saya menemukan masalah pada tampilan git diff di terminal dan kemudian menggunakan opsi --no-pager agar dapat memeriksa perubahan dengan lebih jelas.


### Tugas 2
Jawaban dari Pertanyaan Reflektif
1. Request dari URL akan diarahkan ke `urls.py`, lalu menuju view yang sesuai. View mengambil data dari model dan memasukkannya ke context, kemudian template menggunakan data tersebut untuk menghasilkan HTML yang ditampilkan ke user.

2. Supaya data dan tampilan tidak tercampur. Data bisa diubah atau ditambah melalui database tanpa harus mengubah HTML, sehingga kode lebih rapi dan mudah dikelola.

3. makemigrations digunakan untuk membuat file migration berdasarkan perubahan pada model. Sedangkan migrate digunakan untuk menerapkan migration tersebut ke database.

### AI Disclosure
Dalam pengerjaan tugas 02 ini, saya menggunakan ChatGPT sebagai alat bantu untuk debugging, menyusun unit test, dan memeriksa kelengkapan implementasi. Saya tetap melakukan implementasi, pengujian, dan verifikasi perubahan secara langsung pada project.

### Tugas 3
Jawaban dari pertanyaan reflektif Tugas 3

1. Kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara  manual karena bisa menghubungan form secara langsung dengan model, sehingga field form bisa dibuat berdasarkan field pada model & proses validasi dan juga penyimpanandata jadi lebih mudah.
Dengan ModelForm, kita ga perlu membuat field form HTML manual.
{%csrf_token %} ditambahkan pada form untuk membantu melindungi aplikasi dari cross site request forgery, serangan yang bisa membuat req tidak atas nama pengguna

2. Format data JSON lebih disukai (diabnding XML) karena formatnya lebih ringkas & lebih mudah dibaca serta diprose oleh aplikasi.

3. Saat view mengembalikan data portofolio dalam bentuk JSON, data dari model Django diambil dari database dulu. Setelah itu, data tersebut diubah dari  Django menjadi format JSson menggunakan proses serialization. JSON kemudian dikembalikan melalui HTTP response dengan tipe aplication/json. Serialization diperlukan karena model Django ga bisa langsung dikirim sebagai JSON, sehingga datanya perlu dikonversi ke format yang dapat dikirim melalui response dan diproses oleh aplikasi lain dulu