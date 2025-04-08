from models import Todo
from datetime import datetime

def test_todo_creation(db):
    todo = Todo(title='Test Todo', description='Test Description')
    db.session.add(todo)
    db.session.commit()

    assert todo.id is not None
    assert todo.title == 'Test Todo'
    assert todo.description == 'Test Description'
    assert todo.completed == False
    assert isinstance(todo.created_at, datetime)
    assert isinstance(todo.updated_at, datetime)

def test_todo_to_dict(db):
    todo = Todo(title='Test Todo', description='Test Description')
    db.session.add(todo)
    db.session.commit()

    todo_dict = todo.to_dict()
    assert todo_dict['id'] == todo.id
    assert todo_dict['title'] == 'Test Todo'
    assert todo_dict['description'] == 'Test Description'
    assert todo_dict['completed'] == False
    assert isinstance(todo_dict['created_at'], str)
    assert isinstance(todo_dict['updated_at'], str) 