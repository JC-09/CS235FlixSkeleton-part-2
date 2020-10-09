from flask import Blueprint, render_template

import CS235Flix.utilities.utilities as utilities
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from CS235Flix.movies.movies import SearchForm, SearchByTitleForm


home_blueprint = Blueprint(
    'home_bp', __name__
)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        form=SearchForm(),
        handler_url=url_for('movies_bp.search'),
        title_form = SearchByTitleForm(),
        handler_url_title = url_for('movies_bp.search_by_title')
    )

