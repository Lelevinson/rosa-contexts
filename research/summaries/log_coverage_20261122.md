# Cakupan log ROSA: temuan, kontrol, dan riwayat attempt

22 November 2026, Asia/Taipei. Ringkasan konteks Carlene/krln dari sumber lokal
rosa-research. Pengelompokan topik ini tidak memindahkan folder, mengganti hasil,
atau menggabungkan denominator studi yang berbeda. Source produksi tetap revisi
`d9991aad80d46b581150e85dff52f29d9619bce7` selama diagnostik yang dilaporkan.

## Kesimpulan yang didukung

Pada satu diagnostik terarah, ROSA menerima hasil native kosong untuk ekor
301–400 dari file 400 baris, lalu menyatakan **seluruh file bebas ERROR**,
padahal uppercase literal ERROR ada di baris 50. Kontrol berikutnya memisahkan
kesalahan faktual dari kecukupan bukti: saksi positif B dan kosong lengkap C
mendukung jawabannya; D benar faktual pada file bersih tetapi bukti tetap parsial.

Ini bukti kasus konkret pada satu model/seed dengan instruksi awal read_log yang
eksplisit. Bukan estimasi frekuensi, baseline pemilihan num_lines tanpa arahan,
uji C1/Concord, atau manfaat terhadap penalaran model. Prototipe controller
sesudah diagnostik baru diuji lokal tanpa inference; lihat
[ringkasan prototipe](log_controller_prototype_20261122.md).

## Kontrak tool yang diperiksa

Native read_log memuat seluruh file dengan readlines, memilih ekor num_lines,
menolak jendela di atas 200 baris, baru menerapkan filter substring case
insensitive pada teks bernomor/strip. Jumlah match bukan ukuran domain pencarian.
Readlines seluruh file tidak berarti seluruh file difilter atau dilihat model.
Error cap/validasi/akses tidak menjadi hasil kosong yang sah. Tidak ada parameter
native untuk mengambil prefix arbitrer.

SHA-256 source log.py yang diaudit:
`87c86928fba283cb66e35b01f88f6bb15b2a5e4ef37c985c84c2a2c0a860f77c`.
Aturan pembuktian sederhana: satu saksi literal sah cukup untuk keberadaan;
ketiadaan global membutuhkan scope lengkap dengan predikat sesuai.

## Riwayat lengkap keluarga log

Nama A/B/C/D bersifat lokal per studi; fixture, pesan, budget, dan menu tidak
boleh diasumsikan sama hanya karena hurufnya sama.

| Sumber lokal / tahap | Attempt dan setup | Hasil serta batas |
|---|---|---|
| log_coverage_20261121, tool contract | 5 fixture; 9 native tool calls + 1 boundary stub; provider 0 | Kontrak ekor/cap/substring terukur; bukan perilaku model. Screening NO-GO klaim algoritmik tetap berlaku. |
| log_coverage_20261121/model_decision_20261121 | 6 episode checkpoint: 3 PARTIAL, 3 DIRECT; read_log + search_log studi, prompt JSON; replay/satu receipt sintetis | PARTIAL 3/3 negatif global unsupported, A/C salah faktual. DIRECT A/B benar didukung, C menahan keputusan setelah error. Bukan baseline menu penuh atau isolasi manfaat mekanisme. |
| log_coverage_20261121/full_baseline_20261121 | 2 episode, prompt/menu/invoke asli dengan guard, tanpa arahan num_lines | A gagal validasi opsional sebelum body; B menerima error cap lalu timeout. Keduanya NOT_EXPOSED, bukan lulus. Callback child tidak lengkap; hasil direkonstruksi dari HTTP/native trace. |
| log_coverage_20261121/full_baseline_B_followup_20261121 | 1 follow-up B bersih, dipilih sesudah timeout; HTTP/deadline diperpanjang dan callback diperbaiki | Kosong 351–400 diterima; klaim antara terlalu luas, upaya prefix mengulang ekor. Enam iterasi berakhir cap tanpa jawaban final. Label lama NOT_EXPOSED mensyaratkan jawaban akhir; penerimaan receipt tetap benar-benar teramati. |
| read_log_abcd_20261121 | 4 episode menu penuh tanpa arahan num_lines: A 400/ERROR50, B 200 bersih, C 400/ERROR50 dengan open kedua ditolak, D 400 bersih | A EXPOSED kosong 351–400 lalu error literal filter lowercase, tanpa jawaban faktual akhir. B benar/didukung isi penuh. C error akses sebelum receipt kosong; D timeout. Bukan bukti salah-negatif global final dari studi ini. |
| read_log_abcd_20261121_now | Hanya PROTOCOL.md, tanpa freeze/raw run/hasil di folder itu | Catat sebagai protocol-only; tidak dihitung sebagai episode atau eksperimen selesai. Tidak mengisi celah praregistrasi studi lain secara retroaktif. |
| read_log_targeted_20261122 | 1 episode A dengan instruksi awal ERROR/100, tanpa receipt suntikan | Kosong 301–400 diterima; jawaban global bebas ERROR salah dan unsupported. |
| read_log_targeted_controls_20261122 | 3 episode baru B/C/D, konfigurasi/template sama A, instance/history baru; A tidak diulang | Saksi B dan kosong lengkap C benar/didukung; D benar tetapi unsupported sesudah kosong parsial. Semua kondisi kontrol tercapai. |

Studi ABCD tanpa arahan juga memiliki celah dokumentasi: protokol naratif pada
path studi tidak tercantum dalam freeze; rekonstruksi setelah run dilabeli.
Runner/input/fixture/source memang terbeku dan receipt A dapat diverifikasi dari
trace. Protokol diagnostik terarah A dan tiga kontrol berikutnya ada dan di-hash
sebelum inference masing-masing. Artefak lama dan penilaiannya tidak diubah.

Tidak ada satu definisi EXPOSED yang dapat digabung begitu saja: follow-up B lama
memakai syarat jawaban final, sedangkan studi kemudian memisahkan penerimaan
kosong parsial dari keberadaan jawaban akhir. Terangkan kedua sumbu, pertahankan
label lama, jangan menjumlahkan semuanya menjadi rate tunggal.

## Diagnostik terarah A bersama kontrol B–D

Template meminta read_log num_lines=100 dan level_filter="ERROR", kemudian
menanyakan apakah SELURUH file bebas dari substring literal ERROR huruf besar.
Posisi/kondisi fixture tidak dibocorkan. Baris lain teks netral, tanpa varian
lowercase, sehingga filter native case insensitive setara pada fixture ini.

| Kasus | Bukti diterima sebelum klaim | Jawaban | Kebenaran | Bukti | Tugas terverifikasi |
|---|---|---|---|---|---|
| A historis: 400, ERROR50 | Kosong 301–400, request 2 sukses | Seluruh file bebas ERROR | Salah | Tidak cukup | Gagal |
| B baru: 400, ERROR350 | Saksi literal baris 350, request 2 sukses | Tidak bebas ERROR | Benar | Cukup | Berhasil |
| C baru: 80 bersih | Kosong seluruh 1–80, request 2 sukses | Seluruh file bebas ERROR | Benar | Cukup | Berhasil |
| D baru: 400 bersih | Kosong 301–400, request 2 sukses | Seluruh file bebas ERROR | Benar | Tidak cukup | Belum terverifikasi |

B/C tidak membutuhkan kosong parsial agar menjadi kontrol yang berhasil.
Keempatnya memberi respons final, tetapi penyelesaian tugas terverifikasi
mensyaratkan jawaban benar dan didukung bukti. Tidak ada tool lanjutan pada
keempat episode. Receipt dicocokkan ke call model, native return, ToolMessage/ID,
payload HTTP dan respons sukses; bukan ukuran perhatian internal model.

Kutipan A:

> Ya, **SELURUH file run.log bebas dari substring literal "ERROR" huruf besar**.

D menulis:

> Jika ada baris yang mengandung "ERROR", mereka akan muncul dalam hasil filter tersebut, tetapi hasilnya kosong.

Ini alasan cakupan yang tidak sah untuk seluruh 400 baris. Ringkasan "0 baris"
tanpa rentang bisa ambigu secara terpisah, tetapi kalimat final SELURUH jelas
global. Tidak ada respons antara tersendiri setelah receipt sebelum final;
ucapan antara pada studi lama tetap dicatat menurut konteksnya sendiri.

ROSA prompt/menu/invoke asli dengan guard: 47 tool default, sembilan system
prompt, default max_iterations=100; budget eksternal enam request/12 tool starts,
HTTP 180 detik, episode 600 detik. qwen3.5:9b, temperature=0, seed=20261121,
reasoning=false, num_ctx=16384, num_predict=2048, keep_alive=0, nonstream.
Isolasi konfigurasi dan guard read-only/path fixture, bukan unrestricted atau
sandbox OS kuat. Tidak ada guard firing, retry, timeout atau cap pada A terarah
dan B–D baru. String angka model diterima validator native, tidak dikoreksi runner.

A historis: 2 request, 12.202 input + 270 output token. B–D baru: 6 request,
36.633 input + 734 output. Gabungan deskriptif 8 request/respons, 4 read_log,
1.280 baris/14.094 byte dimuat ke Python; bukan biaya rerun A. Preflight/oracle
terpisah; I/O disk fisik tidak diukur. Tidak membandingkan latency lintas studi
sebagai efek kausal karena setup/budget/beban berbeda.

## Keputusan dan bukti yang tetap lokal

Temuan cukup untuk mendokumentasikan kesalahan cakupan pada diagnostik terarah
dan membangun prototipe engineering yang diverifikasi deterministik. Belum ada
hasil yang mengubah NO-GO klaim algoritmik reuse/interval, membuktikan manfaat
model, atau membandingkan C1/Concord. B–D dipilih setelah A, satu seed per kondisi;
bukan replikasi acak atau benchmark.

Locator berikut adalah teks relatif repo sumber rosa-research, bukan tautan
snapshot atau file yang dipublikasikan:

- `research/studies/log_coverage_20261121/` beserta tiga substudinya: REPORT,
  PROTOCOL, FREEZE, runner, oracle, dan raw run masing-masing.
- `research/studies/read_log_abcd_20261121/REPORT.md` dan run
  `20261121T155250_966029Z`; `read_log_abcd_20261121_now/PROTOCOL.md` terpisah.
- `research/studies/read_log_targeted_20261122/`, run
  `20261121T163921_868533Z`: TRACE, RESULTS, AUDIT, ASSESSMENT, FINAL_CHECKS.
- `research/studies/read_log_targeted_controls_20261122/`, run
  `20261121T165106_454472Z`, COMBINED_ASSESSMENT dan manifest evidence.

Raw/source/freeze tidak dipindahkan atau diedit untuk publikasi. Snapshot ini
reported evidence penulis, bukan audit independen tim. Lihat
[indeks seluruh studi](../STUDY_INDEX.md) dan
[screening awal](../studies/log_coverage_20261121/SCREENING.md).
