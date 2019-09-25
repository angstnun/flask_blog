import click
from flask_sqlalchemy import SQLAlchemy as sa
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import (
    Table, Column, Integer, 
    String, MetaData, ForeignKey,
    Boolean, Date, Text, DateTime
)
from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import (
    sessionmaker, relationship
)

metadata = MetaData()
engine = create_engine('mssql+pyodbc://sa:sindrome@localhost/flaskr?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server', poolclass=NullPool)
Session = sessionmaker(bind=engine)

users = Table('user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False),
    Column('password', String(128), nullable=False),
    Column('dateCreated', DateTime, nullable=False, server_default=func.now()),
    Column('dateUpdated', DateTime, nullable=False, server_default=func.now(), onupdate=func.now()),
    Column('isActive', Boolean, default=True),

)

posts = Table('post', metadata,
    Column('id', Integer, primary_key=True),
    Column('author_id', Integer, ForeignKey("user.id"), nullable=False),
    Column('title', String(128), nullable=False),
    Column('text', Text, nullable=False),
    Column('dateCreated', DateTime, nullable=False, server_default=func.now()),
    Column('dateUpdated', DateTime, nullable=False, server_default=func.now(), onupdate=func.now()),
    Column('isActive', Boolean, default=True),
)

metadata.reflect(engine, only=['user', 'post'])
Base = automap_base(metadata=metadata)
Base.prepare()
User, Post = Base.classes.user, Base.classes.post

def GetDB():
    connection = engine.connect()
    return connection
    
def GetSession():
    newSession = Session()
    return newSession
    
database = sa()

@click.command('init-db')
@with_appcontext
def init_db_command():
    metadata.create_all(GetDB())
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(init_db_command)
