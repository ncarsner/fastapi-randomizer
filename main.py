import random
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Tags metadata for API documentation
tags_metadata = [
    {
        "name": "Random Playground",
        "description": "Generate random numbers",
    },
    {
        "name": "Random Items Management",
        "description": "Create, shuffle, read, update and delete items",
    },
]

app = FastAPI(
    title="Randomizer API",
    description="Shuffle lists, pick random items, and generate random numbers.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "https://example.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory database
items_db = []
items_db_set = set()

# Pydantic models
class Item(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="The item name"
    )

class BulkItemsRequest(BaseModel):
    names: list[str] = Field(
        min_length=1,
        max_length=500,
        description="List of item names"
    )

class ItemResponse(BaseModel):
    message: str
    item: str

class ItemListResponse(BaseModel):
    original_order: list[str]
    randomized_order: list[str]
    count: int

class ItemUpdateResponse(BaseModel):
    message: str
    old_item: str
    new_item: str

class ItemDeleteResponse(BaseModel):
    message: str
    deleted_item: str
    remaining_items_count: int

class BulkItemsAddResponse(BaseModel):
    message: str
    added_items: list[str]
    skipped_duplicates: list[str]
    count_added: int
    count_skipped: int

class BulkItemsDeleteResponse(BaseModel):
    message: str
    deleted_count: int
    remaining_items_count: int

# Endpoints
@app.get("/", tags=["Random Playground"])
async def home():
    return FileResponse("static/index.html")

@app.get("/random/{max_value}", tags=["Random Playground"])
async def get_random_number(max_value: int):
    return {
        "max": max_value,
        "random_number": random.randint(1, max_value)
    }

@app.get("/random-between", tags=["Random Playground"])
async def get_random_number_between(
        min_value: Annotated[int, Query(
            title="Minimum Value",
            description="The minimum random number",
            ge=1,
            le=1000000
        )] = 1,
        max_value: Annotated[int, Query(
            title="Maximum Value",
            description="The maximum random number",
            ge=1,
            le=1000000
        )] = 99
    ):
    if min_value > max_value:
        raise HTTPException(status_code=400, detail="min_value can't be greater than max_value")

    return {
        "min": min_value,
        "max": max_value,
        "random_number": random.randint(min_value, max_value)
    }

@app.post("/items", response_model=ItemResponse, tags=["Random Items Management"])
async def add_item(item: Item):
    if item.name in items_db_set:
        raise HTTPException(status_code=400, detail="Item already exists")

    items_db.append(item.name)
    items_db_set.add(item.name)
    return ItemResponse(
        message="Item added successfully",
        item=item.name
    )

@app.post("/items/bulk", response_model=BulkItemsAddResponse, tags=["Random Items Management"])
async def add_items_bulk(payload: BulkItemsRequest):
    added_items: list[str] = []
    skipped_duplicates: list[str] = []

    for index, raw_name in enumerate(payload.names):
        name = raw_name.strip()
        # Skip empty or whitespace-only names instead of rejecting the whole request
        if not name:
            continue
        if len(name) > 100:
            raise HTTPException(
                status_code=422,
                detail=f"Item '{name[:20]}...' exceeds max length of 100"
            )
        if name in items_db_set:
            skipped_duplicates.append(name)
            continue

        items_db.append(name)
        items_db_set.add(name)
        added_items.append(name)

    return BulkItemsAddResponse(
        message="Bulk add completed",
        added_items=added_items,
        skipped_duplicates=skipped_duplicates,
        count_added=len(added_items),
        count_skipped=len(skipped_duplicates),
    )

@app.get("/items", response_model=ItemListResponse, tags=["Random Items Management"])
async def get_randomized_items():
    randomized = items_db.copy()
    random.shuffle(randomized)

    return ItemListResponse(
        original_order=items_db,
        randomized_order=randomized,
        count=len(items_db)
    )

@app.put("/items/{update_item_name}", response_model=ItemUpdateResponse, tags=["Random Items Management"])
async def update_item(update_item_name: str, item: Item):
    if update_item_name not in items_db_set:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.name in items_db_set and item.name != update_item_name:
        raise HTTPException(
            status_code=409,
            detail="An item with that name already exists"
        )

    index = items_db.index(update_item_name)
    items_db[index] = item.name
    items_db_set.discard(update_item_name)
    items_db_set.add(item.name)

    return ItemUpdateResponse(
        message="Item updated successfully",
        old_item=update_item_name,
        new_item=item.name
    )

@app.delete("/items/{item}", response_model=ItemDeleteResponse, tags=["Random Items Management"])
async def delete_item(item: str):
    if item not in items_db_set:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db.remove(item)
    items_db_set.remove(item)

    return ItemDeleteResponse(
        message="Item deleted successfully",
        deleted_item=item,
        remaining_items_count=len(items_db)
    )

@app.delete("/items", response_model=BulkItemsDeleteResponse, tags=["Random Items Management"])
async def delete_all_items():
    deleted_count = len(items_db)
    items_db.clear()
    items_db_set.clear()

    return BulkItemsDeleteResponse(
        message="All items deleted successfully",
        deleted_count=deleted_count,
        remaining_items_count=0
    )