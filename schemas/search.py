from typing import Union, Optional, List
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, EmailStr, StrictStr, UUID4


class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 10
    fileType: Optional[str] = None
    language: Optional[str] = None
    user: Optional[str] = None
    model_id: Optional[int] = 1
    index_name: Optional[str] = 'search-1771489134990'

class SearchResponseItem(BaseModel):
    title: str
    chunk: str
    chunk_id: Optional[str]
    parent_id: Optional[str]


class SearchResponse(BaseModel):
    results: List[SearchResponseItem]

class RagResponse(BaseModel):
    results: str

class RagRequest(BaseModel):
    query: str