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

    async function fetchRecipeDetails(recipeId) {
        try {
            const response = await fetch(`/recipe/${recipeId}`);
            const data = await response.json();

            if (response.ok) {
                displayRecipeDetails(data);
            } else {
                resultsDiv.innerHTML = `<p>${data.error}</p>`;
            }
        } catch (error) {
            resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    }

    function displayResults(results) {
        resultsDiv.innerHTML = '';
        if (results.length === 0) {
            resultsDiv.innerHTML = '<p>No recipes found. Do you have anything else in your kitchen?</p>';
            return;
        }

        results.forEach(recipe => {
            const recipeDiv = document.createElement('div');
            recipeDiv.classList.add('recipe');
            recipeDiv.setAttribute('data-id', recipe.id)

            const recipeTitle = document.createElement('h2');
            recipeTitle.textContent = recipe.title;
            recipeDiv.appendChild(recipeTitle);

            if (recipe.image) {
                const recipeImage = document.createElement('img');
                recipeImage.src = recipe.image;
                recipeDiv.appendChild(recipeImage);
            }

            recipeDiv.addEventListener('click', () => {  // Add click event listener
                fetchRecipeDetails(recipe.id);
            });

            resultsDiv.appendChild(recipeDiv);
        });
    }

    function displayRecipeDetails(details) {
        resultsDiv.innerHTML = '';
    
        const recipeTitle = document.createElement('h2');
        recipeTitle.textContent = details.title;
        resultsDiv.appendChild(recipeTitle);
    
        if (details.image) {
            const recipeImage = document.createElement('img');
            recipeImage.src = details.image;
            resultsDiv.appendChild(recipeImage);
        }
    
        const ingredientsList = document.createElement('ul');
        details.extendedIngredients.forEach(ingredient => {
            const listItem = document.createElement('li');
            listItem.textContent = `${ingredient.amount} ${ingredient.unit} ${ingredient.name}`;
            ingredientsList.appendChild(listItem);
        });
        resultsDiv.appendChild(ingredientsList);
    
        const instructions = document.createElement('div');
        instructions.innerHTML = details.instructions;  // Set as HTML to render properly
        resultsDiv.appendChild(instructions);

        const saveButton = document.createElement('button');
        saveButton.textContent = 'Save to Favorites';
        saveButton.addEventListener('click', () => saveToFavorites(details.id));
        resultsDiv.appendChild(saveButton);
    }
    
    async function saveToFavorites(recipeId) {
        try {
            const response = await fetch(`/save-favorite/${recipeId}`, { method: 'POST' });
            const data = await response.json();
            if (response.ok) {
                alert('Recipe saved to favorites!');
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }
});
