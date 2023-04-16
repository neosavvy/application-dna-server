import datetime
import json
import uuid

import pytz
from sqlalchemy import Column, func, MetaData
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, Mutable
from sqlalchemy.orm.session import object_session
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy import DDL, event

meta = MetaData(naming_convention={"ix": "ix_%(column_0_label)s",
                                   "uq": "uq_%(table_name)s_%(column_0_name)s",
                                   "ck": "ck_%(table_name)s_%(constraint_name)s",
                                   "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                                   "pk": "pk_%(table_name)s"
                                   })

Base = declarative_base(metadata=meta)

CASCADE = 'all, delete-orphan'

class HasCreateTime(object):
    """Add created_at"""
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)


class HasCreateEventTime(HasCreateTime):
    """created_at + event_at"""
    event_at = Column(DateTime(timezone=True), nullable=False, index=True)


class HasCreateUpdateTime(HasCreateTime):
    """created_at + updated_at"""
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(),
                        nullable=False, index=True)


class HasDeleteTime(object):
    """deleted_at"""
    deleted_at = Column(DateTime(timezone=True), default=None, nullable=True, index=True)

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def mark_deleted(self):
        self.deleted_at = datetime.datetime.now(tz=pytz.utc)


class HasCreateUpdateDeleteTime(HasCreateUpdateTime, HasDeleteTime):
    """created_at + updated_at + deleted_at"""
