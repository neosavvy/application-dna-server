import uuid
from sqlalchemy import Column, String, DateTime, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from dna.common.model.base_types import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=str(uuid.uuid4()))
    updated_at = Column(DateTime(timezone=True), server_default=text('now()'), onupdate=datetime.now)
    username = Column(Text, nullable=True, unique=True)
    full_name = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True)
    website = Column(Text, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'updated_at': self.updated_at.isoformat(),
            'username': self.username,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'website': self.website
        }
