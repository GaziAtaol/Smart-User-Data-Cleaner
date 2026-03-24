# Smart User Data Cleaner

## Türkçe

### Proje Hakkında

`Smart User Data Cleaner`, CSV, JSON, Excel ve veritabanı kaynaklarından gelen ham kullanıcı verilerini
otomatik olarak temizleyen, doğrulayan ve raporlayan bir Python kütüphanesidir.

### Özellikler

- Çoklu kaynak desteği: CSV, JSON, Excel, SQLite / PostgreSQL
- Akıllı temizleme: eksik değer, yineleme, format hatası
- Anomali tespiti: IQR, Z-score, Isolation Forest
- JSON tabanlı kural motoru
- Pydantic şema doğrulama
- HTML ve PDF raporlama
- Typer CLI + opsiyonel Streamlit / FastAPI arayüzü

### Hızlı Başlangıç

```bash
git clone https://github.com/gaziataol/Smart-User-Data-Cleaner.git
cd Smart-User-Data-Cleaner
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --help
```
