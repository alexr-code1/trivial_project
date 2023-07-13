from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'sample_db'

mysql = MySQL(app)

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

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to retrieve the grid cells and their colors
@app.route('/grid_cells', methods=['GET'])
def get_grid_cells():
    grid = [{'cell_id': cell_id, 'color': grid_cells[cell_id]} for cell_id in grid_cells]
    return jsonify(grid)

# Route to update the color of a grid cell
@app.route('/update_cell', methods=['POST'])
def update_cell():
    cell_id = request.form['cell_id']
    color = request.form['color']
    
    # Update the color in the database
    cur = mysql.connection.cursor()
    cur.execute('UPDATE cells SET color = %s WHERE cell_id = %s', (color, cell_id))
    mysql.connection.commit()
    cur.close()
    
    # Update the color in the grid_cells dictionary
    grid_cells[cell_id] = color
    
    return jsonify({'message': 'Cell color updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
