# This file is where we store the standard routes for all location of the website
# Routes related to authentication are in auth.py

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note
from . import db
import json

views_blueprint = Blueprint('views_str', __name__)

@views_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
        return redirect(url_for('views_str.home')) # stops from submitting form again on page refresh

    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.index)
    return render_template('home.html', user=current_user, notes=notes)

@views_blueprint.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data) # converts json formatted string to python dictionary
    noteId = data['noteId']
    note = Note.query.get(noteId) # .get(noteId) is the same as .filter_by(id=noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
            # returns an empty response to the .then function runs in javascript
        
@views_blueprint.route('/sort-database', methods=['POST'])
def sort_database():
    data = json.loads(request.data)
    note_ids = data['note_ids']

    i = 0
    for note_id in note_ids:
        db.session.query(Note).get(note_id).index = i
        i += 1
    db.session.commit()

    return jsonify({})