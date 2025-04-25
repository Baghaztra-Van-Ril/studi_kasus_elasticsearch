# Studi Kasus Elasticsearch

Sebuah kamus kata / glosarium sederhana. Implementasi dengan **Flask**, **MySQL**, dan **Elasticsearch**. Data disimpan di database MySQL dan diindeks ke Elasticsearch untuk fitur pencarian yang lebih cepat.

---

## Fitur yang Diimplementasikan

- Create dan delete data berbasis GUI web
- Search dengan suport typo
- Autocomplete saat mencoba search

---

## Teknologi yang Digunakan

- Python 3
- Flask
- MySQL
- Elasticsearch

---

## Cara Menjalankan

### Clone repository

```bash
git clone https://github.com/Baghaztra-Van-Ril/studi_kasus_elasticsearch.git

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

### Siapkan autocomplete

Kirim requst `PUT` ke `http://localhost:9200/glossary_index` dengan basic auth elasticsearch.
```json
{
  "mappings": {
    "properties": {
      "term": {
        "type": "search_as_you_type"
      },
      "definition": {
        "type": "text"
      }
    }
  }
}
```

### Jalankan aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000/`. GUI tersedia di browser.

---

## API Documentation

### `POST /glossary`  
Tambah glossary baru  
  
```bash
curl -X POST http://localhost:5000/glossary -H "Content-Type: application/json" -d "{\"term\": \"istilah_baru\", \"definition\": \"penjelasan istilah\"}"
```

---

### `GET /glossary`  
Ambil semua glossary  

```bash
curl http://localhost:5000/glossary
```

---

### `GET /search?q=keyword`  
Cari glossary berdasarkan keyword  
 
```bash
curl "http://localhost:5000/search?q=keyword"
```

---

### `DELETE /glossary/<id>`  
Hapus glossary berdasarkan ID  

```bash
curl -X DELETE http://localhost:5000/glossary/1
```

---

### `POST /seed`  
Generate data dummy (dianggap 10 jika tanpa request arguments)

Generate 10 data dummy 
```bash
curl -X POST "http://localhost:5000/seed"
```

Generate 100 data dummy 
```bash
curl -X POST "http://localhost:5000/seed?n=100"
```
