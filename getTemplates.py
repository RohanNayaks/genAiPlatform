from Guardial import InputGuardial as IG
class TemplateCreator:

    def __init__(self,text):
        #Initiing the variable to generate Template
        self.templateResponse = self.generateIntentTemplate(text)
    
    def getMaskeddata(self,text):
        #this method calls Guardial class and masks the data
        maskedData = IG(text).result_data
        return maskedData
    
    def generateIntentTemplate(self,text):
        #The method takes the data and generates the template
        data = self.getMaskeddata(text)
        return data

