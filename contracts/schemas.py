from typing import List, Literal
from pydantic import BaseModel


class ClothingItem(BaseModel):
    """Metadata extracted by the vision model for one clothing item."""

    cloth_id: str
    category: Literal["Top", "Bottom", "Footwear", "Outerwear", "Accessory"]
    subcategory: str  # e.g. Shirt, Jeans, Sneakers
    color_name: str
    color_embedding: List[float] | None = None       #make it optional
    pattern: str
    fabric: str
    fit: str
    texture: str
    sleeve: str | None = None
    neck: str | None = None
    season: List[Literal["Spring", "Summer", "Autumn", "Winter"]]
    style_tags: List[str]
    occasion_tags: List[str]    #this comes from model but not reliable now, so use mock data 
    img_url: str


class Wardrobe(BaseModel):
    """A user's wardrobe."""

    user_id: str
    items: List[ClothingItem]


class WeatherContext(BaseModel):
    city: str
    temperature: float      # in Celsius
    condition: str          # e.g. "Sunny", "Rainy", "Cloudy"
    season: Literal["Spring", "Summer", "Autumn", "Winter"]



class UserRequest(BaseModel):
    """Inputs provided when requesting an outfit recommendation."""
    user_id: str
    mood: Literal[
        "Happy",
        "Confident",
        "Classy",
        "Casual",
        "Sporty",
    ]
    occasion: Literal[
        "Work",
        "Meeting",
        "Party",
        "Festival",
        "Date",
        "Travel",
        "Day Out",
        "Casual",
        "wedding",
        "interview"
    ]
    city: str       #weather api needs city 



class UserPreference(BaseModel):
    user_id: str
    preferred_styles: List[str]        # e.g. ["Minimal", "Casual"]
    disliked_styles: List[str]         # e.g. ["Streetwear", "Bohemian"]  
    preferred_colors: List[str]        # e.g. ["Black", "White", "Navy"]
    avoided_colors: List[str]          # e.g. ["Neon", "Orange"]
    fit_preference: str                # e.g. "Slim", "Oversized", "Regular"
    additional_notes: str | None = None  # freeform — "I like to look approachable but not boring"


class OutfitScore(BaseModel):
    score: int          # 0-100
    reasoning: str      # why this score was given


class FeedbackRequest(BaseModel):
    user_id: str
    outfit_reasoning: str
    user_score: int        # user's rating 1-5
    score_reasoning: str   # AI's scoring reasoning
           
    