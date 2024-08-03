document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsDiv = document.getElementById('results');
    const loadingSpinner = document.getElementById('loading-spinner');

    searchForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const query = document.getElementById('query').value.trim();
        if (!query) {
            resultsDiv.innerHTML = '<p>Please enter a search query.</p>';
            return;
        }

        resultsDiv.innerHTML = '';
        loadingSpinner.style.display = 'block';

        try {
            const response = await fetch(`/search?query=${query}`);
            const data = await response.json();

            loadingSpinner.style.display = 'none';

            if (response.ok) {
                displayResults(data.results);
            } else {
                resultsDiv.innerHTML = `<p>${data.error}</p>`;
            }
        } catch (error) {
            loadingSpinner.style.display = 'none';
            resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    });

    function displayResults(results) {
        resultsDiv.innerHTML = '';
        if (results.length === 0) {
            resultsDiv.innerHTML = '<p>No recipes found. Do you have anything else in your kitchen?</p>';
            return;
        }

        results.forEach(recipe => {
            const recipeDiv = document.createElement('div');
            recipeDiv.classList.add('recipe');

            const recipeTitle = document.createElement('h2');
            recipeTitle.textContent = recipe.title;
            recipeDiv.appendChild(recipeTitle);

            if (recipe.image) {
                const recipeImage = document.createElement('img');
                recipeImage.src = recipe.image;
                recipeDiv.appendChild(recipeImage);
            }

            resultsDiv.appendChild(recipeDiv);
        });
    }
});
