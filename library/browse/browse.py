from flask import Blueprint, render_template,request,url_for,session,redirect
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField,HiddenField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

from library.browse import service
import library.adapters.repository as repo
from library.authentication.authentication import login_required
from library.forms.sharedForms import *

browse_blueprint = Blueprint(
    'browse_bp', __name__)

#empty route?
@browse_blueprint.route('/', methods=['GET'])
def browse():
    search= searchForm()
    # display book in batch
    previous_url = None
    next_url = None 
    currentPos = request.args.get('pos')
    currentPos = 0 if currentPos == None else int(currentPos)
    
    bulkSize = 5

    if currentPos == None or currentPos == 0 :
        # no more previous book
        previousPos = 0
        #disable url to previous batch
       

    elif  currentPos <=bulkSize:
        # there is previous book, but smaller than bulksize number of book to display
        previousPos = 0
        previous_url = url_for('browse_bp.browse', pos = 0)
    else:
        previousPos = currentPos - bulkSize
        previous_url = url_for('browse_bp.browse', pos = previousPos)
  
    newPos,nextBatch,books = service.get_book_bulk(currentPos,bulkSize,repo.repo_instance)

    if nextBatch:
        next_url = url_for('browse_bp.browse', pos = newPos)
  

    info = [[b.cover_url,url_for('browse_bp.viewBook',id = b.book_id, show = False)] for b in books]
    data = request.args.get('date')


    return render_template(
        'browse/browse.html',
        info= info,
        prev_batch_url = previous_url,
        next_batch_url = next_url,
        sidebarSearchForm = search

    )

@browse_blueprint.route('/viewBook', methods=['GET'])
def viewBook():

    search= searchForm()
    bookID = int(request.args.get('id'))

    show = False if request.args.get('show') == "False" else True


    # get book object
    book = service.get_book_by_id(bookID,repo.repo_instance)
    imageUrl = book.cover_url
    # the link is for a default image, do not show cover image if its a default 
    if imageUrl == "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png":
        imageUrl = None
    reviews = service.get_reviews_for_book(bookID, repo.repo_instance)
    if reviews is None:
        reviews = []

    return render_template(
        'browse/viewBook.html',
        reviews = reviews,
        show =  show,
        book = book,
        showReviewUrl = url_for('browse_bp.viewBook',id = bookID, show = True),
        newCommentUrl = url_for('browse_bp.addComment',id = bookID),
        sidebarSearchForm = search
    )


@browse_blueprint.route('/addComment', methods=['GET', 'POST'])
@login_required
def addComment():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']
    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an book id, when subsequently called with a HTTP POST request, the book id remains in the
    # form.
    form = reviewForm()
    search= searchForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the book id, representing the commented book, from the form.
        book_id = int(form.book_id.data)
        
       

        # Use the service layer to store the new comment.
        print("***************",type(form.rating.data))
        service.add_review(user_name, book_id, form.review.data, int(form.rating.data), repo.repo_instance)

        # Retrieve the book in dict form.
        book = service.get_book_by_id(book_id, repo.repo_instance)

        # Cause the web browser to display the page of all books that have the same date as the commented book,
        # and display all comments, including the new comment.
        return redirect(url_for('browse_bp.viewBook',id = book_id, show = True))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the book id, representing the book to comment, from a query parameter of the GET request.
        book_id = int(request.args.get('id'))
        reviews = service.get_reviews_for_book(book_id, repo.repo_instance)

        # Store the book id in the form.
        form.book_id.data = book_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the book id of the book being commented from the form.
        book_id = int(form.book_id.data)
        reviews = service.get_reviews_for_book(book_id, repo.repo_instance)

    # For a GET or an unsuccessful POST, retrieve the book to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    book = service.get_book_by_id(book_id, repo.repo_instance)
    return render_template(
        'browse/review.html',
        book=book,
        form=form,
        handler_url=url_for('browse_bp.addComment'),
        sidebarSearchForm = search

    )


class reviewForm(FlaskForm):
    review = StringField('Add a review', 
        [
            DataRequired(),
            Length(min=5, message='Your comment is too short,please have at least 5 letters')
        ])
    book_id = HiddenField("book_id")
    rating =  SelectField("Rating",choices=[1,2,3,4,5])
    submit = SubmitField('Confirm')
