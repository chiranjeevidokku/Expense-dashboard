from database import Base, engine
import models

print("Creatig models in postgresSQL")
Base.metadata.create_all(bind=engine)
print("Tables created ")