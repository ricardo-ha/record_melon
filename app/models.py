from pydantic import BaseModel

class Reminder(BaseModel):
    datetime_: str
    task: str
    

