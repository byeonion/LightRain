from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import Required, Length
from wtforms import ValidationError
from ..models import User, List, Article


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('确认')
    

class ArticleEditForm(FlaskForm):
    title = StringField('编辑标题', validators=[Required(), Length(1, 128)])
    body = TextAreaField('编辑文章')
    list = SelectField('所属目录', coerce=int)
    submit = SubmitField('确定')
    
    def __init__(self, *args, **kwargs):
        super(ArticleEditForm, self).__init__(*args, **kwargs)
        self.list.choices = [(list.id, list.listname)
                             for list in List.query.order_by(List.listname).all()]
    
    
class PostForm(FlaskForm):
    title = StringField('标题', validators=[Required(), Length(1, 128)])
    body = TextAreaField('文章')
    list = SelectField('所属目录', coerce=int)
    submit = SubmitField('发表')
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.list.choices = [(list.id, list.listname)
                             for list in List.query.order_by(List.listname).all()]
    

class ListForm(FlaskForm):
    name = StringField('目录名称', validators=[Required(), Length(1, 128)])
    submit = SubmitField('确定')
    