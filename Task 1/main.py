from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

# Связующая таблица для отношений между игроками и бустами
player_boost = Table('player_boost', Base.metadata,
    Column('player_id', ForeignKey('players.id'), primary_key=True),
    Column('boost_id', ForeignKey('boosts.id'), primary_key=True),
    Column('quantity', Integer, default=1)
)

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    first_login = Column(DateTime, default=datetime.utcnow)
    total_points = Column(Integer, default=0)
    
    boosts = relationship("Boost", secondary=player_boost, back_populates="players")
    logins = relationship("Login", back_populates="player")

    def __repr__(self):
        return f"<Player(name='{self.name}', first_login='{self.first_login}', total_points='{self.total_points}')>"

class Boost(Base):
    __tablename__ = 'boosts'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    
    players = relationship("Player", secondary=player_boost, back_populates="boosts")

    def __repr__(self):
        return f"<Boost(type='{self.type}')>"

class Login(Base):
    __tablename__ = 'logins'
    id = Column(Integer, primary_key=True)
    login_time = Column(DateTime, default=datetime.utcnow)
    player_id = Column(Integer, ForeignKey('players.id'))

    player = relationship("Player", back_populates="logins")

    def __repr__(self):
        return f"<Login(player_id='{self.player_id}', login_time='{self.login_time}')>"

# Создаем БД
engine = create_engine('sqlite:///game.db')
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Пример создания игрока и буста
new_player = Player(name="John Doe")
session.add(new_player)
session.commit()

new_boost = Boost(type="Speed Boost")
session.add(new_boost)
session.commit()

# Пример добавления буста игроку
new_player.boosts.append(new_boost)
session.commit()

print(session.query(Player).all())
print(session.query(Boost).all())
print(session.query(Login).all())
