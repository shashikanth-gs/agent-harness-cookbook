import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_litellm import ChatLiteLLM

class MockChatModel(GenericFakeChatModel):
    def bind_tools(self, *args, **kwargs):
        return self

def get_chat_model(
    mock_responses: list[BaseMessage] | None = None,
    model: str | None = None
) -> BaseChatModel:
    """
    Factory to retrieve a LangChain-compatible Chat Model.
    
    If MOCK_LLM is "true", returns a GenericFakeChatModel using the provided mock_responses.
    Otherwise, returns a ChatLiteLLM integration using the provided model name or AHC_MODEL env var.
    """
    is_mock = os.getenv("MOCK_LLM", "true").lower() == "true"
    
    if is_mock:
        if not mock_responses:
            raise ValueError("mock_responses must be provided when MOCK_LLM is true")
        return MockChatModel(messages=iter(mock_responses))
    
    # Use specified model or fallback to env var
    model_name = model or os.getenv("AHC_MODEL")
    if not model_name:
        raise ValueError("A model must be provided or AHC_MODEL environment variable must be set.")
        
    return ChatLiteLLM(model=model_name)
