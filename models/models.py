import pandas as pd 
import torch
import numpy as np 
import cv2
import io
import json
import base64
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
from gensim.models.doc2vec import Doc2Vec
from models.preprocessing import text_preprocessing, image_preprocessing
from catboost import CatBoostClassifier
from gensim.models.doc2vec import TaggedDocument



class Doc2VecModel:

    def __init__(self, model_path='./models/doc2vec.model'):
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
        tagged_data = [TaggedDocument(words=d, tags=[str(i)]) for i, d in enumerate(preprocessed_doc)]
       
        vectors = pd.DataFrame(self.model.infer_vector(doc.words) for doc in tagged_data)
        return vectors
    

    def nlp_cam(self, documents):

        with open ('./models/words.json', 'r') as f:
            dct = json.load(f)

        preprocessed_doc = text_preprocessing(documents)[0]
        preprocessed_doc = set(preprocessed_doc)
        pos_intercept = set(dct['positive']) & preprocessed_doc
        neg_intercept = set(dct['negative']) & preprocessed_doc

        n = '\n'
        return f'Слова в описании, оказывающие положительное влияние на привлекательность:\n' \
            f'{n}{" ".join(list(pos_intercept)) if pos_intercept else "таких слов нет"}.\n' \
            f'Слова, оказывающие негативное влияние на привлекательность:\n' \
            f'{n}{" ".join(list(neg_intercept)) if neg_intercept else "таких слов нет"}'


        
class CBclassifier:
    def __init__(self, model_path='./models/CB.cbm'):
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


class CVmodel:

    def __init__(self, model_path='./models/cvResNet.pth'):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model_path = model_path
        self.model = self.load_model(model_path).to(self.device)

    def load_model(self, model_path):
        try:
            model = torch.load(model_path)
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

        self.model.eval()
        with torch.no_grad():
            preds = torch.sigmoid(self.model(input))
        
        return preds
    

    def create_gradient_cam(self, path_to_image):

       
        target_layers = [list(self.model.children())[4][-1]]
        image_path = path_to_image
        tensor_image = self.preprocess(image_path)
        tensor_image = tensor_image.to(self.device)

        cam = GradCAM(model=self.model, target_layers=target_layers)

        img = np.array(Image.open(image_path).convert('RGB'))
        img = cv2.resize(img, (224, 224))
        img = np.float32(img) / 255


        targets = [ClassifierOutputTarget(1)]

        grayscale_cam = cam(input_tensor=tensor_image, targets=targets)

        grayscale_cam = grayscale_cam[0, :]
        print(grayscale_cam.shape)
        print(img.shape)
        print(tensor_image.size())
        visualization = show_cam_on_image(img, grayscale_cam, use_rgb=True)
        cam = np.uint8(255*grayscale_cam[0, :])
        cam = cv2.merge([cam, cam, cam])
        images = np.hstack((np.uint8(255*img), cam , visualization))
    
        image = Image.fromarray(images)

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return img_str

    

if __name__ == '__main__':
    model = Doc2VecModel('./models/doc2vec.model')
    text = pd.read_csv('/Users/nikitasenyatkin/Downloads/texts_labeled.tsv', sep='\t')
    text = pd.Series(text['INPUT:comment'])[:3]
    text = 'очень плохой чай не советую никому не хотим вам его предлагать'
    d2v = model.infer(text)
    model.nlp_cam(text)
    cb = CBclassifier('./models/CB.cbm')
    print(cb.infer(d2v))

    cv = CVmodel('./models/cvResNet.pth')
    print(cv.infer('/Users/nikitasenyatkin/Desktop/Снимок экрана 2024-05-27 в 23.02.02.png'))




