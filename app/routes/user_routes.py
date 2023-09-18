from flask import render_template, redirect, url_for, flash, request, url_for
from flask_login import current_user,login_required
from app.forms.user_forms import UpdateProfileForm
from app import app



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        # Add code to handle profile picture upload
        current_user.save()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('home/profile.html', title='Profile', form=form)
