# -*- coding: utf-8 -*-

import random

from PIL import Image
import os

# тут я тестирую алгоритм сражения с ИИ
height = 600
coords = [(0, 0), (0, 200), (0, 400),
          (200, 0), (200, 200), (200, 400),
          (400, 0), (400, 200), (400, 400)]


def prepare_new_set():
    listdir = os.listdir("static/img/for_mortal/set/")
    file = random.choice(listdir)
    filename = f"static/img/for_mortal/set/{file}"
    with open("train.csv", mode="r") as f:
        for line in f.readlines():
            if file in line:
                label = line.strip("\n").split(",")[1]
                break
    img = Image.open(filename).resize((600, 600))
    step = 200
    i = 0
    for x in range(0, height, step):
        for y in range(0, height, step):
            puzzle = img.crop((x, y, x + step, y + step))
            puzzle.save(f"static/img/for_mortal/marked/{i}.png")
            i += 1
    return label


def machine_to_russian_point(name):
    with open("definitions.csv", mode="r", encoding="windows-1251") as f:
        for line in f.readlines():
            file, machine_name, russian_name = line.strip("\n").split(",")
            if name == machine_name:
                return russian_name


def russian_to_machine_point(name):
    with open("definitions.csv", mode="r") as f:
        for line in f.readlines():
            file, machine_name, russian_name = line.strip("\n").split(",")
            if name == russian_name:
                return machine_name


def create_image_from_empty_tiles(empty_tiles):
    main_img = Image.new("RGB", (height, height), (255, 255, 255))
    not_empty_tiles = [x for x in range(9) if x not in empty_tiles]
    for i in not_empty_tiles:
        main_img.paste(Image.open(f"static/img/for_mortal/marked/{i}.png"), coords[i])
    return main_img


def prepare_ten_positions(label):
    all_labels = list()
    with open("definitions.csv", mode="r") as file:
        for line in file.readlines():
            name, label, russian_label = line.strip("\n").split(",")
            all_labels.append(russian_label)
    all_labels = [random.choice(all_labels) for _ in range(10)]
    all_labels.append(machine_to_russian_point(label))
    random.shuffle(all_labels)
    print(machine_to_russian_point(label))
    return all_labels.index(machine_to_russian_point(label)), all_labels


if __name__ == '__main__':
    prepare_new_set()
    # create_image_from_empty_tiles([1, 2, 5, 6, 8]).show()

    empty_tiles_main_image = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    for _ in range(8):
        random.shuffle(empty_tiles_main_image)
        del empty_tiles_main_image[0]
        main_img_for_test_ai = create_image_from_empty_tiles(empty_tiles_main_image)
        main_img_for_test_ai.show()
        ai_choose = 2  # тут я НЕ сделал model.predict
        ai_predict = [0, 1, 2, 3, 4]  # это сложно объяснить)
        anwser = int(input(f"--> {ai_predict}"))  # 1
        correct_anwser = 1
        if anwser == correct_anwser == ai_choose:
            print("Ничья")
            break
        elif anwser == correct_anwser:
            print("Человек победил. ИИ проиграл")
            break
        elif ai_choose == correct_anwser:
            print("ИИ выиграл. Человек нет")
            break
        elif len(empty_tiles_main_image) == 0:
            print("Ничья")
