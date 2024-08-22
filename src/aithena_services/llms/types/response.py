"""Response for AithenaServices API."""

from typing import AsyncGenerator, Generator

from llama_index.core.base.llms.types import ChatResponse as LlamaIndexChatResponse

from .message import Message


class ChatResponse(LlamaIndexChatResponse):
    """Modified LlamaIndex ChatResponse with Message as AithenaServices Message."""

    class Config:  # pylint: disable=missing-class-docstring, too-few-public-methods
        arbitrary_types_allowed = True

    message: Message  # type: ignore

    @classmethod
    def from_llamaindex(
        cls, llama_index_response: LlamaIndexChatResponse
    ) -> "ChatResponse":
        """Create ChatResponse from LlamaIndex ChatResponse."""
        msg = Message(**llama_index_response.message.dict())
        li_ = llama_index_response.copy(update={"message": msg})
        return cls(**li_.dict())


ChatResponseGen = Generator[ChatResponse, None, None]
ChatResponseAsyncGen = AsyncGenerator[ChatResponse, None]
