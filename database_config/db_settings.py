import asyncpg
import logging
from database_config.config import DB_CONFIG

class DatabaseError(Exception):
    """Custom exception for handling database errors."""
    pass

class AsyncDatabase:
    def __init__(self):
        self.conn = None
        self.transaction = None

    async def __aenter__(self):
        try:
            self.conn = await asyncpg.connect(**DB_CONFIG)
            self.transaction = self.conn.transaction()
            await self.transaction.start()
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")
            raise DatabaseError("Failed to connect to the database.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.transaction.rollback()
                logging.error(f"Error in DB operation: {exc_val}")
            else:
                await self.transaction.commit()
        finally:
            if self.conn is not None:
                await self.conn.close()

    async def execute(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE)"""
        try:
            await self.conn.execute(query, *params)
        except Exception as e:
            logging.error(f"Exception during query execution: {e}")
            raise DatabaseError(f"Failed to execute query: {query}")

    async def fetchone(self, query, params=None):
        """Fetch a single row from the database"""
        try:
            return await self.conn.fetchrow(query, *params)
        except Exception as e:
            logging.error(f"Exception during fetchone: {e}")
            raise DatabaseError("Failed to fetch data.")

    async def fetchall(self, query, params=None):
        """Fetch multiple rows from the database"""
        try:
            return await self.conn.fetch(query, *params)
        except Exception as e:
            logging.error(f"Exception during fetchall: {e}")
            raise DatabaseError("Failed to fetch data.")

    async def execute_and_fetch(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE) and fetch the result"""
        try:
            return await self.conn.fetchrow(query, *params)
        except Exception as e:
            logging.error(f"Exception during execute_and_fetch: {e}")
            raise DatabaseError(f"Failed to execute query: {query}")

async def execute_query(query, params=None, fetch=None):
    """Run async queries properly"""
    async with AsyncDatabase() as db:
        params = params or ()
        print(query)
        print(params)
        print(fetch)
        data = None
        if fetch == "all":
            data = await db.fetchall(query, params)
        elif fetch == "one":
            data = await db.fetchone(query, params)
        elif fetch == "return":
            data = await db.execute_and_fetch(query, params)
        else:
            await db.execute(query, params)

        print(data)

        return data
