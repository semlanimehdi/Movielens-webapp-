from flask import Flask, render_template , request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, BIGINT, CHAR ,VARCHAR, ForeignKey 
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy import text
from sqlalchemy import Index 
from sqlalchemy import distinct
from sqlalchemy import and_
from sqlalchemy import create_engine, inspect 
from sqlalchemy.dialects.mysql import VARCHAR, LONGTEXT




Base = declarative_base()

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__,template_folder='template')
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Mehdi11061997@localhost/movielens"

# initialize the app with the extension
db.init_app(app)

 #Connect to the database
engine = create_engine("mysql://root:Mehdi11061997@localhost/movielens")
 #import tables
class movies(db.Model):
    __tablename__ = 'movies'
    movieId = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(String(50))

class newtable(db.Model):
    __tablename__ = 'newtable'

    movieId = db.Column(db.Integer, primary_key=True)
    avg_rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer)


class newtable2(db.Model):
    __tablename__ = 'newtable2'
    title = db.Column(VARCHAR(255))
    userId = db.Column(LONGTEXT)
    rating = db.Column(Float)
    idd=db.Column(Integer, primary_key=True)


class links(db.Model):
    __tablename__ = 'links'
    linkid= Column(Integer,primary_key=True)
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    tmdbId = Column(Integer)
    imdbId = Column(CHAR(9))

class ratings(db.Model):
    __tablename__ = 'ratings'
    userId = Column(Integer)
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    rating = Column(Float)
    timestamp = Column(BIGINT)
    id = Column(VARCHAR(100),primary_key=True)


movie = relationship("movies", back_populates="ratings")


#NO-USED TABLES   
"""

class genome_tags(db.Model):
    __tablename__ = 'genome_tags'
    tagId = Column(Integer, ForeignKey('genome_scores.tagId'))
    tag = Column(VARCHAR(255))

class genome_scores(db.Model):
    __tablename__ = 'genome_scores'
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    tagId = Column(Integer,primary_key=True)
    relevence = Column(Float)

class tags(db.Model):
    __tablename__ = 'tags'
    tagid= Column(Integer,primary_key=True)
    userId = Column(Integer)
    movieId = Column(Integer, ForeignKey('movies.movieId'))
    tag = Column(VARCHAR(255))
    timestamp = Column(BIGINT)
    """



###############################
#creating new table2 (newtable2=each movie with all users)
'''
def create_newtable2():
    with app.app_context():
            db.create_all()
            insert_query = text(
                "SELECT  movies.title, GROUP_CONCAT(DISTINCT ratings.userId) AS users , ratings.rating FROM movies JOIN ratings ON movies.movieId = ratings.movieId GROUP BY  movies.movieId, ratings.rating HAVING COUNT(DISTINCT ratings.userId) > 10")
            engine.execute(insert_query)
create_newtable2() 
'''
#creating new table2 (newtable= each movie with avg rating and count )

''' 

def create_newtable():
    with app.app_context():
            db.create_all()
            insert_query = text(
                "SELECT movieId, AVG(rating), COUNT(rating) FROM ratings GROUP BY movieId")
            engine.execute(insert_query)
create_newtable()  
'''
###############################
 # Create a session to the database
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/', methods=['GET'])
def view_movies():
    # Query the database for all movies
    data =session.query(movies).all()
    #data=movies.query.all()
    return render_template('index.html',data=data)


@app.route('/search', methods=['GET', 'POST'])
def search():
   
    query = request.form.get('search')
    results = session.query(movies).filter(movies.title.like('%' + query + '%')).all()

    return render_template('search.html',results=results, query=query)


###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
#ROUTE FOR ALL GENRES (I USED TABLE BUTON )
@app.route('/action', methods=['GET', 'POST'])
def action():
    
    action=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'action' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('action.html',action=action)

@app.route('/adventure', methods=['GET', 'POST'])
def adventure():
    
    adventure=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'adventure' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('adventure.html',adventure=adventure)

@app.route('/animation', methods=['GET', 'POST'])
def animation():
    
    animation=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'animation' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('animation.html',animation=animation)

@app.route('/children', methods=['GET', 'POST'])
def children():
    children=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'children' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('children.html',children=children)

@app.route('/comedy', methods=['GET', 'POST'])
def comedy():
    comedy=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'comedy' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('comedy.html',comedy=comedy)

@app.route('/crime', methods=['GET', 'POST'])
def crime():
    crime=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'crime' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('crime.html',crime=crime)

@app.route('/documentary', methods=['GET', 'POST'])
def documentary():
    documentary=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'documentary' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('documentary.html',documentary=documentary)

@app.route('/drama', methods=['GET', 'POST'])
def drama():
    drama=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'drama' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('drama.html',drama=drama)

@app.route('/fantasy', methods=['GET', 'POST'])
def fantasy():
    fantasy=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'fantasy' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('fantasy.html',fantasy=fantasy)


@app.route('/filmnoir', methods=['GET', 'POST'])
def filmnoir():
    filmnoir=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'filmnoir' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('filmnoir.html',filmnoir=filmnoir)

@app.route('/horror', methods=['GET', 'POST'])
def horror():
    horror=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'horror' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('horror.html',horror=horror)

@app.route('/musical', methods=['GET', 'POST'])
def musical():
    musical=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'musical' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('musical.html',musical=musical)

@app.route('/mystery', methods=['GET', 'POST'])
def mystery():
    mystery=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'mystery' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('mystery.html',mystery=mystery)

@app.route('/romance', methods=['GET', 'POST'])
def romance():
    romance=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'romance' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('romance.html',romance=romance)

@app.route('/scifi', methods=['GET', 'POST'])
def scifi():
    scifi=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'scifi' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('scifi.html',scifi=scifi)

@app.route('/thriller', methods=['GET', 'POST'])
def thriller():
    thriller=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'thriller' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('thriller.html',thriller=thriller)


@app.route('/war', methods=['GET', 'POST'])
def war():
    war=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'war' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('war.html',war=war)

@app.route('/western', methods=['GET', 'POST'])
def western():
    western=db.session.query(movies.movieId, movies.title, movies.genres, newtable.avg_rating,
                                            newtable.rating_count) \
                .join(newtable, movies.movieId == newtable.movieId) \
                .filter(movies.genres.like('%' + 'western' + '%')) \
                .order_by(newtable.rating_count.desc(), newtable.avg_rating.desc()) \
                .limit(20)
    return render_template('western.html',western=western)
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
@app.route('/users', methods=['GET', 'POST'])
def users():
    users =db.session.query(newtable2).all()
    return render_template('users.html', users=users)


@app.route('/allusers', methods=['GET', 'POST'])
def allusers():
    quer = request.form.get('user')
    allusers = session.query(newtable2).filter(newtable2.title.like('%' + quer + '%')).all()
    return render_template('allusers.html', allusers=allusers)

if __name__ == '__main__':
    app.run(debug=True)



'''
# Query the database for all movies
mo = session.query(ratings).all()
movie_id = mo[0].rating

# Print the titles of all the movies
print(movie_id)
    

# Close the session
session.close()
'''
