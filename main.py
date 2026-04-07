from fastapi import FastAPI, HTTPException
from reducelatency import FirstCache as fc
from jailbreak import JailbreakGuard
from loguru import logger
from schemas import ResponseRequest, ResponseOutput, ErrorResponse
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

# POST endpoint with request body
@app.post("/getResponse", response_model=ResponseOutput, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
def get_response(request: ResponseRequest) -> ResponseOutput:
    try:
        logger.info(f"[API] Received request - text: {request.text}, model: {request.model}, masking: {request.masking}, is_masking: {request.is_masking}")

        # Jailbreak check BEFORE cache (early exit)
        if jailbreak_guard.is_jailbreak(request.text):
            logger.warning(f"[API] Jailbreak attempt detected, rejecting request: {request.text}")
            raise HTTPException(status_code=400, detail="Request rejected: potential jailbreak detected")

        if "generate" in request.text.lower():
            # Triggers the Cache method.
            logger.info("[API] 'generate' keyword found, triggering cache method")
            response = first_cache.getCacheAnswer(
                text=request.text,
                modelName=request.model,
                masking=request.masking,
                is_masking=request.is_masking
            )

            if response is None:
                logger.error("[API] Cache returned None response")
                raise HTTPException(status_code=500, detail="Failed to generate response from model")

            logger.info(f"[API] Response generated successfully: {response}")
            return ResponseOutput(response=response)
        else:
            logger.info("[API] 'generate' keyword not found, returning standard response")
            return ResponseOutput(response="This is the standard response")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] Error: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went wrong")

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