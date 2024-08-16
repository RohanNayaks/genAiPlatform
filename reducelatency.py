import redis

class FirstCache:

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

        
    def getCacheAnswer(self,text):
        #self.r.set(text,"Correct Response")
        response = self.r.get(text)
        if(response is not None):
            return response
        else:
            print("Send data to Template Class")



