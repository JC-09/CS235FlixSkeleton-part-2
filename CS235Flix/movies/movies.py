# CS235Flix/movies/movies.py

from datetime import date
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import CS235Flix.adapters.repository as repo
import CS235Flix.utilities as utilities
import CS235Flix.movies.services as services

from CS235Flix.authentication.authentication import login_required

# Configure Blueprint
movies_blueprint = Blueprint(
    'movies_bp', __name__
)

@movies_blueprint.route('/movies_by_release_year', methods=['GET'])
def movies_by_release_year():
    # Read query parameters
    target_year = request.args.get('year')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the latest and the oldest movies in the series.
    latest_movie = services.get_latest_movie(repo.repo_instance)
    oldest_movie = services.get_oldest_movie(repo.repo_instance)

    if target_year is None:
        # No year query parameter, so return movies from the latest release year of the series
        target_year = latest_movie['release_year']
    else:
        # Convert target_year from string to int
        target_year = int(target_year)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int
        movie_to_show_reviews = int(movie_to_show_reviews)

    # Fetch movie(s) from the target year. This call also returns the previous and next release year for movies
    # immediately before and after the target year
    movies, previous_year, next_year = services.get_movies_by_release_year(target_year, repo.repo_instance)

    latest_movie_url = None
    oldest_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        # There is at least one movie for the target release year.
        if previous_year is not None:
            # There are movies on a previous year, so generate URLs for the 'previous' and 'oldest' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_release_year', year=int(previous_year))
            oldest_movie_url = url_for('movies_bp.movies_by_release_year', year=int(oldest_movie['release_year']))

        # There are movies on a newer year, so generate URLs for the 'next' and 'latest' navigation buttons.
        if next_year is not None:
            next_movie_url = url_for('movies_bp.movies_by_release_year', year=int(next_year))
            latest_movie_url = url_for('movies_bp.movies_by_release_year', year=int(latest_movie['release_year']))

        # Construct urls for viewing movie reviews and adding reviews
        for movie in movies:
            movie['view_review_for'] = url_for('movies_bp.movies_by_release_year', year=target_year, view_reviews_for=movie['id'])
            movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

        # Generate the webpage to display the article
        return render_template(
            'movies/movies.html',
            title='Movies',
            movies_title=target_year,
            movies=movies,
            selected_movies=utilities.get_selected_movies(len(movies) * 2),
            genre_urls=utilities.get_genres_and_urls(),
            latest_movie_url=latest_movie_url,
            oldest_movie_url=oldest_movie_url,
            next_movie_url=next_movie_url,
            prev_movie_url=prev_movie_url,
            show_reviews_for_movie=movie_to_show_reviews
        )

    # No movies to show, so return the homepage
    return redirect(url_for('home_bp.home'))



@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 10

    # Read query parameter.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent article id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int
        movie_to_show_reviews = int(movie_to_show_reviews)


    if cursor is None:
        # None cursor query parameter, so initialise cursor to start the begining
        cursor = 0
    else:
        # Convert cursor from string to int
        cursor = int(cursor)

    # Retrieve movie ids for movies that are classified with genre_name
    movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)

    # Retrieve the batch of articles to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)


    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and last navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', tag=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids)/movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', tag=genre_name, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor, view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

    # Generate the webpage to display the movies
    return render_template(
        'movies/movies.html',
        title='Movies',
        movie_title='Movies classified as ' + genre_name,
        movies=movies,
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        next_movie_url=next_movie_url,
        prev_movie_url=prev_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )



@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an movie id, when subsequently called with a HTTP POST request, the movie id remains in the form

    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the movie id, representing the reviewed movie, from the form.
        movie_id = int(form.movie_id.data)
        rating = int(form.rating)

        # Use the service layer to store the new review
        services.add_review(form.review.data, username, movie_id, rating, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)
        genre_name = movie['genres'][0]

        # Cause the web browser to display the page of all movies that have the same genre as the reviewed movie, and
        # display all reviews, including the new review.
        return redirect(url_for('movies_bp.movies_by_genre', genre=genre_name))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page include a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'movies/review_on_movie',
        title='Edit movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_on_movie'),
        selected_movies=utilities.get_selected_movies(),
        genre_url=utilities.get_genres_and_urls()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = TextAreaField('Please rate the movie at 1 to 10', [
        DataRequired()])
    movie_id = HiddenField("Article id")
    submit = SubmitField('Submit')




