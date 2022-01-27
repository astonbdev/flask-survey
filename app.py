from dis import Instruction
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

response = []


@app.get('/')
def show_survey():

    return render_template("survey_start.html",
     title=survey.title,
     instruction=survey.instructions)

@app.post('/begin')
def show_question():

    return render_template('question.html', question = survey.questions[0])

