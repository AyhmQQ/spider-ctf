import os
import magic

class Ingestor:
    def __init__(self, max_file_size=1024*1024, max_files=50):
        try:
            self.mime = magic.Magic(mime=True)
        except Exception:
            self.mime = None
        self.max_file_size = max_file_size
        self.max_files = max_files

    def classify_file(self, filepath):
        mime_type = "unknown"
        if self.mime:
            try:
                mime_type = self.mime.from_file(filepath)
            except Exception:
                pass
        
        file_extension = os.path.splitext(filepath)[1].lower()

        if 'python' in mime_type or file_extension == '.py':
            return 'python_source'
        elif 'text' in mime_type or file_extension in ['.txt', '.log', '.md']:
            return 'text'
        elif 'json' in mime_type or file_extension == '.json':
            return 'structured_data'
        elif file_extension in ['.pem', '.pub']:
            return 'key_material'
        elif 'binary' in mime_type or file_extension in ['.enc', '.bin']:
            return 'binary'
        else:
            return 'unknown'

    def ingest(self, paths):
        files_to_process = []
        for path in paths:
            if os.path.isfile(path):
                files_to_process.append(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        files_to_process.append(os.path.join(root, file))
                        if len(files_to_process) >= self.max_files: break
            if len(files_to_process) >= self.max_files: break

        ingested_data = []
        for filepath in files_to_process:
            if os.path.getsize(filepath) > self.max_file_size:
                continue
            
            file_type = self.classify_file(filepath)
            try:
                with open(filepath, 'rb') as f:
                    raw_content = f.read()
                try:
                    content = raw_content.decode('utf-8')
                except UnicodeDecodeError:
                    content = raw_content.hex()
                
                ingested_data.append({
                    'filepath': filepath,
                    'type': file_type,
                    'content': content
                })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
        
        return ingested_data
