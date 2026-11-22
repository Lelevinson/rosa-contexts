# Context penelitian Carlene / krln

22 November 2026, Asia/Taipei. Mulai dari [keputusan sekarang](ACTIVE_STATE.md),
lalu [indeks seluruh studi](STUDY_INDEX.md). Snapshot ini mengelompokkan hasil
menurut topik, tanpa memindahkan folder atau mengubah artefak eksperimen asli.

## Laporan gabungan yang tersedia dalam snapshot

- [Cakupan log](summaries/log_coverage_20261122.md): seluruh perjalanan tool/stub,
  checkpoint, baseline penuh, attempt error/cap, lalu diagnostik terarah A–D.
  A salah setelah kosong parsial; D benar tetapi unsupported; B/C didukung bukti.
- [Prototipe controller log](summaries/log_controller_prototype_20261122.md):
  FOUND/ABSENT/UNKNOWN, satu fallback full scan, sinkron invoke_log dan tool opsional;
  29 tes prototipe + 9 tes native lulus tanpa inference provider. Bukan bukti
  penalaran model membaik atau mekanisme produksi sudah diterapkan.
- [Stale observation/reread](summaries/stale_observation_reread_20261122.md):
  false-current claim, attempt reread NOT_EXPOSED, diagnostik readiness,
  dan dua episode reread baru yang benar. Bukan perbandingan arm berpasangan.
- [Koreksi dua invoke](studies/carlene_two_invoke_context_20261120/REPORT.md):
  pilot, pengulangan, klarifikasi instruksi; keputusan kandidat tetap PARKED.
- [Screening log awal](studies/log_coverage_20261121/SCREENING.md): NO-GO klaim
  algoritmik, tetap dipertahankan terpisah dari temuan engineering berikutnya.
- [Screening laporan setelah aksi](studies/action_stop_screening_20261121/REPORT.md):
  empiris UNKNOWN; source/raw aksi tim belum tersedia saat screening.

## Cara memakai konteks ini

Indeks mencakup 13 direktori studies utama dan tiga sub-studi log, termasuk
attempt gagal, tidak dijalankan, sintesis tanpa inference, serta folder protocol-only.
Jumlah baris indeks bukan jumlah eksperimen/episode independen. Prototipe di luar
studies dicatat terpisah. Huruf A–D, setup dan arti label exposure berbeda antarstudi;
jangan menyatukan denominator atau menghapus attempt buruk.

Sumber otoritatif berada di rosa-research. Member/krln adalah mirror Markdown
terpilih, bukan backup atau arsip runnable. Raw trace, source, fixture, protocol,
freeze dan penilaian rinci tetap lokal. Locator berformat code dalam laporan
adalah path relatif repo sumber, bukan link snapshot. Hanya tautan Markdown ke
file allowlist yang dapat dibuka di mirror. Baca important_missing_context pada
manifest; source_commit_sha tidak membuktikan bytes untracked sudah committed.

Laporan ini reported evidence penulis. Klaim signifikan memerlukan pemeriksaan
source/raw dan batas eksperimen; tidak ada adjudikasi tim independen yang diklaim.
Publikasi konteks ini tidak menjalankan model, ROS, held-out atau eksperimen baru.
