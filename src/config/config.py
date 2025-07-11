from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml
from pathlib import Path

from src.core.reranker import RerankerConfig
from src.core.retriever import RankFusionConfig
from src.retrievers.global_retriever import GlobalRetrieverConfig
from src.retrievers.local_retriever import LocalRetrieverConfig


class SystemConfig(BaseModel):
    model_cache_dir: Path
    output_dir: Path
    log_level: str

class DataConfig(BaseModel):
    corpus_path: Path
    categories_path: Path
    classifier_training_data: Path
    all_doc_path: Path
    local_doc_path: Path
    queries_path: Path
    output_path: Path

class VectorDBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='VECTOR_DB_')
    
    collection_name: str
    host: str = "localhost"
    port: int = 6333
    api_key: str | None = None # Optional API key

# class LexicalConfig(BaseModel):
#     index_name: str
#     top_k: int

# class SemanticConfig(BaseModel):
#     embedding_model: str
#     top_k: int
#     vector_db: VectorDBConfig

# class GlobalRetrievalConfig(BaseModel):
#     lexical: LexicalConfig
#     semantic: SemanticConfig

# class LocalRetrievalConfig(BaseModel):
#     classifier_model: str
#     top_k_per_category: int

# class RankFusionConfig(BaseModel):
#     method: str
#     top_n_candidates: int

# class RerankerConfig(BaseModel):
#     cross_encoder_model: str
#     batch_size: int

class PipelineConfig(BaseModel):
    enable_local_retriever: bool
    enable_global_retriever: bool
    enable_reranker: bool
    local_retriever: LocalRetrieverConfig
    global_retriever: GlobalRetrieverConfig
    rank_fusion: RankFusionConfig
    reranker: RerankerConfig

# --- The main Configuration Model ---
# This class ties everything together.
class Config(BaseModel):
    system: SystemConfig
    data: DataConfig
    pipeline: PipelineConfig

# --- Helper function to load the config ---
def load_config(config_path: str | Path = "config/config.yaml") -> Config:
    """Loads configuration from a YAML file and validates it with Pydantic."""
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    return Config(**config_data)

# You can create a global config instance to be imported by other modules
# Or, even better, load it in your main entry point and pass it down.
# See Step 4.