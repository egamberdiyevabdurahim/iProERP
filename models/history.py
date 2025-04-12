import models.user
from database_config.db_settings import execute_query
from utils.additions import tas_t


class HistoryModel:
    def __init__(
            self,
            idn = None,
            user_id = None,
            message = None,
            message_id = None,
            created_at = None,
    ):
        self.idn = idn
        self.user_id = user_id
        self.message = message
        self.message_id = message_id
        self.created_at = created_at

    @classmethod
    async def get_table_name(cls):
        return 'history_model'

    @classmethod
    async def create_table(cls):
        query = f"""
        CREATE TABLE IF NOT EXISTS {await cls.get_table_name()} (
            idn SERIAL PRIMARY KEY,
            user_id INT REFERENCES {await models.user.UserModel.get_table_name()}(idn),
            message TEXT,
            message_id TEXT,
            created_at TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW())
        )
        """
        await execute_query(query=query)
        return None

    @classmethod
    async def create(
            cls,
            user_id,
            message,
            message_id
    ):
        query = f"""
        INSERT INTO {await cls.get_table_name()}
        (user_id, message_id, message)
        VALUES ($1, $2, $3)
        """
        return await execute_query(
            query=query,
            params=(user_id, str(message_id), str(message))
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
    async def get_by_user(cls, user):
        query = f"""
            SELECT *
            FROM {await cls.get_table_name()}
            WHERE user_id=$1
            """
        result = await execute_query(
            query=query,
            params=(int(user),),
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []