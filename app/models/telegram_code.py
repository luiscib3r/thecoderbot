from pydantic import BaseModel, Field
from typing import Union


class TelegramCode(BaseModel):
    x_message_id: str = Field(alias="id")
    x_text: str = Field(alias="text")
    x_chat_id: str = Field(alias="chat_id")
    x_from_id: str = Field(alias="from_id")
    x_date: str = Field(alias="date")
    x_image: Union[str, bool] = Field(False, alias="image")

    class Config:
        allow_population_by_field_name = True
