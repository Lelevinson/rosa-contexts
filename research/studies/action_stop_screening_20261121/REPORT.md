# Screening laporan berbasis bukti setelah agent berhenti

21 November 2026, Asia/Taipei. **Status empiris UNKNOWN.** Catatan screening
read-only atas sumber yang dapat diakses, bukan laporan eksperimen aksi baru.
Dua ending belum terbukti terjadi setelah goal terkirim atau robot bergerak.

## Bukti yang diverifikasi dan batas akses

ROSA lokal main `d9991aad80d46b581150e85dff52f29d9619bce7`, evaluation main
`f35ed0962ba0c4c3e682185ebd98f535c436b37c`. Konteks Levinson dibaca pada
`70e61ae87e1e073ecee66d1906850fec23d90797`; krln sebelumnya
`576f6c03193a8f78fffd797a9296473228f6f21f`. Protokol main dibaca sebelum
manifest/important_missing_context, lalu START_HERE, ACTIVE_STATE dan indeks.
Head remote cocok saat investigasi read-only; tidak perlu mengganti branch.

Manifest mengecualikan Python dan raw trace. Source S1/S2, loop aksi, freeze,
RESULTS_LOG dan direktori raw run yang dirujuk tidak ditemukan pada workspace
lokal yang diperiksa. Source executor melalui GitHub pada source SHA manifest
`8ca6309ae95ca0ec477eb3790bde31904525e657` dan branch sumber mendapat 404.
Ini batas akses, bukan bukti source hanya ada di satu komputer.

Hash dokumen tim cocok dengan manifest saat investigasi: action-dev protocol
`5f899cbe3ce3e549ba23767ee146b24b2831bbe3e9440fc2598f253dd6ff050b`, report
`b9d40e564a535edbd3c642bfef0d5b6ea32f97aa99338c12a24421da38c64d53`.
Identitas dokumen terverifikasi; perilaku executor dan episode tidak terverifikasi
langsung dari source/raw. Tidak ada catatan audit raw aksi lokal yang ditemukan;
catatan ini mempertahankan batas investigasi sebelumnya, tanpa mengarang trace.

## Dilaporkan tim, bukan audit episode independen

Dokumen yang dibaca pada ref Levinson di atas (locator pada snapshot anggota itu):
`research/studies/action_dev_switch_20261118/{PROTOCOL.md,REPORT.md}`,
`research/studies/action_tool_s1_20261118/DESIGN.md`,
`research/studies/action_tool_s2_20261118/{REPORT_S2.md,PROTOCOL_SMOKE.md}`,
dan `research/decisions/2026-11-17-finish-gate-check.md`.
Ini locator teks, bukan tautan ke file dalam snapshot krln.

Protokol menyebut loop turtlesim mandiri turunan smoke_loop, bukan integrasi C1.
C1 utama dilaporkan memiliki menu read-only dan memblokir write tools. Kemampuan
aksi loop terpisah tidak boleh dialihkan sebagai kemampuan C1 yang terverifikasi.

Studi aksi: 8 tugas authored × 4 model × 2 seed × OFF/ON = 128 episode,
64 per arm. Success beku OFF 45/64, ON 47/64; class B switch. Laporan mencatat
rotate calls 94/95, goals sent 86/86, seluruh goal terkirim SUCCEEDED, nol lock,
dan satu ending cap/backend error per arm. Correction note 19 November dibaca;
kesalahan denominator wrapper di prose lama tidak digunakan. Statistik agregat
ini tidak menentukan apa yang terjadi dalam dua ending.

| Pertanyaan per ending | OFF | ON |
|---|---|---|
| Task/model | Belum diketahui | Belum diketahui |
| Model meminta aksi; goal benar-benar dikirim | Belum diketahui | Belum diketahui |
| Hasil executor; pose dan waktu sampel | Belum diketahui | Belum diketahui |
| Cap atau backend error; langkah berhenti | Belum diketahui | Belum diketahui |
| Keluaran yang akhirnya diterima pengguna | Belum diketahui | Belum diketahui |

Backend error dalam protokol termasuk HTTP/parsing backend model, bukan otomatis
TIMEOUT robot. Pembacaan evaluator setelah loop tidak membuktikan observasi itu
pernah tersedia bagi model/pengguna. Tidak ada task text, identitas episode atau
raw trace privat yang diterbitkan di catatan ini.

## Kontrak yang dilaporkan dan kontrol terkuat

Desain S1 membedakan validasi permintaan, pengiriman goal, penerimaan/status,
pembatalan dan lock. UNKNOWN_LOCKED adalah state executor, berbeda dari result
TIMEOUT. Status SUCCEEDED maupun target goal tidak membuktikan posisi akhir.
Sampel pose harus terikat robot/session dan waktu setelah goal terakhir;
memanggil observe_state setelah aksi belum menjamin waktu sampelnya juga baru.
Source tidak tersedia untuk memeriksa freshness maupun alur exception sebenarnya.

Kontrol terkuat: template deterministik dari event/status/timestamp/pose yang sama,
menampilkan hal diketahui dan belum diketahui, tanpa request model tambahan.
Contoh bersyarat berikut bukan rekonstruksi kedua episode:

| Bukti publik tersedia | Kandidat pelaporan | Template sederhana |
|---|---|---|
| REJECTED, tidak mengirim goal | Permintaan ini ditolak sebelum goal dikirim | Sama |
| SUCCEEDED, tanpa pose yang memenuhi syarat | Goal dilaporkan SUCCEEDED; pose akhir belum terverifikasi | Sama |
| TIMEOUT, pembatalan/berhenti terkonfirmasi | Deadline terlewati; pembatalan terkonfirmasi; pencapaian target belum dibuktikan | Sama |
| TIMEOUT + UNKNOWN_LOCKED | Hasil aksi/berhenti belum terkonfirmasi; aksi berikutnya diblokir | Sama |

Merangkum event/status belum memberi keputusan atau informasi berbeda. Jika
kandidat melakukan pembacaan atau reconciliation tambahan, kontrol harus mendapat
akses setara; native reads, waktu dan biaya tambahan harus dihitung.

## Overlap dan hipotesis

Finish gate meminta perbaikan ending model; laporan deterministik tidak perlu
request tambahan, tetapi kontrol template juga demikian. Temuan 25/33 bare-text
endings sudah supported dari 336 episode C1 adalah reported evidence pada populasi
lain. Post-action-state switch menambah observasi ke hasil tool saat loop berjalan;
menampilkan kembali observasi itu di laporan akhir belum menjadi mekanisme baru.

Metode primer yang dibaca saat investigasi:
[SafeActBench](https://arxiv.org/html/2610.07753v1) §§3–4 mengikat bukti ke entitas,
state dan urutan aksi; spesifikasi tersembunyi evaluator tidak boleh menjadi input
policy. [ECT](https://arxiv.org/html/2608.23623v1) memeriksa claim/receipt/scope/replay,
bergantung pada kontrak dan adapter tepercaya, bukan bukti posisi fisik.
[Evidence-Guided Recovery](https://arxiv.org/html/2610.41453v1) §§3–5 membedakan bukti
publik, efek aktual, pekerjaan tertunda dan handoff; memakai model transisi terbatas
yang dinyatakan, bukan kemampuan yang otomatis tersedia dari timeout robot.
Hasil paper tidak diaudit ulang atau dianggap hasil ROSA.

Hipotesis: aksi mungkin sudah terjadi tetapi pengguna kehilangan laporan berguna.
Dua ending yang dilaporkan belum membuktikannya. **Belum GO merancang tes.**
Jika hanya peringkasan event/status yang sama, klaim algoritmiknya NO-GO;
putusan empiris tetap UNKNOWN karena bukti penting tidak dapat diakses.

Bukti minimum pembuka kembali: source executor/backend/loop dan freeze yang tepat,
dua raw trace development terkait beserta hubungan request–goal–result–pose–ending,
dan keluaran yang benar-benar diterima pengguna. Semuanya perlu diaudit lokal;
raw trace tetap tidak dipublikasikan. Tidak ada eksperimen/model/robot baru.
