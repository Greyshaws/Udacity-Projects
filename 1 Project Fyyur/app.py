#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
from psycopg2 import _psycopg
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

   data = []

   locations = Venue.query.all()

   global location

   for location in locations:
         unique_area = []

         data.append({
     'city' : location.city,
     'state' : location.state,
     'venues' : unique_area
   })

         areas = Venue.query.filter_by(state=location.state, city=location.city).all()

         for area in areas:
               num_upcoming_shows = 0
               shows = Show.query.filter_by(venue_id = area.id).all()

               for show in shows:
                     if show.start_time > datetime.now():
                           num_upcoming_shows = num_upcoming_shows + 1
                           
                           unique_area.append({
                             'id': area.id,
                             'name': area.name,
                             'num_upcoming_shows': len(num_upcoming_shows)
                            })
       

   return render_template("pages/venues.html", locations=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():

 search_term = request.form.get("search_term", "")
 results = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
 data = []

 global result

 for result in results:
       num_upcoming_shows = Show.query.filter(Show.venue_id == result.id).filter(Show.start_time > datetime.now()).all()

       data.append({
    'id' : result.id,
    'name' : result.name,
    'num_upcoming_shows' : len(num_upcoming_shows)
  })

 response = {
   'venues': data,
   'count' : len(results)
 }

 return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  location = Venue.query.filter_by(Venue.id==venue_id).first()
  shows = Show.query.filter(venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
  upcoming_shows = []
  past_shows = []

  for show in shows:
        if show.start_time > datetime.now():
              upcoming_shows.append(data)
        else:
              past_shows.append(data)
        data = {
          'artist_id': show.artist_id,
          'artist_name': db.session.query(Artist).filter_by(id=show.artist_id).first().name,
          'artist_image_link': db.session.query(Artist).filter_by(id=show.artist_id).first().image_link,
          'start_time': format_datetime(str(show.start_time))
        }
  

  data={
    "id": location.id,
    "name": location.name,
    "genres": location.genres,
    "address": location.address,
    "city": location.city,
    "state": location.state,
    "phone": location.phone,
    "website_link": location.website_link,
    "facebook_link": location.facebook_link,
    "seeking_talent": location.seeking_talent,
    "seeking_description": location.seeking_talent,
    "image_link": location.seeking_description,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  } 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

 try:
    data = request.form

    name = data['name']
    city = data['city']
    state = data['state']
    phone = data['phone']
    genres = data['genres']
    image_link = data['image_link']
    facebook_link = data['facebook_link']
    website_link = data['website_link']
    seeking_talent = data['seeking_venue']
    seeking_description = data['seeking_description']

    venue = Venue(name=name, 
                  city=city, 
                  state=state, 
                  phone=phone, 
                  genres=genres, 
                  image_link=image_link, 
                  facebook_link=facebook_link,
                  website_link=website_link, 
                  seeking_talent=seeking_talent, 
                  seeking_description=seeking_description)
    
    db.session.add(venue)
    db.session.commit()
    flash('Venue' + data['name'] + 'was successfully listed!')
 except:
    db.session.rollback()
    flash('An error occurred. Venue ' + data['name'] + ' could not be listed.')
 finally: 
    db.session.close()
 return render_template('pages/home.html')
  
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    location = Venue.query.get(venue_id)
    location_name = location.name

    db.session.delete(location)
    db.session.commit()

    flash('Venue ' + location_name + ' was deleted')
  except:
    flash(' an error occurred and Venue ' + location_name + ' could not be deleted')
    db.session.rollback()
  finally:
    db.session.close()

  return jsonify({'success': True})

@app.route('/artists')
def artists():
      
  data = []

  artists = Artist.query.all()

  for artist in artists:
        upcoming_shows = Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).all()

        data.append({
     'id': artist.id,
     'name': artist.name,
     'num_upcoming_shows': len(upcoming_shows)
   })     

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

 search_term = request.form.get("search_term", "")
 results = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
 data = []

 global result

 for result in results:
       num_upcoming_shows = Show.query.filter(Show.artist_id == result.id).filter(Show.start_time > datetime.now()).all()

       data.append({
    'id' : result.id,
    'name' : result.name,
    'num_upcoming_shows' : len(num_upcoming_shows)
  })

       response = {
   'venues': data,
   'count' : len(results)
 }
 
 return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.filter_by(artist.id==artist_id).first()
  shows = Show.query.filter(artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
  upcoming_shows = []
  past_shows = []

  for show in shows:
        if show.start_time > datetime.now():
              upcoming_shows.append(data)
        else:
              past_shows.append(data)
        data = {
          'artist_id': show.venue_id,
          'artist_name': db.session.query(Venue).filter_by(id=show.venue_id).first().name,
          'artist_image_link': db.session.query(Venue).filter_by(id=show.venue_id).first().image_link,
          'start_time': format_datetime(str(show.start_time))
        }
  

  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "address": artist.address,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website_link": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_talent": artist.seeking_talent,
    "seeking_description": artist.seeking_talent,
    "image_link": artist.seeking_description,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  } 
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
      
  form = ArtistForm()
  
  artist = Artist.query.filter(Artist.id == artist_id).first()
 
  result = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "address": artist.address,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website_link": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_talent": artist.seeking_talent,
    "seeking_description": artist.seeking_talent,
    "image_link": artist.image_link,
  }
  return render_template('forms/edit_artist.html', form=form, artist=result)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  try:
    form = ArtistForm()

    artist = Artist.query.filter(Artist.id == artist_id).first()

    artist.name = form.name.data
    artist.genres = form.genres.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('Artist' + request.form['name'] + 'was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  finally: 
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  venue = Venue.query.filter(Venue.id == venue_id).first()
  
  result = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website_link": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_talent,
    "image_link": venue.image_link,
  }
  return render_template('forms/edit_venue.html', form=form, venue=result)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  try:
    form = VenueForm()

    venue = Venue.query.filter(Venue.id == venue_id).first()

    venue.name = form.name.data
    venue.genres = form.genres.data
    venue.address = form.address.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('Venue' + request.form['name'] + 'was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  finally: 
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  try:
    data = request.form

    name = data['name']
    city = data['city']
    state = data['state']
    phone = data['phone']
    genres = data['genres']
    image_link = data['image_link']
    facebook_link = data['facebook_link']
    website_link = data['website_link']
    seeking_venue = data['seeking_venue']
    seeking_description = data['seeking_description']

    artist = Artist(name=name, 
                  city=city, 
                  state=state, 
                  phone=phone, 
                  genres=genres, 
                  image_link=image_link, 
                  facebook_link=facebook_link,
                  website_link=website_link, 
                  seeking_venue=seeking_venue, 
                  seeking_description=seeking_description)
    
    db.session.add(artist)
    db.session.commit()
    flash('Artist' + data['name'] + 'was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + data['name'] + ' could not be listed.')
  finally: 
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  data = []
  shows = db.session.query(Show).join(Artist).join(Venue).all()

  for show in shows:
        data.append({
          'venue_id': show.venue_id,
          'venue_name': show.venue.name,
          'artist_id': show.artist_id,
          'artist_name': show.artist.name,
          'artist_image_link': show.artist.image_link,
          'start_time': format_datetime(str(show.start_time))
        })
 
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    data = request.form

    artist_id = data['artist_id']
    venue_id = data['venue_id']
    start_time = data['start_time']

    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error ocurred. Show could not be listed.')
  finally:
    db.session.close()

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
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
