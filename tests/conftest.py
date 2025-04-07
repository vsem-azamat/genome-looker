import io
import random
import pytest
from pathlib import Path
from fastapi import UploadFile

from backend.core.config import cnfg
from backend.core.dependencies import GenomeService

@pytest.fixture
def real_genome_service() -> GenomeService:
    service = GenomeService(datasets_dir=Path(cnfg.DATASETS_DIR))
    return service

@pytest.fixture
def randomized_genome_deb_file(real_genome_service: GenomeService) -> UploadFile:
    datasets = list(real_genome_service.get_dataset_paths())
    assert len(datasets) > 0, "No datasets found in the directory."

    mixed_rows = []
    for dataset in datasets:
        with open(dataset, "r") as f:
            lines = f.readlines()
            rows = random.sample(lines, min(100, len(lines)))
            mixed_rows.extend(rows)
    random.shuffle(mixed_rows)
    mixed_file = io.StringIO()
    mixed_file.write("".join(mixed_rows))
    mixed_file.seek(0)
    mixed_file.name = "randomized_genome.bed"
    
    mock_file = UploadFile(
        filename=mixed_file.name,
        file=io.BytesIO(mixed_file.getvalue().encode()),
    )
    return mock_file

@pytest.fixture
def bad_genome_deb_file() -> UploadFile:
    """
    Create a mock file that is not a valid BED file.
    """
    bad_file = io.StringIO("This is not a valid BED file.")
    bad_file.name = "bad_genome.bed"
    
    mock_file = UploadFile(
        filename=bad_file.name,
        file=io.BytesIO(bad_file.getvalue().encode()),
    )
    return mock_file
