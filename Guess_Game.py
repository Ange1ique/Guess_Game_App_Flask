import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models import Animals
import json


# global variables for "recursive" function
animalsOriginal = {}
animals = {}
rememberAnswer = ""


@app.route('/', methods=["GET", "POST"])
def index():
    global animalsOriginal
    global animals
    global rememberAnswer
    if request.method == "POST":
        if request.form['action'] == "start":
            return render_template('startvraag.html')
        elif request.form['action'] == "check":
            # code for offline game and offline storage
            # with open("animals.json", "r", encoding="utf-8") as f:
            #     animalsOriginal = json.load(f)
            #     f.close()
            animalsData = Animals.query.filter_by(id=1).first()
            animalsOriginal = animalsData.json_animals
            animals = animalsOriginal
            question = animals.get('A')
            return render_template('game.html', question = question)
        elif request.form['action'] == "cancel":
            return render_template('start.html')
        elif request.form['action'] == "ja":
            if isinstance(animals.get('B'), dict):
                animals = animals.get('B')
                question = animals.get('A')
                return render_template('game.html', question = question)
            else:
                final_question = "Is het dier een " + animals.get('B') + "?"
                rememberAnswer = 'B'
                return render_template('finale.html', final_question = final_question)
        elif request.form['action'] == "nee":
            if isinstance(animals.get('C'), dict):
                animals = animals.get('C')
                question = animals.get('A')
                return render_template('game.html', question = question)
            else:
                final_question = "Is het dier een " + animals.get('C') + "?"
                rememberAnswer = 'C'
                return render_template('finale.html', final_question = final_question)
        elif request.form['action'] == "goed":
            return render_template('geraden.html')
        elif request.form['action'] == "fout":
            return render_template('nieuw.html')
        elif request.form['action'] == "correct":
            new_animal = request.form["new_animal"]
            new_animal = new_animal.lower()
            new_question = request.form["new_question"]
            new_question = new_question.lower().capitalize()
            if not new_question.endswith("?"):
                new_question = new_question + "?"
            return render_template('check.html',
                                    new_animal=new_animal,
                                    new_question=new_question)
        elif request.form['action'] == "opslaan":
            animal = request.form["animal"]
            new_animal = request.form["new_animal"]
            question = request.form["question"]
            new_question = request.form["new_question"]
            if animal != "" and animal != new_animal:
                new_animal = animal
            if question != "" and question != new_question:
                new_question = question
            wrong_animal = animals.get(rememberAnswer)
            animals[rememberAnswer] = {'A': new_question, 'B': new_animal, 'C': wrong_animal}
            # code for offline game and offline storage
            # with open('animals.json', 'w', encoding='utf-8') as f:
            #     json.dump(animalsOriginal, f, ensure_ascii=False, indent=4)
            #     f.close()
            # try:
                # animalsUpdated=Animals(
                #     id=0,
                #     json_animals=animalsOriginal
                # )
            animalUpdate = Animals.query.get(1)
            animalUpdate.json_animals = animalsOriginal
            db.session.commit()
            # json_animals=animalsOriginal
            # test=Animals(
            #     json_animals=json_animals
            # )
            # db.session.add(test)
            # db.session.commit()
            return render_template('opgeslagen.html')
            # except:
            #     print("shit")
            #     return render_template('start.html')
    else:
        return render_template('start.html')

if __name__ == '__main__':
    app.run()
