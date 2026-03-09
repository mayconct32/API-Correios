from abc import ABC, abstractmethod
from src.correios_cep.model.address import Address


class IDatabaseConnection(ABC):
    """
    Interface genérica para conexão com banco de dados.

    O Repository depende desta abstração, não de uma implementação concreta.
    Isso permite trocar o banco de dados sem modificar o Repository.
    """

    @abstractmethod
    async def execute(self, sql: str, data: tuple = ()) -> list[dict]:
        """
        Executa uma query SQL.

        Args:
            sql: Query SQL a ser executada.
            data: Parâmetros da query.

        Returns:
            Lista de dicionários com os resultados.
        """
        pass


class ICorreiosRepository(ABC):
    """
    Interface para repositório de endereços dos Correios.

    O Service depende desta abstração, não do CorreiosRepository concreto.
    Isso permite trocar o repositório sem modificar o Service.
    """

    @abstractmethod
    async def get_the_address(
        self,
        zipcode: str | None = None,
        city: str | None = None
    ) -> Address | list[Address]:
        """
        Busca endereços por CEP ou cidade.

        Args:
            zipcode: CEP como filtro principal (retorna no máximo 1).
            city: Nome da cidade (usado se CEP não informado).

        Returns:
            Address ou lista de Address.

        Raises:
            AddressNotFoundException: Quando nenhum endereço for encontrado.
            ValueError: Quando nenhum filtro for fornecido.
        """
        pass
