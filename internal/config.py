
SECRET_KEY = "5d365f8e828a767de204b0126a9d5aa57b70cd97fe8bbb23a3693829e2e0e446"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SQLALCHEMY_DATABASE_URL = "sqlite:///./chatrooms.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

REDIS_DATABASE_URL = "redis://localhost:6379"
