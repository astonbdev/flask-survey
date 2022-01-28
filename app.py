from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
# global variable for string name for session
answer_keyname = 'survey_answers'

SURVEY = []


@app.get('/')
def show_survey():
    """this function display the start of the survey"""
    

    return render_template("survey_select.html",
                           surveys = surveys)


@app.post('/begin')
def survey_start():
    """redirects to beginning of questions in survey"""
    #breakpoint()
    survey_code = request.form["survey_id"]
    #breakpoint()
    #This is an interesting bit, look here: https://stackoverflow.com/questions/929777/why-does-assigning-to-my-global-variables-not-work-in-python
    global SURVEY
    SURVEY = surveys[survey_code]

    print("SURVEY:", SURVEY)
    print(SURVEY.title)
    print(SURVEY.instructions)

    session[answer_keyname] = []
    return redirect('/question/0')


@app.get('/question/<int:question_number>')
def show_question(question_number):
    """displays question in survey based on question_number, 
    handling redirects if finished or not current question"""
    #print(SURVEY.title)
    #breakpoint()

    # is the user manually accessing question
    # redirect if survey finished
    if len(session[answer_keyname]) == len(SURVEY.questions):
        flash("Survey completed!")
        return redirect("/completion")

    # is the user manually acessing question
    # redirect to current question
    if len(session[answer_keyname]) != question_number:
        #breakpoint()
        flash("Questions must be answer in order!")
        return redirect(f"/question/{len(session[answer_keyname])}")

    return render_template('question.html',
                           question=SURVEY.questions[question_number],
                           question_number=question_number
                           )


@app.post('/answer')
def submit_answer():
    """this function extract question number and answer from request body,
    append answer to the response list and 
    redirect to the next question or completion page
    """

    question_number = request.form['question_number']
    question_number = int(question_number) + 1
    # print(question_number)
    # breakpoint()
    #answer_keyname append(request.form.get("answer"))
    #session[answer_keyname].append(request.form.get("answer"))
    answers = session[answer_keyname]
    answers.append(request.form.get("answer"))
    session[answer_keyname] = answers
    #breakpoint()

    # this is to test whether or not the survey has been completed
    # are we done in the correct way?
    if len(SURVEY.questions) > question_number:
        return redirect(f'/question/{question_number}')
    else:
        return redirect('/completion')


@app.get('/completion')
def thank_user():
    """this function display html completion page"""

    # breakpoint()
    return render_template('completion.html')
