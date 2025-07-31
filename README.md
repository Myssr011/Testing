# Plagiarism Detection System

Sistema deteksi kemiripan dokumen skripsi menggunakan Flask web application dengan algoritma TF-IDF dan cosine similarity.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Configuration
Copy `.env.example` to `.env` dan sesuaikan konfigurasi database:

```env
# Database Configuration
DB_HOST=if.unismuh.ac.id
DB_PORT=3388
DB_NAME=iqball
DB_USER=root
DB_PASSWORD=mariabelajar
DATABASE_URL=mysql+pymysql://root:mariabelajar@if.unismuh.ac.id:3388/iqball

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-very-secret-key-change-this-in-production
```

### 3. Database Migration
```bash
# Setup database tables
python migrate_app.py

# Seed sample data
python seed_database.py
```

### 4. Run Application
```bash
# Development mode
python run_flask.py

# Production mode
gunicorn -c gunicorn.conf.py app.flask_app:app
```

Aplikasi akan berjalan di: `http://localhost:5000`

## 📁 Project Structure

```
plagiarism-checker/
├── app/
│   ├── flask_app.py          # Main Flask application
│   ├── templates/            # HTML templates
│   └── static/              # CSS, JS, images
├── src/
│   ├── preprocessing.py      # Text preprocessing
│   ├── vectorizer.py        # TF-IDF vectorization
│   ├── similarity.py        # Similarity calculation
│   └── evaluation.py        # System evaluation
├── database/
│   ├── models.py            # SQLAlchemy models
│   ├── config.py            # Database configuration
│   └── migrations/          # Database migrations
├── config/
│   └── settings.yaml        # Application settings
├── uploads/                 # Uploaded files
├── results/                 # Analysis results
└── requirements.txt         # Python dependencies
```

## 🔧 Features

### Web Interface
- **Upload & Analysis**: Upload dokumen dan analisis kemiripan
- **System Evaluation**: Evaluasi performa sistem
- **Settings**: Konfigurasi algoritma dan preprocessing
- **Information**: Dokumentasi dan bantuan

### API Endpoints
- `POST /api/upload` - Upload dan analisis file
- `POST /api/evaluation/run` - Jalankan evaluasi sistem
- `POST /api/settings/update` - Update pengaturan sistem

### Core Algorithms
- **Text Preprocessing**: Tokenization, stemming, stopword removal
- **TF-IDF Vectorization**: Document term frequency analysis
- **Cosine Similarity**: Document similarity calculation
- **System Evaluation**: Precision, recall, F1-score metrics

## 🧪 Testing Database Connection

Jalankan script test sederhana untuk memastikan koneksi database:

```python
# test_connection.py
import os
import sys
import socket
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    host = os.getenv('DB_HOST')
    port = int(os.getenv('DB_PORT', 3306))
    
    try:
        socket.create_connection((host, port), timeout=10)
        print(f"✅ Connection to {host}:{port} successful")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == '__main__':
    test_connection()
```

## 🔐 Admin Login

Default admin credentials (ubah setelah setup):
- **Username**: admin
- **Password**: admin123

## 📊 Database Schema

### Tables
- `users` - User accounts dan roles
- `abstracts` - Document metadata dan content
- `similarity_results` - Hasil analisis kemiripan
- `detection_batches` - Batch processing results
- `system_logs` - System activity logs

## 🛠️ Development

### Environment Variables
```env
# Development
FLASK_ENV=development
FLASK_DEBUG=True

# Production
FLASK_ENV=production
FLASK_DEBUG=False
```

### Code Structure
- **Frontend**: Bootstrap 5 + vanilla JavaScript
- **Backend**: Flask + SQLAlchemy
- **Database**: MySQL/MariaDB
- **Processing**: scikit-learn + NLTK + Sastrawi

## 📝 Production Deployment

### With Gunicorn
```bash
gunicorn -c gunicorn.conf.py app.flask_app:app
```

### With Docker (optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app.flask_app:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

Untuk bantuan dan pertanyaan:
- Email: support@example.com
- GitHub Issues: [Create Issue](https://github.com/devnolife/plagiarism-checker/issues)
