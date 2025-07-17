The coin flip guess application allows users to play a game of guessing the side the coin flipped to. The game data of the user is stored in one SQLite file. 

The site is composed of four pages: index.html, SelectCoinSide.html, FlipResult.html, and FlipsHistory.html. The pages are styled through Bootstrap 5 and share the same nav and footer html files that are injected through Flask. Results of each game are generated and displayed through Flask.

The site has five buttons: Play Game (redirects to game page), Submit Guess (passes user guess to app.py), Play Again (redirects to game page), Go to game history (redirects to history page), and Clear History (removes game history in SQLite file). 

The number of games that can be played is limited by SQLite file capacity. 

Privacy of Data Stored by the Application

Stored game data is in SQLite file. 

Application Limitations

Game data cannot be recovered if SQLite file is lost or corrupted. The coin flips are pseudorandom. 

Detailed Description of Site Pages

Quick Summary of Site Pages
index.html 		Home page that explains game and has button to play the game
SelectCoinSide.html 	Web form for user to select coin side guess
FlipResult.html	Page displays current game results after form submission
FlipsHistory.html	Page displays all game data in local storage
bootstrap.html	Bootstrap 5 links that are injected by Flask into heads of pages
nav.html		Nav bar that is injected by Flask into pages
footer.html		Footer that is injected by Flask into pages

Home Page (index.html)
This page explains the game and prompts users to click the button to begin playing. The button is a link to the route that generates the web form page, SelectCoinSide.html. 

Web form Page (SelectCoinSide.html) 
In this page, the user is informed through text that the coin has been flipped and prompted to select their guess of heads or tails and clicks the submit button to initiate the route that flips the coin.  

Flip Result Page (FlipResult.html) 
The page displays the game data of the current game: the game number, the user selection, 
the coin side flipped to, and the game outcome. 

Flips History Page (FlipsHistory.html)
This page displays the game data of every game the user has played in a table. 

API of functions in Flask Document (app.py)
	flip_coin() – Simulates coin flip and returns side result
	get_game_outcome(user_selection, coin_side_result)-Returns game outcome using coin       side parameters
	get_sql_command(command_name)-Returns requested sql command from commands.sql
	create_games_table()-Creates games table if it does not exist
	save_game_inputs(user_selection, coin_side_result, game_outcome)-Saves game inputs to SQLite database
	get_current_game_record()-Returns record of current game
	get_all_game_records()- Returns all game records
	get_total_games()-Returns total number of games

Route Functions:
‘/’ and ‘/index.html’	index()-Returns render of template index.html
‘/playGame’		generate_form()-Returns render of template SelectCoinSide.html
‘/flip’			flip()-Gets game inputs, saves them by passing them to  save_game_inputs(), and returns redirect to route of flip_result()
‘/flip_result’		flip_result()-Gets current game data by calling get_current_game_record() and injects the data into returned render of template ‘FlipResult.html’
‘/history’		history()-Gets all game data and total number of games by calling get_all_game_records() and get_total_games(), respectively. Then, game data and total number of games is injected into returned render of template ‘FlipsHistory.html’
‘/clear_games’		clear_games()-Deletes all game data in SQLite database and returns redirect to route of history()
