from fastapi import APIRouter

from zimplorer.routes.schemas import DummyData

router = APIRouter(
    prefix="/dummy",
    tags=["all"],
)


@router.get(
    "",
    responses={
        200: {
            "description": "Returns a dummy value",
        },
        404: {"description": "Dummy value not found"},
    },
)
async def home() -> DummyData:
    return DummyData(value="something")
