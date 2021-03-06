#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from forms import *
from flask_wtf import Form
from logging import Formatter, FileHandler
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import babel
import dateutil.parser
import json
from flask_migrate import Migrate
import datetime
#from posix import abort
from enum import Enum
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case
from models import *

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    """Formats the date
    Args:
        date value and format type needed
    Returns:
        The formatted date
    """
    date = value
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    """Returns:
        The home page"""
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
    """
    Shows venues
    Returns:
        a page that contains a list of all venues"""
    #data = Area.query.all()

    areas = []

    for ven in Venue.query.distinct(Venue.city):

        city = ven.city
        venues = Venue.query.filter_by(
            city=ven.city).all()
        state = ven.state

        areas.append({
            'city': city,
            'venues': venues,
            'state': state
        })

    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """
    Shows search results.

    Returns:
        the page of search results of venues
    """

    term = request.form.get('search_term', '')
    q = Venue.query.filter(Venue.name.ilike(f'%{term}%'))
    result = q.all()
    result_count = q.count()

    response = {
        "count": result_count,
        "data": result
    }

    return render_template('pages/search_venues.html', results=response, search_term=term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
    Shows venue information

    Args:
        venue id

    Returns:
        a page that shows details of a venue based on its ID
    """

    data = Venue.query.get(venue_id)

    # shows = {
    #     "upcoming_shows": Show.query.filter(Show.venue_id == venue_id).filter(
    #         Show.start_time >= func.current_date()).all(),
    #     "past_shows": Show.query.filter(Show.venue_id == venue_id).filter(
    #         Show.start_time < func.current_date()).all(),

    #     "past_shows_count": db.session.execute(
    #         db.session
    #         .query(Show)
    #         .filter(Show.venue_id == venue_id).filter(
    #             Show.start_time < func.current_date())
    #         .statement.with_only_columns([func.count()])
    #     ).scalar(),

    #     "upcoming_shows_count": db.session.execute(
    #         db.session
    #         .query(Show)
    #         .filter(Show.venue_id == venue_id).filter(
    #             Show.start_time >= func.current_date())
    #         .statement.with_only_columns([func.count()])
    #     ).scalar()
    # }

    return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create')
def create_venue_form():
    """
    Create a new venue in the databse
    Returns:
        a page that contains a form to create a new venue"""
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """Redirects to home page and returns the result of adding a new venue"""

    error = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form['genres']
        facebook_link = request.form['facebook_link']

        nVenue = Venue(name=name, city=city, state=state, address=address,
                       phone=phone, genres=genres, facebook_link=facebook_link)

        db.session.add(nVenue)

        db.session.commit()

        # addArea = Area.query.filter_by(city=city, state=state).first()
        # if not addArea:
        #     try:
        #         nArea = Area(city=city, state=state)
        #         db.session.add(nArea)
        #         db.session.commit()
        #         try:
        #             nVenue.area = nArea.id
        #             db.session.commit()
        #         except:
        #             db.session.rollback()
        #             error = True
        #     except:
        #         db.session.rollback()
        #         error = True
        # else:
        #     try:
        #         nVenue.area = addArea.id
        #         db.session.commit()
        #     except:
        #         db.session.rollback()
        #         error = True

    except Exception as e:
        print(e)
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')

# https://stackoverflow.com/questions/64423601/form-delete-method-in-flask-sqlalchemy-not-working


@app.route('/venues/<int:venue_id>', methods=['POST'])
def delete_venue(venue_id):
    """

    Returns:
        the result of deleting a venue
    Args:
        venue id
    """
    # Used POST instead of delete because browser doesn't support DELETE method
    error = False
    try:
        ven = Venue.query.get(venue_id)
        db.session.delete(ven)
        db.session.commit()

    except Exception as e:
        print(e)
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if not error:
            flash('Venue was successfully deleted!')
            return render_template('pages/home.html')
        else:
            flash('An error occurred. Venue ' +
                  request.form['name'] + ' could not be deleted.')
        return None

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    """
    Shows all artists in database
    Returns:
        a page that contains a list of all artists
    """
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():

    term = request.form.get('search_term', '')
    q = Artist.query.filter(Artist.name.like(f'%{term}%'))
    result = q.all()
    count = q.count()

    response = {
        "count": count,
        "data": result
    }
    return render_template('pages/search_artists.html', results=response, search_term=term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """
    Shows information of the artist

    Returns:
        a page that contains details of an artist based on his ID.

    Args:
        artist id
    """
    data = Artist.query.get(artist_id)

    # shows = {
    #     "upcoming_shows": Show.query.filter(Show.artist_id == artist_id).filter(
    #         Show.start_time >= func.current_date()).all(),
    #     "past_shows": Show.query.filter(Show.artist_id == artist_id).filter(
    #         Show.start_time < func.current_date()).all(),

    #     "past_shows_count": db.session.execute(
    #         db.session
    #         .query(Show)
    #         .filter(Show.artist_id == artist_id).filter(
    #             Show.start_time < func.current_date())
    #         .statement.with_only_columns([func.count()])
    #     ).scalar(),

    #     "upcoming_shows_count": db.session.execute(
    #         db.session
    #         .query(Show)
    #         .filter(Show.artist_id == artist_id).filter(
    #             Show.start_time >= func.current_date())
    #         .statement.with_only_columns([func.count()])
    #     ).scalar()
    # }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """
    Form of editing artist.

    Returns:
        a page that contains a form to edit an artist.
    Args:
        Artist id"""
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    """
    edit artist info in database.
    Returns:
        Redirects to artist page returning the result of editing his details.
    Args:
        artist id
    """
    error = False
    try:

        nArtist = Artist.query.get(artist_id)

        nArtist.name = request.form['name']
        nArtist.city = request.form['city']
        nArtist.state = request.form['state']
        nArtist.phone = request.form['phone']
        nArtist.genres = request.form['genres']
        nArtist.facebook_link = request.form['facebook_link']

        db.session.commit()

    except Exception as e:
        print(e)
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Artist ' + request.form['name'] +
              ' was successfully edited!')
    else:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be edited.')

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """
    Editing a venue information

    Returns:
        a page that contains a form to edit a venue
    Args:
        Venue id"""
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """
    editing a venue
    Returns:
        a message of the result of a editing a venue on venue page.
    Args:
        Venue id"""

    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    error = False
    try:

        nVenue = Venue.query.get(venue_id)

        nVenue.name = request.form['name']
        nVenue.city = request.form['city']
        nVenue.state = request.form['state']
        nVenue.address = request.form['address']
        nVenue.phone = request.form['phone']
        nVenue.genres = request.form['genres']
        nVenue.facebook_link = request.form['facebook_link']

        db.session.commit()

    except Exception as e:
        print(e)
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Venue ' + request.form['name'] +
              ' was successfully edited!')
    else:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be edited.')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    """
    form of editing artist
    Returns:
        a page that contains a form to create a new artist record"""
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """
    creates a new artist

    Returns: 
        Redirects to home page showing the result of adding a new artist"""

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success

    error = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        genres = request.form['genres']
        facebook_link = request.form['facebook_link']

        nArtist = Artist(name=name, city=city, state=state,
                         phone=phone, genres=genres, facebook_link=facebook_link)

        db.session.add(nArtist)

        db.session.commit()

    except Exception as e:
        print(e)
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    """
    Showing the list of all shows in database

    Returns:
        a page that contains a list of all shows"""
    data = Show.query.all()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    """
    A form to createa show

    Returns:
        a page that contains a form to create a new show record"""

    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    """
    Adds a new show in the databse
    Returns:
        Redirects to home page showing the result of adding the new show"""

    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success

    error = False
    try:
        artist_id = request.form['artist_id']
        start_time = request.form['start_time']
        venue_id = request.form['venue_id']

        nShow = Show(artist_id=artist_id,
                     start_time=start_time, venue_id=venue_id)

        db.session.add(nShow)

        db.session.commit()

    except Exception as e:
        print(e)
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        flash('Show was successfully listed!')
    else:
        flash('Show could not be listed.')

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
