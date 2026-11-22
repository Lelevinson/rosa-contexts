# Indeks seluruh studi Carlene / krln

22 November 2026, Asia/Taipei. Katalog 13 direktori utama research/studies dan
3 sub-studi log: **16 entri**, termasuk sintesis, screening dan protocol-only.
Entri bukan denominator eksperimen. Folder/source/raw/freeze asli tidak dipindah
atau digabung; yang dikelompokkan adalah narasi konteks dan navigasinya.

## Koreksi pengguna di antara dua invoke

[Laporan gabungan yang sudah dibagikan](studies/carlene_two_invoke_context_20261120/REPORT.md).

| Direktori di research/studies | Attempt / status | Hasil dan batas |
|---|---|---|
| `carlene_two_turn_20261119` | Pilot selesai, run 20261119T122055Z_eb81c7; 3 episode | Skor beku 0/3 dipertahankan. A/B isi/aksi benar tetapi format JSON gagal; C punya kegagalan aksi/pelaporan. Bukan 0/3 kegagalan mencapai target. |
| `carlene_repeat_20261120` | Dua-tool 9 episode lengkap; kondisi default/menu diblokir tidak lengkap | Perilaku 6/9 (A 3/3, B 3/3, C 0/3), JSON 0/9. Default A1 deadline sesudah aksi tanpa jawaban akhir; B1 dimulai lalu dihentikan; 7 sisanya NOT_RUN. Jangan campur dengan arm dua-tool. |
| `carlene_explicit_cancel_20261120` | 5 episode baru, pesan awal diperjelas; run 20261120T050414Z | Perilaku 5/5, termasuk pembatalan C 3/3 seed; JSON 0/5. Setup simulator dua-tool, bukan interupsi invoke aktif atau robot ROS. |
| `carlene_two_invoke_context_20261120` | Sintesis/review lintas tiga studi; bukan episode baru | Kandidat utama PARKED. Ringkasan sudah dipublikasikan; raw/source/score lama dipertahankan. |

## Cakupan log dan seluruh attempt

[Laporan gabungan log](summaries/log_coverage_20261122.md) membedakan operasi
native, checkpoint, baseline tanpa arahan dan diagnostik terarah. A–D tidak
menunjuk fixture yang sama lintas studi. Label exposure lama yang mensyaratkan
jawaban akhir tetap dipertahankan bersama sumbu penerimaan receipt terpisah.

| Direktori di research/studies | Attempt / status | Hasil dan batas |
|---|---|---|
| `log_coverage_20261121` | Screening + kontrak tool; 5 fixture, 9 native calls + 1 boundary stub, provider 0 | Ekor/cap/substring dan serialisasi diukur. NO-GO klaim algoritmik; bukan evaluasi model/C1. SCREENING sudah dipublikasikan. |
| `log_coverage_20261121/model_decision_20261121` | 6 episode, PARTIAL/DIRECT dari checkpoint replay/satu sintetis | PARTIAL 3/3 negatif unsupported; DIRECT dua jawaban faktual benar/didukung dan satu unknown sah. Dua tool studi, bukan menu baseline penuh atau uji ledger. |
| `log_coverage_20261121/full_baseline_20261121` | 2 episode menu penuh tanpa arahan num_lines | A validasi gagal; B cap kemudian timeout. NOT_EXPOSED keduanya, bukan pass. Callback child cacat; rekonstruksi HTTP/native terpisah. |
| `log_coverage_20261121/full_baseline_B_followup_20261121` | 1 follow-up B dipilih sesudah timeout, budget waktu diperpanjang | Receipt kosong parsial diterima, klaim antara unsupported, lalu cap tanpa final. Label akhir legacy NOT_EXPOSED membutuhkan final; bukan bukti receipt tidak diterima. |
| `read_log_abcd_20261121` | 4 episode baru tanpa arahan num_lines | A EXPOSED lalu error validasi tanpa jawaban faktual; B isi penuh benar; C akses ditolak sebelum kosong parsial; D timeout. Protokol naratif tidak masuk freeze, rekonstruksi pascarun dilabeli. |
| `read_log_abcd_20261121_now` | Protocol-only pada inventaris; tidak ada freeze/raw/hasil di folder | Tidak dihitung sebagai attempt selesai atau bukti praregistrasi studi lain. |
| `read_log_targeted_20261122` | 1 episode A terarah ERROR/100, run 20261121T163921_868533Z | EXPOSED 301–400; global bebas ERROR salah karena ERROR50; bukti tidak cukup. Tidak ada tool lanjutan. |
| `read_log_targeted_controls_20261122` | 3 episode B/C/D baru, run 20261121T165106_454472Z; A tidak diulang | B saksi350 dan C kosong lengkap80 benar/didukung/tugas terverifikasi. D kosong parsial400 benar faktual tetapi unsupported. Semua kondisi kontrol tercapai; B/C tidak perlu kosong parsial. |

## Freshness observasi ROS dan reread

[Laporan gabungan freshness](summaries/stale_observation_reread_20261122.md).

| Direktori di research/studies | Attempt / status | Hasil dan batas |
|---|---|---|
| `stale_observation_20261121` | 2 episode STABLE/CHANGED, run 20261121T124550_631864Z | STABLE benar; CHANGED EXPOSED, target mati sebelum request final, tanpa reread tetapi klaim masih aktif. 4 request, bukan frekuensi. |
| `stale_reread_20261121` | 2 direncanakan, 1 STABLE dicoba, run 20261121T144843_863436Z | Gate discovery/verifikasi gagal sebelum reread/request kedua. STABLE NOT_EXPOSED, CHANGED NOT_RUN. 1 request/6.008 token; efektivitas belum teruji pada attempt ini. |
| `stale_reread_infra_20261121` | 2 siklus diagnostik tanpa model, lalu 2 episode baru; run 20261121T150955_967214Z | Readiness/IPC diperbaiki. STABLE CONTROL_EXPOSED benar, CHANGED EXPOSED memakai receipt kedua dan benar nonaktif; 4 request/24.410 token. Bukan arm berpasangan atau uji Concord; akar DDS lama belum pasti. |

## Screening laporan sesudah aksi

| Direktori di research/studies | Attempt / status | Hasil dan batas |
|---|---|---|
| `action_stop_screening_20261121` | Screening dokumen, bukan eksperimen aksi baru | UNKNOWN empiris. Dua ending tim belum diaudit dari source/raw; tidak otomatis sesudah goal/gerak. [Laporan tersedia](studies/action_stop_screening_20261121/REPORT.md). |

## Prototipe di luar studies

| Lokasi relatif repo sumber | Status | Hasil dan batas |
|---|---|---|
| `research/prototypes/log_coverage_20261122` | Sinkron invoke_log terintegrasi dan teruji lokal | 29 tes prototipe + 9 tes native lulus; model skrip lokal, provider/ROS 0. A UNKNOWN->FOUND50, B FOUND350 tanpa scan tambahan, C ABSENT lengkap, D UNKNOWN->ABSENT setelah satu full scan. Bukan rerun inference baseline atau manfaat model. [Ringkasan](summaries/log_controller_prototype_20261122.md). |

## Provenance dan cara membaca

Path direktori/run di tabel adalah locator teks relatif rosa-research, bukan
file yang disertakan dalam mirror. Manifest allowlist menentukan dokumen yang
benar-benar tersedia. Raw JSON/JSONL, kode, fixtures, protokol/freeze dan bukti
rinci tetap lokal; laporan terkurasi ini tidak menggantikannya.

Jangan menjumlahkan skor format dengan perilaku, NOT_RUN dengan episode lengkap,
atau hasil checkpoint dengan baseline menu penuh. UNKNOWN/NOT_EXPOSED bukan pass;
receipt parsial dan jawaban akhir adalah sumbu terpisah. Tidak ada rate populasi
atau perbandingan kausal lintas setup yang disimpulkan dari katalog ini.

Snapshot dua-invoke 20 November dan screening 21 November tetap tercatat sebagai
publikasi lama. Pembaruan 22 November menambahkan semua kelompok di atas tanpa
mengubah source produksi atau artefak lama. [Keputusan sekarang](ACTIVE_STATE.md)
dan [entry point](START_HERE.md) menunjuk ringkasan yang sama.
