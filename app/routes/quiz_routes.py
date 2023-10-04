from datetime import datetime
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


def reset_exam_session():
    """Resets or removes session variables related to the exam."""
    session.pop('selected_questions', None)
    session.pop('current_question_number', None)

def end_exam(user_exam):
    """Handles the end of the exam logic."""
    correct_answers = Result.objects(user_exam=user_exam, is_correct=True).count()
    total_questions = len(session['selected_questions'])
    score = (correct_answers / total_questions) * 100
    user_exam.score = score
    user_exam.finished_at = datetime.utcnow()
    user_exam.save()

@app.route('/start_exam/<exam_id>', methods=['GET', 'POST'])
def start_exam(exam_id):
    user = User.objects.get(id=session['user_id'])
    exam = Exam.objects.get(id=exam_id)

    user_exam = UserExam.objects(user=user, exam=exam).first()
    if not user_exam:
        user_exam = UserExam(user=user, exam=exam)
        user_exam.save()

    if 'selected_questions' not in session:
        all_questions = [question.id for subsection in Subsection.objects(exam=exam) for question in subsection.questions]
        session['selected_questions'] = random.sample([str(q_id) for q_id in all_questions], 3)

    if 'current_question_number' not in session:
        session['current_question_number'] = 1

    if session['current_question_number'] > len(session['selected_questions']):
        reset_exam_session()
        return redirect(url_for('exam_results', exam_id=exam_id))

    current_question_id = ObjectId(session['selected_questions'][session['current_question_number'] - 1])
    current_question = Question.objects.get(id=current_question_id)

    form = QuestionForm()
    form.choices.choices = [(key, value) for key, value in current_question.choices.items()]

    if form.validate_on_submit():
        submitted_at = datetime.utcnow()
        selected_answer = form.choices.data
        is_correct = selected_answer == current_question.correct_answer
        
        
        result = Result(
            user_exam=user_exam,
            question=current_question,
            selected_answer=selected_answer,
            time_taken='unknown',  # Convert time_taken to string to match the field type
            is_correct=is_correct,
            submitted_at=submitted_at
        )
        result.save()

        if form.submit_next.data:
            session['current_question_number'] += 1
            # Record the time the next question is presented
            session['question_start_time'] = datetime.utcnow()
            return redirect(url_for('start_exam', exam_id=exam_id))
        elif form.submit_end.data:
            end_exam(user_exam)
            reset_exam_session()
            return redirect(url_for('exam_results', exam_id=exam_id))
        

    return render_template('home/start_exam.html', exam=exam, current_question=current_question, form=form)



@app.route('/exam_results/<exam_id>')
def exam_results(exam_id):
    # Fetch the latest UserExam for the current user and specific exam_id
    user_exam_latest = UserExam.objects(user=session['user_id'], exam=exam_id).order_by('-timestamp').first()

    # If no matching UserExam is found, handle the error appropriately (redirect, show an error message, etc.)
    if not user_exam_latest:
        return redirect(url_for('some_error_route'))

    # Fetch the results for this specific UserExam
    results = Result.objects(user_exam=user_exam_latest)

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
