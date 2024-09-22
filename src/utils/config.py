gcs_temp_location = 'gs://bucket_alexandre_teste/temp/'

schema={
        'fields': [
            {'name': 'uuid', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'embeddings', 'type': 'FLOAT', 'mode': 'REPEATED'},
            {'name': 'content', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'chunk_number', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'file_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'mime_type', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'gs_uri', 'type': 'STRING', 'mode': 'NULLABLE'}
        ]
    }