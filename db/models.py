from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from db import Base

ist_offset = timedelta(hours=5, minutes=30)
ist = timezone(ist_offset)

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    prompt_text = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.now(ist))

    # A prompt can have multiple generated content entries
    generated_contents = relationship("GeneratedContent", back_populates="prompt", cascade="all, delete")

class GeneratedContent(Base):
    __tablename__ = "generated_contents"
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Track who generated the content
    content_text = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.now(ist))

    # Relationships
    prompt = relationship("Prompt", back_populates="generated_contents")
    reviews = relationship("Review", back_populates="generated_content", cascade="all, delete")  # **Changed to uselist=True**
    user = relationship("User", back_populates="generated_contents")  # Link to the user who generated it

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)  # **Primary key is review_id**
    content_id = Column(Integer, ForeignKey("generated_contents.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Track who reviewed the content
    updated_content = Column(Text, nullable=False)
    comment = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, default=datetime.now(ist))

    # Relationships
    generated_content = relationship("GeneratedContent", back_populates="reviews")  # **Updated**
    reviewer = relationship("User", back_populates="reviews")  # Link to the user who reviewed it

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(ist))

    # Relationships
    generated_contents = relationship("GeneratedContent", back_populates="user", cascade="all, delete")
    reviews = relationship("Review", back_populates="reviewer", cascade="all, delete")
