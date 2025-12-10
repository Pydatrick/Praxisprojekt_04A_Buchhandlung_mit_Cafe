from sqlalchemy import create_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import os

# paths
ROOT_DIR = Path(__file__).resolve().parent
path_env = ROOT_DIR / 'sql' / 'data' / 'secret' / '.env'
# load env bs = bookstore, cs = coffeeshop
load_dotenv(path_env)
user_bs     = os.getenv('BOOKSTORE_DB_USER')
password_bs = os.getenv('BOOKSTORE_DB_PASSWORD')
host_bs     = os.getenv('BOOKSTORE_DB_HOST')
port_bs     = os.getenv('BOOKSTORE_DB_PORT')
db_name_bs  = os.getenv('BOOKSTORE_DB_NAME')

user_cs     = os.getenv('COFFEE_SHOP_DB_USER')
password_cs = os.getenv('COFFEE_SHOP_DB_PASSWORD')
host_cs     = os.getenv('COFFEE_SHOP_DB_HOST')
port_cs     = os.getenv('COFFEE_SHOP_DB_PORT')
db_name_cs  = os.getenv('COFFEE_SHOP_DB_NAME')

BOOKSTORE_DB_URL   = f"postgresql://{user_bs}:{password_bs}@{host_bs}:{port_bs}/{db_name_bs}"
COFFEE_SHOP_DB_URL = f"postgresql://{user_cs}:{password_cs}@{host_cs}:{port_cs}/{db_name_cs}"

engine_bookstore   = create_engine(BOOKSTORE_DB_URL)
engine_coffee_shop = create_engine(COFFEE_SHOP_DB_URL)

SessionLocal_Bookstore   = sessionmaker(autocommit = False, 
                                        autoflush  = False, 
                                        bind       = engine_bookstore
                                        )

SessionLocal_Coffee_Shop = sessionmaker(autocommit = False, 
                                        autoflush  = False, 
                                        bind       = engine_coffee_shop
                                        )

# Base für bookstore models
mapper_registry_bookstore = registry()
Base_Bookstore = mapper_registry_bookstore.generate_base()
# Base für coffee_shop models
mapper_registry_coffee_shop = registry()
Base_Coffee_Shop = mapper_registry_coffee_shop.generate_base()


# db-sessions
def get_bookstore_db():
    bookstore_db = SessionLocal_Bookstore()
    try:
        yield bookstore_db
    finally:
        bookstore_db.close()

def get_coffee_shop_db():
    coffee_shop_db = SessionLocal_Coffee_Shop()
    try:
        yield coffee_shop_db
    finally:
        coffee_shop_db.close()