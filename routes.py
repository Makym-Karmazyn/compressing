import logging

from flask import render_template, jsonify, Flask, request
from main import compress, decompress

# Налаштування логування
app = Flask(__name__)


@app.route("/", methods=["GET"])
def compress_or_decompress1():
    """Перенаправлення на сторінку."""
    return render_template("index.html")


@app.route("/compress_or_decompress", methods=["POST"])
def compress_or_decompress2():
    """
    Хендлер стиснення.
    Отримує файл з HTML та повертає його в шифр.
    """
    response_data = None
    uploaded_file = request.files.get("file")
    user_choice = request.form.get("compress_or_decompress")
    print(user_choice)
    filename = uploaded_file.filename
    if filename[-4:] == ".txt":
        filename2 = filename[:-4]

        if uploaded_file:
            if user_choice == "compress":
                compress(filename2)
                response_data = {
                'message': "compresed",
                'filename': f"{filename[:-4]}_compressed.bin",
            }
            else:
                decompress(filename2)
                response_data = {
                    'message': "decompresed",
                    'filename': f"{filename[:-4]}_decompressed.txt",
                }
        else:
            response_data = {'message': "No file uploaded"}
    else:
        response_data = {
            'message': "something wrong",
            'filename': "something wrong",
        }
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(port=8037, debug=True)
