from database import Session
from models import Flat
from datetime import datetime

with Session() as session:
    flat = Flat(rooms=2, price=420.2, area=50.5,
                permalink="abs.kkdsajflk", published=datetime.now())
    session.add(flat)
    session.commit()
