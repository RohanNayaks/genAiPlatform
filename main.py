from fastapi import FastAPI, Query
from reducelatency import FirstCache as fc
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Create FastAPI instance
app = FastAPI()

# Instantiate FirstCache
first_cache = fc()

# Define a GET endpoint
@app.get("/getResponse")
def get_response(text: str = Query(..., description="Input text"), model: str = Query(..., description="Model name")):
    if "generate" in text.lower():
        # Triggers the Cache method.
        response = first_cache.getCacheAnswer(text=text, modelName=model)
        return {"response": response}
    else:
        return {"response": "This is the standard response"}

# Main method to run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)






# from reducelatency import FirstCache as fc
# import warnings
# warnings.filterwarnings('ignore')
# #initial  method to be executed
# if __name__ == "__main__":
#     text = input("Try saying 'Generate Utterances for [intent name]': ")
#     model = input("what is the model name: ")

#     if "generate" in text.lower():
#         #triggers the Cache method.
#         print(fc().getCacheAnswer(text=text,modelName=model))
#     else:
#         print("This is the standard response")