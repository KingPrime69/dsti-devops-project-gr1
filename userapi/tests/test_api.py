def test_create_user(client):
    r = client.post("/users", json={"username": "pascal", "email": "pascal@example.com"})
    assert r.status_code == 201
    assert r.json()["id"]

def test_create_double(client):
    payload = {"username": "jean", "email": "jean@example.com"}
    client.post("/users", json=payload)
    r = client.post("/users", json=payload)
    assert r.status_code == 409

def test_get_user(client):
    created = client.post("/users", json={"username": "anna", "email": "anna@example.com"}).json()
    r = client.get(f"/users/{created['id']}")
    assert r.status_code == 200
    assert r.json()["username"] == "anna"

def test_missing_user(client):
    assert client.get("/users/9999999").status_code == 404

def test_update_user(client):
    created = client.post("/users", json={"username": "martine", "email": "martine@example.com"}).json()
    r = client.patch(f"/users/{created['id']}", json={"email": "martine.2@example.com"})
    assert r.json()["email"] == "martine.2@example.com"

def test_delete_user(client):
    created = client.post("/users", json={"username": "jack", "email": "jack@example.com"}).json()
    assert client.delete(f"/users/{created['id']}").status_code == 204
    assert client.get(f"/users/{created['id']}").status_code == 404