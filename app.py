from flask import Flask, render_template, request
import requests
from werkzeug.datastructures import FileStorage
from io import BytesIO
import main

app = Flask(__name__, static_url_path='/static')
result = ""


@app.route('/')
def index():
    return render_template('index.html')

 
@app.route('/secret')
def secret():
    return ":eyes:"


@app.route('/desmos')
def desmos():
    try:
        global result
        return render_template('desmos.html', equations=result)
    except Exception as e:
        return str(e)


@app.route('/', methods=['POST'])
def run_script():
    try:
        global result

        image_file = request.files['image']

        path = 'temp_path'
        image_file.save(path)

        image = main.get_image(path)

        if image is None:
            return render_template('index.html')

        equation_image = main.EquationImage(image)

        # equation_image.display_image()

        result = equation_image.get_equations(image)

        return render_template('index.html', equations=result)
    except Exception as e:
        return str(e)
    


if __name__ == '__main__':
    app.run(debug=True)
