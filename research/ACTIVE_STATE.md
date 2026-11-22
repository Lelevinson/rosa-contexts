# Active state Carlene / krln

22 November 2026, Asia/Taipei. Keputusan dan hasil sekarang:

- **TERAMATI — kesalahan cakupan log pada diagnostik terarah.** A menerima kosong
  301–400 dari 400 baris lalu mengklaim seluruh file bebas ERROR, padahal ERROR50.
  B saksi ERROR350 dan C kosong lengkap 80 baris benar/didukung; D bersih 400
  benar faktual tetapi bukti ekornya tidak cukup. Satu episode per kondisi,
  instruksi awal ERROR/100 eksplisit; bukan rate umum atau baseline tanpa arahan.
  [Laporan gabungan log](summaries/log_coverage_20261122.md).
- **TERIMPLEMENTASI / TERUJI LOKAL — controller log riset.** Adapter coverage,
  full literal search dan status kode; UNKNOWN parsial memicu paling banyak satu
  full scan tambahan. Jalur sinkron invoke_log terintegrasi dengan ROSA asli;
  respons model/history tetap asli dan verified_answer dipisah. 29 tes prototipe
  serta 9 tes native lulus, provider 0. Plain invoke/astream tidak otomatis
  diperbaiki; provider nyata/efek model belum diuji. [Ringkasan prototipe](summaries/log_controller_prototype_20261122.md).
- **TERAMATI — stale observation dan reread baru.** Ada satu false-current claim
  CHANGED tanpa reread. Attempt reread awal NOT_EXPOSED karena infrastruktur;
  studi baru sesudah readiness/IPC diperbaiki menghasilkan STABLE/CHANGED yang
  benar dengan receipt kedua. Controller memaksa reread; bukan pilihan model,
  arm berpasangan atau bukti keunggulan Concord. [Rangkaian freshness](summaries/stale_observation_reread_20261122.md).
- **NO-GO klaim algoritmik — reuse/cakupan.** Kontrol interval/cache sederhana
  setara pada ruang lingkup screening. Temuan model dan prototipe engineering
  tidak mengubah keputusan novelty atau mengukur C1. [Screening awal](studies/log_coverage_20261121/SCREENING.md).
- **UNKNOWN empiris — laporan setelah aksi.** Dua ending tim belum terbukti
  sesudah goal terkirim; source loop/raw tidak tersedia saat audit. Tidak ada
  dasar mengubah status menjadi hasil eksperimen lokal. [Screening aksi](studies/action_stop_screening_20261121/REPORT.md).
- **DECIDED / PARKED — koreksi dua invoke.** Pada simulator yang diuji, instruksi
  lebih jelas sudah cukup. Pilot 0/3 beku, pengulangan 6/9 perilaku dan klarifikasi
  5/5 tetap terpisah; format JSON dan kondisi default parsial tidak dicampur.
  [Laporan gabungan](studies/carlene_two_invoke_context_20261120/REPORT.md).

Tidak ada klaim bahwa perbaikan controller membuktikan penalaran model lebih baik,
frekuensi salah telah diukur, atau source produksi sudah diubah. Full search direct
adalah pembanding sederhana yang sudah tersedia lokal; belum ada batch inference
pembanding atau alasan empiris baru untuk klaim algoritme lebih kompleks.

Lihat [indeks lengkap](STUDY_INDEX.md) untuk attempt gagal, label legacy,
protocol-only dan provenance. Studi/source/freeze lama dipertahankan; pembaruan
entry point dan laporan konteks dapat mengubah hash dokumen navigasi yang tercatat
pada freeze lama. Jangan menambal freeze atau mererun studi untuk menyiasatinya.

Publikasi 20 November dan screening 21 November tetap bagian histori member/krln.
Pembaruan 22 November menambahkan sintesis log/freshness/prototipe dan katalog,
bukan eksperimen baru. Manifest mirror mencatat waktu sinkronisasi, allowlist dan
hash per file; source utama masih untracked, sehingga HEAD saja bukan identitas
bytes dokumen. Raw/source tetap lokal, bukan tersimpan dalam snapshot konteks.
