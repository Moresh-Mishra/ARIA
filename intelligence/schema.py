from pydantic import BaseModel, Field


class Parameters(BaseModel):
    date: str | None = None
    time: str | None = None
    location: str | None = None
    title: str | None = None
    content: str | None = None


class Intent(BaseModel):
    intent: str = Field(
        description="The action the user wants to perform."
    )

    task: str = Field(
        description="A concise description of what the user wants done."
    )

    parameters: Parameters

    missing_information: list[str] = Field(
        default_factory=list
    )

    requires_confirmation: bool