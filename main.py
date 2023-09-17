from flask import Flask, request
import requests
from faker import Faker

app = Flask(__name__)
fake = Faker()


@app.route('/requirements')
def requirements_display():
    try:
        with open('requirements.txt', 'r', encoding='utf-16le') as file:
            res = file.read()
        return res
    except FileNotFoundError:
        return 'No file with such name!'


@app.route('/users/generate')
def generate_fake_info():
    count = request.args.get('count', default=101)
    try:
        count = int(count)
        if int(count) < 1:
            return 'Enter positive number!'
    except ValueError:
        return 'Enter correct number!'
    info = list()
    for i in range(1, count + 1):
        name = 'Name: ' + fake.name()
        mail = 'Email: ' + fake.ascii_email()
        info.append(f'{i}. {name}, {mail}')
    return info


@app.route('/mean/')
def mid_height_weight():
    with open('hw.csv', 'r') as file:
        lines = file.read().split('\n')[1:-2:]
        weight_list = list()
        height_list = list()
        for i in lines:
            line = i.split(',')
            weight = float(line[2])
            height = float(line[1])
            height_list.append(height)
            weight_list.append(weight)
    return f'Middle height: {(sum(height_list) / len(height_list)) * 2.54} centimeters,\n' \
           f'Middle weight: {(sum(weight_list) / len(weight_list)) * 0.45} kilogram'


@app.route('/space/')
def num_astro():
    res = requests.get('http://api.open-notify.org/astros.json')
    if res.status_code == 200:
        data = res.json()
        number_of_astro = data.get('number')
        if number_of_astro is not None:
            return f'There are {number_of_astro} astronauts'


if __name__ == '__main__':
    app.run()
