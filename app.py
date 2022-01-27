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
def survey_start():
    """redirects to beginning of questions in survey"""
    return redirect('/question/0')

@app.get('/question/<int:question_number>')
def show_question(question_number):
    """displays question in survey based on question_number"""

    return render_template('question.html', question = survey.questions[question_number])


@app.post('/answer')
def submit_answer():
    question_number = request.referrer.partition('question/')[2]
    question_number = int(question_number) + 1
    # print(question_number)
    # breakpoint()
    response.append(request.args.get("answer"))

    return redirect(f'/question/{question_number}')

