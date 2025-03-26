-- Create Player table
CREATE TABLE Player (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100),
    birthday DATE,
    height NUMBER,
    weight NUMBER,
    overall_rating NUMBER,
    potential NUMBER,
    preferred_foot CHAR(1) CHECK (preferred_foot IN ('R', 'L')),
    attacking_work_rate VARCHAR2(100),
    defensive_work_rate VARCHAR2(100),
    crossing NUMBER
);

-- Create Team table
CREATE TABLE Team (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100),
    abbrev VARCHAR2(10),
    logo VARCHAR2(255),
    build_up_play_speed VARCHAR2(20) CHECK (build_up_play_speed IN ('Balanced', 'Fast', 'Slow')),
    build_up_play_dribble VARCHAR2(20) CHECK (build_up_play_dribble IN ('Lots', 'Little', 'Normal')),
    build_up_play_passing VARCHAR2(20) CHECK (build_up_play_passing IN ('Mixed', 'Short', 'Long')),
    creation_date TIMESTAMP
);

-- Create Country table
CREATE TABLE Country (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100),
    abbrev VARCHAR2(10),
    flag VARCHAR2(255),
    is_eu NUMBER(1) CHECK (is_eu IN (0, 1)),
    tz_offset NUMBER
);

-- Create League table
CREATE TABLE League (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country_id NUMBER NOT NULL REFERENCES Country(id),
    name VARCHAR2(100),
    photo VARCHAR2(255)
);

-- Create Weather table
CREATE TABLE Weather (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    conditions VARCHAR2(100)
);

-- Create Match table
CREATE TABLE Matches (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    home_team_id NUMBER NOT NULL REFERENCES Team(id),
    away_team_id NUMBER NOT NULL REFERENCES Team(id),
    ht_goal NUMBER,
    at_goal NUMBER,
    league_id NUMBER NOT NULL REFERENCES League(id),
    season VARCHAR2(50),
    weather_id NUMBER NOT NULL REFERENCES Weather(id),
    odds_home FLOAT,
    odds_draw FLOAT,
    odds_away FLOAT,
    match_date TIMESTAMP
);

-- Create MatchPlayer table
CREATE TABLE MatchPlayer (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    player_id NUMBER NOT NULL REFERENCES Player(id),
    match_id NUMBER NOT NULL REFERENCES Matches(id)
);
