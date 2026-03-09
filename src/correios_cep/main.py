import logging
from http import HTTPStatus
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.correios_cep.controller.correios_controller import app as correios
from src.correios_cep.container import container
from src.correios_cep.exceptions import AppException


# Configurar logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format="\033[32m%(levelname)s - \033[93m%(message)s\033[m"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação e garante o carregamento dos
    dados de CEP.

    Parâmetros:
        app (FastAPI): instância principal da aplicação FastAPI.

    Retorna:
        AsyncIterator[None]: contexto assíncrono usado pelo FastAPI no
            ciclo de vida.
    """
    logger.info("=" * 60)
    logger.info("Iniciando aplicação - Carregando dados de CEP")
    logger.info("=" * 60)
    
    try:
        setup_repository = container.get_setup_repository()
        
        # Verifica se dados já estão carregados
        dados_existem = await setup_repository.check_postal_codes_exist()
        
        if dados_existem:
            logger.info("✓ Dados de CEP já carregados no banco de dados")
        else:
            logger.info("Iniciando download do arquivo CSV...")
            
            import_service = container.get_postal_code_import_service()
            await import_service.import_postal_codes()
            
            logger.info("✓ Arquivo CSV importado com sucesso no banco de dados")
    
    except AppException as e:
        logger.error(f"Erro na aplicação: {e.message}")
    except Exception as e:
        logger.error(f"Erro inesperado durante inicialização: {str(e)}", exc_info=True)
    
    logger.info("=" * 60)
    logger.info("Aplicação iniciada e pronta para receber requisições")
    logger.info("=" * 60)
    yield


app = FastAPI()


app.include_router(correios)