class Config:
    SECRET_KEY = 'ab57ccec0f56942a5ca33215f9d2d88c'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # caminho relativo em relação ao nosso arquivo
    SQLALCHEMY_TRACK_MODIFICATIONS = False