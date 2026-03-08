from src.correios_cep.database import MysqlDBConnection
from src.correios_cep.model.address import Address
from src.correios_cep.exceptions import AddressNotFoundException


class CorreiosRepository:
    def __init__(self, db_connection: MysqlDBConnection):
        self.db_connection = db_connection
    
    async def get_the_address(
        self,
        zipcode: str | None = None,
        city: str | None = None
    ) -> Address | list[Address]:
        """
        Busca um ou vários endereços usando filtros de CEP ou cidade.

        Parâmetros:
            zipcode (str | None): CEP usado como filtro principal; retorna
                no máximo um registro.
            city (str | None): nome da cidade usado quando o CEP não é
                informado.

        Retorna:
            Address | list[Address]: um endereço para CEP ou lista para
                cidade.
        """
        if zipcode:
            sql = (
                "SELECT zipcode, state, city, Neighborhood, street "
                "FROM correios_ceps WHERE zipcode = %s LIMIT 1"
            )
            rows = await self.db_connection.execute(sql=sql, data=(zipcode,))
            if not rows:
                raise AddressNotFoundException(f"CEP {zipcode} não encontrado")
            return Address(**rows[0])

        if city:
            sql = (
                "SELECT zipcode, state, city, Neighborhood, street "
                "FROM correios_ceps WHERE city = %s"
            )
            rows = await self.db_connection.execute(sql=sql, data=(city,))
            if not rows:
                raise AddressNotFoundException(f"Nenhum endereço em {city}")
            return [Address(**row) for row in rows]

        raise ValueError("CEP ou cidade é obrigatório")
    