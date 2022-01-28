from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def show_survey():
    """this function display the start of the survey"""

    session["survey_answers"] = []

    return render_template("survey_start.html",
                           title=survey.title,
                           instruction=survey.instructions)


@app.post('/begin')
def survey_start():
    """redirects to beginning of questions in survey"""

    return redirect('/question/0')


@app.get('/question/<int:question_number>')
def show_question(question_number):
    """displays question in survey based on question_number, 
    handling redirects if finished or not current question"""

    # is the user manually accessing question
    # redirect if survey finished
    if len(session["survey_answers"]) == len(survey.questions):
        flash("Survey completed!")
        return redirect("/completion")

    # is the user manually acessing question
    # redirect to current question
    if len(session["survey_answers"]) != question_number:
        #breakpoint()
        flash("Questions must be answer in order!")
        return redirect(f"/question/{len(session['survey_answers'])}")

    return render_template('question.html',
                           question=survey.questions[question_number],
                           question_number=question_number
                           )


@app.post('/answer')
def submit_answer():
    """this function extract question number and answer from request body,
    append answer to the response list and 
    redirect to the next question or completion page
    """

    question_number = request.form.get('question_number')
    question_number = int(question_number) + 1
    # print(question_number)
    # breakpoint()
    # survey_answers.append(request.form.get("answer"))
    #session["survey_answers"].append(request.form.get("answer"))
    answers = session["survey_answers"]
    answers.append(request.form.get("answer"))
    session["survey_answers"] = answers
    #breakpoint()

    # this is to test whether or not the survey has been completed
    # are we done in the correct way?
    if len(survey.questions) > question_number:
        return redirect(f'/question/{question_number}')
    else:
        return redirect('/completion')


@app.get('/completion')
def thank_user():
    """this function display html completion page"""

    # breakpoint()
    return render_template('completion.html')
