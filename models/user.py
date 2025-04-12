from database_config.db_settings import execute_query
from utils.additions import tas_t


class UserModel:
    def __init__(
            self,
            idn = None,
            chat_id = None,
            tg_username = None,
            first_name = None,
            last_name = None,
            email = None,
            phone_number = None,
            password = None,
            used = None,
            role = None,
            is_deleted = None,
            created_at = None,
            updated_at = None,
            deleted_at = None
    ):
        if chat_id:
            chat_id = int(chat_id)
        self.idn = idn
        self.chat_id = chat_id
        self.tg_username = tg_username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.used = used
        self.role = role
        self.is_deleted = is_deleted
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @classmethod
    async def get_table_name(cls):
        return 'user_model'

    @classmethod
    async def create_table(cls):
        query = f"""
        CREATE TABLE IF NOT EXISTS {await cls.get_table_name()} (
            idn SERIAL PRIMARY KEY,
            chat_id VARCHAR(255),
            tg_username VARCHAR(64),
            first_name VARCHAR(64),
            last_name VARCHAR(64),
            email VARCHAR(64),
            phone_number VARCHAR(20),
            password VARCHAR(100),
            used BIGINT DEFAULT 1,
            role SMALLINT DEFAULT 0,
            is_deleted BOOLEAN DEFAULT FALSE,
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
            chat_id: int=None,
            tg_username: str=None,
            first_name: str=None,
            last_name: str=None,
            email: str=None,
            phone_number: str=None,
            password: str=None,
            role: int=0
    ):
        query = f"""
        INSERT INTO {await cls.get_table_name()}
        (chat_id, tg_username, first_name, last_name, email, phone_number, password, role)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """
        return await execute_query(
            query=query,
            params=(str(chat_id), tg_username, first_name, last_name, email, phone_number, password, role)
        )

    @classmethod
    async def delete(cls, chat_id):
        query = f"""
        UPDATE {await cls.get_table_name()}
        SET is_deleted=TRUE, deleted_at=$1
        WHERE chat_id=$2 AND role <> 2
        """
        return await execute_query(
            query=query,
            params=(tas_t(), str(chat_id))
        )

    async def save(self):
        query = f"""
        UPDATE {await self.get_table_name()}
        SET tg_username=$1, first_name=$2, last_name=$3, email=$4, phone_number=$5,
            password=$6, role=$7, is_deleted=$8, updated_at=$9, used=$10
        WHERE idn=$11
        """
        await execute_query(
            query,
            params=(
                self.tg_username, self.first_name, self.last_name, self.email,
                self.phone_number, self.password, self.role, self.is_deleted,
                tas_t(), self.used, self.idn
            )
        )

    async def use(self):
        await self.column_updater(chat_id=self.chat_id, col_name='used', data=self.used+1)

    @classmethod
    async def column_updater(cls, chat_id, col_name, data):
        query = f"""
        UPDATE {await cls.get_table_name()}
        SET {col_name}=$1, updated_at=$2
        WHERE chat_id=$3
        """
        return await execute_query(
            query=query,
            params=(data, tas_t(), str(chat_id))
        )

    @classmethod
    async def get_data(cls, chat_id):
        query = f"""
        SELECT *
        FROM {await cls.get_table_name()}
        WHERE chat_id=$1
        """
        result = await execute_query(
            query=query,
            params=(str(chat_id),),
            fetch='one'
        )
        if result:
            return cls(**result)
        return None

    @classmethod
    async def get_by_idn(cls, idn):
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