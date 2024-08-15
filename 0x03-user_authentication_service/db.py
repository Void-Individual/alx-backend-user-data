#!/usr/bin/env python3
"""Module containing the db class"""

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

# from typing import TypeVar
from user import Base, User
# T = TypeVar('T', bound='User')


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method to save user to tghe database and return
        a user object"""

        if email and hashed_password:
            session = self._session
            user = User()
            user.email = email
            user.hashed_password = hashed_password
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

        return None

    def find_user_by(self, **kwargs) -> None:
        """This method takes in keyword args and returns the first row
        found in the users table as filtered by the methods input args"""

        if not kwargs:
            raise InvalidRequestError("No args were passed")

        session = self._session
        try:
            resp = session.query(User).filter_by(**kwargs).one()
            return resp
        except NoResultFound:
            raise NoResultFound("No results match")
        except InvalidRequestError:
            raise InvalidRequestError("")
