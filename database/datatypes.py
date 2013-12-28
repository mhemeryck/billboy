from datetime import datetime
from sqlalchemy import (Column, Boolean, Integer, Float, String, Enum, DateTime,
                        ForeignKey, Table)
from sqlalchemy.orm import relationship

from database import Base


class Bill(Base):
    
    """Shopping bill"""
    
    __tablename__ = 'bills'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now())
    amount = Column(Float)
    paid_by = Column(Enum('katrien', 'martijn'))
    