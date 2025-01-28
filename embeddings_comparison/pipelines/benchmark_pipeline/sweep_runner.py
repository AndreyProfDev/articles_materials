import json
import os
import time
from dataclasses import dataclass, field

import hydra
from conf import hugging_face_conf, open_ai_conf
from hydra.core.config_store import ConfigStore
from metaflow import Runner
from omegaconf import MISSING, DictConfig, OmegaConf

# Initialize config store
cs = ConfigStore.instance()

# Register main config class
defaults = [{"embedding_model": MISSING}]


@dataclass
class Config:
    defaults: list[dict[str, str]] = field(default_factory=lambda: defaults)


cs.store(name="config", node=Config)

# Register model configs in config store
hugging_face_conf.register_models_in_config_store()
open_ai_conf.register_models_in_config_store()

# Define tag to identify identify all runs of this sweep
TAG = f"sweep_{int(time.time())}"


@hydra.main(config_name="config", version_base=None)
def benchmark(cfg: DictConfig) -> None:
    dict_conf = OmegaConf.to_container(cfg, resolve=True)
    json_conf = json.dumps({"config": dict_conf})
    env = os.environ.copy()
    env.update({"METAFLOW_FLOW_CONFIG_VALUE": json_conf})
    with Runner("pipelines/benchmark_pipeline/benchmark_pipeline.py", env=env).run(
        tags=[TAG, f"model:{cfg.embedding_model.model_name}"]
    ) as running:
        print("Benchmark finished")


if __name__ == "__main__":
    benchmark()
