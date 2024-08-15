# mypy: disable-error-code="import-untyped"
"""Ollama implementation based on LlamaIndex."""

# pylint: disable=too-many-ancestors
from typing import Any, Sequence

from llama_index.llms.azure_openai import AzureOpenAI as LlamaIndexAzureOpenAI

from aithena_services.envvars import AZURE_OPENAI_ENV_DICT
from aithena_services.llms.types import (
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    Message,
)
from aithena_services.llms.utils import check_and_cast_messages


class AzureOpenAI(LlamaIndexAzureOpenAI):
    """AzureOpenAI LLMs."""

    def __init__(self, **kwargs: Any):
        kwargs["api_key"] = AZURE_OPENAI_ENV_DICT["api_key"]
        kwargs["azure_endpoint"] = AZURE_OPENAI_ENV_DICT["azure_endpoint"]
        kwargs["api_version"] = AZURE_OPENAI_ENV_DICT["api_version"]
        if AZURE_OPENAI_ENV_DICT["model"] is not None and "model" not in kwargs:
            kwargs["model"] = AZURE_OPENAI_ENV_DICT["model"]
        if AZURE_OPENAI_ENV_DICT["engine"] is not None and "engine" not in kwargs:
            kwargs["engine"] = AZURE_OPENAI_ENV_DICT["engine"]
        super().__init__(**kwargs)

    def chat(self, messages: Sequence[dict | Message], **kwargs: Any) -> ChatResponse:
        messages = check_and_cast_messages(messages)
        llama_index_response = super().chat(messages, **kwargs)
        msg = Message(**llama_index_response.message.dict())
        return llama_index_response.copy(update={"message": msg})

    def stream_chat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponseGen:
        messages = check_and_cast_messages(messages)
        llama_stream = super().stream_chat(messages, **kwargs)

        def gen() -> ChatResponseGen:

            for response in llama_stream:
                msg = Message(**response.message.dict())
                yield response.copy(update={"message": msg})

        return gen()

    async def astream_chat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        messages = check_and_cast_messages(messages)
        llama_stream = super().astream_chat(messages, **kwargs)

        async def gen() -> ChatResponseAsyncGen:

            async for response in await llama_stream:
                msg = Message(**response.message.dict())
                yield response.copy(update={"message": msg})

        return gen()

    async def achat(
        self, messages: Sequence[dict | Message], **kwargs: Any
    ) -> ChatResponse:
        messages = check_and_cast_messages(messages)
        llama_index_response = await super().achat(messages, **kwargs)
        msg = Message(**llama_index_response.message.dict())
        return llama_index_response.copy(update={"message": msg})
