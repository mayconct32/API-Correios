import os
from dotenv import load_dotenv
from mysql.connector.aio import connect
from src.correios_cep.exceptions import DatabaseException


load_dotenv(override=True)


class MysqlDBConnection:
    def __init__(self):
        self._host = os.getenv("HOST")
        self._user = os.getenv("USER")
        self._password = os.getenv("PASSWORD")
        self._database = os.getenv("DATABASE")
        self.conn = None
        
        if not all([self._host, self._user, self._password, self._database]):
            raise DatabaseException("Variáveis de ambiente do banco de dados não configuradas")

    async def _connection(self):
        try:
            connection = await connect(
                user=self._user,
                password=self._password,
                host=self._host,
                database=self._database,
                allow_local_infile=True
            )
            return connection
        except Exception as e:
            raise DatabaseException(f"Erro ao conectar ao banco: {e}") from e

    async def execute(
        self, 
        sql: str, 
        data=None,
        operation="SELECT"
    ):
        if not self.conn:
            self.conn = await self._connection()
        try:
            async with await self.conn.cursor(dictionary=True) as cursor:
                await cursor.execute(sql, data)
                if operation == "SELECT":
                    return await cursor.fetchall()
                else:
                    await self.conn.commit()
        except Exception as e:
            raise DatabaseException(f"Erro ao executar operação: {e}") from e

