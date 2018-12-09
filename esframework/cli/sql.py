from sqlalchemy import create_engine
from esframework.data_sources.sqlalchemy.models import SqlDomainRecord


def create_event_store():
    print("Setting up - event store")
    engine = create_engine('sqlite:///:memory:', echo=True)
    model = SqlDomainRecord()
    model.metadata.create_all(engine)
    print("Done setting up event store")


def truncate_event_store():
    print("Truncating event store")
