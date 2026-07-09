from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ModelProfile:
    chat_model: str
    embedding_model: str
    rerank_model: str
    judge_model: str
    direct_nvidia_chat_model: str


NVIDIA_DEMO_PROFILE = ModelProfile(
    chat_model="nvidia_nim/mistralai/mistral-small-4-119b-2603",
    embedding_model="nvidia_nim/nvidia/nv-embedqa-e5-v5",
    rerank_model="nvidia/llama-nemotron-rerank-1b-v2",
    judge_model="nvidia_nim/mistralai/mistral-small-4-119b-2603",
    direct_nvidia_chat_model="mistralai/mistral-small-4-119b-2603",
)


def get_model_profile() -> ModelProfile:
    return ModelProfile(
        chat_model=os.getenv("AHC_CHAT_MODEL", os.getenv("AHC_MODEL", NVIDIA_DEMO_PROFILE.chat_model)),
        embedding_model=os.getenv("AHC_EMBEDDING_MODEL", NVIDIA_DEMO_PROFILE.embedding_model),
        rerank_model=os.getenv("AHC_RERANK_MODEL", NVIDIA_DEMO_PROFILE.rerank_model),
        judge_model=os.getenv("AHC_JUDGE_MODEL", NVIDIA_DEMO_PROFILE.judge_model),
        direct_nvidia_chat_model=os.getenv("AHC_DIRECT_NVIDIA_CHAT_MODEL", NVIDIA_DEMO_PROFILE.direct_nvidia_chat_model),
    )
