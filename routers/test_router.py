from fastapi import APIRouter, HTTPException
from schemas.test_schema import TestCreate, TestResponse
from logger.logger import get_logger



logger = get_logger(__file__)
router = APIRouter()



@router.post(path="/test")
async def test(test : TestCreate) -> TestResponse:
    logger.debug(f"Test : {test}")
    return test
