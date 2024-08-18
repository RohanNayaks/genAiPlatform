from reducelatency import FirstCache as fc
import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    text = input("Try saying 'Generate Utterances for [intent name]': ")

    if "generate" in text.lower():
        print(fc().getCacheAnswer(text=text))
    else:
        print("This is the standard response")