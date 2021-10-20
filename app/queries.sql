-- name: get_movie_with_id^
-- Get a movie with the given title_id
SELECT * FROM titles WHERE title_id = :title_id;

-- name: get_cast_for_title
-- Get the cast for a given title
SELECT * FROM crew WHERE title_id = :title_id;

-- name: get_show_with_id^
-- Get the show with the given title_id
SELECT * FROM titles WHERE title_id = :title_id;

-- name: get_title_type$
-- Get the type of title, movie, tvSeries, etc.
SELECT type FROM titles WHERE title_id = :title_id;

-- name: get_seasons_in_show$
-- Get the number of seasons in a show
SELECT
	COUNT(DISTINCT season_number)
FROM
	episodes
WHERE
	show_title_id = :title_id;

-- name: get_episodes_in_season$
-- Get the number of episodes in a season for a given title with given title_id
SELECT
	COUNT(*)
FROM
	episodes
WHERE
	show_title_id = :title_id
	AND season_number = :season_number;

-- name: get_episode_for_title_season_number_episode_number^
-- Get the episode title info for the title_id, season number and episode number
SELECT
	*
FROM
	titles
WHERE
	title_id IN(
		SELECT
			episode_title_id FROM episodes
		WHERE
			show_title_id = :title_id
			AND season_number = :season_number
			AND episode_number = :episode_number);

-- name: get_episodes_for_season
-- Get the episodes for the season
SELECT
	*
FROM
	titles
WHERE
	title_id IN(
		SELECT
			episode_title_id FROM episodes
		WHERE
			show_title_id = 'tt1475582'
			AND season_number = 1);