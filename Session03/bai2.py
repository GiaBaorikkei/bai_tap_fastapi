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

@app.get("/books/available")
def get_books_available():
    list_books_available = []
    for i in books:
        if i["is_available"] == False:
            list_books_available.append(i)
    return {
        "message": "Danh sách sách đang được mượn",
        "data": list_books_available
    }

@app.get("/books/borrowed")
def get_books_borrowed():
    list_books_borrowed = []
    for j in books:
        if j["is_available"] == True:
            list_books_borrowed.append(j)
    return {
        "message": "Danh sách sách có thể mượn",
        "data": list_books_borrowed
    }


