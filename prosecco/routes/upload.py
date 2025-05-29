from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
import uuid
import os
from prosecco.config import db, scheduler, File_state
from prosecco.models import File_trk
from prosecco.utils import process_file_job

upload_route = Blueprint('upload', __name__)

@upload_route.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify(success=False, error='Nenhum arquivo enviado'), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, error='Arquivo sem nome'), 400

    chosen_name = request.form.get('filename')
    filename = chosen_name if chosen_name else file.filename


    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

 
    file.save(file_path)

    new_file = File_trk(user_id=current_user.id, filename=filename, filepath=file_path, file_state=File_state.UPLOADED) #type:ignore

    db.session.add(new_file)
    db.session.commit()

    scheduler.add_job(
        id=f'process_file_{new_file.id}',
        func=process_file_job,
        args=[new_file.id],
        trigger='date'
    )

    return jsonify(success=True, message='Upload recebido e processamento iniciado', file_id=new_file.id), 202
