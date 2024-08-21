import json
class InvokeGenAI:

    def __init__(self,templateCreated):
        self.templateCreated = templateCreated
        self.model_functions = {
            "phy3": self.phy3Model,
            "openAI": self.phy3Model,
            # Add more models and their functions here
        }

    def invoke_model(self, model_name):
        # Get the corresponding function based on the model name
        func = self.model_functions.get(model_name)

        if func:
            response = func()  # Call the respective function
            return response
        else:
            print(f"No function found for the model name: {model_name}")
            # Handle cases where the model name doesn't match any function
    
    def phy3Model(self):
        data = f"Ph3 model response for {self.templateCreated}"
        return data

