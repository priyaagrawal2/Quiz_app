from app import app
from models import db, Quiz, Question

with app.app_context():
    db.create_all()

    print("Seeding database...")

    # -------------------------
    # CREATE QUIZZES
    # -------------------------
    math_quiz = Quiz.query.filter_by(title="Basic Maths").first()
    if not math_quiz:
        math_quiz = Quiz(title="Basic Maths", description="10 basic maths questions")
        db.session.add(math_quiz)

    english_quiz = Quiz.query.filter_by(title="English Tenses").first()
    if not english_quiz:
        english_quiz = Quiz(title="English Tenses", description="10 tense questions")
        db.session.add(english_quiz)

    db.session.commit()

    # -------------------------
    # REMOVE OLD QUESTIONS
    # -------------------------
    Question.query.delete()
    db.session.commit()

    # -------------------------
    # MATH QUESTIONS
    # -------------------------
    math_questions = [
        ("What is 5 + 3?", "6", "7", "8", "9", "8"),
        ("What is 10 - 4?", "5", "6", "7", "8", "6"),
        ("What is 6 × 2?", "10", "11", "12", "13", "12"),
        ("What is 15 ÷ 3?", "4", "5", "6", "7", "5"),
        ("What is 9 + 6?", "14", "15", "16", "17", "15"),
        ("What is 7 × 3?", "18", "19", "20", "21", "21"),
        ("What is 20 - 8?", "10", "11", "12", "13", "12"),
        ("What is 8 ÷ 2?", "2", "3", "4", "5", "4"),
        ("What is 11 + 9?", "18", "19", "20", "21", "20"),
        ("What is 14 - 5?", "7", "8", "9", "10", "9"),
    ]

    for q in math_questions:
        db.session.add(Question(
            quiz_id=math_quiz.id,
            question_text=q[0],
            option1=q[1],
            option2=q[2],
            option3=q[3],
            option4=q[4],
            correct_option=q[5]
        ))

    # -------------------------
    # ENGLISH QUESTIONS
    # -------------------------
    english_questions = [
        ("She ___ to school every day.", "go", "goes", "gone", "going", "goes"),
        ("They ___ playing football now.", "is", "are", "was", "be", "are"),
        ("I ___ my homework yesterday.", "do", "did", "done", "doing", "did"),
        ("He ___ already eaten food.", "has", "have", "had", "is", "has"),
        ("We ___ watching TV right now.", "is", "are", "was", "were", "are"),
        ("She ___ a letter tomorrow.", "write", "writes", "will write", "wrote", "will write"),
        ("They ___ to the market last week.", "go", "went", "gone", "going", "went"),
        ("I ___ coffee every morning.", "drink", "drinks", "drank", "drunk", "drink"),
        ("He ___ sleeping when I called.", "is", "was", "were", "be", "was"),
        ("We ___ finished our work.", "has", "have", "had", "are", "have"),
    ]

    for q in english_questions:
        db.session.add(Question(
            quiz_id=english_quiz.id,
            question_text=q[0],
            option1=q[1],
            option2=q[2],
            option3=q[3],
            option4=q[4],
            correct_option=q[5]
        ))

    db.session.commit()

    print("✅ Database seeded successfully!")