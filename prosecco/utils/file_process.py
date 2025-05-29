def process_file_job(file_id):
    from prosecco.app import prosecco 
    from prosecco.config import db
    from prosecco.models import File_trk
    from prosecco.config import File_state

    with prosecco.app_context():
        file_record = db.session.query(File_trk).filter(File_trk.id == file_id).first()
        if not file_record:
            print(f'Arquivo {file_id} não encontrado para processamento.')
            return

        print(f"Processando arquivo: {file_record.filepath}")

        import time
        time.sleep(5)

        file_record.file_state = File_state.PROCESSED
        db.session.commit()

        print(f"Processamento finalizado para: {file_record.filepath}")
 