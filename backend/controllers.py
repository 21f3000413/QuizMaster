from flask import render_template, request, url_for,flash, redirect, current_app as app, session
from backend.models import *
from datetime import date, datetime


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user exists with email and password
        user = User.query.filter_by(email=email, password=password).first()

        # if not user:
        #     return render_template("login.html", msg="User does not exist. Please sign up.", msg_type="danger")

        # Redirect based on role
        if user.role == 0:
            return redirect(url_for("admin_dashboard", name=email))
        elif user.role == 1:
            return redirect(url_for("user_dashboard", name=email, user_id=user.id))
        else:
            return render_template("login.html", msg="Invalid credentials. Try again.", msg_type="danger")

    return render_template("login.html", msg="", msg_type="")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        # qualification = request.form.get("qualification")
        # dob = request.form.get("dob")

        # dob = datetime.strptime(dob, "%Y-%m-%d").date()

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists! Try logging in.", "danger")  # Flash message
            return render_template("register.html")  # Redirect to clear message on reload

        new_user = User(email=email, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! You can now log in.", "success")  # Success message
        return render_template("login.html")  # Redirect to login page

    return render_template("register.html")



@app.route("/admin/<name>")
def admin_dashboard(name):
    subjects = Subject.query.all()
    return render_template("admin_dashboard.html", name=name, subjects=subjects)



@app.route("/subject/<name>", methods=["GET", "POST"])
def add_subject(name):
    if request.method == "POST":
        subject_name = request.form.get("subject_name")
        code = request.form.get("code")
        credit = request.form.get("credit")
        description = request.form.get("description")

        if not subject_name or not code or not credit or not description:
            flash("All fields are required!", "danger")
            return render_template("add_subject.html", name=name)

        # Check if the subject already exists
        # existing_subject = Subject.query.filter_by(subject_code=code).first()
        # if existing_subject:
        #     flash("A subject with this code already exists!", "warning")
        #     return render_template("add_subject.html", name=name))

        # Create a new subject entry
        new_subject = Subject(sub_name=subject_name, subject_code=code, credits=credit, description=description)
        db.session.add(new_subject)
        db.session.commit()

        flash("Subject added successfully!", "success")
        return redirect(url_for("admin_dashboard", name=name))

    return render_template("add_sub.html", name=name)



@app.route('/edit_subject/<int:subject_id>/<string:name>', methods=['GET', 'POST'])
def edit_subject(subject_id, name):
    subject = Subject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        subject.sub_name = request.form['subject_name']
        subject.subject_code = request.form['code']
        subject.credits = request.form['credit']
        subject.description = request.form['description']

        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin_dashboard', name=name))

    return render_template('edit_sub.html', subject=subject, name=name)



@app.route('/delete_subject/<int:subject_id>/<string:name>', methods=['GET'])
def delete_subject(subject_id, name):
    subject = Subject.query.get_or_404(subject_id)
    
    # # Store the subject name before deleting for the flash message
    subject_name = subject.sub_name
    
    db.session.delete(subject)
    db.session.commit()
    
    flash(f'Subject "{subject_name}" deleted successfully!', 'danger')
    return redirect(url_for('admin_dashboard', name=name))



@app.route('/add_chapter/<int:subject_id>/<string:name>', methods=['GET', 'POST'])
def add_chapter(subject_id, name):
    # Verify the subject exists
    # subject = Subject.query.get_or_404(sub_id)
    
    if request.method == 'POST':
        chapter_no = request.form.get('chapter_no')
        chapter_name = request.form.get('chapter_name')

        # Validate input
        # if not chapter_no or not chapter_name:
        #     flash("Chapter number and name are required.", "danger")
        #     return redirect(url_for('add_chapter', sub_id=sub_id, name=name))
        
        # # Check for duplicate chapter number in the subject
        # existing_chapter = Chapter.query.filter_by(
        #     sub_id=sub_id, 
        #     chap_no=chapter_no
        # ).first()
        
        # if existing_chapter:
        #     flash("A chapter with this number already exists in the subject.", "danger")
        #     return redirect(url_for('add_chapter', sub_id=sub_id, name=name))

        # Create new chapter
        new_chapter = Chapter(
            sub_id=subject_id, 
            chap_name=chapter_name, 
            chap_no=chapter_no
        )

        # try:
        db.session.add(new_chapter)
        db.session.commit()
        flash("Chapter added successfully!", "success")
        return redirect(url_for('admin_dashboard', name=name))
        # except Exception as e:
        #     db.session.rollback()
        #     flash(f"Error adding chapter: {str(e)}", "danger")
        #     return redirect(url_for('add_chapter', sub_id=sub_id, name=name))

    return render_template('add_chap.html', sub_id=subject_id, name=name)



@app.route('/edit_chapter/<int:chapter_id>/<string:name>', methods=['GET', 'POST'])
def edit_chapter(chapter_id, name):
    chapter = Chapter.query.get_or_404(chapter_id)
    sub_id = chapter.sub_id  # Get the associated subject
    chapters = Chapter.query.filter_by(sub_id=sub_id).all()
    
    if request.method == 'POST':
        new_chapter=request.form.get("chapter_name")
        chapter_no=request.form.get("chapter_no")
        chapter.chap_name=new_chapter
        chapter.chap_no=chapter_no
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
        # # Check if an existing chapter is selected
        #     chapter_no = existing_chapter.chap_no
        # else:
        #     # Use form input
        #     chapter_name = request.form['chapter_name']
        #     chapter_no = request.form['chapter_no']
        
        # # Validate input
        # if not chapter_name or not chapter_no:
        #     flash("Chapter name and number are required.", "danger")
        #     return redirect(request.url)
        
        # # Check for duplicate chapter number in the same subject
        # existing_chapter_check = Chapter.query.filter_by(
        #     sub_id=subject.id, 
        #     chap_no=chapter_no
        # ).first()
        
        # if existing_chapter_check and existing_chapter_check.id != chapter_id:
        #     flash("A chapter with this number already exists in the subject.", "danger")
        #     return redirect(request.url)
        
        # # Update chapter
        # chapter.chap_name = chapter_name
        # chapter.chap_no = chapter_no
        
        # db.session.commit()
        # flash("Chapter updated successfully!", "success")
        # return redirect(url_for('admin_dashboard', name=name))
    
    return render_template('edit_chap.html', chapter=chapter, name=name, chapters=chapters)

@app.route('/delete_chapter/<int:chapter_id>/<string:name>', methods=['GET'])
def delete_chapter(chapter_id, name):
    chapter = Chapter.query.get_or_404(chapter_id)
    
    # Store chapter details before deletion
    chapter_name = chapter.chap_name
    subject_name = chapter.subject.sub_name
    
    # try:
    db.session.delete(chapter)
    db.session.commit()
    flash(f'Chapter "{chapter_name}" from subject "{subject_name}" deleted successfully!', 'danger')
    # except Exception as e:
    # db.session.rollback()
    # flash(f"Error deleting chapter: {str(e)}", "danger")
    
    return redirect(url_for('admin_dashboard', name=name))



@app.route('/quiz_management/<string:name>')
def quiz_management(name):
    # Fetch all quizzes with their associated chapters and subjects
    quizzes = Quiz.query.join(Chapter).join(Subject).all()
    return render_template('quiz_management.html', name=name, quizzes=quizzes)



@app.route('/quiz/<string:name>', methods=['GET', 'POST'])
def add_quiz(name):
    # Fetch all chapters with their associated subjects
    chapters = Chapter.query.join(Subject).all()
    
    if request.method == 'POST':
        # Get form data
        chapter_id = request.form.get('chapter_id')
        quiz_title = request.form.get('quiz_title')
        duration = request.form.get('duration')
        date_of_quiz = request.form.get('date_of_quiz')
        total_questions = request.form.get('total_questions')

        # Validate input
        if not all([chapter_id, quiz_title, duration, date_of_quiz, total_questions]):
            flash('All fields are required!', 'danger')
            return redirect(request.url)

        # Convert date
        try:
            date_of_quiz = datetime.strptime(date_of_quiz, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format!', 'danger')
            return redirect(request.url)

        # Create new quiz
        new_quiz = Quiz(
            chapter_id=chapter_id, 
            quiz_title=quiz_title, 
            duration=int(duration), 
            date_of_quiz=date_of_quiz, 
            no_of_ques=int(total_questions)
        )

        try:
            db.session.add(new_quiz)
            db.session.commit()
            flash('Quiz added successfully!', 'success')
            return redirect(url_for('quiz_management', name=name))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding quiz: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('add_quiz.html', name=name, chapters=chapters)



@app.route('/edit_quiz/<int:quiz_id>/<string:name>', methods=['GET', 'POST'])
def edit_quiz(quiz_id, name):
    # Fetch the specific quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Fetch all chapters with their associated subjects
    chapters = Chapter.query.join(Subject).all()
    
    if request.method == 'POST':
        # Get form data
        chapter_id = request.form.get('chapter_id')
        quiz_title = request.form.get('quiz_title')
        duration = request.form.get('duration')
        date_of_quiz = request.form.get('date_of_quiz')
        total_questions = request.form.get('total_questions')

        # Validate input
        if not all([chapter_id, quiz_title, duration, date_of_quiz, total_questions]):
            flash('All fields are required!', 'danger')
            return redirect(request.url)

        # Convert date
        try:
            date_of_quiz = datetime.strptime(date_of_quiz, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format!', 'danger')
            return redirect(request.url)

        # Update quiz details
        quiz.chapter_id = chapter_id
        quiz.quiz_title = quiz_title
        quiz.duration = int(duration)
        quiz.date_of_quiz = date_of_quiz
        quiz.no_of_ques = int(total_questions)
        
        try:
            db.session.commit()
            flash('Quiz updated successfully!', 'success')
            return redirect(url_for('quiz_management', name=name))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating quiz: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('edit_quiz.html', quiz=quiz, name=name, chapters=chapters)



@app.route('/delete_quiz/<int:quiz_id>/<string:name>', methods=['GET'])
def delete_quiz(quiz_id, name):
    # Fetch the specific quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    
    try:
        # Store quiz title for flash message
        quiz_title = quiz.quiz_title
        
        # Delete the quiz
        db.session.delete(quiz)
        db.session.commit()
        
        flash(f'Quiz "{quiz_title}" deleted successfully!', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting quiz: {str(e)}', 'danger')
    
    return redirect(url_for('quiz_management', name=name))



@app.route('/add_question/<int:quiz_id>/<string:name>', methods=['GET', 'POST'])
def add_question(quiz_id, name):
    # Fetch the specific quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        # Get form data for the question
        question_statement = request.form.get('question_statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')

        # Validate input
        if not all([question_statement, option1, option2, option3, option4, correct_option]):
            flash('All fields are required!', 'danger')
            return redirect(request.url)

        # Check if we've reached the maximum number of questions for the quiz
        existing_questions = Question.query.filter_by(quiz_id=quiz_id).count()
        if existing_questions >= quiz.no_of_ques:
            flash(f'Maximum number of questions ({quiz.no_of_ques}) reached for this quiz!', 'warning')
            return redirect(url_for('quiz_management', name=name))

        # Create new question
        new_question = Question(
            quiz_id=quiz_id,
            ques_statement=question_statement,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=int(correct_option)
        )

        try:
            db.session.add(new_question)
            db.session.commit()
            flash('Question added successfully!', 'success')
            return redirect(url_for('quiz_management', name=name))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding question: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('add_question.html', quiz=quiz, name=name)

@app.route('/edit_question/<int:question_id>/<string:name>', methods=['GET', 'POST'])
def edit_question(question_id, name):
    # Fetch the specific question
    question = Question.query.get_or_404(question_id)
    
    if request.method == 'POST':
        # Get form data for the question
        question.ques_statement = request.form.get('question_statement')
        question.option1 = request.form.get('option1')
        question.option2 = request.form.get('option2')
        question.option3 = request.form.get('option3')
        question.option4 = request.form.get('option4')
        question.correct_option = request.form.get('correct_option')

        # Validate input
        if not all([question.ques_statement, question.option1, question.option2, 
                    question.option3, question.option4, question.correct_option]):
            flash('All fields are required!', 'danger')
            return redirect(request.url)

        try:
            db.session.commit()
            flash('Question updated successfully!', 'success')
            return redirect(url_for('quiz_management', name=name))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating question: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('edit_question.html', question=question, name=name)

@app.route('/delete_question/<int:question_id>/<string:name>', methods=['GET'])
def delete_question(question_id, name):
    # Fetch the specific question
    question = Question.query.get_or_404(question_id)
    
    try:
        # Store quiz details for flash message
        quiz_title = question.quiz.quiz_title
        
        # Delete the question
        db.session.delete(question)
        db.session.commit()
        
        flash(f'Question from quiz "{quiz_title}" deleted successfully!', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting question: {str(e)}', 'danger')
    
    return redirect(url_for('quiz_management', name=name))



@app.route("/admin/user_details/<name>")
def user_details(name):
    # Fetch all users from the database
    users = User.query.all()
    return render_template('user_details.html', name=name, users=users)



@app.route('/analytics/<name>')
def analytics(name):
    # Count total subjects, quizzes, users, and active quizzes
    total_subjects = Subject.query.count()
    total_quizzes = Quiz.query.count()
    total_users = User.query.filter(User.role == 1).count()  # Only count regular users, not admins
    
    # Get active quizzes (quizzes with date >= today)
    today = date.today()
    active_quizzes = Quiz.query.filter(Quiz.date_of_quiz >= today).count()
    
    # Get all subjects for the bar chart
    subjects = Subject.query.all()
    
    # Calculate the maximum number of chapters for any subject (for progress bar scaling)
    max_chapters = 1  # Default to 1 to avoid division by zero
    for subject in subjects:
        if len(subject.chapters) > max_chapters:
            max_chapters = len(subject.chapters)
    
    return render_template('analytics.html', 
                          name=name,
                          total_subjects=total_subjects,
                          total_quizzes=total_quizzes, 
                          total_users=total_users,
                          active_quizzes=active_quizzes,
                          subjects=subjects,
                          max_chapters=max_chapters)



@app.route("/search/<name>", methods=["GET", "POST"])
def search(name):
    if request.method == "POST":
        search_txt = request.form.get("search_txt")
        by_subject = search_by_subject(search_txt)
        by_quiz = search_by_quiz(search_txt)
        by_user = search_by_user(search_txt)
        if by_subject:
            return render_template("admin_dashboard.html", name=name, subjects=by_subject)
        elif by_quiz:
            return render_template("quiz_management.html", name=name, quizzes=by_quiz)
        elif by_user:
            return render_template("user_details.html", name=name, users=by_user)
        else:
            return render_template("admin_dashboard.html", name=name, msg="No matching results found.")
    return redirect(url_for("admin_dashboard", name=name))





@app.route("/user_dashboard/<name>/<int:user_id>")
def user_dashboard(name, user_id):
    # Get the current date
    date_today = date.today()
    
    # Fetch upcoming quizzes with explicit joins
    quizzes = db.session.query(Quiz)\
        .join(Chapter, Quiz.chapter_id == Chapter.id)\
        .join(Subject, Chapter.sub_id == Subject.id)\
        .filter(Quiz.date_of_quiz >= date_today)\
        .with_entities(
            Quiz.id,
            Quiz.quiz_title,
            Chapter.chap_name.label('chapter_name'),
            Quiz.date_of_quiz,
            Quiz.duration
        ).all()
    
    # Get user's previous scores with quiz details
    user_scores = db.session.query(Score)\
        .join(Quiz, Score.quiz_id == Quiz.id)\
        .filter(Score.user_id == user_id)\
        .with_entities(
            Score.total_score,
            Score.time_stamp,
            Score.pass_fail_,
            Quiz.quiz_title
        ).order_by(Score.time_stamp.desc()).limit(5).all()
    
    return render_template(
        "user_dashboard.html", 
        name=name, 
        user_id=user_id, 
        quizzes=quizzes, 
        date_today=date_today,
        user_scores=user_scores
    )



@app.route("/scores/<int:user_id>/<name>")
def user_scores(user_id, name):
    scores = Score.query.filter_by(user_id=user_id).all()
    # Assuming each score has a related quiz
    quizzes = {score.quiz_id: Quiz.query.get(score.quiz_id) for score in scores}
    return render_template('scores.html', scores=scores, quizzes=quizzes, name=name, user_id=user_id)



@app.route('/user_summary/<name>/<user_id>')
def user_summary(name, user_id):
    # Fetch user's quiz scores
    user_scores = db.session.query(Score, Quiz, Chapter)\
        .join(Quiz, Score.quiz_id == Quiz.id)\
        .join(Chapter, Quiz.chapter_id == Chapter.id)\
        .filter(Score.user_id == user_id)\
        .all()

    # Process scores for chart data
    chapter_scores = {}
    for score, quiz, chapter in user_scores:
        if chapter.chap_name not in chapter_scores:
            chapter_scores[chapter.chap_name] = []
        chapter_scores[chapter.chap_name].append(score.total_score / quiz.no_of_ques * 100)

    # Calculate average score for each chapter
    chart_data = [{"chapter": chap, "score": round(sum(scores) / len(scores), 2)} 
                  for chap, scores in chapter_scores.items()]

    return render_template('user_summary.html', name=name, user_id=user_id, chart_data=chart_data)



@app.route('/view_quiz/<int:quiz_id>', methods=['GET'])
def view_quiz(quiz_id):
    # Fetch quiz details
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter = quiz.chapter
    subject = chapter.subject
    
    # Get user_id from query parameters
    user_id = request.args.get('user_id')
    name = request.args.get('name')
    
    return render_template('view_quiz.html', quiz=quiz, chapter=chapter, subject=subject, user_id=user_id,name=name)




@app.route('/start_quiz/<int:quiz_id>/<name>/<int:user_id>', methods=['GET', 'POST'])
def start_quiz(quiz_id, name, user_id):
    # Fetch the quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Fetch all questions for the quiz
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    
    # Check if there are any questions for this quiz
    if not questions:
        flash('No questions available for this quiz yet.', 'warning')
        return redirect(url_for('user_dashboard', name=name, user_id=user_id))
    
    # Get the current question index from query parameters or default to 0
    question_index = request.args.get('question_index', 0, type=int)
    
    # Make sure the question index is valid
    if question_index >= len(questions):
        # If we've gone through all questions, redirect to results
        return redirect(url_for('submit_quiz', quiz_id=quiz_id, name=name, user_id=user_id))
    
    # Render the current question
    return render_template(
        'begin_quiz.html',
        quiz=quiz,
        question=questions[question_index],
        question_index=question_index,
        total_questions=len(questions),
        name=name,
        user_id=user_id
    )



@app.route("/save_answer/<int:quiz_id>/<name>/<int:question_index>/<int:user_id>", methods=["POST"])
def save_answer(quiz_id, name, question_index, user_id):
    selected_answer = request.form.get("answer")
    
    # Initialize quiz_answers in session if it doesn't exist
    if "quiz_answers" not in session:
        session["quiz_answers"] = {}
    
    # Save the selected answer in the session
    session["quiz_answers"][f"quiz_{quiz_id}_q{question_index}"] = int(selected_answer)
    session.modified = True
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    total_questions = len(questions)
    
    # Check if this is the last question
    if int(question_index) + 1 < total_questions:
        # Go to next question
        next_index = int(question_index) + 1
        return redirect(f"/start_quiz/{quiz_id}/{name}/{user_id}?question_index={next_index}")
    else:
        # Submit the quiz
        return redirect(f"/submit_quiz/{quiz_id}/{name}/{user_id}")



@app.route("/submit_quiz/<int:quiz_id>/<name>/<int:user_id>")
def submit_quiz(quiz_id, name, user_id):
    # Get user, quiz, and answers
    user = User.query.get_or_404(user_id)
    quiz = Quiz.query.get_or_404(quiz_id)
    answers = session.get("quiz_answers", {})
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    total_questions = len(questions)
    
    # Calculate score
    correct_answers = 0
    for index, question in enumerate(questions):
        correct_option = question.correct_option
        user_answer = answers.get(f"quiz_{quiz_id}_q{index}")
        if user_answer is not None and int(user_answer) == correct_option:
            correct_answers += 1
    
    # Calculate percentage and pass/fail status
    percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    pass_fail_status = "Pass" if percentage >= 40 else "Fail"
    
    # Check if user already has a score for this quiz
    existing_score = Score.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
    
    if existing_score:
        # Update existing score
        existing_score.total_score = correct_answers
        existing_score.pass_fail_ = pass_fail_status  # Make sure this line is correct
        existing_score.time_stamp = datetime.now()
        score = existing_score
    else:
        # Create new score
        score = Score(
            quiz_id=quiz_id,
            user_id=user_id,
            total_score=correct_answers,
            pass_fail_=pass_fail_status  # Make sure this line is correct
        )
        db.session.add(score)
    
    # Commit changes to database
    db.session.commit()
    
    # Clear quiz answers from session
    session.pop("quiz_answers", None)
    
    # Render result page
    return render_template(
        "quiz_result.html",
        name=name,
        user_id=user_id,
        score=score,
        quiz=quiz,
        total_questions=total_questions,
        correct_answers=correct_answers,
        percentage=percentage
    )


@app.route('/quiz_result/<int:quiz_id>/<name>/<int:user_id>', methods=['GET'])
def quiz_result(quiz_id, name, user_id):
    # Fetch score details
    score = Score.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
    quiz = Quiz.query.get_or_404(quiz_id)
    
    return render_template('quiz_result.html', 
                          score=score, 
                          quiz=quiz, 
                          name=name, 
                          user_id=user_id)




@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    # Redirect to login page
    return redirect(url_for("login"))




##################################################################################################################
def search_by_subject(search_txt):
    subjects=Subject.query.filter(Subject.sub_name.ilike(f"%{search_txt}%")).all()
    return subjects

def search_by_quiz(search_txt):
    return Quiz.query.join(Chapter).filter(Chapter.chap_name.ilike(f"%{search_txt}%")).all()


def search_by_user(search_txt):
    users = User.query.filter(
        User.name.ilike(f"%{search_txt}%") |
        User.email.ilike(f"%{search_txt}%")
    ).all()
    search_results = [
        {
            "name": user.name,
            "email": user.email,
            "total_quizzes": len(user.scores),
            "average_score": round(sum(score.total_scored for score in user.scores) / len(user.scores), 2)
            if user.scores else 0
        }
        for user in users
    ]
    return search_results
