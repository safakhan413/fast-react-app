# models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from .database import Base

class Cluster(Base):
    __tablename__ = 'Clusters'

    clusterId = Column(String(50), primary_key=True)

    # Relationships
    users = relationship('User', back_populates='cluster')

    def __repr__(self):
        return f"<Cluster(clusterId='{self.clusterId}')>"

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)  # _id from JSON
    userId = Column(String(9), unique=True, nullable=False)
    originationTime = Column(Integer, nullable=False)
    clusterId = Column(String(50), ForeignKey('Clusters.clusterId', ondelete='SET NULL', onupdate='CASCADE'))

    # Relationships
    cluster = relationship('Cluster', back_populates='users')
    phones = relationship('Phone', secondary='User_Phones', back_populates='users')
    voicemails = relationship('Voicemail', secondary='User_Voicemails', back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, userId='{self.userId}')>"

class Phone(Base):
    __tablename__ = 'Phones'

    phoneId = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String(20), unique=True, nullable=False)
    phoneModel = Column(String(50), nullable=True)
    purchaseDate = Column(String(50), nullable=True)  # Changed to String to accommodate NULL or string data

    # Relationships
    users = relationship('User', secondary='User_Phones', back_populates='phones')

    def __repr__(self):
        return f"<Phone(identifier='{self.identifier}')>"

class Voicemail(Base):
    __tablename__ = 'Voicemails'

    vmId = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String(20), unique=True, nullable=False)
    setupDate = Column(String(50), nullable=True)  # Changed to String to accommodate NULL or string data
    storageCapacity = Column(Integer, nullable=True)

    # Relationships
    users = relationship('User', secondary='User_Voicemails', back_populates='voicemails')

    def __repr__(self):
        return f"<Voicemail(identifier='{self.identifier}')>"

class UserPhones(Base):
    __tablename__ = 'User_Phones'
    userId = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    phoneId = Column(Integer, ForeignKey('Phones.phoneId', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    def __repr__(self):
        return f"<UserPhones(userId={self.userId}, phoneId={self.phoneId})>"

class UserVoicemails(Base):
    __tablename__ = 'User_Voicemails'
    userId = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    vmId = Column(Integer, ForeignKey('Voicemails.vmId', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    def __repr__(self):
        return f"<UserVoicemails(userId={self.userId}, vmId={self.vmId})>"
