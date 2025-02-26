# Import a special function from SQLAlchemy that helps us create database models.
from sqlalchemy.ext.declarative import declarative_base

# Create a "Base" from which we will define our database tables.
# This acts as a template for creating the database structure.
Base = declarative_base()