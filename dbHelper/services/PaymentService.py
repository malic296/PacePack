from dbHelper.DBModels import Payment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class PaymentService:
    def __init__(self):
        self.session = SessionLocal()

    def add_payment(self, price, state, payment_date, userid):
        new_payment = Payment(
            price=price,
            state=state,
            date=payment_date,
            userid=userid
        )
        self.session.add(new_payment)
        self.session.commit()
        return new_payment.id

    def get_payment_by_id(self, payment_id):
        return self.session.query(Payment).filter(Payment.id == payment_id).first()

    def get_all_payments(self):
        return self.session.query(Payment).all()

    def delete_payment(self, payment_id):
        payment = self.get_payment_by_id(payment_id)
        if payment:
            self.session.delete(payment)
            self.session.commit()
            return True
        return False

    def close(self):
        self.session.close()
