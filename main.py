from fastapi import FastAPI, Query, HTTPException
from reducelatency import FirstCache as fc
from jailbreak import JailbreakGuard
from loguru import logger
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure logger
logger.add("logs/app.log", rotation="500 MB", retention="7 days")

# Create FastAPI instance
app = FastAPI()

# Instantiate FirstCache and JailbreakGuard
first_cache = fc()
jailbreak_guard = JailbreakGuard()

# Define a GET endpoint
@app.post("/getResponse")
def get_response(
    text: str = Query(..., description="Input text"),
    model: str = Query(..., description="Model name"),
    masking: str = Query(None, description="Masking strategy: 'gliner' or default"),
    is_masking: bool = Query(False, description="Enable masking"),
):
    logger.info(f"[API] Received request - text: {text}, model: {model}, masking: {masking}, is_masking: {is_masking}")

    # Jailbreak check BEFORE cache (early exit)
    if jailbreak_guard.is_jailbreak(text):
        logger.warning(f"[API] Jailbreak attempt detected, rejecting request: {text}")
        raise HTTPException(status_code=400, detail="Request rejected: potential jailbreak detected")

    if "generate" in text.lower():
        # Triggers the Cache method.
        logger.info("[API] 'generate' keyword found, triggering cache method")
        response = first_cache.getCacheAnswer(text=text, modelName=model, masking=masking, is_masking=is_masking)
        logger.info(f"[API] Response generated successfully: {response}")
        return {"response": response}
    else:
        logger.info("[API] 'generate' keyword not found, returning standard response")
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