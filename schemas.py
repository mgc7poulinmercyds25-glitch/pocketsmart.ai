from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


PlannerType = Literal["home", "party", "jewelry"]


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: str
    password: str


class HomeRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1)
    style: str = Field(default="Modern", min_length=1, max_length=100)
    notes: str = Field(default="", max_length=1000)
    quantities: dict[str, int] = Field(default_factory=dict)

    @field_validator("quantities")
    @classmethod
    def positive_quantities(cls, value):
        return {str(k): max(0, int(v)) for k, v in value.items()}


class PartyRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    event_type: str = Field(min_length=2, max_length=100)
    guests: int = Field(gt=0, le=100_000)
    venue: str = Field(default="Not decided", max_length=200)
    city: str = Field(default="", max_length=100)
    notes: str = Field(default="", max_length=1000)


class RecommendationItem(BaseModel):
    name: str
    category: str
    estimated_price: int
    platform: str
    search_url: str
    reason: str
    quantity: int = 1


class RecommendationResponse(BaseModel):
    planner: PlannerType
    title: str
    budget: int
    estimated_total: int
    remaining_budget: int
    summary: str
    budget_breakdown: dict[str, int]
    recommendations: list[RecommendationItem]
    ai_powered: bool = False
    disclaimer: str


class JewelryRequest(BaseModel):
    budget: int = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="Elegant", min_length=1, max_length=100)
    outfit_description: str = Field(default="", max_length=1000)
