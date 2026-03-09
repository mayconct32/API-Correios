import os
import tempfile
from typing import Optional
import httpx
from src.correios_cep.repository.setup_repository import SetupRepository
from src.correios_cep.exceptions import CSVDownloadException, CSVFileException


class CSVDownloadService:
    def __init__(self, url: str):
        self._url = url
    
    async def download(self) -> Optional[str]:
        """
        Baixa o arquivo CSV a partir da URL configurada.

        Parâmetros:
            Nenhum.

        Retorna:
            Optional[str]: conteúdo textual do arquivo CSV baixado.
        """
        client = httpx.AsyncClient()
        try:
            response = await client.get(self._url, timeout=30.0)
            response.raise_for_status()
            return response.text
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            raise CSVDownloadException(f"Erro ao baixar CSV: {e}") from e
        finally:
            await client.aclose()


class CSVFileService:
    def __init__(self, temp_dir: Optional[str] = None):
        self._temp_dir = temp_dir or tempfile.gettempdir()
    
    def save(self, filename: str, content: str) -> str:
        """
        Salva conteúdo textual em um arquivo CSV temporário no disco.

        Parâmetros:
            filename (str): nome do arquivo temporário que será criado.
            content (str): conteúdo que será gravado no arquivo.

        Retorna:
            str: caminho absoluto do arquivo gerado no sistema de arquivos.
        """
        filepath = os.path.join(self._temp_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            return filepath
        except IOError as e:
            raise CSVFileException(f"Erro ao salvar arquivo: {e}") from e
    
    def delete(self, filepath: str) -> None:
        """
        Remove um arquivo temporário do disco, caso ele exista.

        Parâmetros:
            filepath (str): caminho absoluto do arquivo a ser removido.

        Retorna:
            None.
        """
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError as e:
                raise CSVFileException(f"Erro ao deletar arquivo: {e}") from e


class PostalCodeImportService:
    """
    Serviço de alto nível que orquestra a importação de CEPs via CSV.

    Parâmetros:
        Nenhum.

    Retorna:
        PostalCodeImportService: instância preparada para importar e
            limpar arquivos CSV.
    """
    
    def __init__(
        self,
        csv_download_service: CSVDownloadService,
        csv_file_service: CSVFileService,
        setup_repository: SetupRepository
    ):
        self._csv_download = csv_download_service
        self._csv_file = csv_file_service
        self._setup_repository = setup_repository
        self._csv_filename = "postal_codes.csv"
    
    async def import_postal_codes(self) -> bool:
        """
        Executa todo o fluxo de importação de CEPs para o banco de dados.

        Parâmetros:
            Nenhum.

        Retorna:
            bool: True se os dados já existiam ou foram importados com
                sucesso.
        """
        # Verifica se já existe dados
        if await self._setup_repository.check_postal_codes_exist():
            return True
        
        filepath = None
        try:
            csv_content = await self._csv_download.download()
            filepath = self._csv_file.save(self._csv_filename, csv_content)
            await self._setup_repository.insert_address(filepath)
            return True
        finally:
            if filepath:
                self._csv_file.delete(filepath)


# Mantém compatibilidade com código legado
class CSVService:
    """
    Fachada legada mantida para compatibilidade com código antigo.

    Parâmetros:
        Nenhum.

    Retorna:
        CSVService: instância de compatibilidade que delega para o novo
            fluxo de importação.
    """
    
    def __init__(self, setup_repository: SetupRepository):
        self._url = "https://raw.githubusercontent.com/miltonhit/miltonhit/main/public-assets/cep-20190602.csv"
        self._setup_repository = setup_repository
        self._csv_download = CSVDownloadService(self._url)
        self._csv_file = CSVFileService()
        self._import_service = PostalCodeImportService(
            self._csv_download,
            self._csv_file,
            setup_repository
        )
    
    async def upload_CSV_file(self) -> Optional[bool]:
        """
        Executa o fluxo legado de importação de CSV usando o novo
        serviço.

        Parâmetros:
            Nenhum.

        Retorna:
            Optional[bool]: resultado booleano retornado pela rotina de
                importação.
        """
        return await self._import_service.import_postal_codes()





