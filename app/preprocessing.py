# import nltk
import numpy as np 
import torch
from torchvision import transforms
from PIL import Image

# from models import nlp_model


def text_preprocessing(text:str) -> np.array:
    '''
    takes text to the input and preprocess it to the format needed to prediction
    '''
    def lemmatize(text:str):
        '''
        takes text, extract lemma for each word and remove stopwords
        '''
        doc = re.sub(patterns, ' ', text)
        tokens = []
        for token in doc.split():
            if token and token not in stopwords_ru:
                token = token.strip()
                token = morph.normal_forms(token)[0]
                tokens.append(token)
        return tokens
    
    def preprocess_text(text:str):
        '''
        takes text, remove punctuation, stopwords, make lemmatization 
        '''
        text = str(text).lower()

        # deleting punctuation
        punc = str.maketrans('', '', string.punctuation)
        text_no_punct = text.translate(punc)

        # lemmatizing
        lematized_text = lemmatize(text_no_punct)

        return lematized_text
    
    preprocessed_text = preprocess_text(text)
    embedding = nlp_model.doc2vec.infer(preprocessed_text)

    return embedding


def image_preprocessing(image_path:str) -> torch.tensor:
    '''
    takes image path and preprocess the image for cv network input
    '''
    image = Image.open(image_path).convert('RGB')

    transform = transforms.Compose([
        transforms.Resize(size=226),
        transforms.CenterCrop(size=254),
        transforms.ToTensor(),
        transforms.Resize((224,224)),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])
    
    tensor_image = transform(image)
    tensor_image = tensor_image.unsqueeze(0)
    
    return tensor_image


if __name__ == '__main__':
    print(image_preprocessing('C:/Users/senia/Desktop/wb sphere analysis/images/0/50.jpg'))
