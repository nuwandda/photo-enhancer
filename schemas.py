import pydantic as _pydantic
from typing import List


class _EnhanceBase(_pydantic.BaseModel):
    encoded_base_img: List[str]
