from flask import Flask, render_template, request
import requests
from werkzeug.datastructures import FileStorage
from io import BytesIO
import main

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

 
@app.route('/secret')
def secret():
    return ":eyes:"


@app.route('/', methods=['POST'])
def run_script():
    try:
        image_file = request.files['image']

        path = 'temp_path'
        image_file.save(path)

        image = main.get_image(path)
        # main.display_image(image)
        points = main.calculate_points(image)
        result = main.get_equations(points, image)
        # return result
        return render_template('index.html', equations=result)

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
