from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import user
from flask_app.models import review

@app.route('/reviews/<int:id>')
def show_review(id):
    if 'id' not in session: return redirect('/')
    this_review = review.Review.get_review_by_id(id)
    return render_template('review_show_one.html', review = this_review)

@app.route('/reviews/new')
def new_review():
    if 'id' not in session: return redirect('/')
    id = session['id']
    return render_template('write_review.html', user = user.User.get_id(id))
    # why is a user being returned to the review form page

@app.route('/reviews/create', methods=['POST'])
def generate_review():
    if review.Review.new_review(request.form):
        return redirect('/users/home')
    return redirect('/reviews/new')

@app.route('/reviews/edit/<int:id>', methods=['GET', 'POST'])
def edit_review(id):
    if 'id' not in session: return redirect('/')
    if request.method == "GET":
        this_review = review.Review.get_review_by_id(id)
        return render_template('edit_review.html', review = this_review)
    if request.method == "POST":
        if review.Review.edit_review(request.form):
            return redirect('/users/home')
        return redirect(f'/reviews/edit/{id}')

@app.route('/reviews/update', methods=['POST'])
def update_review():
    if review.Review.edit_review(request.form):
        return redirect('/users/home')
    return redirect(f'/reviews/edit/{session["review_id"]}')

@app.route('/reviews/delete/<int:id>')
def delete_review(id):
    if 'id' not in session: return redirect('/')
    this_review = review.Review.get_review_by_id(id)
    if this_review.user_id != session['id']:
        return redirect('/reviews/{id}')
    review.Review.delete_review(id)
    return redirect(f'/users/{session["id"]}/reviews')
