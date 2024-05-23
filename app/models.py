import pandas as pd 
import torch
from gensim.models.doc2vec import Doc2Vec
from preprocessing import text_preprocessing, image_preprocessing
from catboost import CatBoostClassifier




class Doc2VecModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        try:
            model = Doc2Vec.load(model_path)
            print(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def preprocess(self, text):
        return text_preprocessing(text)

    def infer(self, documents):

        if self.model is None:
            print("Model not loaded. Cannot perform inference.")
            return None
        

        preprocessed_doc = self.preprocess(documents)
        vectors = pd.DataFrame(self.model.infer_vector(doc.words) for doc in preprocessed_doc)
        return vectors
    
    def train(self, hyperparameters):
        pass



class CBclassifier:
    def __init__(self, model_path):
        self.model_path = model_path 
        self.model = self.load_model(model_path)


    def load_model(self, model_path):
        try:
            model = CatBoostClassifier().load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
        

    def infer(self, vectors):

        if self.model is None:
            print("Model not loaded. Cannot perform inference.")
            return None

        preds = self.model.predict_proba(vectors)
        return preds 
    
    
    def train(self, hyperparameters):
        pass



class CVmodel:

    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        try:
            torch.load(model_path)
            print(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
        
        
    def preprocess(self, path_to_image):

        return image_preprocessing(path_to_image)
    
    def infer(self, path_to_image):

        if self.model is None:
            print("Model not loaded. Cannot perform inference.")
            return None
        
        input = self.preprocess(path_to_image)

        model.eval()
        with torch.no_grad:
            preds = model(input)
        
        return preds


    

if __name__ == '__main__':
    # print(image_preprocessing('C:/Users/senia/Desktop/wb sphere analysis/images/0/50.jpg'))
    model = Doc2VecModel('./models/doc2vec.model')
    text = pd.read_csv('/Users/nikitasenyatkin/Downloads/texts_labeled.tsv', sep='\t')
    text = pd.Series(text['INPUT:comment'])[:3]
    text = 'очень плохой чай не советую никому не хотим вам его предлагать'
    d2v = model.infer(text)
    cb = CBclassifier('./models/CB.cbm')
    print(cb.infer(d2v))

    cv = CVmodel('./models/cvResNet.pth')
    print(cv.infer('C:/Users/senia/Desktop/wb sphere analysis/images/0/50.jpg'))

