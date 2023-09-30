from flask import render_template
from app.models.quiz_models import Question, Result, Exam
from app import app



@app.route('/exam')
def exam():
    # Fetching all vendors and exams for display
    # vendors = Vendor.objects.all()
    exams = Exam.objects.all()
    return render_template('home/exam1.html', exams=exams)

@app.route('/product')
def product():
    # Fetching all vendors and exams for display

    return render_template('home/product.html')


@app.route('/exam/<string:exam_id>')
def exam_details(exam_id):
    exam = Exam.objects.get(id=exam_id)
    subsections = exam.subsections
    return render_template('home/exam_detail.html', exam=exam, subsections=subsections)

