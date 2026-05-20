import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clinica-juguetes-secret")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456789")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_DB = os.getenv("MYSQL_DB", "clinica_juguetes")
    MYSQL_CURSORCLASS = "DictCursor"
