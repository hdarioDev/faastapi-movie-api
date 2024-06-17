from database import engine, Base
from models import Movie

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created!")
