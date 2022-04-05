from datetime import datetime, timedelta
from lib2to3.pgen2.token import GREATEREQUAL
from typing import Optional, Sequence

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Interval
from sqlalchemy import func, select, text, desc, and_, or_
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class GetRequestEntity(Base):
    """
    An Orm model for a get request.

    If we captured addition request actions, i.e PUT, POST etc..
    we should think about wheter they get a model of theyre own or perhaps
    have a RequestEntity with an action field on it. For the purposes of this project
    I chose to have a specific model.
    """
    __tablename__ = 'get_requests'

    id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    duration = Column(Interval)
    target_url = Column(String)
    response_code = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "target_url": self.target_url,
            "response_code": self.response_code
        }

    def __repr__(self) -> str:
        return "<GetRequest(id='{}', timestamp='{}', duration='{}', target_url='{}', response_code='{}')>".format(
            self.id, self.timestamp, self.duration, self.target_url, self.response_code)

class Repository:
    '''
    Storage access abstraction.

    Ideally, the rest of the application is not decoupled to any storage related models,
    those are only technicalities.
    '''
    def __init__(self):
        pass

    def connect(self):
        # Sqlite is very primitive ofcourse, we can change it easily (mostly) to any other
        # sqlalchemy backends.
        # Even if we couldn't, due to the Repository's abstraction, we could change the
        # framework easily, i.e using pymongo or other tools.
        self.engine = create_engine("sqlite:///db.sqlite3", echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def insert_get_request(self,
            id: str, timestamp: float, duration: float, target_url: str, response_code: int):
        entity = GetRequestEntity(
            id=id,
            timestamp=datetime.fromtimestamp(timestamp),
            duration=timedelta(seconds=duration),
            target_url=target_url,
            response_code=response_code)
        self.session.add(entity)
        self.session.commit()

    def all_get_requests(self) -> Sequence[GetRequestEntity]:
        return self.session.query(GetRequestEntity)

    # Ideally, the function would not return the GetRequestEntity which is an
    # object used for configuring the ORM.
    # Again, splitting this seemed like an overkill.
    def find_get_request_by_id(self, id: str) -> Optional[GetRequestEntity]:
        return self.session.query(GetRequestEntity).get(id)

    def find_frequent_website(self) -> Optional[str]:
        ans = self.session.query(
            GetRequestEntity.target_url,
            func.count(GetRequestEntity.id).label("count")
            ).group_by(GetRequestEntity.target_url).order_by(desc(text("count"))).limit(1)

        for record in ans:
            return record[0]

        return None
    
    def find_in_time_frame(self, from_time: datetime, to_time: datetime) -> Sequence[GetRequestEntity]:
        items = self.session.query(GetRequestEntity)

        # It could be better to be performed in the database instead of pulling everything in
        # (Although it is buffered i guess..)
        # But, sqlalchemy :(
        # Anyway, the logic is by exclusion
        in_time_frame = []
        for item in items:
            if item.timestamp + item.duration < from_time:
                continue
            if item.timestamp > to_time:
                continue
            in_time_frame.append(item)
        return in_time_frame