from typing import List
from fastapi import APIRouter, Depends
from src.correios_cep.service.service import CorreiosService
from src.correios_cep.interfaces import ICorreiosRepository
from src.correios_cep.repository.correios_repository import CorreiosRepository
from src.correios_cep.database import MysqlDBConnection
from src.correios_cep.model.address import Address


app = APIRouter()


def get_correios_service() -> CorreiosService:
    """
    Retorna a instância de CorreiosService.

    Parâmetros:
        Nenhum.

    Retorna:
        CorreiosService: serviço utilizado para consultas de endereços.
    """
    repository: ICorreiosRepository = CorreiosRepository(MysqlDBConnection())
    return CorreiosService(repository)


@app.get("/zip/{zipcode}", response_model=Address)
async def get_by_zip_code(
    zipcode: str,
    service: CorreiosService = Depends(get_correios_service)
):
    """
    Retorna o endereço associado ao CEP informado.

    Parâmetros:
        zipcode (str): código de CEP usado na consulta.
        service (CorreiosService): serviço responsável pela busca.

    Retorna:
        Address: dados do endereço correspondente ao CEP.
    """
    return await service.get_address_by_postal_code(zipcode=zipcode)


@app.get("/city/{city}", response_model=List[Address])
async def get_by_city(
    city: str,
    service: CorreiosService = Depends(get_correios_service)
):
    """
    Retorna todos os endereços pertencentes à cidade informada.

    Parâmetros:
        city (str): nome da cidade usada como filtro.
        service (CorreiosService): serviço responsável pela busca.

    Retorna:
        List[Address]: lista de endereços encontrados para a cidade.
    """
    return await service.get_address_by_city(city=city) 
