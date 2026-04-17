from flask import Flask, render_template


app = Flask(__name__)


# Base Route
@app.route('/')
def hello():
    return render_template('hello.html')


# Welcome Route
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


# Bye Route
@app.route('/bye')
def bye():
    return render_template('bye.html')

# user name route
@app.route('/user/<name>')

if __name__ == '__main__':
    app.run(debug=True)