from models import Todo

def test_index_route(client, db):
    response = client.get('/')
    assert response.status_code == 200

def test_add_todo(client, db):
    response = client.post('/todo', data={
        'title': 'Test Todo',
        'description': 'Test Description'
    })
    assert response.status_code == 302  # Redirect
    todo = Todo.query.first()
    assert todo.title == 'Test Todo'
    assert todo.description == 'Test Description'

def test_toggle_todo(client, db):
    # Create a todo first
    todo = Todo(title='Test Todo')
    db.session.add(todo)
    db.session.commit()

    response = client.post(f'/todo/{todo.id}/toggle')
    assert response.status_code == 200
    assert response.json['completed'] == True

def test_delete_todo(client, db):
    # Create a todo first
    todo = Todo(title='Test Todo')
    db.session.add(todo)
    db.session.commit()

    response = client.delete(f'/todo/{todo.id}')
    assert response.status_code == 204
    assert Todo.query.count() == 0

def test_health_check(client, db):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
    assert response.json['database'] == 'connected' 