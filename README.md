# IMDb CLI Application Documentation

## Overview

This is a command-line interface (CLI) application for managing a movie database with reviews. It uses MongoDB Atlas as the database backend and provides functionality to manage movies and their associated reviews.

## Technologies Used

- **Python 3**
- **PyMongo**: MongoDB driver for Python
- **python-dotenv**: For loading environment variables
- **MongoDB Atlas**: Cloud-hosted MongoDB database

## Database Structure

The application uses a MongoDB database named `imdb` with two collections:

### Movies Collection (`db.movies`)

Each movie document contains:

- `title`: Movie title (string, capitalized)
- `releaseYear`: Year of release (integer)
- `runtimeMins`: Duration in minutes (integer)
- `language`: Primary language (string, capitalized)
- `genre`: Array of genre strings (capitalized)
- `_id`: MongoDB ObjectId (auto-generated)

### Reviews Collection (`db.reviews`)

Each review document contains:

- `movieId`: Reference to the movie's `_id`
- `userName`: Name of the reviewer (string)
- `rating`: Numeric rating from 1-10 (float)
- `reviewText`: Review comment (string)
- `createdAt`: Timestamp when review was created/updated (datetime)
- `_id`: MongoDB ObjectId (auto-generated)

## Setup Instructions

1. **Install Dependencies**

   ```bash
   pip install pymongo python-dotenv
   ```

2. **Configure Environment Variables**

   Create a `.env` file in the project root with your MongoDB connection string:

   ```.env
   MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

3. **Run the Application**

   ```bash
   python app.py
   ```

## Features & Commands

### 1. Add a Movie

Allows you to add new movies to the database with the following information:

- Title
- Release Year
- Runtime (in minutes)
- Language
- Genres (comma-separated list)

You can add multiple movies in succession by typing "yes" when prompted.

### 2. See All Movies

Displays all movies in the database sorted alphabetically by title. For each movie, it shows:

- Title
- Release Year
- Runtime
- Language
- Genres

### 3. Update a Movie

Select a movie from the list and update one of these fields:

- Title
- Release Year
- Runtime
- Language

### 4. Delete a Movie

Select and delete a movie from the database. This also removes all associated reviews to maintain database integrity.

### 5. Add a Review

Submit a review for a selected movie including:

- Your name (reviewer name)
- Rating (1-10 scale)
- Comment text

Reviews are timestamped automatically.

### 6. Edit a Review

Modify an existing review for a movie. You can update:

- Rating
- Comment text

The timestamp is updated to the current time when edited.

### 7. Delete a Review

Remove a specific review from a movie.

### 8. View Reviews & Ratings

Display all reviews for a selected movie, including:

- Average rating calculation
- Total number of reviews
- Individual reviews with user name, rating, comment, and date

### 9. Exit

Closes the application gracefully.

## Helper Functions

### `select_movie()`

A reusable helper function that:

1. Retrieves all movies sorted alphabetically
2. Displays them as a numbered list
3. Prompts the user to select one by number
4. Returns the selected movie document or `None` if selection fails

This function is used by multiple commands to avoid code duplication.

## Error Handling

The application includes error handling for:

- Invalid numeric inputs (for years, runtime, ratings)
- Empty required fields
- Invalid menu selections
- Out-of-range ratings (ensures 1-10 scale)
- Database connection issues (handled by PyMongo)

## Code Organization

The application follows a modular structure:

- **Main Loop**: Handles command input and routing
- **Command Functions**: Each feature has its own function
- **Helper Functions**: Reusable utilities like `select_movie()`
- **Print Functions**: Display menus and formatting

## Best Practices Demonstrated

- Environment variable usage for sensitive data (connection strings)
- Input validation and error handling
- Cascading deletes (removing reviews when movies are deleted)
- Sorted displays for better user experience
- Confirmation prompts for destructive operations
- Consistent data formatting (capitalization, title case)
