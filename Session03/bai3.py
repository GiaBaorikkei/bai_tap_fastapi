from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Tran Van B",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Learning Java",
        "author": "Nguyễn Văn Nam",
        "category": "programming",
        "year": 2023,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Data Science Handbook",
        "author": "Trần Thị Mai",
        "category": "data science",
        "year": 2022,
        "is_available": False
    },
    {
        "id": 5,
        "title": "Introduction to Cyber Security",
        "author": "Lê Quốc Huy",
        "category": "security",
        "year": 2024,
        "is_available": True
    }
]

@app.get("/books/statistics")
def get_statistics():
    total_books = 0
    available_books = 0
    borrowed_books = 0

    for book in books:
        total_books += 1

        if book["is_available"] == True:
            available_books += 1
        else:
            borrowed_books += 1

    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books
    }
    
@app.get("/books/categories")
def get_categories():
    categories = []

    for book in books:
        if book["category"] not in categories:
            categories.append(book["category"])

    return {
        "categories": categories
    }
    
@app.get("/books/latest")
def get_latest_book():
    if len(books) == 0:
        return {
            "message": "No books available"
        }

    latest_book = books[0]

    for book in books:
        if book["year"] > latest_book["year"]:
            latest_book = book

    return latest_book