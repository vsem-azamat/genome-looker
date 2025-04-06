import io
from typing import Generator
from pathlib import Path
from pybedtools import BedTool
from fastapi import UploadFile

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
            model = JaccardResult.model_validate(result)
            results.append(model)
        return results
