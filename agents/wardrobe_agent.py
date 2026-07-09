import json
from pathlib import Path
from typing import List
from contracts.schemas import Wardrobe, ClothingItem

DATA_PATH = Path(__file__).parent.parent / "mock_data" / "wardrobe.json"

def get_wardrobe(user_id: str) -> List[ClothingItem]:
    """Fetch wardrobe items for a given user from mock data."""
    
    with open(DATA_PATH, "r") as f:
        raw = json.load(f)
    
    wardrobe = Wardrobe(**raw)
    
    if wardrobe.user_id != user_id:
        return []
    
    return wardrobe.items

# if __name__ == "__main__":
#     items = get_wardrobe("user_001")
#     print(f"Found {len(items)} items")
#     print(items[0])