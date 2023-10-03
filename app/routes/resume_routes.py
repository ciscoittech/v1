# app/routes/resume_routes.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from app import app
from app.forms.resume_forms import ResumeUploadForm
# from app.models.resume_models import Resume

# @app.route('/upload_resume', methods=['GET', 'POST'])
# def upload_resume():
#     form = ResumeUploadForm()
    
#     if form.validate_on_submit():
#         # Save the original resume
#         resume = Resume(user=current_user._get_current_object())
#         form.resume.data.save('path_to_save_original_resumes')  # adjust the path
#         resume.original_resume.put(form.resume.data)
#         resume.job_link = form.job_link.data
        
#         # TODO: Here, integrate with GPT to transform the resume based on the job link
        
#         # Save the transformed resume
#         # Assuming `transformed_data` is the file-like object from GPT
#         resume.transformed_resume.put(transformed_data)

#         resume.save()
        
#         flash('Resume processed successfully!', 'success')
#         return redirect(url_for('show_transformed_resume', resume_id=resume.id))
        
#     return render_template('resume/upload_resume.html', form=form)

# @app.route('/show_transformed_resume/<string:resume_id>')
# def show_transformed_resume(resume_id):
#     resume = Resume.objects.get(id=resume_id)
#     # Send the resume data to the frontend
#     return render_template('resume/show_transformed.html', resume=resume)

@app.route('/resume_new', methods=['GET', 'POST'])
def resume_new():
    form = ResumeUploadForm()
  
      
        
    return render_template('resume/new_resume.html', form=form)