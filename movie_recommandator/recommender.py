import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Recommender:
    def __init__(self, movies_path, ratings_path):
        self.movies = pd.read_csv(movies_path)
        self.ratings = pd.read_csv(ratings_path)
        self.svd_model = None
        self.tfidf_matrix = None
        self.movie_indices = None
        self._prepare_models()

    def _prepare_models(self):
        # Prepare collaborative filtering model (Surprise SVD)
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(self.ratings[['userId', 'movieId', 'rating']], reader)
        trainset, _ = train_test_split(data, test_size=0.25, random_state=42)
        self.svd_model = SVD()
        self.svd_model.fit(trainset)

        # Prepare content-based filtering model using genres, director, keywords
        self.movies['metadata'] = self.movies['genres'].fillna('') + ' ' + \
                                  self.movies['director'].fillna('') + ' ' + \
                                  self.movies['keywords'].fillna('')
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.movies['metadata'])
        self.movie_indices = pd.Series(self.movies.index, index=self.movies['movieId']).drop_duplicates()

    def get_collaborative_recommendations(self, user_id, n=10):
        try:
            user_id = int(user_id)
        except:
            return pd.DataFrame()

        user_rated = self.ratings[self.ratings['userId'] == user_id]['movieId'].tolist()
        predictions = []

        for movie_id in self.movies['movieId']:
            if movie_id not in user_rated:
                pred = self.svd_model.predict(user_id, movie_id)
                predictions.append((movie_id, pred.est))

        predictions.sort(key=lambda x: x[1], reverse=True)
        top_movie_ids = [movie_id for movie_id, _ in predictions[:n]]
        return self.movies[self.movies['movieId'].isin(top_movie_ids)]

    def get_content_based_recommendations(self, movie_id, n=10):
        idx = self.movie_indices.get(movie_id)
        if idx is None:
            return pd.DataFrame()
        cosine_sim = linear_kernel(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        sim_indices = cosine_sim.argsort()[:-n-2:-1]
        sim_indices = [i for i in sim_indices if i != idx]
        return self.movies.iloc[sim_indices]

    def get_recommendations(self, user_id, n=10):
        """
        Method exposed to Flask — returns list of recommended movie titles.
        """
        df = self.get_collaborative_recommendations(user_id, n)
        return df['title'].tolist()

    def search_movies(self, query, n=10):
        """
        Search movies by title — returns a list of matching titles.
        """
        matches = self.movies[self.movies['title'].str.contains(query, case=False, na=False)]
        return matches['title'].head(n).tolist()
