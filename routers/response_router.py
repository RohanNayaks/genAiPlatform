from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from schemas import ResponseRequest, ResponseOutput, ErrorResponse
from services.guard_service import JailbreakGuardService
from services.cache_service import CacheService


router = APIRouter()


def get_guard_service() -> JailbreakGuardService:
    return JailbreakGuardService()


def get_cache_service() -> CacheService:
    from services.masking_service import MaskingService
    from services.template_service import TemplateService
    from services.model_service import ModelService
    masking = MaskingService()
    template = TemplateService(masking_service=masking)
    model = ModelService()
    return CacheService(template_service=template, model_service=model)


@router.post("/getResponse", response_model=ResponseOutput, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
def get_response(
    request: ResponseRequest,
    guard: JailbreakGuardService = Depends(get_guard_service),
    cache: CacheService = Depends(get_cache_service),
) -> ResponseOutput:
    try:
        logger.info(f"[Router] Received request - text: {request.text}, model: {request.model}")

        if guard.is_jailbreak(request.text):
            logger.warning(f"[Router] Jailbreak detected: {request.text}")
            raise HTTPException(status_code=400, detail="Request rejected: potential jailbreak detected")

        if "generate" in request.text.lower():
            response = cache.get_response(
                text=request.text,
                model_name=request.model,
                is_masking=request.is_masking,
                masking_strategy=request.masking or "default",
            )
            return ResponseOutput(response=response)

        return ResponseOutput(response="This is the standard response")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Router] Error: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went wrong")
