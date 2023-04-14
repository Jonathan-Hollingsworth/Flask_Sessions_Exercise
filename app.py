from surveys import Question, Survey, surveys
from flask import Flask, request, redirect, render_template, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This makes flash work'

survey  = surveys["satisfaction"]

@app.route('/')
def home_page():
    "displays the homepage"

    return render_template('home.html', title=survey.title, instructions=survey.instructions)

@app.route('/begin', methods=['POST'])
def init_survey():
    "Initializes the survey"

    session['responses'] = []

    return redirect('/questions/0')

@app.route('/questions/<int:number>')
def display_question(number):
    'displays the current question'
    responses = session['responses']
    answer_count = len(responses)

    if answer_count == len(survey.questions):
        return redirect('/thanks')
    
    if number > answer_count:
        flash("Do not try to access invalid questions!")
        return redirect(f'/questions/{answer_count}')
    
    question_data = survey.questions[answer_count]
    question = question_data.question
    allow_text = question_data.allow_text
    choices = question_data.choices
    return render_template('question.html', question=question, choices=choices, text=allow_text, number=number)

@app.route('/answer', methods=['POST'])
def handle_answer():
    'Adds answer to responses and then redirects'
    answer = list(request.form.keys())
    if len(answer) == 1:
        answer = answer[0]
    
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    answer_count = len(responses)

    return redirect(f'/questions/{answer_count}')

@app.route('/thanks')
def thank_user():
    "thanks the user for completing the survey"

    return render_template('thanks.html')