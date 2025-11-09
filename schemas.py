"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- ChildProfile -> "childprofile" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Example schemas (kept for reference):
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Application schemas
class ChildProfile(BaseModel):
    """
    Child profiles for onboarding and personalization
    Collection: "childprofile"
    """
    nickname: str = Field(..., min_length=2, max_length=24, description="Child display nickname")
    age_group: str = Field(..., description="One of: 6-8, 9-12, 13-15")
    parent_email: EmailStr = Field(..., description="Parent/guardian email for consent")
    eco_points: int = Field(0, ge=0, description="Gamified points for progress")
