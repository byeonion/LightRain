from datetime import datetime
import hashlib
from flask import current_app, request, url_for
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
    
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    title = db.Column(db.String(64), index=True)
    author = db.Column(db.String(64), index=True)
    avatar_hash = db.Column(db.String(32))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    style = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('lists.id'))
    
    @staticmethod
    def generate_fake(count=30):
        from random import seed, randint
        import forgery_py
        
        seed()
        for i in range(count):
            a = Article(email=forgery_py.internet.email_address(),
                        title= forgery_py.lorem_ipsum.title(),
                        author=forgery_py.lorem_ipsum.word(),
                        body=forgery_py.lorem_ipsum.sentences(randint(40, 90)),
                        timestamp=forgery_py.date.date(True),
                        style=randint(1, 5))
            db.session.add(a)
            db.session.commit()
            
        
    def __init__(self, **kwargs):
        super(Article, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
        if self.list is None:
            self.list = List.query.first()
                      
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash #or hashlib.md5(
            #self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
            
    def __repr__(self):
        return '<Article %r>' %self.list
        
        
class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    listname = db.Column(db.String(64), index=True)
    articles = db.relationship('Article', backref='list', lazy='dynamic')
    
    @staticmethod
    def generate():
        a = List(listname='科技')
        b = List(listname='财经')
        c = List(listname='体育')
        db.session.add(a)
        db.session.add(b)
        db.session.add(c)
        db.session.commit()
        
    def __repr__(self):
        return '<List: %r>' %self.listname
    
    
    
            
            