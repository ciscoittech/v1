from flask import render_template, request, redirect, url_for, session
from app.models.quiz_models import Question, Exam, Subsection
from app.models.user_models import User, UserExam, Result
from app.forms.quiz_forms import QuestionForm
from bson import ObjectId
import random
from app import app



@app.route('/exam')
def exam():
    # Fetching all vendors and exams for display
    # vendors = Vendor.objects.all()
    exams = Exam.objects.all()
    return render_template('home/exam1.html', exams=exams)



@app.route('/start_exam/<exam_id>', methods=['GET', 'POST'])
def start_exam(exam_id):
    user = User.objects.get(id=session['user_id'])  # Assuming you have a user_id stored in session
    exam = Exam.objects.get(id=exam_id)

    user_exam = UserExam.objects(user=user, exam=exam).first()
    if not user_exam:
        user_exam = UserExam(user=user, exam=exam)
        user_exam.save()

    # If the selected_questions list isn't in the session, create it
    if 'selected_questions' not in session:
        all_questions = [question.id for subsection in Subsection.objects(exam=exam_id) for question in subsection.questions]
        session['selected_questions'] = random.sample([str(q_id) for q_id in all_questions], 3)

    # Initialize current_question_number in session if not present
    if 'current_question_number' not in session:
        session['current_question_number'] = 1

    # If user has finished the last question, redirect to results
    if session['current_question_number'] > len(session['selected_questions']):
        # You might want to reset or remove the session variables here if the user starts over
        # del session['selected_questions']
        # del session['current_question_number']
        return redirect(url_for('exam_results', exam_id=exam_id))

    # Get the current question based on the session's counter
    current_question_id = ObjectId(session['selected_questions'][session['current_question_number'] - 1])
    current_question = Question.objects.get(id=current_question_id)

    # Initialize the form with the choices from the current question
    form = QuestionForm()
    form.choices.choices = [(key, value) for key, value in current_question.choices.items()]

    # If form is submitted
    if form.validate_on_submit():
        # Process the submitted answer (store it, evaluate it, etc.)
        selected_answer = form.choices.data

        
          # Check the answer 
        if selected_answer == current_question.correct_answer:
            result = Result(user_exam=user_exam, question=current_question, selected_answer=selected_answer, time_taken="placeholder", is_correct=True)
            result.save()
        else:
            result = Result(user_exam=user_exam, question=current_question, selected_answer=selected_answer, time_taken="placeholder", is_correct=False)
            result.save()

        # Then, move to next question or end exam based on the button pressed
        if form.submit_next.data:
            session['current_question_number'] += 1
            return redirect(url_for('start_exam', exam_id=exam_id))
        elif form.submit_end.data:
            # Handle the end of the exam logic
            # You might want to reset or remove the session variables here if the user starts over
            # del session['selected_questions']
            # del session['current_question_number']
            return redirect(url_for('exam_results', exam_id=exam_id))

    return render_template('home/start_exam.html', exam=exam, current_question=current_question, form=form)


@app.route('/exam_results/<exam_id>')
def exam_results(exam_id):
    # Fetching the results for the user's last attempt (assuming there's a user session or similar)
    # Note: You'll likely want to link the results to a user and fetch accordingly.
    results = Result.objects.all()  # Fetching all for simplicity; modify this to fit your user-exam session structure

    # Prepare results in a format suitable for rendering
    results_for_rendering = [
        {
            "question_content": result.question.content,
            "is_correct": result.is_correct,
            "user": result.user_exam.user 
        }
        for result in results
    ]

    return render_template('home/exam_results.html', results=results_for_rendering)







@app.route('/product')
def product():
    # Fetching all vendors and exams for display

    return render_template('home/product.html')
