## ⚙️ Setup Guide

### 1. Clone Repository
git clone https://github.com/PBPC05/C05_tugaskelompok.git
cd C05_tugaskelompok

### 2. Create virtual environment
python -m venv env
env\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Copy .env.example → .env and update values

### 5. Copy .gitignore.example → .gitignore and update values

### 6. Migrate models
python manage.py migrate

### 7. Start server
python manage.py runserver