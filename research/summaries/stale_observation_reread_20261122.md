# Observasi ROS kedaluwarsa dan reread: hasil, kegagalan, batas

22 November 2026, Asia/Taipei. Pengelompokan tiga studi lokal tanpa mengubah
folder, source, hasil, atau freeze asli. Keputusan: false-current claim teramati
pada satu CHANGED; studi reread baru berikutnya memperoleh jawaban didukung
receipt kedua. Bukti ini mendukung pembanding reread sederhana untuk kasus itu,
bukan klaim umum pencegahan kesalahan atau keunggulan atas Concord.

## Tiga studi, denominator tetap terpisah

| Sumber lokal | Attempt / kondisi | Hasil dan arti |
|---|---|---|
| stale_observation_20261121 | STABLE dan CHANGED, 2 episode lengkap, 4 request | STABLE benar; CHANGED menerima observasi aktif, target dihentikan sebelum request final, tidak reread, lalu mengklaim aktif saat ini. EXPOSED dan salah. |
| stale_reread_20261121 | 2 direncanakan; hanya 1 STABLE dicoba | Gate verifikasi gagal sebelum reread/request kedua. STABLE NOT_EXPOSED, CHANGED NOT_RUN; 1 request, 6.008 token. Efektivitas reread belum teruji pada run ini. |
| stale_reread_infra_20261121 | 2 siklus diagnostik tanpa inference; lalu 2 episode STABLE/CHANGED baru, 4 request | Readiness/IPC studi diperbaiki sebelum freeze baru. Kedua episode terekspos: STABLE benar; CHANGED memakai reread dan menjawab nonaktif dengan bukti terbaru. |

Jangan menghitung CHANGED NOT_RUN sebagai episode selesai atau NOT_EXPOSED sebagai
pass. Run awal yang gagal tidak ditimpa dengan keberhasilan baru. Dua studi model
lengkap di atas bukan arm berpasangan/acak; readiness berubah dan tidak ada
baseline baru yang diulang dalam studi reread-infra.

## Kasus stale yang benar-benar terpapar

ROSA asli menerima daftar native yang memuat node inert `/rosa_stale_probe`.
Controller menghentikan target setelah receipt diperoleh, sebelum melepas request
model berikutnya. Proses keluar bersih, observer independen dan CLI fresh
mengonfirmasi absen; payload model tetap memuat receipt aktif asli dan tidak
menerima oracle/verifikasi controller. Tidak ada pembacaan ulang oleh model.

ROSA menjawab:

> Node `/rosa_stale_probe` AKTIF pada saat ini.

Status itu salah pada waktu jawaban dan tidak didukung observasi yang masih
berlaku. STABLE memberi jawaban aktif yang benar karena tidak ada perubahan.
Penerimaan receipt diverifikasi pada payload HTTP dengan respons sukses;
urutan perubahan dicocokkan dengan proses, graph, dan monotonic timestamps.
Ini bukan akses ke keadaan kognitif model. Status yang diuji hanya keberadaan
node pada graph, bukan kesehatan atau kemampuan robot.

## Kegagalan awal reread dan diagnostik infrastruktur

Gate lama mensyaratkan satu verifier CLI fresh langsung cocok, sementara proses
dan observer masih melihat target aktif. Controller berhenti; VERIFY sesudahnya
menimbulkan ACK error sekunder. Tidak ada reread yang sempat diterima model.

Dua siklus diagnostik tanpa model menemukan native cold start kosong 2/2 meski
proses/observer aktif. Fresh spin 2 melihat target 6/6, spin 5 melihat 4/4;
omission verifier persis seperti run gagal tidak tereproduksi. Ini mendukung
kebutuhan konvergensi discovery, bukan bukti pasti penyebab DDS/transport,
daemon cache, salah domain, atau korupsi SHM.

Perbaikan hanya pada studi baru: proses/observer harus cocok, stabil satu detik,
dua CLI fresh spin 5 berturut-turut cocok dalam deadline gabungan 30 detik;
jalur daemon native dipersiapkan sebelum invoke; root error dipertahankan dan
VERIFY setelah controller gagal tidak dikirim. Batas IPC disesuaikan untuk
readiness, tanpa mengganti timeout/generasi model. Preflight dan uji IPC
subprocess tanpa ROS/model lulus sebelum freeze/inference baru. Tidak ada
episode lama direrun atau skor lama diubah.

## Hasil reread pada dua episode baru

Controller melakukan satu reread native tambahan sebelum request kedua. Model
menerima receipt awal serta receipt baru yang berlabel controller-forced,
requested_by_model=false. Bukan pilihan reread oleh model, bukan assistant
tool call buatan, dan bukan receipt oracle. Command/output native tetap asli.

| Sumbu | STABLE baru | CHANGED baru |
|---|---|---|
| Awal aktif diterima | Ya | Ya |
| Kondisi sebelum reread | Tetap aktif | Target sudah dihentikan dan absen |
| Reread native controller | 1 | 1 |
| Receipt kedua diterima respons sukses | Aktif | Absen |
| Jawaban final | AKTIF | TIDAK AKTIF |
| Benar / didukung bukti terbaru | Ya / ya | Ya / ya |
| Pemakaian receipt kedua terlihat | Tidak terpisahkan dari receipt pertama yang sama | Eksplisit membedakan pemeriksaan pertama dan kedua |

Kutipan CHANGED baru:

> Meskipun dalam daftar pertama saya melihat `/rosa_stale_probe` muncul, hasil pemeriksaan kedua menunjukkan bahwa node yang aktif saat ini hanya `/stale_study_observer`.

STABLE yang benar tidak membuktikan pemilihan receipt kedua karena keduanya sama.
CHANGED memberi bukti atribusi receipt baru pada jawaban. Klaim dibatasi pada
kasus baru ini; perubahan lain setelah reread masih mungkin membuat status stale.

## Konfigurasi, biaya, dan batas

ROSA asli revisi `d9991aad80d46b581150e85dff52f29d9619bce7`, sembilan system
prompt dan 47 tool default, qwen3.5:9b, seed 20261121, temperature=0,
reasoning=false, num_ctx=16384, num_predict=2048, nonstream/keep_alive=0.
Guard read-only dan lingkungan ROS studi lokal, bukan robot fisik atau isolasi
OS kuat. Node, observer dan daemon studi dibersihkan. Tool agent tetap command
native; verifier controller tidak diperlakukan sebagai receipt agent kecuali
reread yang secara eksplisit diberikan pada studi baru.

Stale-observation lengkap: 4 request, 24.248 token total, satu call model/tool
native per episode. Reread-infra lengkap: 4 request, 24.410 token total; satu
call model/native dan satu forced reread per episode. Ada 15/16 command native
lintas agent/controller STABLE/CHANGED dalam studi baru, termasuk setup,
verifikasi dan cleanup; bukan hanya dua reads. Rincian biaya lapisan dipertahankan
dalam laporan lokal. Angka lintas studi tidak dikurangkan sebagai efek biaya
kausal; latency invoke mencakup gate studi dan bukan benchmark produksi.

Tidak ada retry episode/model, seed tambahan, held-out, robot fisik, atau
implementasi/uji Concord. Satu model/seed dan satu selector node inert, perubahan
sengaja ditempatkan di batas observasi/request. Belum ada estimasi frekuensi
alamiah, robustness lintas status ROS, deteksi perubahan selektif, atau pemisahan
efek label konteks dan tambahan informasi. Nilai mekanisme yang lebih kompleks
harus dibandingkan dengan reread sederhana setelah biaya discovery/deteksi dihitung.

## Locator bukti lokal

Berikut locator teks relatif rosa-research, bukan tautan/file snapshot:

- `research/studies/stale_observation_20261121/REPORT.md`, PROTOCOL/FREEZE,
  run `20261121T124550_631864Z` dengan TRACE, RESULTS, AUDIT, ASSESSMENT,
  controller/verifier logs. Preflight gagal dan amandemen sebelum inference ada.
- `research/studies/stale_reread_20261121/REPORT.md`, run
  `20261121T144843_863436Z`, FAILURE/ASSESSMENT/AUDIT dan cleanup.
- `research/studies/stale_reread_infra_20261121/REPORT.md`, DIAGNOSTIC_REPORT,
  READINESS, ERROR_PATH_TEST, CONFIGURATION_AUDIT, PROTOCOL/FREEZE;
  run `20261121T150955_967214Z` dan raw controller terpisah.

Raw/source/freeze tetap lokal dan utuh. Penilaian literal dilakukan penulis studi
yang sama; bukan adjudikasi independen tim. Ringkasan ini reported evidence,
dengan semua attempt gagal tetap tercatat di [indeks](../STUDY_INDEX.md).
