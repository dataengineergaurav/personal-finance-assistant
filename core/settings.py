import os
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIChatModel


class Settings:
    # Model Configuration
    MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'ollama').lower()
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2')
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')
    OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # MLflow Configuration
    MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', 'sqlite:///mlflow.db')
    MLFLOW_EXPERIMENT_NAME = os.getenv('MLFLOW_EXPERIMENT_NAME', 'Personal Finance Assistant')

    @classmethod
    def get_model(cls, override_provider: str = None):
        """
        Unified model provider selection.
        """
        provider = (override_provider or cls.MODEL_PROVIDER).lower()
        
        if provider in ['gemini', 'google']:
            return GoogleModel(cls.GEMINI_MODEL)
        elif provider == 'ollama':            
            base_url = cls.OLLAMA_BASE_URL
            if 'ollama.com' in base_url.lower() and not base_url.endswith('/v1'):
                base_url = base_url.rstrip('/') + '/v1'
                
            provider_inst = OllamaProvider(
                base_url=base_url,
                api_key=cls.OLLAMA_API_KEY
            )
            return OpenAIChatModel(cls.OLLAMA_MODEL, provider=provider_inst)
        elif provider == 'openai':
            return f'openai:{cls.OPENAI_MODEL}'
        else:
            return GoogleModel(cls.GEMINI_MODEL)

# Global settings instance
settings = Settings()
