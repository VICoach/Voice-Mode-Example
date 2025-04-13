from pydantic import BaseModel
from logger.logger import get_logger
from fastapi import UploadFile


logger = get_logger(__file__)

class TestBase(BaseModel):
    name: str

class TestCreate(TestBase):
    pass

class TestUpdate(TestBase):
    pass

class TestResponse(TestBase):
    pass