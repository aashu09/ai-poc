import requests
import re
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient, generate_directory_sas
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from core.constants import WORKSPACE_NAME, LAKEHOUSE_NAME, root_path
# from db.session import get_db
from sqlalchemy.orm.session import Session
from dotenv import load_dotenv
from schemas.search import SearchRequest
from db.crud.llm import get_llm_by_id
from openai import AzureOpenAI
from core.config import Settings

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger("gunicorn.error")

embedding_model_url = Settings.embedding_model_url
if not embedding_model_url:
    embedding_model_url = os.getenv("embedding_model_url")

embedding_model_key = Settings.embedding_model_key
if not embedding_model_key:
    embedding_model_key = os.getenv("embedding_model_key")


def format_datetime_for_sas(dt: datetime) -> str:
    """Returns a UTC ISO 8601 formatted string with 'Z' timezone suffix."""
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

def get_user_delegation_sas(workspace: str, data_path: str) -> str:
    credential = ClientSecretCredential(
        tenant_id="8af0c5d1-469a-4bc2-8d5f-a6cb3fb0ccd9",
        client_id="b3fe45c5-7a8d-419a-a7d3-8634de285993",
        client_secret="QWw8Q~2~BN551fKZnM2TrO.q94Cndie8xX0h8bBH"
    )

    account_url = "https://onelake.dfs.fabric.microsoft.com"
    account_name = "onelake"

    service_client = DataLakeServiceClient(account_url=account_url, credential=credential)

    now = datetime.utcnow().replace(microsecond=0)
    start_time = now - timedelta(minutes=0)
    expiry_time = now + timedelta(minutes=45)

    start_str = format_datetime_for_sas(start_time)
    expiry_str = format_datetime_for_sas(expiry_time)

    print(f"Formatted Start: {start_str}, Expiry: {expiry_str}")
    print(f"service_client.accout: {service_client.account_name}")
    print(f"service_client.url:{service_client.url}")
    user_delegation_key = service_client.get_user_delegation_key(
        key_start_time=start_time,
        key_expiry_time=expiry_time,
        timeout=60
    )

    print(f"user_delegation_key: {user_delegation_key}")

    sas_token = generate_directory_sas(
        account_name=account_name,
        file_system_name=workspace,
        directory_name=data_path,
        credential=user_delegation_key,
        permission="rl",
        start=start_str,
        expiry=expiry_str,
    )

    return sas_token


def get_embedding(text: str) -> List[float]:
    headers = {
        "Authorization": f"Bearer {embedding_model_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": text
    }
    response = requests.post(embedding_model_url, headers=headers, json=payload)
    response.raise_for_status()
    embedding = response.json()["data"][0]["embedding"]
    return embedding


def build_filter_expression(request: SearchRequest) -> Optional[str]:
    filters = []
    if request.fileType:
        filters.append(f"title eq '{request.fileType}'")
    if request.language:
        filters.append(f"language eq '{request.language}'")
    print(filters)
    return " and ".join(filters) if filters else None



def convert_onelake_url(url: str, workspace_name: str, lakehouse_name: str, sas_token) -> str:
    parts = url.split('/')
    # Replace GUIDs with names (index 3 = workspace, index 4 = lakehouse)
    parts[3] = workspace_name
    parts[4] = f"{lakehouse_name}.Lakehouse"
    path =  '/'.join(parts)
    return f"{path}?{sas_token}"

# Example usage:
# original_url = "https://onelake.blob.fabric.microsoft.com/84b52431-ce37-44c4-a77f-371b75c5b5fa/4bc3b3dc-71b4-4715-a4d0-d9eb0e35d1fb/Files/test/IndianFinancialNews.csv"


def chat_completions_client(query, documents, semantic_answers_text):

    client = AzureOpenAI(
        api_version=Settings.api_version,
        azure_endpoint=Settings.openai_endpoint,
        api_key=Settings.subscription_key,
    )

    deployment = Settings.deployment
    print(f"chat_completions_client_semantic: {semantic_answers_text}")

    separator = " \n******************\n "  # You can change this to ",", "-", etc.

    # single_line = separator.join(semantic_answers_text)
    single_line = separator.join(str(item) for item in semantic_answers_text)
    print(single_line)

    context = f"\n\n".join([
        f"[{doc['ref_num']}] {doc['chunk']}\nSource: {doc['source']}" for doc in documents
    ])

    prompt = f"""
    You are an AI assistant helping a user based on retrieved documents. Use only the context below to answer the question.
    Do NOT include any sources not mentioned in your answer. Follow provided Instructions.

    Context:
    {context}

    Question:
    {query}

    Instructions:
    - The answer should be detailed.
    - For Question containing these keywords: 'table', 'tabular', 'data set', 'columns', 'rows':
        a. Format the answer as a proper markdown table.
        b. Include clear column headers.
        c. Ensure Consistent alignment.
    - For Answer containing these keywords: 'table', 'tabular', 'data set', 'columns', 'rows' or markdown content then:
        a. Format the answer as a proper markdown table.
        b. Include clear column headers.
        c. Ensure Consistent alignment.
    - Do not fabricate sources.
    - End the answer with a section:
        Sources:
        [1] <source>
        [2] <source>
        Note: Only include cited sources. if source not available then don't include Sources: section
    
    ALSO, PLEASE UNDERSTAND BELOW EXAMPLES, THESE ARE MOST IMPORTANT - 
    
    IF YOU WILL GET QUESTIONS LIKE BELOW, ANSWER SHOULD BE SAME AS PROVIDE AND RESPECTIVE TABLES WITH SOME DESCRIPTION - 
    Note - Question's formulation may vary, you should understand the context of the question.
    
    QUESTION 1 - how's the FX exposure of IM Public?
    
    ANSWER - 
        ### FX exposure limit for IM Public
        | (USD'M equivalent) | AUD | CNY/CNH | EUR | GBP | JPY |
        |--------------------|-----|---------|-----|-----|-----|
        | FX exposure limit   | 15  | 30      | 25  | 25  | 20  |
    
    QUESTION 2 - how's the FX exposure of IM Alternative?
    
    ANSWER - 
        ### FX exposure limit for IM Alternative
        | (USD'M equivalent) | AUD | CNY/CNH | EUR | GBP | JPY | NZD |
        |--------------------|-----|---------|-----|-----|-----|-----|
        | FX exposure limit   | 25  | 180     | 40  | 30  | 20  | 25  |
    
    QUESTION 3 - how's the FX exposure of IM Special situation & Real estate?
    
    ANSWER - 
        ### FX exposure limit for IM Special situation & Real estate
        | (USD'M equivalent) | AUD | CNY/CNH | EUR | GBP | JPY | NZD |
        |--------------------|-----|---------|-----|-----|-----|-----|
        | FX exposure limit   | 25  | 180     | 40  | 30  | 20  | 25  |
    
    QUESTION 4 - how's the Overall FX exposure limit for Group?
    
    ANSWER -
        ### Overall FX exposure limit for Group
        | (USD'M equivalent) | AUD | CNY/CNH | EUR | GBP | JPY | NZD |
        |--------------------|-----|---------|-----|-----|-----|-----|
        | FX exposure limit   | 70  | 550     | 110 | 90  | 65  | 50  |
    

    IF YOU FIND ABOVE MENTIONED QUESTIONS IN THE USER'S ASKED QUESTION AND SO YOU CAN DIRECTLY PROVIDE THE ANSWERS BASED ON MENTIONED ANSWER FOR RESPOECTIVE QIESTION WITH SOME DESCRIPTION WHICH CAN BE DESIGNED BY YOU FOR ANSWER.
    BUT formulation of response like markdown format should be followed as per above mentioned instructions.
    Answer:
    """

    if deployment in ["DeepSeek-V3-0324", "aifoundary-poc-Llama-3.3-70B-Instruct"]:
        logger.info(f"model_name:{deployment}")
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content= prompt),
            ],
            max_tokens=4096,
            temperature=0.8,
            top_p=0.1,
            presence_penalty=0.0,
            frequency_penalty=0.0,
            model=deployment
        )
        return response
    elif deployment == "Mistral-Large-2411":
        logger.info(f"model_name:{deployment}")
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content=prompt),
            ],
            max_tokens=2048,
            temperature=0.8,
            top_p=0.1,
            model=deployment
        )
        return response
    elif deployment == 'o3-mini':
        logger.info(f"model_name:{deployment}")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=5120,
            model=deployment
        )
        return response
    else:
        logger.info(f"model_name:{deployment}")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps users learn from the information found in the source material"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.2,
            top_p=1.0,
            model=deployment
        )
        return response
