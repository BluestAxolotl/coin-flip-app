
-- Create games table
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_selection TEXT NOT NULL,
    coin_side_result TEXT NOT NULL,
    game_outcome TEXT NOT NULL
);

-- Insert game record
INSERT INTO games (user_selection, coin_side_result, game_outcome) VALUES (?, ?, ?);

-- Get current game
SELECT * FROM games ORDER BY id DESC LIMIT 1;

-- Get all game records
SELECT * FROM games;

-- Get total games
SELECT MAX(id) FROM games;

-- Delete all game records
DELETE FROM games;

-- Reset game counter
DELETE FROM sqlite_sequence WHERE name='games';