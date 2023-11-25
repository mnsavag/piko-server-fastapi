from fastapi import HTTPException, UploadFile, status
from pydantic import BaseModel
import os
from os.path import abspath
import aiofiles
import uuid


class ContestDirPaths(BaseModel):
    root_system_path: str
    preview_dir: str
    options_dir: str


class FileService:
    async def create_file(
            self,
            path_to_assets_dir: str,
            path_to_server_dir: str,
            _file: UploadFile
        ) -> str:

        system_path = os.path.join(path_to_assets_dir, path_to_server_dir)
        try:
            if not os.path.isdir(system_path):
                os.makedirs(system_path)

            file_name = str(uuid.uuid4()) + "." + _file.filename.split(".")[-1]
            full_path = os.path.join(system_path, file_name)

            async with aiofiles.open(full_path, 'wb') as out_file:
                content = await _file.read()
                await out_file.write(content)
        except Exception:
            raise Exception()
        
        return os.path.join(path_to_server_dir, file_name)

    async def get_paths_to_save_contest_image(
            self, 
            user_id: int | None, 
            contest_id: int | None) -> ContestDirPaths:
        
        file_system_path = abspath("./src/assets")

        contest_dir_name = str(contest_id) if contest_id else str(uuid.uuid4())
        contest_owner = str(user_id) if user_id else "community"

        path_to_contest_dir = os.path.join("contests", contest_owner, contest_dir_name)
        path_to_preview = os.path.join(path_to_contest_dir, "preview")
        path_to_options = os.path.join(path_to_contest_dir, "options")
        
        return ContestDirPaths(
            root_system_path=file_system_path,
            preview_dir=path_to_preview,
            options_dir=path_to_options
        )

        """Доделать api, оформить git, адаптировать frontend под snake_case, проверить и всё"""