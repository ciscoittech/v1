from flask import render_template
from app.models.quiz_models import Vendor, Exam, Subsection, Question
from app import app



@app.route('/exam')
def exam():
    # Fetching all vendors and exams for display
    vendors = Vendor.objects.all()
    return render_template('home/exam.html', vendors=vendors)


@app.route('/exam/<string:exam_id>')
def exam_details(exam_id):
    exam = Exam.objects.get(id=exam_id)
    subsections = exam.subsections
    return render_template('home/exam_detail.html', exam=exam, subsections=subsections)



@app.route('/dummy')
def insert_dummy_data():
    # Delete all previous data (for repeated runs)
    Vendor.objects.delete()
    Exam.objects.delete()
    Subsection.objects.delete()
    Question.objects.delete()

    # Create a vendor
    cisco = Vendor(name="Cisco").save()

    # Create exams for Cisco
    ccna = Exam(vendor=cisco, title="CCNA", description="Cisco Certified Network Associate").save()
    ccnp = Exam(vendor=cisco, title="CCNP", description="Cisco Certified Network Professional").save()

    # Add exams to Cisco vendor's list and save
    cisco.exams.append(ccna)
    cisco.exams.append(ccnp)
    cisco.save()

    # Add a subsection to CCNA
    subnetting = Subsection(exam=ccna, title="Subnetting", description="Learn about IP subnetting").save()
    
    # Add questions to subnetting subsection
    q1 = Question(subsection=subnetting, content="What is subnetting?").save()
    q2 = Question(subsection=subnetting, content="How do you calculate subnets?").save()

    print("Dummy data inserted!")
    return"Dummy data inserted!"

