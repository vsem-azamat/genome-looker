from pydantic import BaseModel

class JaccardResult(BaseModel):
    intersection: int
    union: int
    jaccard: float
    n_intersections: int
    