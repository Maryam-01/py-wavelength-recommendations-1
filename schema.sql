CREATE TABLE artists (
    artist_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT,
    genre TEXT NOT NULL
);

CREATE TABLE tracks (
    track_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    artist_id INTEGER NOT NULL REFERENCES artists(artist_id),
    duration_secs INTEGER,
    release_date DATE,
    play_count INTEGER DEFAULT 0
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    join_date DATE
);

CREATE TABLE listening_events (
    event_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    track_id INTEGER NOT NULL REFERENCES tracks(track_id),
    listened_at TIMESTAMP NOT NULL,
    completion_pct INTEGER,
    device_type TEXT
);
