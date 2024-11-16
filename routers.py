from fastapi import APIRouter
from schemas import STaskAdd, STask, STaskId
from pydantic.types import Annotated
from fastapi.param_functions import Depends
from repository import TaskRepository

router = APIRouter(
    prefix="/tasks",
    tags=["Tacki"],
)


@router.post("")
async def add_task(
    task: Annotated[STaskAdd, Depends()]
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return{"ok": True, "task_id" : task_id}

@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks