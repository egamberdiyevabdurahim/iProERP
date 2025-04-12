import models.user
from database_config.db_settings import execute_query
from utils.additions import tas_t


class DailyReportWorkerModel:
    def __init__(
            self,
            idn = None,
            user_id = None,
            start = None,
            ends = None,
            created_at = None,
            updated_at = None,
    ):
        self.idn = idn
        self.user_id = user_id
        self.start = start
        self.ends = ends
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    async def get_table_name(cls):
        return 'daily_report_worker_model'

    @classmethod
    async def create_table(cls):
        query = f"""
        CREATE TABLE IF NOT EXISTS {await cls.get_table_name()} (
            idn SERIAL PRIMARY KEY,
            user_id INT REFERENCES {await models.user.UserModel.get_table_name()}(idn),
            start TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW()),
            ends TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW()),
            updated_at TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW())
        )
        """
        await execute_query(query=query)
        return None

    @classmethod
    async def create(
            cls,
            user_id
    ):
        query = f"""
        SELECT *
        FROM {await cls.get_table_name()}
        WHERE user_id=$1 AND ends IS NULL
        """
        result = await execute_query(
            query=query,
            params=(user_id,)
        )
        if not result:
            query = f"""
            INSERT INTO {await cls.get_table_name()}
            (user_id)
            VALUES ($1)
            RETURNING idn
            """
            return await execute_query(
                query=query,
                params=(int(user_id),)
            )
        return None

    @classmethod
    async def end(
            cls,
            user_id
    ):
        query = f"""
        UPDATE {await cls.get_table_name()}
        SET ends=$1, updated_at=$2
        WHERE user_id=$3 AND ends IS NULL
        """
        return await execute_query(
            query=query,
            params=(tas_t(), tas_t(), int(user_id))
        )

    @classmethod
    async def column_updater(cls, idn, col_name, data):
        query = f"""
        UPDATE {await cls.get_table_name()}
        SET {col_name}=$1, updated_at=$2
        WHERE idn=$3
        """
        return await execute_query(
            query=query,
            params=(data, tas_t(), int(idn))
        )

    @classmethod
    async def get_data(cls, idn):
        query = f"""
        SELECT *
        FROM {await cls.get_table_name()}
        WHERE idn=$1
        """
        result = await execute_query(
            query=query,
            params=(int(idn),),
            fetch='one'
        )
        if result:
            return cls(**result)
        return None

    @classmethod
    async def get_all(cls):
        query = f"""
        SELECT *
        FROM {await cls.get_table_name()}
        """
        result = await execute_query(
            query=query,
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_user(cls, user_id):
        query = f"""
            SELECT *
            FROM {await cls.get_table_name()}
            WHERE user_id=$1
            """
        result = await execute_query(
            query=query,
            params=(int(user_id),),
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_user_active(cls, user_id):
        query = f"""
                SELECT *
                FROM {await cls.get_table_name()}
                WHERE user_id=$1 AND ends IS NULL
                """
        result = await execute_query(
            query=query,
            params=(int(user_id),),
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []