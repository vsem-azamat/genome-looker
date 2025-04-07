import io
import logging
import aiofiles
from pathlib import Path
from typing import Generator
from pybedtools import BedTool
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import FileResponse

from backend.schemas import JaccardResult, DatasetModel

logger = logging.getLogger(__name__)

class GenomeService:
    def __init__(self, datasets_dir: Path) -> None:
        self.datasets_dir = datasets_dir
        if not self.datasets_dir.exists():
            raise ValueError(f"Dataset directory {self.datasets_dir} does not exist.")
        if not self.datasets_dir.is_dir():
            raise ValueError(f"Dataset directory {self.datasets_dir} is not a directory.")

    def get_datasets(self) -> list[DatasetModel]:
        """
        Get a list of dataset files in the datasets directory.
        """
        return [
            DatasetModel(name=item.name) for item in self.datasets_dir.iterdir()
            if item.is_file() and item.suffix == ".bed"
        ]

    def get_dataset_paths(self) -> Generator[Path, None, None]:
        """
        Get a list of dataset files in the datasets directory.
        """
        for item in self.datasets_dir.iterdir():
            if item.is_file() and item.suffix == ".bed":
                yield item

    def calculate_jaccard(self, file: UploadFile, save: bool) -> list[JaccardResult]:
        """
        Find similar genomes to the uploaded file.
        """
        file_content = file.file.read()
        file.file.seek(0)
        self._validate_bed_file(file)

        file_string_io = io.StringIO(file_content.decode())
        bed_tool_target = BedTool(file_string_io).sort()
        results = []
        for dataset in self.get_dataset_paths():
            bed_tool_dataset = BedTool(dataset).sort()
            result = bed_tool_dataset.jaccard(bed_tool_target)
            result['dataset'] = dataset.name
            model = JaccardResult.model_validate(result)
            results.append(model)

        if save:
            try:
                self.upload_dataset_sync(file)
            except Exception as e:
                logger.warning(f"Failed to save dataset: {e}")

        return results

    async def download_dataset(self, dataset: str) -> FileResponse:
        """
        Download a dataset file.
        """
        dataset_path = self.datasets_dir / dataset
        if not dataset_path.exists():
            raise ValueError(f"Dataset {dataset} does not exist.")
        if not dataset_path.is_file():
            raise ValueError(f"Dataset {dataset} is not a file.")
        
        return FileResponse(dataset_path, media_type='application/octet-stream', filename=dataset)

    def _validate_bed_file(self, file: UploadFile) -> None:
        """
        Validate if the uploaded file is a valid BED file.
        """
        if file.filename is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is required.")
        if not file.filename.endswith('.bed'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be a .bed file.")
        file_string_io = io.StringIO(file.file.read().decode())
        bed_tool = BedTool(file_string_io)
        try:
            bed_tool.sort()
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is not a valid BED file.")

    def upload_dataset_sync(self, file: UploadFile) -> Path:
        """
        Upload a dataset file synchronously.
        """
        self._validate_bed_file(file)
        dataset_path = self.datasets_dir / file.filename # type: ignore
        if dataset_path.exists():
            raise ValueError(f"Dataset {file.filename} already exists.")
        with open(dataset_path, 'wb') as out_file:
            file.file.seek(0)
            content = file.file.read()
            out_file.write(content)
        return dataset_path

    async def upload_dataset(self, file: UploadFile) -> Path:
        """
        Upload a dataset file.
        """
        self._validate_bed_file(file)
        dataset_path = self.datasets_dir / file.filename # type: ignore
        if dataset_path.exists():
            raise ValueError(f"Dataset {file.filename} already exists.")
        
        async with aiofiles.open(dataset_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return dataset_path

    def delete_dataset(self, dataset: str) -> None:
        """
        Delete a dataset file.
        """
        dataset_path = self.datasets_dir / dataset
        if not dataset_path.exists():
            raise ValueError(f"Dataset {dataset} does not exist.")
        if not dataset_path.is_file():
            raise ValueError(f"Dataset {dataset} is not a file.")
        
        dataset_path.unlink()
