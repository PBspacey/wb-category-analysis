from flask import Flask, request, render_template, redirect, url_for


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

if __name__ == '__main__':
    app.run(debug=True)