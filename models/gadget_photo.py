import models.gadget
from database_config.db_settings import execute_query
from utils.additions import tas_t


class GadgetPhotoModel:
    def __init__(
            self,
            idn = None,
            gadget = None,
            photo = None,
            created_at = None,
    ):
        self.idn = idn
        self.gadget = gadget
        self.photo = photo
        self.created_at = created_at

    @classmethod
    async def get_table_name(cls):
        return 'gadget_photo_model'

    @classmethod
    async def create_table(cls):
        query = f"""
        CREATE TABLE IF NOT EXISTS {await cls.get_table_name()} (
            idn SERIAL PRIMARY KEY,
            gadget INT REFERENCES {await models.gadget.GadgetModel.get_table_name()}(idn),
            photo TEXT,
            created_at TIMESTAMPTZ DEFAULT timezone('Asia/Tashkent', NOW())
        )
        """
        await execute_query(query=query)
        return None

    @classmethod
    async def create(
            cls,
            gadget,
            photo
    ):
        query = f"""
        INSERT INTO {await cls.get_table_name()}
        (gadget, photo)
        VALUES ($1, $2)
        """
        return await execute_query(
            query=query,
            params=(gadget, photo)
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
            params=(data, tas_t(), idn)
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
    async def get_by_gadget(cls, gadget):
        query = f"""
            SELECT *
            FROM {await cls.get_table_name()}
            WHERE gadget=$1
            """
        result = await execute_query(
            query=query,
            params=(int(gadget),),
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []
