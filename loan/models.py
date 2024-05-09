import os
from contextlib import contextmanager
import sqlalchemy as sqa
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = sqa.create_engine("sqlite:///data.db")

@contextmanager
def session():
    db_name = "data.db"
    #db_file = f"{os.path.dirname(os.path.realpath(__file__))}/{db_name}"
    conn = engine.connect()
    session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    yield session
    session.commit()
    session.close()
    conn.close()

class User(Base):
    __tablename__ = "user"
    username = sqa.Column(sqa.String, primary_key=True)
    loan = sqa.Column(sqa.Float)
    rate = sqa.Column(sqa.Float)
    month_loaned = sqa.Column(sqa.Integer)
    year_loaned = sqa.Column(sqa.Integer)
    #payments = relationship("Payment", backref=backref("user"))

    @classmethod
    def get(cls, username):
        with session() as db:
            return db.query(cls).filter_by(username=username).first()

    @classmethod
    def create(cls, username, loan, rate, month_loaned, year_loaned):
        with session() as db:
            user = cls(
                username=username,
                loan=loan,
                rate=rate,
                month_loaned=month_loaned,
                year_loaned=year_loaned
            )
            db.add(user)
            return user
    
    @classmethod
    def all(cls):
        with session() as db:
            return db.query(cls).all()
    
    @classmethod
    def username_exists(cls, username):
        with session() as db:
            return db.query(cls).filter_by(username=username).first() is not None
    
    def all_payments(self):
        with session() as db:
            return list(db.query(Payment).filter_by(username=self.username))

class Payment(Base):
    __tablename__ = "payment"
    pk = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    username = sqa.Column(sqa.String, sqa.ForeignKey("user.username"))
    amount = sqa.Column(sqa.Float)
    month = sqa.Column(sqa.Integer)
    year = sqa.Column(sqa.Integer)

    @classmethod
    def record(cls, user, amount, month, year):
        with session() as db:
            payment = cls(
                username=user.username,
                amount=amount,
                month=month,
                year=year
            )
            db.add(payment)
            return payment
    
    @classmethod
    def all(cls):
        with session() as db:
            return db.query(cls).all()
    
    def __str__(self):
        return (f"pk={self.pk}, username={self.username}, amount={self.amount},"
            f" month={self.month}, year={self.year}")

Base.metadata.create_all(engine)
