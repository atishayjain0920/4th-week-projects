# Movie Recommendation Speech-to-text Transcription

## Description
This project is a Flask-based web application that provides personalized movie recommendations using a combination of collaborative filtering and content-based filtering techniques. It integrates with The Movie Database (TMDB) API to enhance movie search and recommendation features. The app includes user authentication, allowing users to sign up, log in, and receive tailored movie suggestions based on their preferences and ratings.

## Technologies Used
- **Programming Languages:** Python, JavaScript, HTML, CSS
- **Frameworks & Libraries:** Flask, Flask-Login, Flask-Migrate, SQLAlchemy, Surprise (SVD), scikit-learn, pandas
- **APIs:** The Movie Database (TMDB) API
- **Database:** SQLite
- **Others:** dotenv for environment variable management

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Movie-Recommendation-Speech-to-text-transcription-main/movie_recommandator
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   Create a `.env` file in the project root with the following:
   ```
   TMDB_API_KEY=your_tmdb_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

5. **Initialize the database:**
   ```bash
   flask create-db
   ```

## Running the Project Locally

Start the Flask development server:

```bash
flask run
```

The app will be accessible at `http://127.0.0.1:5000/`.

## Usage

- **User Authentication:** Sign up and log in to access personalized features.
- **Movie Search:** Search for movies by title using TMDB API.
- **Movie Recommendations:** Get movie recommendations based on your ratings and preferences.
- **Web Interface:** Access the home, login, and registration pages through the web UI.

## Core Features and Functionalities

- User registration, login, and session management with Flask-Login.
- Collaborative filtering recommendations using Surprise's SVD algorithm.
- Content-based filtering recommendations using TF-IDF and cosine similarity.
- Integration with TMDB API for movie search and additional recommendations.
- SQLite database with SQLAlchemy ORM and Flask-Migrate for migrations.
- RESTful API endpoints for search and recommendations.
- Responsive web interface with HTML, CSS, and JavaScript.

## Project Structure

```
movie_recommandator/
│
├── api.py                 # API endpoints for movie search and recommendations
├── app.py                 # Main Flask application setup and route definitions
├── auth.py                # User authentication routes and logic
├── models.py              # Database models (User, Movie, Rating)
├── recommender.py         # Recommendation engine implementation
├── test_tmdb.py           # Test script for TMDB API integration
│
├── data/                  # CSV files for movies and ratings data
│   ├── movies.csv
│   └── ratings.csv
│
├── instance/              # SQLite database file
│   └── movie_recommendation.db
│
├── migrations/            # Database migration scripts and configuration
│
├── static/                # Static assets (CSS, JavaScript)
│   ├── css/
│   └── js/
│
└── templates/             # HTML templates for web pages
    ├── index.html
    ├── login.html
    └── registration.html
```

## Contribution Guidelines

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear messages.
4. Push your branch to your fork.
5. Open a pull request describing your changes.

Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please contact:

- Author: Your Name
- Email: your.email@example.com
