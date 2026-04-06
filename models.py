from loguru import logger

class InvokeGenAI:

    def __init__(self,templateCreated):
        logger.info(f"[InvokeGenAI] Initializing with template: {templateCreated}")
        self.templateCreated = templateCreated
        self.model_functions = {
            "phi3": self.phy3Model,
            "openAI": self.OpenAiModel,
            "claude": self.ClaudeModel,
            "gemini": self.GeminiModel,
        }

    def invoke_model(self, model_name):
        # Get the corresponding function based on the model name
        logger.info(f"[InvokeGenAI.invoke_model] Invoking model: {model_name}")
        func = self.model_functions.get(model_name)

        if func:
            logger.info(f"[InvokeGenAI.invoke_model] Model function found for {model_name}, executing")
            response = func()  # Call the respective function
            logger.info(f"[InvokeGenAI.invoke_model] Model execution completed")
            return response
        else:
            logger.error(f"[InvokeGenAI.invoke_model] No function found for the model name: {model_name}")
            # Handle cases where the model name doesn't match any function

    def phy3Model(self):
        logger.info("[InvokeGenAI.phy3Model] Executing Phi3 model")
        data = f"Phi3 model response for {self.templateCreated}"
        logger.info(f"[InvokeGenAI.phy3Model] Phi3 response: {data}")
        return data

    def OpenAiModel(self):
        logger.info("[InvokeGenAI.OpenAiModel] Executing OpenAI model")
        data = f"OpenAI model response for {self.templateCreated}"
        logger.info(f"[InvokeGenAI.OpenAiModel] OpenAI response: {data}")
        return data

    def ClaudeModel(self):
        logger.info("[InvokeGenAI.ClaudeModel] Executing Claude model")
        data = f"Claude model response for {self.templateCreated}"
        logger.info(f"[InvokeGenAI.ClaudeModel] Claude response: {data}")
        return data

    def GeminiModel(self):
        logger.info("[InvokeGenAI.GeminiModel] Executing Gemini model")
        data = f"Gemini model response for {self.templateCreated}"
        logger.info(f"[InvokeGenAI.GeminiModel] Gemini response: {data}")
        return data

