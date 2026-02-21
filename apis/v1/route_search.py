from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from sqlalchemy.orm import Session
# from db.session import get_db
from db.crud.db_domain import get_search_index_by_user
from schemas.search import SearchRequest
import logging
import os
import time
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery, QueryType, QueryCaptionType, QueryAnswerType
from azure.core.credentials import AzureKeyCredential
import re
from openai import AzureOpenAI
from core.search_utils import build_filter_expression, get_embedding, get_user_delegation_sas, convert_onelake_url, \
    chat_completions_client
from core.constants import WORKSPACE_NAME, LAKEHOUSE_NAME, root_path
from dotenv import load_dotenv
from pathlib import Path
from core.config import Settings

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger("gunicorn.error")

router = APIRouter()


endpoint = Settings.openai_endpoint
model_name = Settings.model_name
deployment = Settings.deployment

subscription_key = Settings.subscription_key
api_version = Settings.subscription_key

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# === CONFIG ===
# search_service = "<your-search-service-name>"
# search_index = "lakehouse-index"
# admin_key = "<your-admin-key>"
# embedding_model_url = "<your-embedding-model-endpoint>"
# embedding_model_key = "<your-embedding-model-key>"

search_service = "aisearch-aiexec"
search_index = "search-1771651572608"

search_admin_key = Settings.search_admin_key
if not search_admin_key:
    search_admin_key = os.getenv("search_admin_key")


search_client = SearchClient(
    endpoint=f"https://{search_service}.search.windows.net",
    index_name=search_index,
    credential=AzureKeyCredential(search_admin_key)
)


@router.post("/hybrid_search_v2", response_model=None)
async def hybrid_search_documents_v2(request: SearchRequest):

    search_index_name = request.index_name
    semantic_configuration = f"{search_index_name}-semantic-configuration"
    logger.info(f"index: {search_index_name}")

    search_client = SearchClient(
        endpoint=f"https://{search_service}.search.windows.net",
        index_name=search_index_name,
        credential=AzureKeyCredential(search_admin_key)
    )

    logger.info(f"prompt: {request.query}")
    logger.info(f"model: {request.model_id}")
    query_embedding = get_embedding(request.query)
    filter_expression = build_filter_expression(request)


    if search_index_name != "multimodal-rag-demo":
        start_time = time.time()
        # vector_query = VectorizedQuery(vector=query_embedding, k_nearest_neighbors=50, fields="text_vector")
        # results = search_client.search(
        #     search_text=request.query,
        #     # vector_queries=[vector_query],
        #     top=request.top_k,
        #     search_fields=["title, text"],
        #     # filter=filter_expression,
        #     query_type=QueryType.SEMANTIC,
        #     semantic_configuration_name=f"{semantic_configuration}",
        #     include_total_count=True,
        #     query_caption=QueryCaptionType.EXTRACTIVE,
        #     query_answer=QueryAnswerType.EXTRACTIVE
        # )
        results = search_client.search(
            search_text=request.query,
            include_total_count=True,
            # semantic
            query_type=QueryType.SEMANTIC,
            semantic_configuration_name=semantic_configuration,
            # captions & answers
            query_caption="extractive",
            query_answer="extractive",
            query_answer_count=3
        )
        # results = search_client.search(
        #     search_text=f'"{request.query}"',
        #     query_type=QueryType.SIMPLE,
        #     search_mode="any",  # OR logic
        #     include_total_count=True
        # )
        end_time = time.time()
        logger.info(f"Search Latency: {end_time - start_time}")
        print("%%%%%%%%%%%%")
        print(results)
        print("&&&&&&&&&&&&&&")
        semantic_answers = results.get_answers()
        print(semantic_answers)
        print("************")
        semantic_answers_text = []
        if semantic_answers:
            for answer in semantic_answers:
                print(answer)
                if answer.highlights:
                    semantic_answers_text.append(answer.highlights)
                else:
                    semantic_answers_text.append(answer.text)
        print(semantic_answers_text)
        documents = []
        # for i, doc in enumerate(results):
        #     documents.append({
        #         "title": doc["title"]
        #     })
        #
        # print("AAAAAAAAAAAAAAAA")
        # print(documents)
        titles = [doc.get("title") for doc in results if doc.get("title")]
        print(titles)
        return {
            "result": titles
        }
        # start_time = time.time()
        # response = chat_completions_client(request.query, documents, semantic_answers_text)
        # end_time = time.time()
        #
        # logger.info(f"Model Latency: {end_time - start_time}")
        #
        # result_text = response.choices[0].message.content
        #
        # main_text, source_text = result_text, ""
        # cited_refs, filtered_sources = [], []
        #
        # if "\n\nSources:\n" in result_text:
        #     main_text, source_text = result_text.split("\n\nSources:\n", 1)
        #
        #     cited_refs = sorted(set(map(int, re.findall(r"\[(\d+)\]", source_text))))
        #
        #     filtered_sources = [
        #         doc["source"]
        #         for doc in documents if doc["ref_num"] in cited_refs
        #     ]
        #
        # source_list = set(filtered_sources)
        # if source_list:
        #     logger.info(f"source_list: {[Path(file_path).name for file_path in source_list]}")
        # url_list = []
        # source_list = url_list if url_list else source_list
        # return {
        #     "result": main_text if main_text else result_text,
        #     "source": ",".join(source_list),
        #     "references": documents
        # }
    else:
        start_time = time.time()
        vector_query = VectorizedQuery(vector=query_embedding, k_nearest_neighbors=50, fields="content_embedding",
                                       exhaustive=True)
        results = search_client.search(
            search_text=f'"{request.query}"',
            vector_queries=[vector_query],
            top=request.top_k,
            # search_fields=["title", "chunk"],
            filter=filter_expression,
            query_type=QueryType.SIMPLE,
            semantic_configuration_name=f"{semantic_configuration}",
            query_caption=QueryCaptionType.EXTRACTIVE,
            query_answer=QueryAnswerType.EXTRACTIVE
        )
        end_time = time.time()
        logger.info(f"Search Latency: {end_time - start_time}")

        semantic_answers = results.get_answers()
        semantic_answers_text = ""
        if semantic_answers:
            for answer in semantic_answers:
                if answer.highlights:
                    # print(f"Semantic Answer highlights: {answer.highlights}")
                    semantic_answers_text = answer.highlights
                else:
                    # print(f"Semantic Answer text: {answer.text}")
                    semantic_answers_text = answer.text
                # print(f"Semantic Answer Score: {answer.score}\n")
        documents = []
        for i, doc in enumerate(results):
            documents.append({
                "title": doc["document_title"],
                "chunk": (doc.get("content_text")[:1000] + '...') if doc.get("content_text") else "",
                "chunk_id": doc.get("content_id"),
                "parent_id": doc.get("text_document_id"),
                "source": doc.get("document_title"),
                "ref_num": i + 1
            })

        response = chat_completions_client(request.query, documents, semantic_answers_text)

        result_text = response.choices[0].message.content

        main_text, source_text = result_text, ""
        cited_refs, filtered_sources = [], []

        if "\n\nSources:\n" in result_text:
            main_text, source_text = result_text.split("\n\nSources:\n", 1)

            cited_refs = sorted(set(map(int, re.findall(r"\[(\d+)\]", source_text))))

            filtered_sources = [
                doc["source"]
                for doc in documents if doc["ref_num"] in cited_refs
            ]

        source_list = set(filtered_sources)
        if source_list:
            logger.info(f"source_list: {[Path(file_path).name for file_path in source_list]}")
        if source_list:
            logger.info(f"source_list: {[Path(file_path).name for file_path in source_list]}")
        url_list = []

        source_list = url_list if url_list else source_list
        return {
            "result": main_text if main_text else result_text,
            "source": ",".join(source_list),
            "references": documents
        }
