from typing import Union

from pydantic import BaseModel, EmailStr, StrictStr

class LLMOut(BaseModel):
    id: int
    api_key: Union[str, None] = None
    azure_deployment_model: Union[str, None] = None
    azure_embedding_model: Union[str, None] = None
    open_ai_version: Union[str, None] = None
    open_ai_type: Union[str, None] = None
    model_engine: Union[str, None] = None
    model_name: Union[str, None] = None
    icon_name: Union[str, None] = None
    model_token_limit: int
    description: Union[str, None] = None


class LLMList(BaseModel):
    id: int
    model_engine: Union[str, None] = None
    description: Union[str, None] = None
    model_name: Union[str, None] = None
    icon_name: Union[str, None] = None


class LLMListNew(BaseModel):
    id: int
    model_name: Union[str, None] = None



class LLMCreate(BaseModel):
    api_key: str
    api_base: Union[str, None] = None
    azure_deployment_model: Union[str, None] = None
    azure_embedding_model: Union[str, None] = None
    open_ai_version: Union[str, None] = None
    open_ai_type: str
    model_engine: str
    model_name: str
    icon_name: str
    model_token_limit: int
    description: Union[str, None] = None
    output_token_limit: Union[int, None] = 0
    priority: Union[int, None] = None