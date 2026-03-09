import os
from uuid import uuid4


def save_upload(upload_file, base_dir: str) -> str:
    ext = upload_file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    path = os.path.join(base_dir, filename)

    with open(path, "wb") as f:
        f.write(upload_file.file.read())

    return path