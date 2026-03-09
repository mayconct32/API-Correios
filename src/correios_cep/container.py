from src.correios_cep.database import MysqlDBConnection
from src.correios_cep.interfaces import IDatabaseConnection, ISetupRepository, ICorreiosRepository
from src.correios_cep.repository.correios_repository import CorreiosRepository
from src.correios_cep.repository.setup_repository import SetupRepository
from src.correios_cep.service.correios_service import CorreiosService
from src.correios_cep.service.csvfile_service import (
    CSVDownloadService,
    CSVFileService,
    PostalCodeImportService
)


class Container:
    """
    Container singleton responsável por montar as dependências da
    aplicação.

    Parâmetros:
        Nenhum.

    Retorna:
        Container: instância única para resolver serviços e repositórios.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
        return cls._instance
    
    def get_db_connection(self) -> IDatabaseConnection:
        """
        Cria uma nova instância de conexão com o banco de dados MySQL.

        Parâmetros:
            Nenhum.

        Retorna:
            IDatabaseConnection: conexão configurada para o banco da
                aplicação.
        """
        return MysqlDBConnection()

    def get_setup_repository(self) -> ISetupRepository:
        """
        Cria um SetupRepository associado a uma nova conexão de banco.

        Parâmetros:
            Nenhum.

        Retorna:
            ISetupRepository: repositório para carga e verificação de
                CEPs.
        """
        return SetupRepository(self.get_db_connection())

    def get_correios_repository(self) -> ICorreiosRepository:
        """
        Cria um CorreiosRepository associado a uma nova conexão de banco.

        Parâmetros:
            Nenhum.

        Retorna:
            ICorreiosRepository: repositório usado nas consultas de
                endereços.
        """
        return CorreiosRepository(self.get_db_connection())
    
    def get_correios_service(self) -> CorreiosService:
        """
        Cria uma instância de CorreiosService com repositório injetado.

        Parâmetros:
            Nenhum.

        Retorna:
            CorreiosService: serviço de domínio usado pelos controllers
                da API.
        """
        return CorreiosService(self.get_correios_repository())
    
    def get_postal_code_import_service(self) -> PostalCodeImportService:
        """
        Cria um PostalCodeImportService pronto para importar CEPs via
        CSV.

        Parâmetros:
            Nenhum.

        Retorna:
            PostalCodeImportService: serviço que orquestra a carga de
                CEPs.
        """
        csv_url = "https://raw.githubusercontent.com/miltonhit/miltonhit/main/public-assets/cep-20190602.csv"
        csv_download = CSVDownloadService(csv_url)
        csv_file = CSVFileService()
        
        return PostalCodeImportService(
            csv_download_service=csv_download,
            csv_file_service=csv_file,
            setup_repository=self.get_setup_repository()
        )


# Instância global do container
container = Container()