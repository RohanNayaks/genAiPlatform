from pydantic import BaseModel, Field
from typing import Optional
from loguru import logger


class ResponseRequest(BaseModel):
    """
    Request model for the /getResponse endpoint.

    Attributes:
        text: The input text to process. Must contain 'generate' keyword to trigger cache.
        model: The name of the model to use for generating responses.
        masking: Optional masking strategy ('gliner' or default).
        is_masking: Whether to enable masking for sensitive data. Defaults to False.
    """
    text: str = Field(..., min_length=1, description="Input text to process")
    model: str = Field(..., min_length=1, description="Model name to use")
    masking: Optional[str] = Field(None, description="Masking strategy: 'gliner' or default")
    is_masking: bool = Field(False, description="Enable masking for sensitive data")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Generate Utterances for greeting",
                "model": "gpt-4",
                "masking": "gliner",
                "is_masking": True
            }
        }


class ResponseOutput(BaseModel):
    """
    Response model for the /getResponse endpoint.

    Attributes:
        response: The generated response from the model.
    """
    response: str = Field(..., description="The generated response")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Generated utterances for greeting intent"
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response model for failed requests.

    Attributes:
        detail: Error message describing what went wrong.
    """
    detail: str = Field(..., description="Error message")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Request rejected: potential jailbreak detected"
            }
        }
