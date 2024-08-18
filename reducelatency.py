import redis
from getTemplates import TemplateCreator as TC
class FirstCache:

    def __init__(self):
        #This constructor initates redi
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

        
    def getCacheAnswer(self,text):
        #Checks if the redis already as the value or generates a new response
        #self.r.set(text,"Correct Response")
        #response = self.r.get(text)
        response = None
        if(response is not None):
            return response
        else:
           FinalResponse = TC(text=text).templateResponse
           return FinalResponse



