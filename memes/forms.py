from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class Template(FlaskForm):
    image = FileField('Upload Template image: ', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'], 'Image Only.')])
    name = StringField('Template Name: ', validators=[DataRequired()])
    submit = SubmitField('Add Template')
