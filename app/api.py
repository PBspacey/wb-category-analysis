from flask import Flask, request, render_template, redirect, url_for
from models.models import Doc2VecModel, CBclassifier, CVmodel
import os


current_directory = os.getcwd()
print("Текущая рабочая директория:", current_directory)

new_directory = "."
os.chdir(new_directory)


app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('home.html')


@app.route('/about')
def about_page():
    return render_template('about.html')
 

@app.route('/evaluate')
def evaluate_page():
    return render_template('evaluate.html')

@app.route('/eval_result', methods=['POST', 'GET'])
def process_form():

    text = request.form['textinput']
    file = request.files['file']

    nlp_pred = None
    cv_pred = None 
    mn = None

    if text and file:

        d2v = Doc2VecModel()
        cb = CBclassifier()
        vectors = d2v.infer(text)
        nlp_pred = cb.infer(vectors)

        cv = CVmodel()
        cv_pred = cv.infer(file)

        mn = round(float(200/((1/cv_pred[:,1][0]) + (1/nlp_pred[:,1][0]))), 2)
        nlp_pred = round(nlp_pred[:,1][0]*100, 2)
        cv_pred = round(float(cv_pred[:,1][0]*100), 2)

    
    elif file and not text: 
        cv = CVmodel()
        cv_pred = cv.infer(file)
        cv_pred = round(float(cv_pred[:,1][0]*100), 2)

    
    elif not file and text:
        d2v = Doc2VecModel()
        cb = CBclassifier()

        vectors = d2v.infer(text)
        nlp_pred = cb.infer(vectors)
        nlp_pred = round(nlp_pred[:,1][0]*100, 2)


    return render_template('eval_result.html', nlp_pred=nlp_pred, cv_pred=cv_pred, mn=mn)

if __name__ == '__main__':
    app.run(debug=True)