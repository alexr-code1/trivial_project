from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Define the grid cells and their initial colors
grid_cells = {
    'A1': 'light-grey',
    'A2': 'yellow',
    'A3': 'blue',
    'A4': 'green',
    'A5': 'red',
    'A6': 'yellow',
    'A7': 'blue',
    'A8': 'green',
    'A9': 'light-grey',
    'B1': 'red',
    'B2': 'yellow',
    'B3': 'blue',
    'B4': 'green',
    'B5': 'yellow',
    'B6': 'yellow',
    'B7': 'blue',
    'B8': 'green',
    'B9': 'red',
    'C1': 'green',
    'C2': 'yellow',
    'C3': 'blue',
    'C4': 'green',
    'C5': 'green',
    'C6': 'yellow',
    'C7': 'blue',
    'C8': 'green',
    'C9': 'yellow',
    'D1': 'blue',
    'D2': 'yellow',
    'D3': 'blue',
    'D4': 'green',
    'D5': 'green',
    'D6': 'yellow',
    'D7': 'blue',
    'D8': 'green',
    'D9': 'blue',
    'E1': 'yellow',
    'E2': 'blue',
    'E3': 'green',
    'E4': 'red',
    'E5': 'light-grey',
    'E6': 'yellow',
    'E7': 'yellow',
    'E8': 'red',
    'E9': 'green',
    'F1': 'red',
    'F2': 'yellow',
    'F3': 'blue',
    'F4': 'green',
    'F5': 'red',
    'F6': 'yellow',
    'F7': 'blue',
    'F8': 'green',
    'F9': 'red',
    'G1': 'red',
    'G2': 'yellow',
    'G3': 'blue',
    'G4': 'green',
    'G5': 'red',
    'G6': 'yellow',
    'G7': 'blue',
    'G8': 'green',
    'G9': 'yellow',
    'H1': 'green',
    'H2': 'yellow',
    'H3': 'blue',
    'H4': 'green',
    'H5': 'green',
    'H6': 'yellow',
    'H7': 'blue',
    'H8': 'green',
    'H9': 'blue',
    'I1': 'light-grey',
    'I2': 'yellow',
    'I3': 'red',
    'I4': 'green',
    'I5': 'blue',
    'I6': 'yellow',
    'I7': 'red',
    'I8': 'green',
    'I9': 'light-grey',
}

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)

# Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Question model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('questions', lazy=True))
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grid_cells', methods=['GET'])
def get_grid_cells():
    grid = [{'cell_id': cell_id, 'color': grid_cells[cell_id]} for cell_id in grid_cells]
    return jsonify(grid)

@app.route('/update_cell', methods=['POST'])
def update_cell():
    cell_id = request.form['cell_id']
    color = request.form['color']
    grid_cells[cell_id] = color
    return jsonify({'message': 'Cell color updated successfully'})

@app.route('/players', methods=['GET', 'POST'])
def players():
    if request.method == 'POST':
        with app.app_context():
            player1 = request.form['player1']
            player1_color = request.form['player1_color']
            player2 = request.form['player2']
            player2_color = request.form['player2_color']
            player3 = request.form['player3']
            player3_color = request.form['player3_color']
            player4 = request.form['player4']
            player4_color = request.form['player4_color']

            players = [
                {'name': player1, 'color': player1_color},
                {'name': player2, 'color': player2_color},
                {'name': player3, 'color': player3_color},
                {'name': player4, 'color': player4_color}
            ]

            # Save players to the database
            for player in players:
                new_player = Player(name=player['name'], color=player['color'])
                db.session.add(new_player)
            db.session.commit()

            return render_template('edit_players.html', players=players)
    else:
        return render_template('players.html')

@app.route('/edit_players')
def edit_players():
    with app.app_context():
        players = Player.query.all()
        return render_template('edit_players.html', players=players)

@app.route('/qa', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        with app.app_context():
            category1 = request.form['category1']
            category2 = request.form['category2']
            category3 = request.form['category3']
            category4 = request.form['category4']

            categories = [
                {'name': category1},
                {'name': category2},
                {'name': category3},
                {'name': category4}
            ]

            # Save categories to the database
            for category in categories:
                new_category = Category(name=category['name'])
                db.session.add(new_category)
            db.session.commit()

            return render_template('qa.html', categories=categories)
    else:
        with app.app_context():
            categories = Category.query.all()
            questions = Question.query.all()
            return render_template('qa.html', categories=categories, questions=questions)

@app.route('/add_qa', methods=['POST'])
def add_qa():
    with app.app_context():
        category_id = request.form['category_id']
        question = request.form['question']
        answer = request.form['answer']

        new_question = Question(category_id=category_id, question=question, answer=answer)
        db.session.add(new_question)
        db.session.commit()

        return jsonify({'message': 'QA submitted successfully'})

@app.route('/update_question', methods=['POST'])
def update_question():
    with app.app_context():
        question_id = request.form['id']
        question_text = request.form['question']

        question = Question.query.get(question_id)
        question.question = question_text
        db.session.commit()

        return jsonify({'message': 'Question updated successfully'})

@app.route('/delete_question', methods=['POST'])
def delete_question():
    with app.app_context():
        question_id = request.form['id']

        question = Question.query.get(question_id)
        db.session.delete(question)
        db.session.commit()

        return jsonify({'message': 'Question deleted successfully'})

@app.route('/delete_category', methods=['POST'])
def delete_category():
    with app.app_context():
        category_id = request.form['id']

        category = Category.query.get(category_id)
        db.session.delete(category)
        db.session.commit()

        return jsonify({'message': 'Category deleted successfully'})

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
