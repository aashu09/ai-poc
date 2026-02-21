import os
from pathlib import Path
from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient
import logging

from dotenv import load_dotenv

logger = logging.getLogger("gunicorn.error")

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# keyVaultName = "ecipoc-key-vault"
# # print(keyVaultName)
# logger.info(f"Keyvault - {keyVaultName}")
# KVUri = f"https://{keyVaultName}.vault.azure.net"
# credential = DefaultAzureCredential()
# client = SecretClient(vault_url=KVUri, credential=credential)


class Settings:
    # POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    # POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    # POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    # POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)  # default postgres port is 5432
    # POSTGRES_DB: str = os.getenv("POSTGRES_DB", "dbhig")

    # POSTGRES_USER = client.get_secret("POSTGRES-USER").value
    # # print(POSTGRES_USER)
    # logger.info(f"Postgres user - {POSTGRES_USER}")
    # POSTGRES_PASSWORD = client.get_secret("POSTGRES-PASSWORD").value
    # # print(POSTGRES_PASSWORD)
    # logger.info(f"Postgres password - {POSTGRES_PASSWORD}")
    # POSTGRES_SERVER = client.get_secret("POSTGRES-SERVER").value
    # # print(POSTGRES_SERVER)
    # logger.info(f"Postgres server - {POSTGRES_SERVER}")
    # POSTGRES_PORT = client.get_secret("POSTGRES-PORT").value
    # # print(POSTGRES_PORT)
    # logger.info(f"Postgres port - {POSTGRES_PORT}")
    # POSTGRES_DB = client.get_secret("POSTGRES-DB").value
    # # print(POSTGRES_DB)
    # logger.info(f"Postgres db - {POSTGRES_DB}")

    # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    # print(DATABASE_URL)

    search_admin_key = os.getenv("search_admin_key")
    embedding_model_url = os.getenv("embedding_model_url")
    embedding_model_key = os.getenv("embedding_model_key")

    search_service_name = os.getenv("search_service_name")

    openai_endpoint = os.getenv("openai_endpoint")
    model_name = os.getenv("model_name")
    deployment = os.getenv("deployment")

    subscription_key = os.getenv("subscription_key")
    api_version = os.getenv("api_version")

    search_service_admin_key = search_admin_key #client.get_secret("search-service-admin-key").value


    API_V1_STR = '/api/v1'
    LOG_LEVEL: str = "DEBUG"


settings = Settings()
