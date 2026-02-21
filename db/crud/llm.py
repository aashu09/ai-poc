from schemas.llm import LLMCreate
from db.models.llm import LLM

def get_llm_by_id(model_id, db):
    llm = db.query(LLM).filter(LLM.id == model_id).first()
    return llm


def get_gpt40_mini_llm1_semi_structured(model_number, db):
    llm = db.query(LLM).filter(LLM.model_name.ilike(f"%GPT-4o-mini-v{model_number}")).first()
    return llm


def get_gpt40_mini_llm_idle(db):
    llm = db.query(LLM).filter(LLM.model_name.ilike("%GPT-4o-mini-idle")).first()
    return llm

def get_gpt40_mini_llm3(db):
    llm = db.query(LLM).filter(LLM.model_name.ilike("%GPT-4o-mini-v3")).first()
    return llm

def get_gpt40_mini_llm4(db):
    llm = db.query(LLM).filter(LLM.model_name.ilike("%GPT-4o-mini-v4")).first()
    return llm


def get_gpt40_mini_llm(db):
    llm = db.query(LLM).filter(LLM.model_name.ilike("%GPT-4o-mini%")).first()
    return llm

def get_gpt40_omni_llm(db):
    llm = db.query(LLM).filter(LLM.model_name.ilike("%gpt-4o")).first()
    return llm


def get_llm(db):
    llm = db.query(LLM).filter(LLM.is_visible == True).all()
    return llm


def create_llm(llm_data: LLMCreate, db):
    llm = LLM(api_key=llm_data.api_key, api_base=llm_data.api_base, azure_deployment_model=llm_data.azure_deployment_model,
                      azure_embedding_model=llm_data.azure_embedding_model, open_ai_version=llm_data.open_ai_version,
                      open_ai_type=llm_data.open_ai_type, model_engine=llm_data.model_engine,
                      model_name=llm_data.model_name, icon_name=llm_data.icon_name,
                      model_token_limit=llm_data.model_token_limit, description=llm_data.description,
              output_token_limit=llm_data.output_token_limit)
    db.add(llm)
    db.commit()
    db.refresh(llm)
    return llm


def get_first_llm(db):
    llm = db.query(LLM).first()
    return llm
