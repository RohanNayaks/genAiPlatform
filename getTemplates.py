from Guardial import InputGuardial as IG
class TemplateCreator:

    def __init__(self,text):
        self.templateResponse = self.generateIntentTemplate(text)
    
    def generateIntentTemplate(self,text):
        maskedData = IG(text).result_data
        return maskedData

