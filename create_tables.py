from database import Base, engine
from budget_api import models as bud_models
from transactions_api import models as tr_models
from user_api import models as us_models


print("Creatig models in postgresSQL")
Base.metadata.create_all(bind=engine)
print("Tables created ")