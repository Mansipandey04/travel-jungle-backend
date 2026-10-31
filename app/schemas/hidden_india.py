from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import LayerBlock


class HiddenIndiaBase(BaseModel):
    slug: str = Field(min_length=1, max_length=120)
    destination_id: int
    title: str = Field(min_length=1, max_length=200)
    tagline: str = Field(min_length=1, max_length=300)
    layer_discover: LayerBlock | dict[str, Any]
    layer_experience: LayerBlock | dict[str, Any]
    layer_explore: LayerBlock | dict[str, Any]
    is_published: bool = True
    is_demo: bool = False


class HiddenIndiaCreate(HiddenIndiaBase):
    pass


class HiddenIndiaUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=1, max_length=120)
    destination_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    tagline: str | None = Field(default=None, min_length=1, max_length=300)
    layer_discover: LayerBlock | dict[str, Any] | None = None
    layer_experience: LayerBlock | dict[str, Any] | None = None
    layer_explore: LayerBlock | dict[str, Any] | None = None
    is_published: bool | None = None
    is_demo: bool | None = None


class HiddenIndiaOut(HiddenIndiaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
