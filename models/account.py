import models.user
from database_config.db_settings import execute_query
from utils.additions import tas_t


class AccountModel:
    def __init__(
            self,
            idn = None,
            chat_id = None,
            role = None,
            created_at = None,
            updated_at = None,
            created_by = None,
            updated_by = None,
    ):
        self.idn = idn
        self.chat_id = chat_id
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by

    @classmethod
    async def get_table_name(cls):
        return 'account_model'

    @classmethod
    async def create_table(cls):
        query = f"""
            CREATE TABLE {await cls.get_table_name()} (
                idn SERIAL PRIMARY KEY,
                chat_id VARCHAR(255),
                role INT,
                created_at TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW()),
                updated_at TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW()),
                created_by INT,
                updated_by INT
            )
        """
        await execute_query(query=query)
        return None

    @classmethod
    async def create(
            cls,
            chat_id,
            created_by,
            role,
    ):
        query = f"""
        INSERT INTO {await cls.get_table_name()}
        (chat_id, created_by, role)
        VALUES ($1,$2,$3)
        """
        return await execute_query(
            query=query,
            params=(str(chat_id), created_by, role)
        )

    @classmethod
    async def delete(cls, chat_id):
        query = f"""
        DELETE FROM {await cls.get_table_name()}
        WHERE chat_id=$1
        """
        return await execute_query(
            query=query,
            params=(str(chat_id),)
        )

    @classmethod
    async def column_updater(cls, idn, col_name, data, updated_by=None):
        if updated_by:
            query = f"""
            UPDATE {await cls.get_table_name()}
            SET {col_name}={data}, updated_at=$1, updated_by=$2
            WHERE idn=$3
            """
            return await execute_query(
                query=query,
                params=(tas_t(), updated_by, idn)
            )

        query = f"""
        UPDATE {await cls.get_table_name()}
        SET {col_name}={data}
        WHERE idn=$1
        """
        return await execute_query(
            query=query,
            params=(idn,)
        )

    @classmethod
    async def get_data(cls, chat_id):
        query = f"""
        SELECT idn, chat_id, role, created_by, updated_by, created_at, updated_at
        FROM {await cls.get_table_name()}
        WHERE chat_id=$1
        """
        data = await execute_query(
            query=query,
            params=(str(chat_id),),
            fetch='one'
        )
        if data:
            return cls(**data)
        return None

    @classmethod
    async def get_data_by_idn(cls, idn):
        query = f"""
            SELECT idn, chat_id, role, created_by, updated_by, created_at, updated_at
            FROM {await cls.get_table_name()}
            WHERE idn=$1
            """
        data = await execute_query(
            query=query,
            params=(int(idn),),
            fetch='one'
        )
        if data:
            return cls(**data)
        return None

    @classmethod
    async def get_all(cls, ex=None):
        query = f"""
        SELECT idn, chat_id, role, created_by, updated_by, created_at, updated_at
        FROM {await cls.get_table_name()}
        WHERE 1=1 {ex}
        """
        result = await execute_query(
            query=query,
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []
