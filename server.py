from flask import Flask, render_template, redirect, request, url_for
from functions import answers, questions, generate_new_id
from werkzeug.utils import secure_filename
import os
import data_manager

UPLOAD_FOLDER_A = 'static/uploads_answer'
UPLOAD_FOLDER_Q = 'static/uploads_question'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER_A'] = UPLOAD_FOLDER_A
app.config['UPLOAD_FOLDER_Q'] = UPLOAD_FOLDER_Q


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(list_with_all, upload_path):
    file = request.files['image']
    if file and allowed_file(file.filename):
        file.filename = str(generate_new_id(list_with_all)) + '.jpg'
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_path, filename))
        return filename


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/list')
def list_page():
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    column_names = data_manager.get_column_names()

    if order_direction is None:
        order_direction = 'desc'

    if order_by:
        questions = data_manager.get_sorted_questions(order_by, order_direction)
    else:
        questions = data_manager.get_sorted_questions('submission_time', order_direction)


    return render_template("list.html", column_names=column_names, questions=questions, order_direction=order_direction)


@app.route("/add-question", methods=['POST', 'GET'])
def new_question():

    if request.method == 'POST':

        filename = upload_file(questions, app.config['UPLOAD_FOLDER_Q'])

        new_question_title = request.form['Title']
        new_question_message = request.form['message']
        new_question_image = filename

        data_manager.add_question(new_question_title, new_question_message, new_question_image)
        question_id = data_manager.get_latest_question_id()

        return redirect(url_for('question_answer', question_id=question_id))

    else:
        return render_template('new_question.html')


@app.route('/question/<int:question_id>/vote_up', methods=['POST'])
def vote_question_up(question_id):
    data_manager.vote_question_up(question_id)
    return redirect(url_for('list_page'))


@app.route('/question/<int:question_id>/vote_down', methods=['POST'])
def vote_question_down(question_id):
    data_manager.vote_question_down(question_id)
    return redirect(url_for('list_page'))


@app.route('/answer/<int:question_id>/<int:answer_id>/vote_up', methods=['POST'])
def vote_answer_up(answer_id, question_id):
    data_manager.vote_answer_up(answer_id)
    return redirect(url_for('question_answer', question_id=question_id))


@app.route('/answer/<int:question_id>/<int:answer_id>/vote_down', methods=['POST'])
def vote_answer_down(answer_id, question_id):
    data_manager.vote_answer_down(answer_id)
    return redirect(url_for('question_answer', question_id=question_id))


@app.route('/question/<int:question_id>')
def question_answer(question_id):
    answers = data_manager.get_answers(question_id)
    question = data_manager.get_question(question_id)
    headers_list = data_manager.get_column_names()
    answer_headers = ["id", "submission_time", "vote_number", "question_id", "answer", "image"]

    if question is None:
        return redirect(url_for("list_page"))
    else:
        return render_template("questions.html", question=question, headers_list=headers_list, answer_headers=answer_headers, answers=answers)


@app.route("/question/<int:question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):

    if request.method == 'POST':

        filename = upload_file(answers, app.config['UPLOAD_FOLDER_A'])

        new_answer_message = request.form['message']
        new_answer_image = filename

        data_manager.add_answer(question_id, new_answer_message, new_answer_image)

        return redirect(url_for('question_answer', answers=answers, question_id=question_id))
    else:

        return render_template('new_answer.html', question_id=question_id)


@app.route("/answer/<int:question_id>/<int:answer_id>/delete")
def answer_delete(answer_id, question_id):

    answers = data_manager.get_answer_img_by_id(question_id, answer_id)

    for answer in answers:
        if answer['image']:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER_A'], answer['image']))
    data_manager.delete_answer(answer_id)

    return redirect(url_for('question_answer', answers=answers, question_id=question_id))


if __name__ == "__main__":
    app.run()
