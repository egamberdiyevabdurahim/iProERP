import models.user
import models.model

from database_config.db_settings import execute_query
from utils.additions import tas_t


class GadgetModel:
    def __init__(
            self,
            idn = None,
            hash_idn = None,
            qr_code = None,
            br_code = None,
            name = None,
            description = None,
            price = None,
            imei1 = None,
            imei2 = None,
            model = None,
            seria = None,
            serial_number = None,
            color = None,
            client = None,
            client_name = None,
            client_chat_id = None,
            client_phone_number = None,
            status = None,
            is_deleted = None,
            stop_start_time = None,
            stop_end_time = None,
            stop_duration = None,
            is_stopped = None,
            start_time = None,
            end_time = None,
            auto_run = None,
            expense=None,
            worker = None,
            created_by = None,
            updated_by = None,
            deleted_by = None,
            created_at = None,
            updated_at = None,
            deleted_at = None,
            counter = None,
            matched_column = None,
    ):
        self.idn = idn
        self.hash_idn = hash_idn
        self.qr_code = qr_code
        self.br_code = br_code
        self.name = name
        self.description = description
        self.price = price
        self.imei1 = imei1
        self.imei2 = imei2
        self.model = model
        self.seria = seria
        self.serial_number = serial_number
        self.color = color
        self.client = client
        self.client_name = client_name
        self.client_chat_id = client_chat_id
        self.client_phone_number = client_phone_number
        self.status = status
        self.is_deleted = is_deleted
        self.stop_start_time = stop_start_time
        self.stop_end_time = stop_end_time
        self.stop_duration = stop_duration or 0
        self.is_stopped = is_stopped
        self.start_time = start_time
        self.end_time = end_time
        self.worker = worker
        self.auto_run = auto_run
        self.expense = expense
        self.created_by = created_by
        self.updated_by = updated_by
        self.deleted_by = deleted_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.counter = counter
        self.matched_column = matched_column

    @classmethod
    async def get_table_name(cls):
        return 'gadget_model'

    @classmethod
    async def create_table(cls):
        query = f"""
            CREATE TABLE IF NOT EXISTS {await cls.get_table_name()} (
                idn BIGSERIAL PRIMARY KEY,
                hash_idn TEXT,
                qr_code TEXT,
                br_code TEXT,
                name VARCHAR(255),
                description TEXT,
                price INT,
                imei1 VARCHAR(255),
                imei2 VARCHAR(255),
                model INT REFERENCES {await models.model.ModelModel.get_table_name()}(idn),
                seria INT REFERENCES {await models.model.ModelModel.get_table_name()}(idn),
                serial_number VARCHAR(255),
                color VARCHAR(255),
                client INT REFERENCES {await models.user.UserModel.get_table_name()}(idn),
                client_name VARCHAR(255),
                client_chat_id INT,
                client_phone_number VARCHAR(25),
                status SMALLINT DEFAULT 0,
                is_deleted BOOLEAN DEFAULT FALSE,
                stop_start_time TIMESTAMPTZ,
                stop_end_time TIMESTAMPTZ,
                stop_duration INT DEFAULT 0,
                is_stopped BOOLEAN DEFAULT FALSE,
                start_time TIMESTAMPTZ,
                end_time TIMESTAMPTZ,
                auto_run BOOLEAN DEFAULT FALSE,
                expense INT,
                worker INT REFERENCES {await models.user.UserModel.get_table_name()}(idn),
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
            hash_idn=None,
            qr_code=None,
            br_code=None,
            name=None,
            description=None,
            price=None,
            imei1=None,
            imei2=None,
            model=None,
            seria=None,
            serial_number=None,
            color=None,
            client=None,
            client_name=None,
            client_chat_id=None,
            client_phone_number=None,
            created_by=None,
    ):
        query = f"""
            INSERT INTO {await cls.get_table_name()}
            (hash_idn, qr_code, br_code, name, description, price, imei1, imei2,
            model, seria, serial_number, color, client, client_name,
            client_chat_id, client_phone_number, created_by)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
            """
        await execute_query(
            query=query,
            params=(hash_idn, qr_code, br_code, name, description, int(price), imei1, imei2,
                    model, seria, serial_number, color, client, client_name,
                    client_chat_id, client_phone_number, created_by)
        )
        result = await execute_query(query=f"SELECT * FROM {await cls.get_table_name()} ORDER BY idn DESC LIMIT 1", fetch='one')
        if result:
            return cls(**result)
        return None

    @classmethod
    async def column_updater(cls, idn, col_name, data, updater=None):
        if updater is None:
            query = f"""
            UPDATE {await cls.get_table_name()}
            SET {col_name}=$1, updated_at=$2
            WHERE idn=$3
            """
            return await execute_query(
                query=query,
                params=(data, tas_t(), int(idn))
            )

        query = f"""
            UPDATE {await cls.get_table_name()}
            SET {col_name}=$1, updated_at=$2, updated_by=$3
            WHERE idn=$4
            """
        return await execute_query(
            query=query,
            params=(data, tas_t(), updater, int(idn))
        )

    @classmethod
    async def start(cls, idn):
        query = f"""
            UPDATE {await cls.get_table_name()}
            SET start_time=$1
            WHERE idn=$2
            """
        return await execute_query(
            query=query,
            params=(tas_t(), int(idn))
        )

    @classmethod
    async def end(cls, idn):
        query = f"""
            UPDATE {await cls.get_table_name()}
            SET end_time=$1
            WHERE idn=$2
            """
        return await execute_query(
            query=query,
            params=(tas_t(), int(idn))
        )

    @classmethod
    async def stop(cls, idn):
        query = f"""
            UPDATE {await cls.get_table_name()}
            SET stop_start_time=$1
            WHERE idn=$2
            """
        return await execute_query(
            query=query,
            params=(tas_t(), int(idn))
        )

    @classmethod
    async def continue_(cls, idn):
        query = f"""
            UPDATE {await cls.get_table_name()}
            SET stop_end_time=$1, stop_duration=start_end_time-$2
            WHERE idn=$3
            """
        return await execute_query(
            query=query,
            params=(tas_t(), tas_t(), int(idn))
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
    async def get_all_count(cls, ex='', lt=None, st=None):
        query = f"""
        SELECT COUNT(idn) as counter FROM {await cls.get_table_name()}
        WHERE 1=1 {ex}
        """
        if lt:
            query += f" LIMIT {lt}"

        if st is not None:
            query += f" OFFSET {st}"
        result = await execute_query(query, fetch='one')
        return result[-1]

    @classmethod
    async def get_all(cls, ex='', lt=None, st=None):
        query = f"""
            SELECT *
            FROM {await cls.get_table_name()}
            WHERE 1=1 {ex}
            ORDER BY idn DESC
            """
        if lt:
            query += f" LIMIT {lt}"

        if st:
            query += f" OFFSET {st}"
        result = await execute_query(
            query=query,
            fetch='all'
        )
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_search(cls, search_query, lt=None, st=None):
        query = f"""
            SELECT *,  
                CASE  
                    WHEN CAST(idn AS TEXT) ILIKE $1 THEN 'idn'  
                    WHEN CAST(imei1 AS TEXT) ILIKE $2 THEN 'imei1'  
                    WHEN CAST(imei2 AS TEXT) ILIKE $3 THEN 'imei2'
                    WHEN CAST(serial_number AS TEXT) ILIKE $4 THEN 'serial_number'  
                END AS matched_column
            FROM {await cls.get_table_name()}  
            WHERE (CAST(idn AS TEXT) ILIKE $5 OR 
                    CAST(imei1 AS TEXT) ILIKE $6 OR 
                    CAST(imei2 AS TEXT) ILIKE $7 OR 
                    CAST(serial_number AS TEXT) ILIKE $8) 
                AND is_deleted = FALSE
            ORDER BY idn DESC
            """
        if lt:
            query += f" LIMIT {lt}"

        if st:
            query += f" offset {st}"
        search_query = f"%{search_query.strip()}%",
        params = search_query * 8
        result = await execute_query(query, params=params, fetch='all')
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_search_name(cls, search_query, lt=None, st=None):
        query = f"""
            SELECT t1.*
            FROM {await cls.get_table_name()} t1
            JOIN {await models.model.ModelModel.get_table_name()} t2 ON t1.model = t2.idn
            WHERE CAST(t2.name || ' ' || t1.name AS TEXT) ILIKE $1 AND t1.is_deleted = FALSE
            ORDER BY t1.idn DESC
        """
        if lt:
            query += f" LIMIT {lt}"
        if st:
            query += f" OFFSET {st}"

        search_query = f"%{search_query.strip()}%"
        result = await execute_query(query, params=[search_query], fetch='all')
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_search_idn(cls, search_query, lt=None, st=None):
        query = f"""
                SELECT *
                FROM {await cls.get_table_name()}  
                WHERE CAST(idn AS TEXT) ILIKE $1 AND is_deleted = FALSE
                ORDER BY idn DESC
                """
        if lt:
            query += f" LIMIT {lt}"

        if st:
            query += f" offset {st}"
        search_query = f"%{search_query.strip()}%",
        result = await execute_query(query, params=search_query, fetch='all')
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_search_sn(cls, search_query, lt=None, st=None):
        query = f"""
                SELECT *
                FROM {await cls.get_table_name()}  
                WHERE CAST(serial_number AS TEXT) ILIKE $1 AND is_deleted = FALSE
                ORDER BY idn DESC
                """
        if lt:
            query += f" LIMIT {lt}"

        if st:
            query += f" offset {st}"
        search_query = f"%{search_query.strip()}%",
        result = await execute_query(query, params=search_query, fetch='all')
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_search_imei1(cls, search_query, lt=None, st=None):
        query = f"""
                    SELECT *
                    FROM {await cls.get_table_name()}  
                    WHERE CAST(imei1 AS TEXT) ILIKE $1 AND is_deleted = FALSE
                    ORDER BY idn DESC
                    """
        if lt:
            query += f" LIMIT {lt}"

        if st:
            query += f" offset {st}"
        search_query = f"%{search_query.strip()}%",
        result = await execute_query(query, params=search_query, fetch='all')
        return [cls(**item) for item in result] if result else []

    @classmethod
    async def get_by_search_imei2(cls, search_query, lt=None, st=None):
        query = f"""
                    SELECT *
                    FROM {await cls.get_table_name()}  
                    WHERE CAST(imei2 AS TEXT) ILIKE $1 AND is_deleted = FALSE
                    ORDER BY idn DESC
                    """
        if lt:
            query += f" LIMIT {lt}"

        if st:
            query += f" offset {st}"
        search_query = f"%{search_query.strip()}%",
        result = await execute_query(query, params=search_query, fetch='all')
        return [cls(**item) for item in result] if result else []
