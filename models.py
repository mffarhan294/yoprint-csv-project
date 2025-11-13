from sqlalchemy import Column, Integer, String, Float, DateTime, Text, UniqueConstraint
from datetime import datetime
from db import Base

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    status = Column(String, default="pending")
    message = Column(Text)
    total_rows = Column(Integer, default=0)
    success_rows = Column(Integer, default=0)
    error_rows = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "status": self.status,
            "message": self.message,
            "total_rows": self.total_rows,
            "success_rows": self.success_rows,
            "error_rows": self.error_rows,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    unique_key = Column(String, nullable=False, unique=True)
    product_title = Column(Text)
    product_description = Column(Text)
    style = Column(String)
    sanmar_mainframe_color = Column(String)
    size = Column(String)
    color_name = Column(String)
    piece_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("unique_key", name="uq_products_unique_key"),
    )
