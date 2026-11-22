# Prototipe controller cakupan log: implementasi dan batas verifikasi

22 November 2026, Asia/Taipei. Status: jalur sinkron eksplisit invoke_log selesai
dan diuji deterministik lokal. **29 tes prototipe + 9 tes native lulus**, termasuk
dua tes melalui original ROSA.invoke dengan model skrip lokal. Provider requests
dan native ROS operations nol. Tidak ada batch inference, benchmark besar,
held-out, rerun episode baseline, atau klaim manfaat penalaran model.

Prototipe mengikuti [temuan cakupan log](log_coverage_20261122.md). Ini perbaikan
workflow engineering, bukan klaim algoritme baru atau pembuktian manfaat C1.
Source produksi serta baseline A–D dipertahankan. Rencana README ditulis sebelum
implementasi; HEAD sumber tetap `d9991aad80d46b581150e85dff52f29d9619bce7`.

## Workflow yang benar-benar bekerja

Input eksplisit: file, substring literal, dan case sensitivity. Adapter memanggil
read_log native dari salinan modul terisolasi; tidak monkeypatch modul produksi.
Hasil/exception asli dipertahankan. Metadata searched_range, searched_lines,
total_lines, search_complete dan matching_rule berasal dari operasi yang diamati,
bukan jumlah match atau flag kelengkapan yang diisi model.

Native membaca ekor sebelum filter dan menambah nomor/strip teks. Adapter mencatat
aturan native case-insensitive itu terpisah dari verifikasi pertanyaan terhadap
isi baris asli **hanya pada jendela yang dipilih**. Raw prefix yang ikut dimuat
readlines tidak dijadikan bukti. Prefix nomor baris dan strip native tidak boleh
menjadi saksi literal palsu. Error cap sebelum filter berarti searched_lines=0,
search_complete=false; tidak diubah menjadi pencarian kosong.

search_log memeriksa baris asli UTF-8 sampai EOF, dengan aturan case sensitivity
eksplisit. Semua match dihitung; max_examples hanya membatasi saksi yang dikirim,
bukan scan. Pencarian lengkap tidak memakai batas output native 200 baris.
Pemeriksaan fingerprint file sebelum/sesudah serta hash teks logis mendeteksi
perubahan selama read. Hash menormalisasi universal newlines sebagai teks UTF-8,
bukan ukuran I/O disk atau hash byte fisik asli.

Kode mengevaluasi bukti untuk file dan predikat yang sama:

- FOUND: ada saksi literal sah.
- ABSENT: scope lengkap berhasil diperiksa dan tidak ada kecocokan.
- UNKNOWN: cakupan parsial, error, atau bukti tidak cocok/tidak valid.

UNKNOWN karena cakupan parsial memicu **paling banyak satu** full scan tambahan.
Jika scan gagal, tetap UNKNOWN. Error awal native tidak diretry otomatis; caller
dapat memilih mode direct, yang hanya menjalankan full scan tanpa native read.
Tidak ada oracle fixture di evaluator, cache, memory baru lintas episode, atau
penggabungan interval/snapshot untuk optimasi reuse.

## Hasil lokal terintegrasi

Fixture temporer baru dipakai untuk pengujian, bukan episode inference ulang.

| Kondisi | Setelah ERROR/100 native | Full scan tambahan | Akhir |
|---|---|---:|---|
| A: 400 baris, ERROR50 | UNKNOWN, kosong 301–400 | 1 | FOUND, saksi 50 |
| B: 400 baris, ERROR350 | FOUND, saksi 350 | 0 | FOUND |
| C: 80 bersih | ABSENT, seluruh 1–80 | 0 | ABSENT |
| D: 400 bersih | UNKNOWN, kosong 301–400 | 1 | ABSENT setelah 1–400 |

Tes juga mencakup file kosong, case sensitivity, substring literal bukan regex,
spasi asli, prefix nomor baris palsu, limit contoh tanpa memotong scan, file/predikat
berbeda, source hash berubah, native cap/akses/decode error, perubahan file saat
native/full read, dan kegagalan fallback yang tetap UNKNOWN tanpa retry.

Dalam tes original ROSA.invoke, model skrip meminta native ERROR/100 lalu menjawab
`Ya, SELURUH file run.log bebas ERROR.` Respons dan history assistant itu tetap
asli. Controller membaca bukti baru, menemukan baris 50, dan menghasilkan
`File memiliki ERROR; ditemukan pada baris 50.` original_model_response dan
verified_answer disimpan terpisah dalam trace; teks model tidak ditimpa.
Ini keberhasilan controller/plumbing pada model palsu deterministik, bukan hasil
inference atau peningkatan penalaran model nyata.

## Titik integrasi dan pembanding

VerifiedLogROSA.invoke_log membungkus ROSA.invoke asli, lalu memverifikasi query
secara independen. Factory mempertahankan 47 default tool dan tidak mengubah
source, prompt, schema, atau history. Tidak menggunakan kembali receipt model:
controller selalu melakukan pemeriksaan baru, sehingga ada overhead read tambahan.

Tool search_log tersedia melalui parameter tools bawaan ROSA; registrasi dan
eksekusinya teruji sebagai tool ke-48, tanpa mengganti read_log. Jalur tool-only
tidak memasang controller jawaban; model tetap dapat mengabaikan bukti. Mode
direct CLI/API memakai full scan dan evaluator yang sama untuk pembanding sederhana.

CLI deterministik dari root repo sumber:

```bash
.venv/bin/python -m research.prototypes.log_coverage_20261122 --demo
.venv/bin/python -m research.prototypes.log_coverage_20261122 --file FILE --substring ERROR --case-sensitive --mode direct
```

Tes lokal mengikuti unittest/unittest.mock repo. Dua tes integrasi memakai ROSA
asli dan BaseChatModel skrip lokal, dengan HTTP send dan CLI subprocess diblokir.
Setup ROS yang sudah ada diperlukan untuk impor ROSA ros_version=2, tanpa
menjalankan robot atau command ROS. Tidak ada model/provider baru dikonfigurasi.

## Batas yang masih ada

Integrasi hanya sinkron dan eksplisit invoke_log: plain ROSA.invoke/astream produksi
tidak otomatis diperbaiki. Provider nyata dan jalur streaming belum diuji/dibangun.
Hasil mengacu snapshot read stabil, bukan jaminan file tidak berubah sesudah return.
Tidak ada watcher atau benchmark biaya controller ditambah model.

Batas satu full scan tambahan adalah batas controller per run. Factory wrapper
tidak menambahkan search_log ke model; agent luar pada jalur tool-only memiliki
budget caller sendiri. Semua read yang dipilih model tidak termasuk counter scan
controller. Native adapter dipin ke hash source yang diaudit dan menolak coverage
jika source berubah. Case-insensitive memakai str.lower, bukan regex/casefold.

Hasil tes tidak menjanjikan robustness produksi atau efektivitas terhadap model.
NO-GO klaim algoritmik sebelumnya tidak berubah hanya karena prototipe dibuat.
Implementasi, tes dan raw data runnable tetap di repo riset, bukan snapshot konteks.

Locator lokal: `research/prototypes/log_coverage_20261122/` berisi README,
coverage.py, integration.py, __main__.py, test_workflow.py, START_STATE,
TEST_OUTPUT, NATIVE_TEST_OUTPUT, DEMO_RESULTS, CLI_CHECKS, FINAL_CHECKS dan
EVIDENCE_SHA256. Final checks mencatat 501 file lama tidak berubah pada akhir
implementasi; angka itu berlaku saat prototipe ditutup. Pembaruan navigasi konteks
sesudahnya bukan alasan mengedit freeze atau artefak baseline lama.
