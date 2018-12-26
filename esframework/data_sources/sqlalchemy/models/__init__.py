from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON, UniqueConstraint

Base = declarative_base()


class SqlDomainRecord(Base):
    __tablename__ = 'event_store'

    domain_event_id = Column(String(length=36), primary_key=True, nullable=False)
    aggregate_root_id = Column(String(length=36), nullable=False)
    version = Column(Integer, nullable=False)
    domain_event_name = Column(String(length=255), nullable=False)
    domain_event_body = Column(JSON, nullable=False)
    store_date = Column(String(length=50), nullable=False)
    event_date = Column(String(length=50), nullable=False)
    correlation_id = Column(String(length=36), nullable=False)
    causation_id = Column(String(length=36), nullable=False)
    event_metadata = Column(JSON, nullable=False)

    UniqueConstraint('aggregate_root_id', 'version', name='uix_1')

    def __repr__(self):
        return "<EventStoreRecord(" \
               "domain_event_id='%s', " \
               "aggregate_root_id='%s', " \
               "version='%s'" \
               "domain_event_name='%s'" \
               "domain_event_body='%s'" \
               "store_date='%s'" \
               "event_date='%s'" \
               "correlation_id='%s'" \
               "causation_id='%s'" \
               "event_metadata='%s'" \
               ")>" % \
               (self.domain_event_id, self.aggregate_root_id, self.version,
                self.domain_event_name, self.domain_event_body, self.store_date,
                self.event_date, self.correlation_id, self.causation_id,
                self.event_metadata)
