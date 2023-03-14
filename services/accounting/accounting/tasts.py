import asyncio
from datetime import datetime, timedelta, date

from library.rmq_broker.events import SalaryPaymentEvent
from accounting.db.connection import SessionLocal
from accounting.db.repositories import SalaryPaymentRepository


async def daily_notify_salary_payment(event_queue: asyncio.Queue[SalaryPaymentEvent]):
    date_ = datetime.today()

    while True:
        date_end = datetime.combine(date_, datetime.max.time())
        second_to_wait = (date_end - datetime.now()).total_seconds()

        await asyncio.sleep(second_to_wait)
        await notify_salary_payment(event_queue, date_=date_)

        date_ += timedelta(days=1)


async def notify_salary_payment(event_queue: asyncio.Queue[SalaryPaymentEvent], date_: date):
    db = SessionLocal()
    salary_repository = SalaryPaymentRepository(db)

    salaries = salary_repository.list(date_=date_)
    for salary in salaries:
        event = SalaryPaymentEvent(
            user_public_id=salary.user.public_id,
            date=date_,
            amount=salary.amount
        )
        await event_queue.put(event)
        salary_repository.add(salary)
    salary_repository.session.commit()
