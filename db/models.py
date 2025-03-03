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

    # A prompt can have multiple generated content entries (if you support multiple attempts)
    generated_contents = relationship("GeneratedContent", back_populates="prompt", cascade="all, delete")

class GeneratedContent(Base):
    __tablename__ = "generated_contents"
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    content_text = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.now(ist))

    # Relationship back to the prompt
    prompt = relationship("Prompt", back_populates="generated_contents")
    # One-to-one relationship: each generated content record can have one review
    review = relationship("Review", back_populates="generated_content", uselist=False, cascade="all, delete")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("generated_contents.id"), nullable=False)
    updated_content = Column(Text, nullable=False)
    comment = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, default=datetime.now(ist))

    # Relationship back to the generated content
    generated_content = relationship("GeneratedContent", back_populates="review")
