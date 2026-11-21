# Screening cakupan pencarian log

21 November 2026, Asia/Taipei. **NO-GO untuk klaim algoritmik pada scope sekarang.**
Perbaikan API/tool masih merupakan peluang engineering. Ini screening dan audit
artefak diagnostik tersimpan, bukan pengukuran keberhasilan C1 atau run baru.

## Pertanyaan dan kontrol

Untuk satu log dengan snapshot tetap, rentang inklusif dan predikat eksplisit,
bisakah bukti baca yang sudah tersedia mengurangi pekerjaan menjawab “ada/tidak”?
Saksi positif yang sah cukup untuk “ada”. “Tidak ada” membutuhkan cakupan lengkap
untuk rentang dan predikat yang sesuai; hasil gagal/terpotong tidak cukup.

Kontrol utama: C1 dengan pencarian langsung seluruh rentang, hasil ringkas dan
metadata cakupan. Kontrol sederhana terbaik juga boleh cache bukti/bytes,
menggabungkan interval kompatibel, membaca celah, dan melaporkan keterbatasan.
Akses, metadata, backend dan batas biaya harus sama; evaluator tidak memberi jawaban.

Contoh konseptual sintetis: bukti lengkap tanpa ERROR pada 1–150 dan 251–400
menyisakan 151–250. Kandidat dan kontrol terbaik sama-sama mencari celah itu.
Versi/filter berbeda tidak digabung menjadi bukti negatif. Tidak ada keputusan
berbeda yang mendukung klaim algoritmik. Contoh ini bukan replay eksekusi celah;
API native saat ini tidak mendukung rentang awal–akhir tersebut.

## Diverifikasi dari source dan raw diagnostik lokal

ROSA main `d9991aad80d46b581150e85dff52f29d9619bce7`; evaluation main
`f35ed0962ba0c4c3e682185ebd98f535c436b37c`. Pada `src/rosa/tools/log.py:58`,
`readlines()` memuat seluruh file. Tool mengambil ekor, menolak bagian lebih dari
200 baris sebelum filter, lalu mencocokkan substring tanpa membedakan kapital.
Tidak ada argumen rentang awal–akhir. Registrasi tool, executor stok dan formatter
LangChain lokal diperiksa; jalur ke input model stub diuji dalam run tersimpan.

Run `tool_20261121T065237_786044Z`: 5 fixture sintetis, 9 calls langsung,
dan 1 call pemeriksaan boundary dengan dua invokasi stub. Hash input dalam freeze
cocok saat audit publikasi; source diagnostik dan raw JSON dibaca, tanpa rerun.

| Kasus | Observasi | Batas kesimpulan |
|---|---|---|
| ERROR baris 50 pada file 400 | Ekor 100 menguji 301–400, mengembalikan nol kecocokan; 400 baris/6.401 byte tetap dimuat | Belum mendukung negatif 1–400; hasil JSON untuk stub 236 byte |
| Ekor 200 pada file yang sama | Menguji 201–400, kosong; tetap memuat seluruh file | Prefix belum dicari |
| Seluruh 200 baris bersih | Filter mencakup 1–200, kosong | Negatif lengkap hanya untuk 1–200 |
| Ekor tersedia lalu akses ditolak | Ekor kosong; open berikutnya PermissionError sintetis | Rentang di luar ekor belum dapat dipastikan |
| Seluruh 400, termasuk kontrol bersih | File dimuat, hasil ditolak sebelum filter karena batas 200 | Error bukan bukti negatif |
| INFO error_count=0 | Cocok filter substring ERROR | Bukan bukti severity ERROR |

Total kedua bagian: 10 calls skrip, 10 percobaan open, 9 open/readlines berhasil,
3.020 baris/48.334 byte dimuat ke Python. Sembilan calls langsung memuat 2.620
baris/41.933 byte dengan wall tool 3,629 ms; executor stub terpisah 2,924 ms.
Provider requests 0, tool calls diminta model nyata 0, operasi native ROS 0.
Token, latency C1 dan I/O disk fisik tidak diukur. Setup/hash/oracle terpisah
 dari biaya tool. Kesimpulan tabel ialah audit kontrak, bukan skor jawaban model.

## Dilaporkan tim dan batas akses

Konteks Levinson `70e61ae87e1e073ecee66d1906850fec23d90797`:
canonical rendering live melaporkan 127/144 vs 125/144 supported (class B);
dead-end lookup melaporkan class C atas harm flag look-alike, bukan pengamatan
model benar-benar tersesat. Angka ini tidak diaudit ulang dari raw tim.
Source executor dan raw development C1 tidak tersedia di workspace yang diperiksa;
ref source yang dirujuk manifest tidak dapat diakses melalui GitHub saat screening.
Tidak diverifikasi bahwa backend C1 identik dengan tool lokal. Tidak ada klaim
C1 pernah menjawab salah pada fixture di atas.

## Mekanisme terdekat dan keputusan

Penggabungan cakupan adalah penerapan sempit penalaran kelengkapan data;
[query completeness](https://www.vldb.org/pvldb/vol4/p749-razniewski.pdf) membahas
inferensi dari bagian yang dinyatakan lengkap. [ECT](https://arxiv.org/html/2608.23623v1)
memeriksa receipt, scope dan replay claim. Metode/batas dibaca saat screening;
kebenaran jaminan bergantung pada kontrak/adaptor, bukan sekadar hash atau status.
Tidak ada klaim novelty atau hasil ROSA yang diwarisi dari paper.

Hipotesis engineering: pencarian ringkas dengan snapshot/predikat jelas dapat
memperbaiki kontrak. Mengurangi domain filter belum tentu mengurangi I/O;
backend readlines tetap memuat seluruh file, cache bytes yang sama tersedia bagi
kedua policy, dan biaya index/setup harus dihitung. Manfaat C1 belum diukur.

## Penunjuk bukti yang tetap lokal

Semua path berikut adalah locator teks relatif terhadap repo sumber rosa-research,
bukan tautan yang tersedia di snapshot: `research/studies/log_coverage_20261121/`:
`REPORT.md`, `PROTOCOL.md`, `diagnose.py`, `FREEZE.json`, `ORACLE.json`,
`REUSE_EXAMPLE.json`, `C1_AVAILABILITY.json`, `fixtures/`, serta
`runs/tool_20261121T065237_786044Z/{RESULTS.json,SUMMARY.json,MODEL_BOUNDARY_STUB.json}`.
Source tool SHA-256: `87c86928fba283cb66e35b01f88f6bb15b2a5e4ef37c985c84c2a2c0a860f77c`.
Laporan rinci dan artefak beku tidak diedit untuk publikasi.
Pembaruan dokumentasi entry point pada 21 November mengubah file yang turut
tercatat dalam baseline pra-studi; preflight runner lama akan menolaknya.
Itu bukan perubahan input diagnostik atau alasan menambal freeze/rerun otomatis.
