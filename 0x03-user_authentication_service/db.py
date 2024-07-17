"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import bcrypt
from bcrypt import hashpw
from user import Base, User


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

    def add_user(self, email, hashed_password):
        """
            Adds user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        """
        Find a user by arbitrary keyword arguments.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound(f"No user found with the specified attributes")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided")

    def update_user(self, user_id, **kwargs):
        """
        Update the user's attributes as passed in the method's arguments then
        commit changes to the database
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if not hasattr(user, k):
                raise ValueError("Invalid Attribute")
            setattr(user, k, v)
        self._session.commit()
