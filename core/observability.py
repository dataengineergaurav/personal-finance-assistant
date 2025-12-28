
import mlflow
import time
from typing import Any, Optional, Dict
from contextlib import asynccontextmanager
from core.settings import settings

class MLflowTracker:
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
            mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
            cls._initialized = True

@asynccontextmanager
async def track_agent_run(
    run_name: str, 
    model_name: str, 
    inputs: Dict[str, Any]
):
    """
    Async context manager to track an agent run in MLflow.
    """
    MLflowTracker.initialize()
    
    with mlflow.start_run(run_name=run_name) as run:
        # Log basic params
        mlflow.log_param("model", model_name)
        for k, v in inputs.items():
            mlflow.log_param(f"input_{k}", v)
        
        start_time = time.time()
        try:
            yield run
            # If successful, we can log success metadada if needed here
        except Exception as e:
            mlflow.log_param("error", str(e))
            mlflow.log_metric("success", 0)
            raise e
        finally:
            duration = time.time() - start_time
            mlflow.log_metric("latency", duration)

def log_agent_result(output: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Helper to log result and additional metadata within an active run.
    """
    if mlflow.active_run():
        mlflow.log_text(output, "output.txt")
        if metadata:
            for k, v in metadata.items():
                mlflow.log_param(f"meta_{k}", v)
