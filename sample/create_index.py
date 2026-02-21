""" working python SDK code for create index """
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration
)
from dotenv import load_dotenv
from core.config import Settings
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize the SearchIndexClient
search_service_name = Settings.search_service_name
if not search_service_name:
    search_service_name = os.getenv("search_service_name")

admin_api_key = Settings.search_admin_key
if not admin_api_key:
    admin_api_key = os.getenv("search_admin_key")
endpoint = f"https://{search_service_name}.search.windows.net"
index_client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(admin_api_key))

# Define the index
index_name = "index-graphpoc-001"

index = SearchIndex(
    name=index_name,
    fields=[
        SearchField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="fileName", type=SearchFieldDataType.String, searchable=True, filterable=True, sortable=True,
                    facetable=True),
        SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
        SearchField(name="fileType", type=SearchFieldDataType.String, sortable=True, facetable=True),
        SearchField(name="metadata_storage_path", type=SearchFieldDataType.String, sortable=True),
        SearchField(name="lastModified", type=SearchFieldDataType.DateTimeOffset, sortable=True, facetable=True),
        SearchField(name="language", type=SearchFieldDataType.String, facetable=True),
        SearchField(name="keyPhrases", type=SearchFieldDataType.Collection(SearchFieldDataType.String), searchable=True,
                    filterable=True, facetable=True),

        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            # Set your embedding dimension size (adjust if your model gives different size!)
            vector_search_profile_name="default"  # Link to the profile we define below
        ),
    ],
    vector_search=VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="default-algorithm",
                kind="hnsw",  # HNSW = Hierarchical Navigable Small World graph (good default)
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="default",
                algorithm_configuration_name="default-algorithm"
            )
        ]

    )
)

# Create the index
index_client.create_index(index)

print(f"Index '{index_name}' created successfully.")