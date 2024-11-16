from database import new_session, TaskOrm
from schemas import STaskAdd, STask
from sqlalchemy import select


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id
        

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            tasks_models = result.scalars().all()
            tasks_schemas = [STask.model_validate(task_model) for task_model in tasks_models]
            return tasks_schemas


