from datetime import datetime
import hashlib
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_sqlalchemy import get_debug_queries
from . import main
from ..import db
from flask_login import login_user, login_required, logout_user,current_user
from ..models import Article, User, List
from .forms import LoginForm, ArticleEditForm, PostForm, ListForm


@main.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'main.' \
            and request.endpoint != 'static':
        count = Article.query.count()
        return redirect(url_for('main.index'))
        

@main.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    count = Article.query.count()
    return render_template('index.html')        
        

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['LIGHTRAIN_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response
    
    
@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=current_app.config['LIGHTRAIN_POSTS_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    count = Article.query.count()
    return render_template('index.html', articles=articles, pagination=pagination, count=count)


# @main.route('/list', methods=['GET', 'POST'])
# def list():
    # list1 = Article.query.filter_by(style=1).order_by(Article.timestamp.desc()).all()
    # list2 = Article.query.filter_by(style=2).order_by(Article.timestamp.desc()).all()
    # list3 = Article.query.filter_by(style=3).order_by(Article.timestamp.desc()).all()
    # list4 = Article.query.filter_by(style=4).order_by(Article.timestamp.desc()).all()
    # list5 = Article.query.filter_by(style=5).order_by(Article.timestamp.desc()).all()
    
    # return render_template('list.html', list1=list1, list2=list2, list3=list3, list4=list4, list5=list5)
    

    
@main.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', id=article.id, article=article)
    
    
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is not None and form.password.data == 'cat':
            login_user(user, False)
            return redirect(url_for('main.edit'))
        flash('无效的认证')
    return render_template('login.html', form=form)
    

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出.')
    return redirect(url_for('main.index'))    
    
    
@main.route('/', methods=['GET', 'POST'])
@login_required
def edit():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=current_app.config['LIGHTRAIN_POSTS_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    count = Article.query.count()
    return render_template('index.html', articles=articles, pagination=pagination, count=count)
    
    
@main.route('/article_del/<int:id>', methods=['GET', 'POST'])
@login_required
def article_del(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('已删除')
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=current_app.config['LIGHTRAIN_POSTS_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    count = Article.query.count()
    return render_template('index.html',  articles=articles, pagination=pagination, count=count)
    
    
@main.route('/article_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def article_edit(id):
    article = Article.query.get_or_404(id)
    form = ArticleEditForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.body = form.body.data
        article.list = List.query.get(form.list.data)
        article.timestamp = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
            page, per_page=current_app.config['LIGHTRAIN_POSTS_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        count = Article.query.count()
        return render_template('index.html',  articles=articles, pagination=pagination, count=count)
    form.title.data = article.title
    form.body.data = article.body
    return render_template('article_edit.html', form=form)
    
    
@main.route('/article_add', methods=['GET', 'POST'])
@login_required
def article_add():
    form = PostForm()
    from random import randint
    import forgery_py
    if form.validate_on_submit():
        article = Article(title=form.title.data,
                          body=form.body.data,
                          email=forgery_py.internet.email_address(),
                          author=forgery_py.lorem_ipsum.word(),
                          list = List.query.get(form.list.data),
                          style=randint(1, 5))
        
        db.session.add(article)
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
            page, per_page=current_app.config['LIGHTRAIN_POSTS_PER_PAGE'],
            error_out=False)
        articles = pagination.items
        count = Article.query.count()
        return render_template('index.html',  articles=articles, pagination=pagination, count=count)
    return render_template('article_add.html', form=form)
    
    
@main.route('/lists', methods=['GET', 'POST'])
def lists():
    lists = List.query.order_by(List.id).all()
    count = List.query.count()
    return render_template('lists.html', lists=lists, count=count)
    
    
@main.route('/list/<int:id>', methods=['GET', 'POST'])
def list(id):
    list = List.query.get_or_404(id)
    articles = Article.query.filter_by(list=list).all()
    count = Article.query.count()
    return render_template('list.html', list=list, id=list.id, articles=articles, count=count)
    

@main.route('/list_del/<int:id>', methods=['GET', 'POST'])
@login_required
def list_del(id):
    list = List.query.get_or_404(id)
    db.session.delete(list)
    db.session.commit()
    flash('已删除')
    lists = List.query.order_by(List.id).all()
    count = List.query.count()
    return render_template('lists.html',  lists=lists, count=count)


@main.route('/list_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def list_edit(id):
    list = List.query.get_or_404(id)
    form = ListForm()
    if form.validate_on_submit():
        list.listname = form.name.data
        db.session.add(list)
        db.session.commit()
        lists = List.query.order_by(List.id).all()
        count = List.query.count()
        return render_template('lists.html',  lists=lists, count=count)
    form.name.data = list.listname
    return render_template('list_edit.html', form=form)
    
    
@main.route('/list_add', methods=['GET', 'POST'])
@login_required
def list_add():
    form = ListForm()
    if form.validate_on_submit():
        list = List(listname=form.name.data)
        db.session.add(list)
        db.session.commit()
        lists = List.query.order_by(List.id).all()
        count = List.query.count()
        return render_template('lists.html',  lists=lists, count=count)
    return render_template('list_add.html', form=form)


    

    
    
    
    