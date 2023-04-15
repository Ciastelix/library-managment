from fastapi.testclient import TestClient
from ..main import app
from ..app.schemas import AuthorSchemaIn, BookSchemaIn, LibrarySchemaIn

client = TestClient(app)


# Test root route
def test_root():
    response = client.get("/")
    assert response.status_code == 200


# Test book routes
def test_create_and_get_book():
    book_data = {"name": "Sample Book", "written_at": "2023-04-15"}
    response = client.post("/book", json=book_data)
    assert response.status_code == 201
    book_id = response.json()["id"]

    response = client.get(f"/book?id={book_id}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == book_data["name"]


def test_update_and_delete_book():
    book_data = {"name": "Sample Book", "written_at": "2023-04-15"}
    response = client.post("/book", json=book_data)
    assert response.status_code == 201
    book_id = response.json()["id"]

    updated_book_data = {"name": "Updated Book", "written_at": "2023-04-15"}
    response = client.put(f"/book?id={book_id}", json=updated_book_data)
    assert response.status_code == 200

    response = client.get(f"/book?id={book_id}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == updated_book_data["name"]

    response = client.delete(f"/book?id={book_id}")
    assert response.status_code == 200


# Test author routes
def test_create_and_get_author():
    author_data = {"name": "John Doe"}
    response = client.post("/author", json=author_data)
    assert response.status_code == 201
    author_id = response.json()["id"]

    response = client.get(f"/author?id={author_id}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == author_data["name"]


def test_update_and_delete_author():
    author_data = {"name": "John Doe"}
    response = client.post("/author", json=author_data)
    assert response.status_code == 201
    author_id = response.json()["id"]

    updated_author_data = {"name": "Jane Doe"}
    response = client.put(f"/author?id={author_id}", json=updated_author_data)
    assert response.status_code == 200

    response = client.get(f"/author?id={author_id}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == updated_author_data["name"]

    response = client.delete(f"/author?id={author_id}")
    assert response.status_code == 200


# Test library routes
def test_create_and_get_library():
    library_data = {"name": "Sample Library", "city": "Sample City"}
    response = client.post("/library", json=library_data)
    assert response.status_code == 201
    library_id = response.json()["id"]

    response = client.get(f"/libary?id={library_id}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == library_data["name"]


def test_update_and_delete_library():
    library_data = {"name": "Sample Library", "city": "Sample City"}
    response = client.post("/library", json=library_data)
    assert response.status_code == 201
    library_id = response.json()["id"]

    updated_library_data = {"name": "Updated Library", "city": "Updated City"}
    response = client.put(f"/library?id={library_id}", json=updated_library_data)
    assert response.status_code == 200

    response = client.get(f"/libary?id={library_id}")
    assert response.status_code == 200
    assert response.json()[0]["name"] == updated_library_data["name"]

    response = client.delete(f"/library?id={library_id}")
    assert response.status_code == 200
