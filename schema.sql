CREATE TABLE summoner (
    id INTEGER PRIMARY KEY,
    name STRING
);

CREATE TABLE game (
    gameId INTEGER PRIMARY KEY,
    mapId INTEGER,
    createDate INTEGER,
);
