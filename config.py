import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-coloniaprev-2026'
    
    # URL do banco de dados (Neon/Render costumam usar postgres://)
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    
    # Se não houver DATABASE_URL, tenta usar SQLite ou MySQL
    if not SQLALCHEMY_DATABASE_URI:
        if os.environ.get('USE_MYSQL') == 'True':
            MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
            MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
            MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
            MYSQL_DB = os.environ.get('MYSQL_DB') or 'coloniaprev'
            SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
        else:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

