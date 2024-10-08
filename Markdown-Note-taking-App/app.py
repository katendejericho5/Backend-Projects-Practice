from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from markdown import markdown
from flask_migrate import Migrate
import language_tool_python

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

tool = language_tool_python.LanguageTool('en-US')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Note {self.title}>"

@app.route('/check-grammar', methods=['POST'])
def check_grammar():
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "No content provided"}), 400

    # Check grammar using LanguageTool
    matches = tool.check(content)
    errors = [
        {
            "message": match.message,
            "suggestions": match.replacements,
            "offset": match.offset,
            "length": match.errorLength
        }
        for match in matches
    ]

    return jsonify({"errors": errors})

@app.route('/save-note', methods=['POST'])
def save_note():
    content = request.json.get('content')
    title = request.json.get('title')
    if not content or not title:
        return jsonify({"error": "Title and content are required"}), 400

    note = Note(title=title, content=content)
    db.session.add(note)
    db.session.commit()

    return jsonify({"message": "Note saved successfully", "note_id": note.id})

@app.route('/notes', methods=['GET'])
def list_notes():
    notes = Note.query.all()
    return jsonify([{"id": note.id, "title": note.title} for note in notes])

@app.route('/render-note/<int:note_id>', methods=['GET'])
def render_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    html_content = markdown(note.content)
    return render_template('note.html', content=html_content)

if __name__ == '__main__':
    app.run(debug=True)
