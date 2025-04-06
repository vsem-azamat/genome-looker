from pathlib import Path
from fastapi import UploadFile

from backend.schemes import JaccardResult
from backend.core.dependencies import GenomeService

def test_get_datasets(real_genome_service: GenomeService):
    dataset_list = list(real_genome_service.get_datasets())
    assert isinstance(dataset_list, list)
    assert len(dataset_list) > 0
    assert all(isinstance(dataset, Path) for dataset in dataset_list)

def test_calculate_jaccard(
    real_genome_service: GenomeService,
    randomized_genome_deb_file: UploadFile,
):
    result = real_genome_service.calculate_jaccard(
        randomized_genome_deb_file,
    )
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(item, JaccardResult) for item in result)
