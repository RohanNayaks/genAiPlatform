from guards.Guardial import InputGuardial as IG
from langchain_core.prompts import PromptTemplate
from loguru import logger

class TemplateCreator:

    def __init__(self, text, masking=None, is_masking=False):
        #Initiing the variable to generate Template
        logger.info(f"[TemplateCreator] Initializing with text: {text}, is_masking: {is_masking}")
        self.text = text
        self.masking = masking
        self.is_masking = is_masking
        self.templateResponse = self.callTemplate()
        logger.info("[TemplateCreator] Template creation completed")

    def getMaskeddata(self, text):
        #this method calls Guardial class and masks the data
        logger.info(f"[TemplateCreator.getMaskeddata] Getting masked data for text: {text}")
        if self.masking == "gliner":
            from guards.GlinerGuardial import GLiNERGuardial
            maskedData = GLiNERGuardial(text).result_data
        else:
            maskedData = IG(text).result_data
        logger.info(f"[TemplateCreator.getMaskeddata] Masked data: {maskedData}")
        return maskedData

    def generateIntentTemplate(self,text):
        #The method takes the data and generates the template
        logger.info(f"[TemplateCreator.generateIntentTemplate] Generating intent template")
        data = self.getMaskeddata(text)
        return data

    def callTemplate(self):
        logger.info("[TemplateCreator.callTemplate] Creating prompt template")
        if self.is_masking:
            maskedUtterance = self.generateIntentTemplate(self.text)
        else:
            maskedUtterance = self.text
        prompt_template = PromptTemplate.from_template(
            "Generate utterance for the Intent: {adjective} here are few examples {content}."
        )
        prompt = prompt_template.format(adjective=maskedUtterance, content=maskedUtterance)
        logger.info(f"[TemplateCreator.callTemplate] Prompt template created: {prompt}")
        return prompt