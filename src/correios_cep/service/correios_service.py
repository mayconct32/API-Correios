from src.correios_cep.interfaces import ICorreiosRepository


class CorreiosService:
    def __init__(self, correios_repository: ICorreiosRepository):
        """
        Inicializa o serviço de domínio com o repositório de endereços.

        Parâmetros:
            correios_repository (ICorreiosRepository): repositório usado
                nas consultas de CEP e cidade.

        Retorna:
            None.
        """
        self._correios_repository = correios_repository 
    
    async def get_address_by_postal_code(self, zipcode: str):
        """
        Retorna o endereço correspondente a um CEP específico.

        Parâmetros:
            zipcode (str): CEP usado como filtro principal da consulta.

        Retorna:
            Address: endereço retornado pelo repositório para o CEP
            informado.
        """
        return await self._correios_repository.get_the_address(zipcode=zipcode)

    async def get_address_by_city(self, city: str):
        """
        Retorna todos os endereços localizados em uma cidade.

        Parâmetros:
            city (str): nome da cidade usado como filtro da consulta.

        Retorna:
            list[Address]: lista de endereços encontrados para a cidade.
        """
        return await self._correios_repository.get_the_address(city=city)
