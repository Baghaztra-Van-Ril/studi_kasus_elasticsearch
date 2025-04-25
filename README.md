# Studi Kasus Elasticsearch

Implementasi sederhana integrasi dengan **Flask**, **MySQL**, dan **Elasticsearch**. Data disimpan di database MySQL dan diindeks ke Elasticsearch untuk fitur pencarian yang lebih cepat.

---

## Teknologi yang Digunakan

- **Python 3**
- **Flask**
- **MySQL**
- **Elasticsearch**

---

## Cara Menjalankan

### Clone repository

```bash
git clone https://github.com/Baghaztra-Van-Ril/studi_kasus_elasticsearch.git
```

```bash
cd studi_kasus_elasticsearch
```

### Buat virtual environment

```bash
python -m venv .venv
```

### Aktifkan virtual environment

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/MacOS**:
  ```bash
  source .venv/bin/activate
  ```

### Install dependency

```bash
pip install -r requirements.txt
```

### Konfigurasi database & Elasticsearch

Edit file `config.py` sesuai konfigurasi lokal.

### Jalankan MySQL dan Elasticsearch

Pastikan kedua service ini sudah aktif.

### Jalankan aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000/`

---

## API Documentation

### 🔸 POST `/data`

**Deskripsi:** Menyimpan data ke database dan mengindeks ke Elasticsearch.

**Request Body:**

```json
{
  "content": "Isi data yang ingin disimpan"
}
```

**Response:**

```json
{
  "message": "Data tersimpan dan terindex",
  "id": 1
}
```

---

### 🔸 GET `/search?q=keyword`

**Deskripsi:** Melakukan pencarian data berdasarkan keyword di Elasticsearch.

**Response:**

```json
[
  {
    "content": "Isi data yang cocok dengan keyword"
  },
  ...
]
```

---

## 📊 Alur Kerja

```
[ User Input ]
      ↓
[ Simpan ke MySQL ]
      ↓
[ Index ke Elasticsearch ]
      ↓
[ Pencarian via Elasticsearch ]
      ↓
[ Hasil ditampilkan ]
```
