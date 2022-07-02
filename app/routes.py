import logging
from sre_constants import SUCCESS
from pkg_resources import Requirement
from app import app
from app.modules.analyzer import analyze
from app.modules.scraper import scraper
from flask import render_template, request, redirect, send_file
from os.path import exists
import os

if not os.path.exists("opinions"):
    os.makedirs("opinions")

@app.route('/')
def index():
    text = "With this site you can extract and view results here. \nSite will extract all opinions and calculate total score, number of positive and negative reviews.\nAll this operations made by a special scraper with can extract data via Ceneo web site. Talking about analyzing, it is another special module which can calculate a special data with modules (ex. pandas, matplotlib, numpy).\n\n"
    if not exists("requirements.txt"):
            open("requirements.txt", "w").close()
    with open(f"requirements.txt", "r") as f:
        requirements = f.readlines()
        f.close()
    return render_template('index.html', text=text, requirements=requirements)

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'GET':
        return render_template('extract.html')
    if request.method == 'POST':
        try:
            id = request.form['id']
            if type(id) == str and int(id)>=1:
                scraper(id)
                return render_template('extract.html', success=1)
            else:
                return render_template('extract.html', data="Please enter valid id", success=0)
        except Exception as e:
            data = "Something went wrong. Please check the ID and try again."
            print(e)
            return render_template('extract.html', data=data, success=0)

    
@app.route('/products')
def products():
    filenames = []
    for filename in os.listdir("./opinions/"):
            if filename.endswith(".json"):
                try:
                    filenames.append(analyze(filename.split(".")[0]))
                    filenames.append(filename)
                except:
                    data = {
                'id': filename.split(".")[0],
                'n': 0,
                'p': 0,
                'c': 0,
                'a': 0
                    }
                    filenames.append(data)
    return render_template('products.html', filenames=filenames)

@app.route('/author')
def author():
    name = 'Danylo Kolisnichenko (221733)'
    field = 'Applied Informatics'
    mail = 's221733@student.uek.krakow.pl'
    univ = 'Cracow University of Economics'
    return render_template('author.html', name=name, field=field, mail=mail, univ=univ)

@app.route('/products/<id>/json')
def downloadJSON (id):
    path = f"../opinions/{id}.json"
    return send_file(path, as_attachment=True)

@app.route('/products/<id>/csv')
def downloadCSV (id):
    import pandas as pd
    with open(f"opinions/{id}.json", "r") as f:
        data = pd.read_json(f)
        data.to_csv(f"opinions/{id}.csv", encoding='utf-8', index=True)
    return send_file(f"../opinions/{id}.csv", as_attachment=True)

@app.route('/products/<id>/xlsx')
def downloadXLSX (id):
    import pandas as pd
    with open(f"opinions/{id}.json", "r") as f:
        data = pd.read_json(f)
        path = f"opinions/{id}.xlsx"
        data.to_excel(path)
    return send_file(f"../opinions/{id}.xlsx", as_attachment=True)
