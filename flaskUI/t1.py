import os
from flask import Flask,render_template,request

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route('/')
def home():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'logfiles/')
    print(target)
    file1 = request.files['file1']
    file2 = request.files['file2']
    file_path1 = '/'.join([target, file1.filename])
    file_path2 = '/'.join([target, file2.filename])
    return file_path1 + file_path2


if __name__ == "__main__":
	app.run(debug=True)

