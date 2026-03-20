from sqlalchemy import Column, String, Text, Float
from database import Base


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {"extend_existing": True}

    customer_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    date_of_birth = Column(String)
    account_balance = Column(Float)
    created_at = Column(String)

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "date_of_birth": self.date_of_birth,
            "account_balance": float(self.account_balance)
            if self.account_balance
            else None,
            "created_at": self.created_at,
        }
