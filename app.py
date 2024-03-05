from flask import Flask, render_template, request
import requests
from werkzeug.datastructures import FileStorage
from io import BytesIO
import json
import main

app = Flask(__name__, static_url_path='/static')
result = []


@app.route('/')
def index():
    return render_template('index.html')

 
@app.route('/secret')
def secret():
    return ":eyes:"


@app.route('/desmos')
def desmos():
    try:
        return render_template('desmos.html', equations=json.dumps(result))
    except Exception as e:
        return str(e)
    

@app.route('/', methods=['POST'])
def run_script():
    try:
        result.clear()

        image_file = request.files.getlist('image')
        print(len(image_file))

        for image in image_file:
            path = 'temp_path'
            image.save(path)

            image = main.get_image(path)

            if image is None:
                return render_template('index.html')

            equation_image = main.EquationImage(image)

            # equation_image.display_image()

            equations = equation_image.get_equations(image)

            result.append(equations)
            printed_result = equation_image.get_printed_equations(equations)
            number_of_equations = equation_image.get_num_equations(equations)

        return render_template('index.html', equations=printed_result, equation_count=number_of_equations)
    except Exception as e:
        return str(e)
    


if __name__ == '__main__':
    app.run(debug=True)
