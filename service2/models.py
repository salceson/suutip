from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    ip = Column(String(15))

    def __init__(self, name, email, ip):
        super(User, self).__init__()
        self.name = name
        self.email = email
        self.ip = ip

    def __repr__(self):
        return '<User %r>' % self.name
