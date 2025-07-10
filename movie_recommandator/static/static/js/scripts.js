console.log("✅ scripts.js is running");

async function fetchMovies() {
  const query = document.getElementById('search-bar').value.trim();
  const movieList = document.getElementById('movie-list');
  const recommendationList = document.getElementById('recommendation-list');

  movieList.innerHTML = '';
  recommendationList.innerHTML = '';

  if (!query) return;

  try {
    console.log("fetchMovies called with query:", query);
    const res = await fetch(`/api/search?title=${encodeURIComponent(query)}`);
    const data = await res.json();
    console.log("🔍 Search Response:", data);

    if (data.error) {
      movieList.innerHTML = `<p>${data.error}</p>`;
      return;
    }

    const movieCard = document.createElement('div');
    movieCard.className = 'movie-card';
    movieCard.innerHTML = `
      <img src="${data.poster_path || ''}" alt="${data.title}" />
      <h3>${data.title}</h3>
      <p><strong>Release:</strong> ${data.release_date || 'N/A'}</p>
      <p>${data.overview || 'No description available.'}</p>
    `;
    movieList.appendChild(movieCard);

    console.log("🎯 Fetching recommendations for ID:", data.movieId);
    const recRes = await fetch(`/api/recommend?movieId=${data.movieId}`);
    const recommendations = await recRes.json();
    console.log("✨ Recommendations:", recommendations);

    if (!recommendations.results || !Array.isArray(recommendations.results) || recommendations.results.length === 0) {
      console.log("No recommendations found, showing fallback.");
      // Fallback sample recommendations for testing
      const fallbackRecommendations = [
        {
          title: "The Matrix",
          overview: "A computer hacker learns about the true nature of reality and his role in the war against its controllers.",
          release_date: "1999-03-31",
          poster_path: "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
        },
        {
          title: "Interstellar",
          overview: "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
          release_date: "2014-11-07",
          poster_path: "https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg"
        }
      ];
      fallbackRecommendations.forEach(movie => {
        const recCard = document.createElement('div');
        recCard.className = 'movie-card';
        recCard.innerHTML = `
          <img src="${movie.poster_path}" alt="${movie.title}" />
          <h3>${movie.title}</h3>
          <p><strong>Release:</strong> ${movie.release_date || 'N/A'}</p>
          <p>${movie.overview || 'No description available.'}</p>
        `;
        recommendationList.appendChild(recCard);
      });
      return;
    }

    recommendations.results.forEach(movie => {
      const poster = movie.poster_path
        ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
        : 'https://via.placeholder.com/300x450?text=No+Image';

      const recCard = document.createElement('div');
      recCard.className = 'movie-card';
      recCard.innerHTML = `
        <img src="${poster}" alt="${movie.title}" />
        <h3>${movie.title}</h3>
        <p><strong>Release:</strong> ${movie.release_date || 'N/A'}</p>
        <p>${movie.overview || 'No description available.'}</p>
      `;
      recommendationList.appendChild(recCard);
    });

  } catch (err) {
    console.error("❌ Error:", err);
    movieList.innerHTML = `<p>❌ Could not fetch movie data.</p>`;
  }
}

document.getElementById('search-btn').addEventListener('click', fetchMovies);
