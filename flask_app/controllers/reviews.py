from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import user
from flask_app.models import review

@app.route('/reviews/<int:id>')
def show_review(id):
    if 'id' not in session: return redirect('/')
    this_review = review.Review.get_id(id)
    user_id = {'id':session['id']}
    return render_template('review_show_one.html', review = this_review, user = user.User.get_id(user_id))

@app.route('/reviews/new')
def new_review():
    if 'id' not in session: return redirect('/')
    id = {'id': session['id']}
    # this is throwing a sql error, should use session['id'] in the get_id function instead
    return render_template('write_review.html', user = user.User.get_id(id))
    # why is a user being returned to the review form page

@app.route('/reviews/create', methods=['POST'])
def generate_review():
    # if not review.Review.validate_diner(request.form):
    #     return redirect('/reviews/new')
    # review.Review.new_review(request.form)
    # return redirect('/')

    # validations should be called from the model
    if review.Review.new_review(request.form):
        return redirect('/users/home') # this may need to redirect to my reviews page instead
    return redirect('/reviews/new')

@app.route('/reviews/edit/<int:id>')
def edit_review(id):
    if 'id' not in session: return redirect('/')
    user = review.Review.get_id(id)
    if user.user_id == session['id']:
        session['review_id'] = id
        user_id = {'id':session['id']}
        return render_template('edit_review.html', review = review.Review.get_id(id), user = user_id)
    # same function is being called twice here
    else:
        return redirect('/')
    
@app.route('/reviews/update', methods=['POST'])
def update_review():
    # if not review.Review.validate_review(request.form):
    #     return redirect(f'/reviews/edit/{session["review_id"]}')
    # review.Review.edit_review(request.form)
    # return redirect('/')

    # validations should be called from the model
    if review.Review.edit_review(request.form):
        return redirect('/')
    return redirect(f'/reviews/edit/{session["review_id"]}')

@app.route('/reviews/delete/<int:id>')
def delete_review(id):
    if 'id' not in session:
        return redirect('/')
    this_review = review.Review.get_id(id)
    if this_review.user_id != session['id']:
        return redirect('/')
    review.Review.delete_review(id)
    return redirect('/')