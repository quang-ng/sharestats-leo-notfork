from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Works(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    modified_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    initial_document_id = Column(
        LargeBinary, ForeignKey("documents.hash"), nullable=False
    )
    primary_document_hash = Column(
        LargeBinary, ForeignKey("documents.hash"), nullable=False
    )
    provenance_id = Column(Integer, ForeignKey("provenance.id"))

    # Relationships
    initial_document = relationship("Documents", foreign_keys=[initial_document_id])
    primary_document = relationship("Documents", foreign_keys=[primary_document_hash])
    provenance = relationship("Provenance")


class Documents(Base):
    __tablename__ = "documents"

    hash = Column(LargeBinary, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    s3uri = Column(Text, nullable=False)
    publication_id = Column(Integer, ForeignKey("publication.id"))
    provenance_id = Column(Integer, ForeignKey("provenance.id"))

    # Relationships
    provenance = relationship("Provenance")
    rtransparent = relationship("RTransparent", back_populates="document")
    xml = relationship("XML", back_populates="document")


class RTransparent(Base):
    __tablename__ = "rtransparent"

    id = Column(Integer, primary_key=True)
    document_hash = Column(LargeBinary, ForeignKey("documents.hash"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    version = Column(String(50))
    provenance_id = Column(Integer, ForeignKey("provenance.id"))

    # Relationships
    document = relationship("Documents", back_populates="rtransparent")
    provenance = relationship("Provenance")


class Provenance(Base):
    __tablename__ = "provenance"

    id = Column(Integer, primary_key=True)
    pipeline_name = Column(String(255))
    version = Column(String(50))
    compute = Column(Text)
    personnel = Column(Text)
    comment = Column(Text)


class XML(Base):
    __tablename__ = "xml"

    id = Column(Integer, primary_key=True)
    document_hash = Column(LargeBinary, ForeignKey("documents.hash"), nullable=False)
    xml = Column(Text)

    # Relationships
    document = relationship("Documents", back_populates="xml")
