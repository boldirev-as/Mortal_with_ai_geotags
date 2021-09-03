import os
from operations_with_images import create_image_from_empty_tiles, \
    prepare_new_set, machine_to_russian_point
from flask import Flask, render_template, request, \
    send_from_directory, url_for, redirect
import random

# есть базовый файл base.html где содержится код header, footer, подключение стилей
# остальные файлы по факту наследуются от базового, название файла == страница

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_secret_key'
# model = Model("model.onnx")


@app.route('/', methods=['GET'])
def index():
    global NUMBER_OF_ITERATION
    NUMBER_OF_ITERATION = 0
    return render_template("index.html")


@app.route('/help', methods=['GET'])
def help():
    global NUMBER_OF_ITERATION
    NUMBER_OF_ITERATION = 0
    return render_template("help_with_rules.html")


@app.route('/final/<id_text>', methods=['GET'])
def final(id_text):
    global NUMBER_OF_ITERATION, CORRECT_ANWSER
    NUMBER_OF_ITERATION = 0
    if id_text == "0":
        text = "Ничья ))"
    elif id_text == "1":
        text = "Человек победил. ИИ проиграл"
    else:
        text = "ИИ выиграл. Человек нет"
    anwser = CORRECT_ANWSER[::]
    CORRECT_ANWSER = prepare_new_set()
    return render_template("anwser_model.html", text=text,
                           anwser=machine_to_russian_point(anwser),
                           image="img/for_mortal/final.png")


# тут реализация идеи сражения человека с ИИ
@app.route('/mortal_with_ai', methods=['GET', 'POST'])
def mortal_with_ai():
    global NUMBER_OF_ITERATION, empty_tiles_main_image, CORRECT_ANWSER

    if NUMBER_OF_ITERATION >= 9:
        return redirect("final/0")
    else:
        if NUMBER_OF_ITERATION == 0:
            empty_tiles_main_image = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(empty_tiles_main_image)
        del empty_tiles_main_image[0]

        image = create_image_from_empty_tiles(empty_tiles_main_image)
        image.save("static/img/for_mortal/final.png")
        image = "img/for_mortal/final.png"
        NUMBER_OF_ITERATION += 1

        ai_choose = 2  # тут я НЕ сделал model.predict
        ai_predict = [0, 1, 2, 3, 4]  # это сложно объяснить)
        anwser = 0  # 1
        if anwser == CORRECT_ANWSER:
            print("Человек победил. ИИ проиграл")
            return redirect("final/1")
        elif ai_choose == CORRECT_ANWSER:
            print("ИИ выиграл. Человек нет")
            return redirect("final/2")
    return render_template("mortal_with_ai.html", image=image)


# тестирование ИИ
@app.route('/test_ai', methods=['GET', 'POST'])
def test_ai():
    global NUMBER_OF_ITERATION
    NUMBER_OF_ITERATION = 0
    result = "//-->>-->>-->>//"
    if request.method == "POST":
        try:
            img = request.files['images[]']
            if img is not None:
                img.save(f'static/img/image.png')
            result = model.get_result(Image.open('static/image.png'))
        except Exception as e:
            print(e)

    return render_template("test_ai.html", result=result)


# иконка страницы
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    CORRECT_ANWSER = prepare_new_set()
    NUMBER_OF_ITERATION = 0
    empty_tiles_main_image = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
