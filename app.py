from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, Quiz, Question, Attempt
from forms import RegisterForm, LoginForm, QuizForm, QuestionForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid username or password")

    return render_template("login.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    quizzes = Quiz.query.all()
    return render_template("dashboard.html", quizzes=quizzes)

# -----------------------
# CREATE QUIZ (ADMIN/USER)
# -----------------------
@app.route("/create_quiz", methods=["GET","POST"])
@login_required
def create_quiz():
    form = QuizForm()

    if form.validate_on_submit():
        quiz = Quiz(
            title=form.title.data,
            description=form.description.data,
            created_by=current_user.id
        )

        db.session.add(quiz)
        db.session.commit()

        flash("Quiz created. Now add questions.")
        return redirect(url_for("add_question", quiz_id=quiz.id))

    return render_template("create_quiz.html", form=form)

# -----------------------
# ADD QUESTIONS (MAX 10)
# -----------------------
@app.route("/add_question/<int:quiz_id>", methods=["GET","POST"])
@login_required
def add_question(quiz_id):
    form = QuestionForm()

    count = Question.query.filter_by(quiz_id=quiz_id).count()

    if count >= 10:
        flash("Maximum 10 questions allowed.")
        return redirect(url_for("dashboard"))

    if form.validate_on_submit():
        question = Question(
            quiz_id=quiz_id,
            question_text=form.question_text.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            correct_option=form.correct_option.data
        )

        db.session.add(question)
        db.session.commit()

        flash(f"Question {count+1} added")

        return redirect(url_for("add_question", quiz_id=quiz_id))

    return render_template("add_question.html", form=form)

# -----------------------
# TAKE QUIZ
# -----------------------
@app.route("/take_quiz/<int:quiz_id>", methods=["GET","POST"])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # fetch max 10 questions
    questions = Question.query.filter_by(quiz_id=quiz_id).limit(10).all()

    if not questions:
        flash("No questions available for this quiz.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        score = 0

        for q in questions:
            selected = request.form.get(str(q.id))
            if selected == q.correct_option:
                score += 1

        # save attempt
        attempt = Attempt(
            user_id=current_user.id,
            quiz_id=quiz_id,
            score=score
        )
        print("FORM DATA:", request.form)

        db.session.add(attempt)
        db.session.commit()


        return render_template("result.html", score=score, total=len(questions))

    return render_template("take_quiz.html", quiz=quiz, questions=questions)

# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# -----------------------
# RUN APP
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
