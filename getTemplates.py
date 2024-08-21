from Guardial import InputGuardial as IG
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
class TemplateCreator:

    def __init__(self,text):
        #Initiing the variable to generate Template
        self.text = text
        self.templateResponse = self.callTemplate()
    
    def getMaskeddata(self,text):
        #this method calls Guardial class and masks the data
        maskedData = IG(text).result_data
        return maskedData
    
    def generateIntentTemplate(self,text):
        #The method takes the data and generates the template
        data = self.getMaskeddata(text)
        return data

    def callTemplate(self):
        maskedUtterance = self.generateIntentTemplate(self.text)
        prompt_template = PromptTemplate.from_template(
            "Generate utterance for the Intent: {adjective} here are few examples {content}."
        )
        prompt = prompt_template.format(adjective=maskedUtterance, content=maskedUtterance)
        return prompt