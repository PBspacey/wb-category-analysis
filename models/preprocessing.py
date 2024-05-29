# import nltk
import numpy as np 
import re
import string
import pandas as pd
import torch
from torchvision import transforms
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
from PIL import Image



def text_preprocessing(text) -> np.array:
    '''
    takes text to the input and preprocess it to the format needed to prediction
    '''
    if isinstance(text, str):
        text = pd.Series(text)

    patterns = '[^0-9а-яА-ЯёЁ\s]+'
    stopwords_ru = stopwords.words("russian")
    morph = MorphAnalyzer()

    def lemmatize(text):
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
    
    preprocessed_text = text.apply(lambda x: preprocess_text(x))

    return preprocessed_text


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
    # print(image_preprocessing('C:/Users/senia/Desktop/wb sphere analysis/images/0/50.jpg'))
    text = pd.read_csv('/Users/nikitasenyatkin/Downloads/texts_labeled.tsv', sep='\t')
    text = pd.Series(text['INPUT:comment'])
    text_preprocessing(text)