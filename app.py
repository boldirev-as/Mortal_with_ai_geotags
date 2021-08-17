import os

from flask import Flask, render_template, request, send_from_directory

# есть базовый файл base.html где содержится код header, footer, подключение стилей
# остальные файлы по факту наследуются от базового, название файла == страница

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_secret_key'


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# тут реализация идеи сражения человека с ИИ
@app.route('/mortal_with_ai', methods=['GET', 'POST'])
def mortal_with_ai():
    return render_template("mortal_with_ai.html")


# тестирование ИИ
@app.route('/test_ai', methods=['GET', 'POST'])
def test_ai():
    if request.method == "POST":
        try:
            print(request.files)
            img = request.files['images[]']
            if img is not None:
                img.save(f'static/img/image.png')
            # result = model.get_result(Image.open('static/image.png'))
        except Exception as e:
            print(e)

    return render_template("test_ai.html")


# иконка страницы
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
