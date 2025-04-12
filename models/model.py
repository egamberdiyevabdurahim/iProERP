import models.user
from database_config.db_settings import execute_query
from utils.additions import tas_t


class ModelModel:
    def __init__(
            self,
            idn = None,
            head = None,
            name = None,
            status = None,
            is_deleted = None,
            created_by = None,
            updated_by = None,
            deleted_by = None,
            created_at = None,
            updated_at = None,
            deleted_at = None
    ):
        self.idn = idn
        self.head = head
        self.name = name
        self.status = status
        self.is_deleted = is_deleted
        self.created_by = created_by
        self.updated_by = updated_by
        self.deleted_by = deleted_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @classmethod
    async def get_table_name(cls):
        return 'model_model'

    @classmethod
    async def create_table(cls):
        query = f"""
            CREATE TABLE IF NOT EXISTS {await cls.get_table_name()} (
                idn BIGSERIAL PRIMARY KEY,
                head INT,
                name VARCHAR(255),
                status SMALLINT defAULT 0,
                is_deleted BOOLEAN defAULT FALSE,
                created_by INT REFERENCES {await models.user.UserModel.get_table_name()}(idn),
                updated_by INT REFERENCES {await models.user.UserModel.get_table_name()}(idn),
                deleted_by INT REFERENCES {await models.user.UserModel.get_table_name()}(idn),
                created_at TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW()),
                updated_at TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW()),
                deleted_at TIMESTAMPTZ
            )
            """
        await execute_query(query=query)
        return None

    @classmethod
    async def create(
            cls,
            head=None,
            name=None,
            status=None,
            created_by=None
    ):
        query = f"""
            INSERT INTO {await cls.get_table_name()}
            (head, name, status, created_by)
            VALUES ($1, $2, $3, $4)
            """
        return await execute_query(
            query=query,
            params=(head, name, status, created_by)
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
    async def get_heads(cls):
        query = f"""
                SELECT *
                FROM {await cls.get_table_name()}
                WHERE head IS NULL
                """
        result = await execute_query(
            query=query,
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_head(cls, head):
        query = f"""
                SELECT *
                FROM {await cls.get_table_name()}
                WHERE head=$1
                """
        result = await execute_query(
            query=query,
            params=(int(head),),
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_name(cls, name):
        query = f"""
                SELECT *
                FROM {await cls.get_table_name()}
                WHERE name=$1
                """
        result = await execute_query(
            query=query,
            params=(name,),
            fetch='one'
        )
        if result:
            return cls(**result)
        return None