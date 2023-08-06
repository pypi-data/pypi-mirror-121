from typing import Text
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.orm import declarative_base, registry
from dataclasses import dataclass
from sqlalchemy import MetaData
from sqlalchemy.sql.sqltypes import TEXT

from .base import Base

@dataclass
class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    job_id = Column(String(64))
    program_id = Column(String(64))
    job_status = Column(String(64))
    pod_name = Column(String(64))
    pod_status = Column(String(64))
    data_token = Column(String(64))
    msg_token = Column(String(64))