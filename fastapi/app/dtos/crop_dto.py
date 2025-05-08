from pydantic import BaseModel


class AddCropRequestDTO(BaseModel):
    group_id: int
    name: str
    humid: str
    type: str


class CropDTO(BaseModel):
    crop_id: int
    group_id: int
    name: str
    humid: str
    type: str


class GetCropListRequestDTO(BaseModel):
    group_id: int


class GetCropListResponseDTO(BaseModel):
    crops: list[CropDTO]
