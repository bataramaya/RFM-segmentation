# RFM Segmentation — karya portofolio

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



# RFM Segmentation —  portfolio piece

> **Status: stopped on purpose.** I built this to test code, not to
> answer a business question. The dataset cannot support the analysis
> I attempted — details under "Limitations".

## Question I set out to answer
Group e-commerce customers into actionable segments: who to protect,
who to win back, who to stop paying attention to.

## Data
- 1,000 transaction rows, 946 unique customers
- Window: 2023-04-11 → 2023-06-10 (60 days)
- Columns: customer_id, purchase_date, transaction_amount,
  product, order_id, city

## What I built
`src/rfm.py` — three functions, tested and reusable:
- `load()`       read CSV, force dates into datetime
- `build_rfm()`  1,000 receipts → one row per customer
- `add_scores()` split each metric into five equal-sized groups

## Five things I learned

1. **Dates must be converted, not trusted.** Without `pd.to_datetime`,
   `"2023-4-9"` compares as *greater than* `"2023-4-11"` because
   strings are compared character by character. Wrong result,
   no error raised.

2. **Recency must be measured from the last date in the data**, not
   from today. Using today makes every customer "3 years inactive"
   and destroys all separation between them.

3. **`qcut` rejects duplicate values.** 946 customers had
   frequency = 1, which broke quartile binning.
   `rank(method='first')` is the workaround.

4. **"Other" is not a finding — it's a dumping ground.** It became the
   largest group (378 of 946) purely because it collected everything
   that failed the earlier rules.

5. **A label can look convincing while meaning nothing.** The most
   expensive lesson here. See below.

## Limitations — why I stopped this project

Frequency is one of the three pillars of RFM. Here is the average
frequency inside each segment I created:

| Segment | Avg. frequency |
|---|---|
| New, one-time | 1.00 |
| Average | 1.02 |
| Lapsed, previously strong | 1.07 |
| Champion | 1.15 |

Total spread across four segments: **0.15.** The four groups I claimed
were behaviourally distinct are the same customer, counted again.

The code computed correctly — evidence: the segment whose rule is
`frequency == 1` returned exactly 1.00. What was broken was not the
code. The data simply held no such signal. **You cannot author a label
into existence with another `if` statement.**

Sanity check: segment counts sum to 946, matching unique customers —
no rows were silently dropped.

## Decision
`src/rfm.py` is kept as a tested, reusable component. The analysis
continues on a real transactional dataset with genuine repeat
customers.

## Run it
    pip install pandas
    python olah.py

## [What I would change next time]
> *"Before writing any code, I would ask: what decision is this output
> meant to serve? If the answer is 'how often do customers actually
> come back', then 60 days is immediately insufficient — the median
> repeat-purchase gap alone needs a longer window than the whole
> dataset. That is knowable in 2 minutes, not 40."*
