from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import create_engine, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:////Users/andrey/Desktop/Bybit_traiding_bot/DataBase/karlov_risk_bot.db')

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    gold_standards = relationship('GoldStandard', back_populates='user', cascade='all, delete-orphan',
                                  overlaps="gold_standards")
    high_risks = relationship('HighRisk', back_populates='user', cascade='all, delete-orphan', overlaps="high_risks")
    passive_portfolios = relationship('PassivePortfolio', back_populates='user', cascade='all, delete-orphan',
                                      overlaps="passive_portfolios")


class GoldStandard(Base):
    __tablename__ = 'gold_standard'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    deposit = Column(Integer, nullable=False)
    user = relationship("User", backref='gold_standard')


class HighRisk(Base):
    __tablename__ = 'high_risk'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    deposit = Column(Integer, nullable=False)
    user = relationship("User", backref='high_risk')


class PassivePortfolio(Base):
    __tablename__ = 'passive_portfolio'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    deposit = Column(Integer, nullable=False)
    user = relationship("User", backref='passive_portfolio')


def add_user_in_users(tg_id):
    user = session.query(User).filter_by(telegram_id=tg_id).one_or_none()
    if user is None:
        new_user = User(telegram_id=tg_id)
        session.add(new_user)
        print("User with telegram_id {} added to the database.".format(tg_id))
        session.commit()


def delete_user_in_users(tg_id):
    user = session.query(User).filter_by(telegram_id=tg_id).one_or_none()
    if user:
        session.delete(user)  # Используйте полученный экземпляр пользователя
        session.commit()
        print("Пользователь с telegram_id {} удален из базы данных.".format(tg_id))
    else:
        print("Пользователь с telegram_id {} не найден.".format(tg_id))


def check_id_in_db(tg_id):
    id = session.query(User.telegram_id).filter_by(telegram_id=tg_id).first()
    if id:
        return True
    else:
        return False


def check_id_in_gold(tg_id):
    id = session.query(GoldStandard.user_id).filter_by(user_id=tg_id).first()
    if id:
        return True
    else:
        return False


def check_id_in_high(tg_id):
    id = session.query(HighRisk.user_id).filter_by(user_id=tg_id).first()
    if id:
        return True
    else:
        return False


def check_id_in_passive(tg_id):
    id = session.query(PassivePortfolio.user_id).filter_by(user_id=tg_id).first()
    if id:
        return True
    else:
        return False


def passive_deposite(tg_id):
    deposite = session.query(PassivePortfolio.deposit).filter_by(user_id=tg_id).first()
    if deposite:
        return deposite[0]
    else:
        return None


def gold_deposite(tg_id):
    deposite = session.query(GoldStandard.deposit).filter_by(user_id=tg_id).first()
    if deposite:
        return deposite[0]
    else:
        return None


def heigh_deposite(tg_id):
    deposite = session.query(HighRisk.deposit).filter_by(user_id=tg_id).first()
    if deposite:
        return deposite[0]
    else:
        return None


def add_user_in_gold(tg_id, deposit):
    new_user = GoldStandard(user_id=tg_id, deposit=deposit)
    session.add(new_user)
    session.commit()


def add_user_in_high(tg_id, deposit):
    new_user = HighRisk(user_id=tg_id, deposit=deposit)
    session.add(new_user)
    session.commit()


def add_user_in_passive(tg_id, deposit):
    user = session.query(PassivePortfolio).filter_by(user_id=tg_id).first()
    if user:
        session.delete(user)
        session.commit()
    else:
        print("User not found in HighRisk table")


def delete_user_in_gold(tg_id):
    user = session.query(GoldStandard).filter_by(user_id=tg_id).first()
    if user:
        session.delete(user)
        session.commit()
    else:
        print("User not found in HighRisk table")


def delete_user_in_high(tg_id):
    user = session.query(HighRisk).filter_by(user_id=tg_id).first()
    if user:
        session.delete(user)
        session.commit()
    else:
        print("User not found in HighRisk table")


def delete_user_in_passive(tg_id):
    user = PassivePortfolio(user_id=tg_id)
    session.delete(user)
    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
