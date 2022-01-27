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
    """this function display the start of the survey"""

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

    return render_template('question.html', question=survey.questions[question_number])


@app.post('/answer')
def submit_answer():
    """this function extract question number from referrer URL,
    append answer to the response list and 
    redirect to the next question or completion page
    """

    question_number = request.referrer.partition('question/')[2]
    question_number = int(question_number) + 1
    # print(question_number)
    # breakpoint()
    response.append(request.form.get("answer"))

    if len(survey.questions) > question_number:
        return redirect(f'/question/{question_number}')
    else:
        return redirect('/completion')


@app.get('/completion')
def thank_user():
    """this function display html completion page"""

    # breakpoint()
    return render_template('completion.html')
