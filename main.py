from reducelatency import FirstCache as fc
import warnings
warnings.filterwarnings('ignore')
#initial  method to be executed
if __name__ == "__main__":
    text = input("Try saying 'Generate Utterances for [intent name]': ")
    model = input("what is the model name: ")

    if "generate" in text.lower():
        #triggers the Cache method.
        print(fc().getCacheAnswer(text=text,modelName=model))
    else:
        print("This is the standard response")