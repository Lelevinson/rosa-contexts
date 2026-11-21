# Carlene — koreksi pengguna di antara dua invoke ROSA

20 November 2026, Asia/Taipei. Laporan sumber otoritatif lintas tiga studi;
disiapkan untuk review context member/krln, belum dipublikasikan.

## Keputusan dan pertanyaan riset

**Keputusan Carlene:** parkir koreksi di antara dua invoke sebagai kandidat
improvement utama. Pada cakupan simulator yang diuji, memperjelas instruksi
pengguna sudah cukup agar pembatalan tetap diikuti pembacaan dan laporan akhir.
Keputusan ini berasal dari instruksi Carlene pada tahap dokumentasi ini, bukan
klaim metode baru atau bukti bahwa ROSA menangani semua jenis koreksi.

Pertanyaan: apakah ROSA yang sudah ada dapat menunggu, melanjutkan, mengganti,
atau membatalkan target kedua di antara dua invoke pada instance yang sama?
Studi ini tidak menguji interupsi saat satu invoke masih berjalan.

## Setup yang benar-benar diuji

Satu model Ollama qwen3.5:9b, temperature 0, reasoning off; dua tool simulator:
rotate_to_heading(theta) dan read_heading(). Backend adalah scalar heading Python
yang berubah seketika, bukan robot ROS, turtlesim, atau simulasi fisika.
Operasi native ROS nol pada seluruh trace. Model requests, tool calls yang diminta,
operasi simulator yang dijalankan, jawaban, tokens, waktu dan error direkam terpisah.

Setiap episode: heading awal 0, instance ROSA baru, accumulate_chat_history=True;
instance sama digunakan untuk kedua invoke. Pesan kedua diberikan setelah invoke
pertama selesai. Bukti HTTP memperlihatkan pesan awal, jawaban pertama persis,
dan pesan kedua masuk ke request giliran kedua pada semua episode dua-tool lengkap.
Pengamatan tool_end saja tidak dipakai sebagai bukti penerimaan koreksi.

Setup dua-tool memakai subclass studi dari ROSA lokal: invoke/history/executor
diwarisi; menu dibatasi dan prompt asli ditambah konteks deployment simulator serta
permintaan laporan JSON. Ini bukan ROSA full-menu. Source produksi tidak diubah.
System prompt dan schema dua-tool identik antara tiga studi; klarifikasi di studi
ketiga hanya ditambahkan pada pesan pengguna, tanpa aturan koreksi baru di system.

Opsi tetap: num_ctx 16384, num_predict 2048, 8 iterasi per invoke, timeout request
120 detik, deadline episode 360 detik, keep_alive=0. Model digest:
`d63f830f28d515fefea546f213fca7a75e9dd5176ef51a6deabc952d1c99a911`.
Source ROSA main: `d9991aad80d46b581150e85dff52f29d9619bce7`;
LangChain 0.3.30, core 0.3.86. Digest/settings berasal dari metadata dan payload;
efek internal seed pada server tidak diverifikasi secara independen.

## Tugas dan perubahan tepat pesan pengguna

Pesan awal pilot dan pengulangan, satu string:

> Putar ke 0.5 radian sekarang, lalu tunggu pesanku. Setelah aku memberi kabar, lanjutkan ke target kedua 2.0 radian, lalu baca dan laporkan arah akhir.

Studi klarifikasi mempertahankan teks itu lalu menambahkan satu spasi dan kalimat:

> Setelah pesan keduaku, baik aku melanjutkan, mengganti, maupun membatalkan target kedua, selalu baca arah akhir lalu laporkan.

Pesan kedua tetap A “Lanjut.”, B “Target kedua ganti ke −1.0 radian.”,
C “Batalkan putaran kedua saja.” Target yang seharusnya dikirim: A [0.5,2.0],
B [0.5,-1.0], C [0.5]. C pada tugas lama ambigu mengenai kewajiban read/report
sesudah pembatalan. Tidak ada perubahan diam-diam pada pesan C.

## Hasil tiga studi — pertahankan denominator masing-masing

| Studi / run | Desain | Hasil dan batas |
|---|---|---|
| carlene_two_turn_20261119 / 20261119T122055Z_eb81c7 | A/B/C masing-masing sekali, seed 20261119 | **Skor beku 0/3**, tetap utuh. A/B mencapai heading, membaca dan menyebut angka benar, tetapi gagal parser format. C mengirim [0.5,0.5], tanpa read akhir. |
| carlene_repeat_20261120 / 20261120T025843Z, kondisi pilot_repeat | A/B/C masing-masing tiga kali, seed tetap 20261119 | **6/9 perilaku: A 3/3, B 3/3, C 0/3.** Semua menunggu; semua history sampai. C mengulang rotasi tambahan ke 0.5 dan tidak membaca. |
| carlene_explicit_cancel_20261120 / 20261120T050414Z | A/B sekali pada seed 20261119; C seed 20261119, 20261120, 20261121 | **5/5 perilaku, C 3/3.** Setiap C hanya mengirim rotasi pertama 0.5; setelah pembatalan meminta read_heading, lalu melaporkan 0.5. |

JSON adalah ukuran terpisah: pilot 0/3 melalui parser beku; pengulangan 0/9;
klarifikasi 0/5. Skor perilaku baru tidak mensyaratkan JSON. Kegagalan format A/B
bukan kegagalan mencapai heading atau menyebut angka arah yang benar. Pilot lama
tidak dinilai ulang atau diganti skornya. Penilai baru memisahkan wait, urutan,
aksi tambahan, read akhir, state, history, isi dan format. Pada C lama, jawaban
menyebut 0.5 yang benar sekaligus rencana 2.0, sehingga penilai isi otomatis memberi
uncertain; aksi tambahan dan read yang hilang tetap kegagalan tersendiri.

Kondisi terpisah default_prompt_blocked_menu pada studi pengulangan memakai prompt
dan executor bawaan, 47 schema default + dua simulator; semua implementasi default
diganti penolakan sebelum executor dibuat. A1 mengirim [0.5,2.0] lalu mencapai
deadline 360 detik saat request keempat menunggu respons; belum ada read/jawaban
akhir. Defek stop runner membuat B1 telanjur dimulai, lalu operator menghentikannya:
satu request tanpa respons, tanpa operasi/giliran kedua. Tujuh episode rencana
tidak dijalankan. **Hasil tidak lengkap**, bukan bukti gagal memahami koreksi.
Ini juga bukan ROSA full-menu tanpa pembatasan; workflow default dapat terhalang.
Tidak ada default tool diminta pada trace kondisi ini yang tersedia; bukti
pemblokiran semua implementasi berasal dari tes deterministik sebelum run.

| Kondisi | Requests / respons | Tool calls diminta / operasi simulator | Token input / output tercatat |
|---|---:|---:|---:|
| Pilot | 14 / 14 | 8 / 8 | 19,376 / 428 |
| Pengulangan dua-tool | 42 / 42 | 24 / 24 | 58,128 / 1,284 |
| Prompt bawaan/menu diblokir, termasuk parsial | 5 / 3 | 2 / 2 | 18,377 / 123 |
| Klarifikasi | 22 / 22 | 12 / 12 | 30,863 / 654 |

Tokens adalah hitungan endpoint; kondisi parsial merupakan batas bawah karena
dua request tanpa respons. Tidak ada error pada tiga kondisi dua-tool lengkap.
Error deadline/interrupt bawaan dipisahkan dari perilaku model, tidak disembunyikan.

## Verifikasi, provenance dan bukti lokal

Pada persiapan laporan ini, protokol, hasil JSON, seluruh raw trace ketiga run
(termasuk parsial), serta freeze dibaca lokal. Target/read, jawaban, hitungan
request/respons/tool/operasi/token, urutan dua invoke, dan history HTTP dicocokkan
dengan artefak asli. Semua hash dalam ketiga freeze masih cocok. Tidak ada bukti
utama yang tidak dapat diakses. Ini audit artefak tersimpan, bukan eksperimen ulang
atau replikasi independen hasil model; laporan setup tim lain tetap reported evidence.

Setiap studi mempunyai PROTOCOL.md, FREEZE.json dan REPORT.md. Bukti raw hanya lokal:
`research/studies/<study-id>/artifacts/<run-id>/`, dengan ID pada tabel hasil.
Pilot: A/B/C.jsonl, results.json; pengulangan: pilot_repeat_*.jsonl,
default_prompt_blocked_menu_*.jsonl, results.json, STOP_RECORD.json; klarifikasi:
*_seed*.jsonl, results.json, audit.json. Ini penunjuk teks untuk pemilik sumber,
bukan tautan snapshot atau izin membagikan raw trace. Artefak/source tidak disalin.

SHA-256 protokol beku (mengidentifikasi teks protokol asli, bukan seluruh bukti):

| Studi | PROTOCOL.md SHA-256 | results.json SHA-256 |
|---|---|---|
| Pilot | `55e50082672e8e84559c851c1b9be02392929436953881cdda154340fc8b5c08` | `af6051c73172113113cdeb427e57b6409c829f6dd8f560ed3a60c9cd4ef14b89` |
| Pengulangan | `124933d4960fc16745ba2050faa50aa1c27612abb95956eb8f68ac53de1f9669` | `744164733435f11522cbbee7ecaf203cafd597042b08026ed2d5edecbe085a0a` |
| Klarifikasi | `4a964b47dedbf4a0d85913ff3a4e10987833448ae2f1a21077952aab2ed90b46` | `5d32f70c58afa1443bd9ff5342eb5d9180bc0fe1d88d9e41035a67b20dbd193c` |

Byte context ini belum ada di commit source: file dokumentasi masih untracked.
Manifest snapshot harus menyatakan source_git_state dan hash per file; source HEAD
di atas tidak membuktikan byte context tersimpan di commit itu. Freeze/protokol/raw
lama tetap lokal utuh dan tidak ditimpa oleh laporan gabungan ini.

## Batas kesimpulan dan tindak lanjut

Satu model, tugas authored sederhana, simulator scalar, temperature 0. Pengulangan
seed tetap mengukur konsistensi konfigurasi; seed berbeda pada temperature 0 tidak
menjamin variasi, dan ketiga jawaban C klarifikasi identik. A/B studi klarifikasi
bukan kontrol lengkap lintas seed. State evaluator dibaca langsung dari simulator,
bukan sensor fisik independen. Tidak menguji koreksi dalam satu eksekusi atau robot.

Hasil tidak digabung menjadi satu tingkat keberhasilan: parser/skor pilot berbeda
dari skor perilaku berikutnya; wording awal dan jadwal seed berubah pada klarifikasi;
kondisi prompt/menu bawaan berbeda dan tidak lengkap; pengulangan tidak independen.
Perubahan hasil konsisten dengan manfaat kejelasan instruksi, tanpa membuktikan
efek kausal umum. Pada cakupan ini, tidak diperlukan improvement ROSA tambahan.

Keputusan parkir tidak melarang evaluasi pertanyaan lain bila muncul bukti baru;
tidak ada metode baru, klaim kemampuan semua koreksi, atau jadwal eksperimen lanjutan.
Langkah saat ini hanya review laporan dan diff snapshot terpilih sebelum publikasi.
