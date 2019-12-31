from flask_wtf import FlaskForm
from wtforms.fields import HiddenField
from wtforms.fields import StringField
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired


class SummaryForm(FlaskForm):
    scan = SubmitField('Re-Scan')
    continue_ = SubmitField('Continue')


class FontOcrForm(FlaskForm):
    code = HiddenField('Code', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')
