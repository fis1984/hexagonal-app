# src/infrastructure/persistence/unit_of_work.py
from sqlalchemy.orm import sessionmaker
from core.ports.i_unit_of_work import IUnitOfWork

class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()