-- seed.sql
-- Sample data reused from the Wavelength listening database sprint,
-- so this is the same domain learners already know.

INSERT INTO artists (artist_id, name, country, genre) VALUES
  (1, 'ABBA',     'Sweden',          'Pop'),
  (2, 'Blondie',  'United States',   'New Wave'),
  (3, 'The Cure', 'United Kingdom',  'Post-Punk');

INSERT INTO tracks (track_id, title, artist_id, duration_secs, release_date, play_count) VALUES
  (1,  'Dancing Queen',          1, 232, '1976-08-16', 4821),
  (2,  'Mamma Mia',              1, 213, '1975-08-27', 3902),
  (3,  'The Winner Takes It All',1, 295, '1980-07-21', 5103),
  (4,  'Waterloo',               1, 168, '1974-03-04', 6234),
  (5,  'Heart of Glass',         2, 258, '1979-01-20', 7654),
  (6,  'Call Me',                2, 243, '1980-02-01', 5490),
  (7,  'One Way or Another',     2, 191, '1979-09-01', 9102),
  (8,  'Atomic',                 2, 237, '1980-09-08', 4120),
  (9,  'Lovesong',               3, 201, '1989-08-12', 6721),
  (10, 'Friday I''m in Love',    3, 219, '1992-05-01', 8901),
  (11, 'Close to Me',            3, 213, '1985-09-20', 3301),
  (12, 'Boys Don''t Cry',        3, 156, '1979-06-28', 2890);

INSERT INTO users (user_id, username, join_date) VALUES
  (1, 'nova_ears',    '2022-03-14'),
  (2, 'rhythmbox',    '2021-07-09'),
  (3, 'waveform99',   '2023-01-15'),
  (4, 'deeplistener', '2020-11-22'),
  (5, 'trackjunkie',  '2022-08-03');

INSERT INTO listening_events (event_id, user_id, track_id, listened_at, completion_pct, device_type) VALUES
  (1,  1, 1,  '2024-11-01T22:14:00Z', 87,  'mobile'),
  (2,  1, 1,  '2024-11-02T23:01:00Z', 100, 'desktop'),
  (3,  2, 2,  '2024-11-03T08:22:00Z', 45,  'mobile'),
  (4,  3, 7,  '2024-11-03T12:05:00Z', 100, 'desktop'),
  (5,  4, 6,  '2024-11-04T09:11:00Z', 73,  'mobile'),
  (6,  1, 3,  '2024-11-04T21:30:00Z', 100, 'desktop'),
  (7,  2, 9,  '2024-11-05T07:45:00Z', 62,  'mobile'),
  (8,  5, 7,  '2024-11-05T14:22:00Z', 100, 'desktop'),
  (9,  3, 4,  '2024-11-05T18:30:00Z', 88,  'tablet'),
  (10, 4, 1,  '2024-11-06T11:00:00Z', 100, 'desktop'),
  (11, 1, 9,  '2024-11-06T22:15:00Z', 55,  'mobile'),
  (12, 2, 5,  '2024-11-07T08:00:00Z', 100, 'mobile'),
  (13, 5, 3,  '2024-11-07T16:45:00Z', 90,  'desktop'),
  (14, 3, 12, '2024-11-08T13:20:00Z', 78,  'tablet'),
  (15, 4, 7,  '2024-11-08T20:00:00Z', 100, 'desktop'),
  (16, 1, 6,  '2024-11-09T23:10:00Z', 100, 'mobile'),
  (17, 2, 10, '2024-11-10T07:30:00Z', 42,  'mobile'),
  (18, 5, 9,  '2024-11-10T12:00:00Z', 100, 'desktop');

SELECT setval('artists_artist_id_seq', (SELECT MAX(artist_id) FROM artists));
SELECT setval('tracks_track_id_seq', (SELECT MAX(track_id) FROM tracks));
SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users));
SELECT setval('listening_events_event_id_seq', (SELECT MAX(event_id) FROM listening_events));
