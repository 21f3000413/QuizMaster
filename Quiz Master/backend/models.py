
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


# Entity User
class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    name=db.Column(db.String,nullable=False)
    qualification=db.Column(db.String,nullable=False)
    DOB=db.Column(db.Date,nullable=False)
    role=db.Column(db.Integer,default=1)

    scores=db.relationship("Score",cascade="all,delete",backref="user",lazy="select")
    


# Entity Subject
class Subject(db.Model):
    __tablename__="subject"
    id=db.Column(db.Integer,primary_key=True)
    sub_name=db.Column(db.String,nullable=False)
    subject_code=db.Column(db.String,nullable=False,unique=True)
    description=db.Column(db.String,nullable=False)
    credits = db.Column(db.Integer, nullable=False)

    chapters=db.relationship("Chapter",cascade="all,delete",backref="subject",lazy="select")



# Entity Chapter
class Chapter(db.Model):
    __tablename__="chapter"
    id=db.Column(db.Integer,primary_key=True)
    sub_id=db.Column(db.Integer,db.ForeignKey("subject.id"),nullable=False)
    chap_name=db.Column(db.String,nullable=False)
    chap_no=db.Column(db.Integer,nullable=False)

    quizzes=db.relationship("Quiz",cascade="all,delete",backref="chapter",lazy="select")



# Entity Quiz
class Quiz(db.Model):
    __tablename__="quiz"
    id=db.Column(db.Integer,primary_key=True)
    chapter_id=db.Column(db.Integer,db.ForeignKey("chapter.id"),nullable=False)
    quiz_title=db.Column(db.String,nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    date_of_quiz=db.Column(db.Date,nullable=False)
    no_of_ques=db.Column(db.Integer,nullable=False)

    scores=db.relationship("Score",cascade="all,delete",backref="quiz",lazy="select")
    questions=db.relationship("Question",cascade="all,delete",backref="quiz",lazy="select")



# Entity Question
class Question(db.Model):
    __tablename__="question"
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
    ques_statement=db.Column(db.Text,nullable=False)
    option1 = db.Column(db.String,nullable=False)
    option2 = db.Column(db.String,nullable=False)
    option3 = db.Column(db.String,nullable=False)
    option4 = db.Column(db.String,nullable=False)
    correct_option = db.Column(db.Integer,nullable=False)

    

    
# Entity Score
class Score(db.Model):
    __tablename__="score"
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    time_stamp = db.Column(db.DateTime,nullable=False,default=func.now())
    total_score=db.Column(db.Integer,nullable=False,default=0)
    pass_fail_=db.Column(db.String,nullable=False,default="Fail")
