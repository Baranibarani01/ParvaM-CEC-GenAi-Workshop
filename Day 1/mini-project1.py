# Average Rating Calculator

def rate_movies(**ratings):
    if not ratings:
        print("No movies rated yet!")
        return

    total = sum(ratings.values())
    count = len(ratings)
    average = total / count

    print(f"🎬 {count} movies rated")
    print(f"⭐ Average rating: {average:.1f}/10")
    print("\nRatings:")

    for movie, rating in ratings.items():
#alt+9734(⭐), 
        stars = "★" * (rating // 2) + "☆" * (5 - (rating // 2))
        print(f"{movie}: {rating}/10 {stars}")

    # Find best movie
    best = max(ratings, key=ratings.get)
    print(f"\n🏆 Best movie: {best} ({ratings[best]}/10)")


# Example usage
rate_movies(
    Inception=9,
    Avatar=7,
    Dune=8,
    Avengers=9
)
