
import os 
import datetime


class local_ops:

    def ls(local_folder:str) -> list[dict]:
        """ls is function get the recursive list of the given folder """
        files_data = []
        for foldername, _, filenames in os.walk(local_folder):
            for filename in filenames:
                full_path = os.path.join(foldername, filename)
                relative_path = os.path.relpath(full_path, local_folder)
                
                # Get file size in bytes
                file_size = os.path.getsize(full_path)

                # Get last modified time in ISO 8601 format
                last_modified_timestamp = os.path.getmtime(full_path)
                last_modified = datetime.datetime.fromtimestamp(last_modified_timestamp)

                dt_utc = last_modified.astimezone(datetime.timezone.utc)

                last_modified_iso = dt_utc.isoformat()[:-9] + 'Z'

                files_data.append({
                    'name': filename,
                    'path': relative_path,
                    'size': file_size,
                    'modtime': last_modified_iso 
                })
        return files_data

