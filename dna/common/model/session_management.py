import asyncio
import contextlib
import os
from functools import wraps
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as sa_sessionmaker, Session, scoped_session
from sqlalchemy import event
from sqlalchemy.exc import DatabaseError

from . import connection_string

logging.getLogger('sqlalchemy.pool')
logger = logging.getLogger('foliofficient.dna.db.core')
logger.info("Initializing database pool")

global_engine = create_engine(connection_string, pool_size=2, max_overflow=20, echo=False)
session_factory = sa_sessionmaker(bind=global_engine)
global_session = scoped_session(session_factory)



@contextlib.contextmanager
def create_session() -> Session:
    """
    Contextmanager that will create and teardown a global_session.
    """
    session = global_session()
    try:
        logger.debug("Returning session")
        yield session
        logger.debug("Committing session")
        session.commit()
        logger.debug("Session committed, returning")
    except DatabaseError as e:
        logger.error(f"Session rolled back due to error: {str(e)}")
        session.rollback()
        raise


def managed_session(func):
    """
    Function decorator that provides a global_session if it isn't provided.
    If you want to reuse a global_session or run the function as part of a
    database transaction, you pass it to the function, if not this wrapper
    will create one and close it for you.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_session = 'session'

        func_params = func.__code__.co_varnames
        func_name = func.__name__
        session_in_args = arg_session in func_params and func_params.index(arg_session) < len(args)
        session_in_kwargs = arg_session in kwargs

        if session_in_kwargs or session_in_args:
            # session was already provided by the ultimate method caller
            logger.debug(f"Session provided to {func_name}, return immediately")
            if not asyncio.iscoroutinefunction(func):
                # func isn't a coroutine so invoke it normally
                return func(*args, **kwargs)
            else:
                # func is a coroutine, so invoke it asynchronously
                async def execute():
                    return await func(*args, **kwargs)

                return execute()
        else:
            # session wasn't provided by ultimate method caller, so provide one
            logger.debug(f"No session provided to {func_name}, creating a new one")
            if not asyncio.iscoroutinefunction(func):
                # func isn't a corutine so invoke it normally
                with create_session() as session:
                    kwargs[arg_session] = session
                    logger.debug(f"Session returned to func {func_name}")
                    return func(*args, **kwargs)
            else:
                # func is a corutine, so invoke it asynchronously
                async def execute():
                    with create_session() as session:
                        kwargs[arg_session] = session
                        return await func(*args, **kwargs)

                return execute()

    return wrapper
