import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist, album=None):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    if album is None:
        albums = session.query(Album).filter(Album.artist == artist).all()
    else:
        albums = session.query(Album).filter(Album.artist == artist).filter(Album.album == album).all()
    return albums


def savetodb(rec):
    """
    Сохраняет данные в БД
    """

    newalbum = Album(
        year=rec["year"],
        artist=rec["artist"],
        genre=rec["genre"],
        album=rec["album"]
    )
    session = connect_db()
    session.add(newalbum)
    session.commit()