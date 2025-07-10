from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_login import login_required

load_dotenv()

api_bp = Blueprint('api', __name__)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# 🎬 Movie Search API
@api_bp.route('/search')
@login_required
def search_movie():
    import logging
    import time
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    title = request.args.get('title')
    if not title:
        return jsonify({"error": "Missing title"}), 400
    if not TMDB_API_KEY:
        logging.error("TMDB API key is missing.")
        return jsonify({"error": "Missing TMDB API key"}), 500

    logging.info(f"/api/search called with title: {title}")

    tmdb_url = (
        "https://api.themoviedb.org/3/search/movie"
        f"?api_key={TMDB_API_KEY}&query={requests.utils.quote(title)}"
        "&language=en-US&page=1&include_adult=false"
    )

    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)

    try:
        response = session.get(tmdb_url, timeout=5)
        logging.info(f"TMDB API response status: {response.status_code}")
        response.raise_for_status()
    except requests.Timeout as e:
        logging.error(f"TMDB API request timed out: {e}")
        return jsonify({"error": "TMDB API request timed out"}), 504
    except requests.ConnectionError as e:
        logging.error(f"TMDB API connection error: {e}")
        return jsonify({"error": "TMDB API connection error"}), 503
    except requests.HTTPError as e:
        status_code = response.status_code if response else 500
        if status_code == 503:
            logging.error(f"TMDB API service unavailable (503): {e}")
            return jsonify({"error": "TMDB API service unavailable (503)"}), 503
        logging.error(f"TMDB API HTTP error: {e}")
        return jsonify({"error": "TMDB API HTTP error", "details": str(e)}), status_code
    except requests.RequestException as e:
        logging.error(f"TMDB API request failed: {e}")
        return jsonify({"error": "TMDB API error", "details": str(e)}), 500

    data = response.json()
    results = data.get('results', [])
    if not results:
        return jsonify({"error": "Movie not found"}), 404

    movie = results[0]
    return jsonify({
        "movieId": movie.get("id"),
        "title": movie.get("title"),
        "overview": movie.get("overview"),
        "release_date": movie.get("release_date"),
        "poster_path": (
            f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
            if movie.get("poster_path") else None
        )
    })

# ✨ Movie Recommendation API
@api_bp.route('/recommend')
@login_required
def recommend_movies():
    movie_id = request.args.get('movieId')
    if not movie_id:
        return jsonify({"error": "Missing movieId"}), 400

    rec_url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
        f"?api_key={TMDB_API_KEY}&language=en-US&page=1"
    )
    try:
        rec_response = requests.get(rec_url, timeout=5)
        rec_response.raise_for_status()
    except requests.RequestException as e:
        print(f"TMDB Recommendation fetch failed: {e}")
        return jsonify({"error": "Failed to fetch recommendations", "details": str(e)}), 500

    data = rec_response.json()
    recommendations = data.get('results', [])

    # ✅ Return as object with 'results' key
    return jsonify({
        "results": [
            {
                "title": movie.get("title"),
                "overview": movie.get("overview"),
                "release_date": movie.get("release_date"),
                "poster_path": (
                    f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
                    if movie.get("poster_path") else None
                )
            }
            for movie in recommendations[:10]
        ]
    })
