from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email,Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class QuizForm(FlaskForm):
    title = StringField("Quiz Title", validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Create Quiz")

class QuestionForm(FlaskForm):
    question_text = StringField("Question", validators=[DataRequired()])
    option1 = StringField("Option 1", validators=[DataRequired()])
    option2 = StringField("Option 2", validators=[DataRequired()])
    option3 = StringField("Option 3", validators=[DataRequired()])
    option4 = StringField("Option 4", validators=[DataRequired()])

    correct_option = RadioField(
        "Correct Answer",
        choices=[
            ("1", "Option 1"),
            ("2", "Option 2"),
            ("3", "Option 3"),
            ("4", "Option 4"),
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Add Question")