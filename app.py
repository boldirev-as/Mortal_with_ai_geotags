import os

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_secret_key'


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/mortal_with_ai', methods=['GET', 'POST'])
def mortal_with_ai():
    global game_started, empty_tiles_main_image
    game_started = True
    if len(empty_tiles_main_image) == 0:
        game_started = False
    else:
        pass
    return render_template("mortal_with_ai.html")


@app.route('/test_ai', methods=['GET', 'POST'])
def test_ai():
    return render_template("mortal_with_ai.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    game_started = False
    empty_tiles_main_image = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    port = int(os.environ.get("PORT", 5000))
    app.run(host="localhost", port=port)
