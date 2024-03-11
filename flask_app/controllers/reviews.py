from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.review import Review

@app.route('/review/<int:id>')
def show_review(id):
    if 'id' not in session:
        return redirect('/')
    review = Review.get_id(id)
    user_id = {'id':session['id']}
    return render_template('review_show_one.html', review = review, user = User.get_id(user_id))

@app.route('/review/new')
def new_review():
    if 'id' not in session:
        return redirect('/')
    id = {'id': session['id']}
    return render_template('write_review.html', user = User.get_id(id))

@app.route('/review/create', methods=['POST'])
def generate_review():
    if not Review.validate_diner(request.form):
        return redirect('/review/new')
    Review.new_review(request.form)
    return redirect('/')
    if Review.new_review(request.form):
        return redirect('/')
    return redirect('/review/new')

@app.route('/review/edit/<int:id>')
def edit_review(id):
    if 'id' not in session:
        return redirect('/')
    user = Review.get_id(id)
    if user.user_id == session['id']:
        session['review_id'] = id
        user_id = {'id':session['id']}
        return render_template('edit_review.html', review = Review.get_id(id), user = user_id)
    else:
        return redirect('/')
    
@app.route('/review/update', methods=['POST'])
def update_review():
    if not Review.validate_review(request.form):
        return redirect(f'/review/edit/{session["review_id"]}')
    Review.edit_review(request.form)
    return redirect('/')
    if Review.edit_review(request.form):
        return redirect('/')
    return redirect(f'/review/edit/{session["review_id"]}')

@app.route('/review/delete/<int:id>')
def delete_review(id):
    if 'id' not in session:
        return redirect('/')
    review = Review.get_id(id)
    if review.user_id != session['id']:
        return redirect('/')
    Review.delete_review(id)
    return redirect('/')