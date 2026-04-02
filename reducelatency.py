import redis
from getTemplates import TemplateCreator as TC
from models import InvokeGenAI as IGI
from loguru import logger

class FirstCache:

    def __init__(self):
        #This constructor initates redi
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        logger.info("[FirstCache] Initialized Redis connection")


    def getCacheAnswer(self,text,modelName):
        #Checks if the redis already as the value or generates a new response
        logger.info(f"[FirstCache.getCacheAnswer] Starting cache check for text: {text}, model: {modelName}")
        #self.r.set(text,"Correct Response")
        #response = self.r.get(text)
        response = None
        if(response is not None):
            logger.info("[FirstCache.getCacheAnswer] Cache hit - returning cached response")
            return response
        else:
           logger.info("[FirstCache.getCacheAnswer] Cache miss - generating new response")
           utteranceWithTemplate = TC(text=text).templateResponse
           logger.info("[FirstCache.getCacheAnswer] Template created, invoking model")
           invokeGenAI = IGI(templateCreated=utteranceWithTemplate)
           modelResponse = invokeGenAI.invoke_model(model_name=modelName)
           logger.info(f"[FirstCache.getCacheAnswer] Model response received: {modelResponse}")

           return modelResponse





