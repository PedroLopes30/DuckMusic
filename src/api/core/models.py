from sqlmodel import SQLModel , Field

class BaseModel(SQLModel):
    id : int | None = Field(
        title="id",
        default=None,
        primary_key=True,
    )