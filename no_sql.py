from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Get the connection string
uri = os.getenv("MONGODB_CONNECTION_STRING")

# Connect to MongoDB Atlas
client = MongoClient(uri, server_api=ServerApi("1"))

# Switch to the correct database
db = client["imdb"]
# We will use two collections: db.movies and db.reviews

def main():
    print("---------------------------------------")
    print("      WELCOME TO IMDB CLI      ")
    print("---------------------------------------")
    
    while True:
        print_commands()
        command = input("\n>> Enter a command number: ")
        print("-" * 30)
        
        if command == "1":
            add_movies()
        elif command == "2":
            list_movies()
        elif command == "3":
            update_movie()
        elif command == "4":
            delete_movie()
        elif command == "5":
            review_movie()
        elif command == "6":
            edit_review()
        elif command == "7":
            delete_review()
        elif command == "8":
            see_movie_reviews()
        elif command == "9":
            print("Exiting the application....")
            print("Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

def print_commands():
    print("\nCommands:")
    print("1. Add a movie")
    print("2. See all movies")
    print("3. Update a movie")
    print("4. Delete a movie")
    print("5. Add a Review")
    print("6. Edit a Review")
    print("7. Delete a Review")
    print("8. View Reviews & Ratings")
    print("9. Exit")

# --- Helper Function ---
def select_movie():
    """Helper to list movies and let user pick one by index."""
    movies = list(db.movies.find().sort("title"))
    if not movies:
        print("No movies found in collection.")
        return None

    for index, movie in enumerate(movies, 1):
        print(f"{index}. {movie['title']} ({movie['releaseYear']})")
    
    try:
        selection = int(input("\nSelect a movie number: ")) - 1
        if 0 <= selection < len(movies):
            return movies[selection]
        else:
            print("Invalid selection number.")
            return None
    except ValueError:
        print("Please enter a valid number.")
        return None

def add_movies():
    while True:
        try:
            print("\n--- Add New Movie ---")
            title = input("Title: ").strip().title()
            if not title:
                print("Title cannot be empty.")
                continue

            release_year = int(input("Release Year: "))
            runtime = int(input("Runtime (minutes): "))
            language = input("Language: ").strip().capitalize()
            genre = [entry.strip().capitalize() for entry in input("Genres (comma separated): ").split(",")]
            
            document = {
                "title": title,
                "releaseYear": release_year,
                "runtimeMins": runtime,
                "language": language,
                "genre": genre
            }
            
            inserted = db.movies.insert_one(document)
            print(f"Successfully inserted '{title}' (ID: {inserted.inserted_id})")
            
            proceed = input("Add another? (yes/no): ").lower().strip()
            if proceed != "yes": break
            
        except ValueError:
            print("Error: Year and Runtime must be integers.")

def list_movies():
    print("\n--- Movie Collection ---")
    movies = db.movies.find().sort("title")
    count = 0
    for movie in movies:
        count += 1
        print(f"Title:    {movie['title']}")
        print(f"Year:     {movie['releaseYear']}")
        print(f"Runtime:  {movie['runtimeMins']} mins")
        print(f"Language: {movie['language']}")
        print(f"Genres:   {', '.join(movie['genre'])}")
        print("-" * 20)
    
    if count == 0:
        print("No movies found.")

def update_movie():
    print("\n--- Update Movie ---")
    movie = select_movie()
    if not movie: return

    print(f"\nUpdating: {movie['title']}")
    print("1. Title")
    print("2. Release Year")
    print("3. Runtime")
    print("4. Language")
    
    choice = input("What do you want to update? (1-4): ")
    update_field = {}

    try:
        if choice == "1":
            new_title = input("Enter new title: ").title()
            update_field = {"title": new_title}
        elif choice == "2":
            new_year = int(input("Enter new year: "))
            update_field = {"releaseYear": new_year}
        elif choice == "3":
            new_time = int(input("Enter new runtime: "))
            update_field = {"runtimeMins": new_time}
        elif choice == "4":
            new_lang = input("Enter new language: ").capitalize()
            update_field = {"language": new_lang}
        else:
            print("Invalid choice.")
            return

        db.movies.update_one({"_id": movie["_id"]}, {"$set": update_field})
        print("Movie updated successfully.")

    except ValueError:
        print("Invalid input format.")

def delete_movie():
    print("\n--- Delete Movie ---")
    movie = select_movie()
    if not movie: return

    confirm = input(f"Are you sure you want to delete '{movie['title']}'? (yes/no): ").lower()
    if confirm == "yes":
        # Delete the movie
        db.movies.delete_one({"_id": movie["_id"]})
        # Optional: Delete associated reviews to keep DB clean
        db.reviews.delete_many({"movie_id": movie["_id"]})
        print("Movie and associated reviews deleted.")
    else:
        print("Deletion cancelled.")

def review_movie():
    print("\n--- Add a Review ---")
    movie = select_movie()
    if not movie: return

    reviewer = input("Your Name: ").strip()
    if not reviewer:
        print("Cannot leave username blank")
    try:
        rating = float(input("Rating (1-10): "))
        if not (1 <= rating <= 10):
            print("Rating must be between 1 and 10.")
            return
    except ValueError:
        print("Rating must be a number.")
        return

    comment = input("Comment: ").strip()

    review_doc = {
        "movieId": movie["_id"],
        "userName": reviewer,
        "rating": rating,
        "reviewText": comment,
        "createdAt": datetime.now()
    }

    db.reviews.insert_one(review_doc)
    print(f"Review added for '{movie['title']}'.")

def see_movie_reviews():
    print("\n--- Read Reviews ---")
    movie = select_movie()
    if not movie: return

    reviews = list(db.reviews.find({"movieId": movie["_id"]}))
    
    if not reviews:
        print(f"No reviews found for {movie['title']}.")
        return

    # Calculate Average
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    print(f"\nAverage Rating: {avg_rating:.1f}/10 ({len(reviews)} reviews)")
    print("-" * 20)

    for r in reviews:
        print(f"User:    {r['userName']}")
        print(f"Rating:  {r['rating']}/10")
        print(f"Comment: {r['reviewText']}")
        print(f"Date:    {r['createdAt'].strftime('%Y-%m-%d')}")
        print("." * 20)

def edit_review():
    print("\n--- Edit a Review ---")
    # First pick the movie
    movie = select_movie()
    if not movie: return

    # Find reviews for this movie
    reviews = list(db.reviews.find({"movieId": movie["_id"]}))
    if not reviews:
        print("No reviews to edit for this movie.")
        return

    # Let user pick which review to edit
    for i, r in enumerate(reviews, 1):
        print(f"{i}. {r['userName']} - {r['rating']}/10 - '{r['reviewText'][:30]}...'")

    try:
        selection = int(input("\nSelect review number to edit: ")) - 1
        if not (0 <= selection < len(reviews)):
            print("Invalid selection.")
            return
        
        target_review = reviews[selection]
        
        print(f"Editing review by {target_review['userName']}")
        new_rating = input(f"New Rating (current: {target_review['rating']}): ")
        new_comment = input(f"New Comment (current: {target_review['reviewText']}): ")

        updates = {}
        if new_rating:
            updates["rating"] = float(new_rating)
        if new_comment:
            updates["reviewText"] = new_comment
        
        updates["createdAt"] = datetime.now() # Update timestamp

        if updates:
            db.reviews.update_one({"_id": target_review["_id"]}, {"$set": updates})
            print("Review updated.")
        else:
            print("No changes made.")

    except ValueError:
        print("Invalid input.")

def delete_review():
    print("\n--- Delete a Review ---")
    movie = select_movie()
    if not movie: return

    reviews = list(db.reviews.find({"movie_id": movie["_id"]}))
    if not reviews:
        print("No reviews to delete.")
        return

    for i, r in enumerate(reviews, 1):
        print(f"{i}. {r['userName']} - {r['rating']}/10 - '{r['reviewText'][:30]}...'")

    try:
        selection = int(input("\nSelect review number to delete: ")) - 1
        if not (0 <= selection < len(reviews)):
            print("Invalid selection.")
            return
        
        target_review = reviews[selection]
        db.reviews.delete_one({"_id": target_review["_id"]})
        print("Review deleted.")

    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()