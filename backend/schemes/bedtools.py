from pydantic import BaseModel

class JaccardResult(BaseModel):
    dataset: str
    intersection: int
    union: int
    jaccard: float
    n_intersections: int
