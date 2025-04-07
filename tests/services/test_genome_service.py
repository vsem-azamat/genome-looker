import pytest
from pathlib import Path
from fastapi import UploadFile
from fastapi import HTTPException

from backend.schemes import JaccardResult, DatasetModel
from backend.core.dependencies import GenomeService

def test_get_datasets(real_genome_service: GenomeService):
    dataset_list = real_genome_service.get_datasets()
    assert isinstance(dataset_list, list)
    assert len(dataset_list) > 0
    assert all(isinstance(dataset, DatasetModel) for dataset in dataset_list)

    for dataset in dataset_list:
        assert isinstance(dataset.name, str)
        assert dataset.name.endswith(".bed")
        assert (real_genome_service.datasets_dir / dataset.name).exists()

def test_get_dataset_paths(real_genome_service: GenomeService):
    dataset_list = list(real_genome_service.get_dataset_paths())
    assert isinstance(dataset_list, list)
    assert len(dataset_list) > 0
    assert all(isinstance(dataset, Path) for dataset in dataset_list)

def test_validate_bed_file(
    real_genome_service: GenomeService,
    bad_genome_deb_file: UploadFile,
    randomized_genome_deb_file: UploadFile,
):
    with pytest.raises(HTTPException):
        real_genome_service._validate_bed_file(bad_genome_deb_file)

    try:
        real_genome_service._validate_bed_file(randomized_genome_deb_file)
    except HTTPException:
        pytest.fail("Validation failed for a valid BED file.")

def test_calculate_jaccard(
    real_genome_service: GenomeService,
    randomized_genome_deb_file: UploadFile,
):
    result = real_genome_service.calculate_jaccard(
        file=randomized_genome_deb_file,
        save=False,
    )
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(item, JaccardResult) for item in result)
