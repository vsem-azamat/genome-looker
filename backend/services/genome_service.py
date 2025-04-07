import io
from typing import Generator
from pathlib import Path
from pybedtools import BedTool
from fastapi import UploadFile
from fastapi.responses import FileResponse

from backend.schemes import JaccardResult

class GenomeService:
    def __init__(self, datasets_dir: Path) -> None:
        self.datasets_dir = datasets_dir
        if not self.datasets_dir.exists():
            raise ValueError(f"Dataset directory {self.datasets_dir} does not exist.")
        if not self.datasets_dir.is_dir():
            raise ValueError(f"Dataset directory {self.datasets_dir} is not a directory.")

    def get_datasets(self) -> Generator[Path, None, None]:
        """
        Get a list of dataset files in the datasets directory.
        """
        for item in self.datasets_dir.iterdir():
            if item.is_file() and item.suffix == ".bed":
                yield item

    def calculate_jaccard(self, file: UploadFile) -> list[JaccardResult]:
        """
        Find similar genomes to the uploaded file.
        """
        file_string_io = io.StringIO(file.file.read().decode())
        bed_tool_target = BedTool(file_string_io).sort()
        results = []
        for dataset in self.get_datasets():
            bed_tool_dataset = BedTool(dataset).sort()
            result = bed_tool_dataset.jaccard(bed_tool_target)
            result['dataset'] = dataset.name
            model = JaccardResult.model_validate(result)
            results.append(model)
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
