
from flask import Flask, render_template, request, redirect, url_for
import random
import sqlite3
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# Function to simulate coin flip and return the result
def flip_coin():
    return "Heads" if random.randint(0, 1) == 0 else "Tails"


# Function that returns game outcome using coin side parameters
def get_game_outcome(user_selection, coin_side_result):
    return "Won" if user_selection == coin_side_result else "Lost"


def get_sql_command(command_name):
    # Define the filename of the SQL command file
    sql_filename = 'static/sql/commands.sql'

    # Read the contents of the SQL file
    with open(sql_filename, 'r') as file:
        sql_content = file.read()

    # Split the SQL content into individual commands
    commands = sql_content.split(';')

    # Find the command with the specified name
    for command in commands:
        if command_name in command:
            return command.strip()

    # If command not found
    return None


# Function to create the games table if it doesn't exist
def create_games_table():
    # Get create table command
    sql_command = get_sql_command('Create games table')

    if sql_command is None:
        print("Command not found")
        return

    # Connect to SQLite database
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    # Execute the SQL command
    cursor.execute(sql_command)

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Function to save game inputs to session storage and SQLite database
def save_game_inputs(user_selection, coin_side_result, game_outcome):

    # Create table if it does not already exist
    create_games_table()

    # Get insert game command
    sql_command = get_sql_command('Insert game record')

    if sql_command is None:
        print("Command not found")
        return

    # Connect to SQLite database
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    # Execute the SQL command
    cursor.execute(sql_command, (user_selection, coin_side_result, game_outcome))

    # Commit changes and close connection
    conn.commit()
    conn.close()


def get_current_game_record():
    # Get command that returns current game
    sql_command = get_sql_command('Get current game')

    if sql_command is None:
        print("Command not found")
        return

    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    cursor.execute(sql_command)
    last_game_record = cursor.fetchone()

    conn.close()
    return last_game_record


def get_all_game_records():
    # Get command that returns all games
    sql_command = get_sql_command('Get all game records')

    if sql_command is None:
        print("Command not found")
        return

    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    cursor.execute(sql_command)
    all_game_records = cursor.fetchall()

    conn.close()
    return all_game_records


def get_total_games():
    # Get command that returns total games
    sql_command = get_sql_command('Get total games')

    if sql_command is None:
        print("Command not found")
        return

    # Connect to the database
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    # Query the database to get the maximum ID value
    cursor.execute(sql_command)
    max_id = cursor.fetchone()[0]  # Get the maximum ID value

    # Close the database connection
    conn.close()

    # Checking for no games
    if max_id is None:
        max_id = 0

    # Return total games
    return max_id


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/playGame')
def generate_form():
    return render_template('SelectCoinSide.html')


@app.route('/flip', methods=['POST'])
def flip():
    # Extract user selection from form data
    user_selection = request.form['user_selection']
    # Flip the coin to get the result
    coin_side_result = flip_coin()
    # Get game outcome
    game_outcome = get_game_outcome(user_selection, coin_side_result)
    # Save game inputs to session and SQLite database
    save_game_inputs(user_selection, coin_side_result, game_outcome)
    # Redirect to flip result page
    return redirect(url_for('flip_result'))


@app.route('/flip_result')
def flip_result():
    # Get the last game data from DB
    last_game_data = get_current_game_record()
    # Render flip result template with game data
    return render_template('FlipResult.html', last_game_data=last_game_data)


@app.route('/history')
def history():
    # Get game data
    game_data = get_all_game_records()
    # Get total number of games
    total_games = get_total_games()
    return render_template('FlipsHistory.html', game_data=game_data, total_games=total_games)


@app.route('/clear_games', methods=['POST'])
def clear_games():
    # Get command that deletes all games
    sql_command = get_sql_command('Delete all game records')

    if sql_command is None:
        print("Command not found")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()

    # Execute SQL command to delete all records from the games table
    cursor.execute(sql_command)

    # Get reset game counter command
    sql_command = get_sql_command('Reset game counter')

    if sql_command is None:
        print("Command not found")
        return

    # Reset the auto-increment counter
    cursor.execute(sql_command)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    # Redirect the user back to the history page after clearing the table
    return redirect(url_for('history'))


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
