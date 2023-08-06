from typing import Text
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base, registry
from dataclasses import dataclass
from sqlalchemy import MetaData
from sqlalchemy.sql.sqltypes import TEXT

from .base import Base

@dataclass
class RuntimeProgram(Base):
    __tablename__ = 'runtime_program'

    id = Column(Integer, primary_key=True)
    program_id = Column(String(64))
    user_id = Column(Integer)
    name = Column(String(64))
    data = Column(LargeBinary(length=(2**32)-1))
    program_metadata = Column(TEXT)
    status = Column(String(64))
    data_type = Column(String(64))
