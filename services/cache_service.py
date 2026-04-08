import redis
from loguru import logger
from services.template_service import TemplateService
from services.model_service import ModelService


class CacheService:
    """S - Single responsibility: check cache, generate on miss, return result."""

    def __init__(self, template_service: TemplateService, model_service: ModelService):
        self.template_service = template_service
        self.model_service = model_service
        self._redis = None
        logger.info("[CacheService] Initialized (Redis connection deferred)")

    def _get_redis(self) -> redis.Redis:
        if self._redis is None:
            self._redis = redis.Redis(host="localhost", port=6379, decode_responses=True)
            logger.info("[CacheService] Redis connection established")
        return self._redis

    def get_response(self, text: str, model_name: str, is_masking: bool = False, masking_strategy: str = "default") -> str:
        logger.info(f"[CacheService] Checking cache for text: {text}")

        try:
            cached = self._get_redis().get(text)
            if cached is not None:
                logger.info("[CacheService] Cache hit")
                return cached
        except redis.ConnectionError:
            logger.warning("[CacheService] Redis unavailable, skipping cache")
            cached = None

        logger.info("[CacheService] Cache miss, generating response")
        prompt = self.template_service.build(text=text, is_masking=is_masking, masking_strategy=masking_strategy)
        response = self.model_service.generate(model_name=model_name, prompt=prompt)

        try:
            self._get_redis().set(text, response)
            logger.info("[CacheService] Response cached")
        except redis.ConnectionError:
            logger.warning("[CacheService] Redis unavailable, response not cached")

        logger.info(f"[CacheService] Returning response: {response}")
        return response
