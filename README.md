# RFM Segmentation — Lab (bukan karya portofolio)

> **Status: dihentikan dengan sadar.** Proyek ini saya buat untuk
> menguji kode, bukan untuk menjawab pertanyaan bisnis. Datanya
> sintetis dan tidak mendukung analisis yang saya coba lakukan.
> Detail di bagian "Limitasi".

## Pertanyaan yang ingin dijawab
Mengelompokkan pelanggan e-commerce ke segmen actionable
(siapa dijaga, siapa dikejar, siapa dilupakan) memakai RFM.

## Data
- 1.000 baris transaksi, 946 pelanggan unik
- Rentang: 2023-04-11 → 2023-06-10 (60 hari)
- Kolom: customer_id, purchase_date, transaction_amount,
  product, order_id, city

## Yang dibangun
`src/rfm.py` — tiga fungsi, sudah teruji dan siap dipakai ulang:
- `load()`      baca CSV + paksa tanggal jadi tipe datetime
- `build_rfm()` 1.000 struk → 1 baris per pelanggan
- `add_scores()` potong tiap metrik ke 5 kelompok sama rata

## Lima hal yang saya pelajari

1. **Tanggal harus dikonversi, bukan dipercaya.** Tanpa
   `pd.to_datetime`, `"2023-4-9"` dianggap lebih besar dari
   `"2023-4-11"` karena teks dibandingkan huruf per huruf.
   Hasilnya salah total — tanpa memunculkan error.

2. **Recency wajib diukur dari tanggal terakhir data**, bukan
   dari hari ini. Kalau pakai hari ini, seluruh pelanggan
   berumur "3 tahun tanpa belanja" dan tidak ada yang bisa
   dibedakan.

3. **`qcut` menolak angka kembar.** 946 pelanggan punya
   frequency = 1, yang membuat pembagian kuartil gagal.
   `rank(method='first')` jadi penyangganya.

4. **Kategori "Lainnya" bukan temuan, itu tempat sampah.**
   Ia selalu jadi kelompok terbesar karena menampung sisa
   aturan yang tidak cocok — di sini 378 dari 946 orang.

5. **Label bisa terlihat meyakinkan sambil kosong makna.**
   Ini yang paling mahal. Lihat di bawah.

## Limitasi — kenapa proyek ini saya hentikan

Frequency adalah salah satu dari tiga pilar RFM. Ini rata-rata
frequency tiap segmen yang saya buat:

| Segmen | Rata-rata frekuensi |
|---|---|
| Baru mampir sekali | 1,00 |
| Biasa saja | 1,02 |
| Kabur, dulu bagus | 1,07 |
| Pelanggan Emas | 1,15 |

Rentang keempat kelompok: **0,15.** Empat segmen yang saya
klaim berbeda ternyata orang yang sama, dihitung ulang.

Kode ini menghitung dengan benar (buktinya: segmen yang
syaratnya `frequency == 1` menghasilkan tepat 1,00). Yang
rusak bukan kodenya — datanya memang tidak punya informasi
itu. **Label tidak bisa diciptakan lewat `if` baru.**

## Keputusan
`src/rfm.py` saya simpan sebagai komponen siap pakai. Analisis
dilanjutkan pada dataset transaksi nyata yang memiliki
pelanggan berulang.

## Cara menjalankan
    pip install pandas
    python olah.py

## Yang akan saya ubah jika mengulang
Sebelum menulis kode, saya akan bertanya: hasil analisis ini nanti dipakai untuk memutuskan apa? Kalau jawabannya 
'mencari siapa yang harus dikirimi voucher bulan depan', maka 60 hari langsung tidak cukup — dan itu ketahuan sebelum sejam kode ditulis, bukan sesudah.
