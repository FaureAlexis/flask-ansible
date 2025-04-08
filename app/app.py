import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Todo
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'sqlite:///todos.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
        return render_template('index.html', todos=todos)

    @app.route('/todo', methods=['POST'])
    def add_todo():
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('Title is required!', 'error')
            return redirect(url_for('index'))
        
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        
        flash('Todo added successfully!', 'success')
        return redirect(url_for('index'))

    @app.route('/todo/<int:id>/toggle', methods=['POST'])
    def toggle_todo(id):
        todo = Todo.query.get_or_404(id)
        todo.completed = not todo.completed
        db.session.commit()
        return jsonify(todo.to_dict())

    @app.route('/todo/<int:id>', methods=['DELETE'])
    def delete_todo(id):
        todo = Todo.query.get_or_404(id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    @app.route('/health')
    def health_check():
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            return jsonify({
                'status': 'healthy',
                'database': 'connected'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'database': str(e)
            }), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 