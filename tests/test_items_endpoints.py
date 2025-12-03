"""Tests for item management endpoints."""


class TestAddItem:
    """Tests for POST /items endpoint."""

    def test_add_item_success(self, client):
        """Test successfully adding an item."""
        response = client.post("/items", json={"name": "Apple"})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item added successfully"
        assert data["item"] == "Apple"

    def test_add_multiple_items(self, client):
        """Test adding multiple items sequentially."""
        items = ["Apple", "Banana", "Cherry"]
        for item in items:
            response = client.post("/items", json={"name": item})
            assert response.status_code == 200
            data = response.json()
            assert data["item"] == item

    def test_add_duplicate_item(self, client):
        """Test adding a duplicate item."""
        client.post("/items", json={"name": "Apple"})
        response = client.post("/items", json={"name": "Apple"})
        assert response.status_code == 400
        data = response.json()
        assert "already exists" in data["detail"]

    def test_add_item_empty_name(self, client):
        """Test adding an item with empty name."""
        response = client.post("/items", json={"name": ""})
        assert response.status_code == 422  # Validation error

    def test_add_item_long_name(self, client):
        """Test adding an item with name exceeding max length."""
        long_name = "A" * 101
        response = client.post("/items", json={"name": long_name})
        assert response.status_code == 422  # Validation error

    def test_add_item_max_length(self, client):
        """Test adding an item at max allowed length."""
        max_name = "A" * 100
        response = client.post("/items", json={"name": max_name})
        assert response.status_code == 200

    def test_add_item_with_special_characters(self, client):
        """Test adding items with special characters."""
        special_items = ["🍎 Apple", "Test-Item", "Item_123", "Item (1)"]
        for item in special_items:
            response = client.post("/items", json={"name": item})
            assert response.status_code == 200
            data = response.json()
            assert data["item"] == item

    def test_add_item_missing_name(self, client):
        """Test adding an item without name field."""
        response = client.post("/items", json={})
        assert response.status_code == 422


class TestGetItems:
    """Tests for GET /items endpoint."""

    def test_get_items_empty(self, client):
        """Test getting items when database is empty."""
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert data["original_order"] == []
        assert data["randomized_order"] == []
        assert data["count"] == 0

    def test_get_items_with_data(self, client, sample_items):
        """Test getting items with populated database."""
        for item in sample_items:
            client.post("/items", json={"name": item})
        
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == len(sample_items)
        assert set(data["original_order"]) == set(sample_items)
        assert set(data["randomized_order"]) == set(sample_items)
        assert data["original_order"] == sample_items

    def test_get_items_randomization(self, client, sample_items):
        """Test that randomized order is different from original."""
        for item in sample_items:
            client.post("/items", json={"name": item})
        
        # Call multiple times to check randomization
        randomized_orders = []
        for _ in range(10):
            response = client.get("/items")
            data = response.json()
            randomized_orders.append(tuple(data["randomized_order"]))
        
        # Very unlikely all 10 shuffles produce the same order
        assert len(set(randomized_orders)) > 1

    def test_get_items_original_order_unchanged(self, client, sample_items):
        """Test that original order remains consistent."""
        for item in sample_items:
            client.post("/items", json={"name": item})
        
        for _ in range(5):
            response = client.get("/items")
            data = response.json()
            assert data["original_order"] == sample_items


class TestUpdateItem:
    """Tests for PUT /items/{update_item_name} endpoint."""

    def test_update_item_success(self, client, populated_db):
        """Test successfully updating an item."""
        old_name = populated_db[0]
        new_name = "NewApple"
        
        response = client.put(
            f"/items/{old_name}",
            json={"name": new_name}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item updated successfully"
        assert data["old_item"] == old_name
        assert data["new_item"] == new_name

    def test_update_item_not_found(self, client):
        """Test updating a non-existent item."""
        response = client.put(
            "/items/NonExistent",
            json={"name": "NewName"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_update_item_to_existing_name(self, client, populated_db):
        """Test updating an item to a name that already exists."""
        old_name = populated_db[0]
        existing_name = populated_db[1]
        
        response = client.put(
            f"/items/{old_name}",
            json={"name": existing_name}
        )
        assert response.status_code == 409
        data = response.json()
        assert "already exists" in data["detail"]

    def test_update_item_empty_name(self, client, populated_db):
        """Test updating an item with empty name."""
        old_name = populated_db[0]
        response = client.put(
            f"/items/{old_name}",
            json={"name": ""}
        )
        assert response.status_code == 422

    def test_update_item_special_characters(self, client, populated_db):
        """Test updating an item with special characters in URL."""
        client.post("/items", json={"name": "Test Item"})
        response = client.put(
            "/items/Test%20Item",
            json={"name": "Updated Item"}
        )
        assert response.status_code == 200

    def test_update_item_preserves_order(self, client, populated_db):
        """Test that updating preserves item position in list."""
        old_name = populated_db[1]  # Second item
        new_name = "UpdatedItem"
        
        client.put(f"/items/{old_name}", json={"name": new_name})
        
        response = client.get("/items")
        data = response.json()
        assert data["original_order"][1] == new_name


class TestDeleteItem:
    """Tests for DELETE /items/{item} endpoint."""

    def test_delete_item_success(self, client, populated_db):
        """Test successfully deleting an item."""
        item_to_delete = populated_db[0]
        
        response = client.delete(f"/items/{item_to_delete}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item deleted successfully"
        assert data["deleted_item"] == item_to_delete
        assert data["remaining_items_count"] == len(populated_db) - 1

    def test_delete_item_not_found(self, client):
        """Test deleting a non-existent item."""
        response = client.delete("/items/NonExistent")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_delete_all_items(self, client, populated_db):
        """Test deleting all items sequentially."""
        for item in populated_db:
            response = client.delete(f"/items/{item}")
            assert response.status_code == 200
        
        response = client.get("/items")
        data = response.json()
        assert data["count"] == 0

    def test_delete_item_special_characters(self, client):
        """Test deleting an item with special characters."""
        item_name = "Test Item 🍎"
        client.post("/items", json={"name": item_name})
        
        import urllib.parse
        encoded_name = urllib.parse.quote(item_name)
        response = client.delete(f"/items/{encoded_name}")
        assert response.status_code == 200

    def test_delete_middle_item(self, client, populated_db):
        """Test deleting an item from the middle of the list."""
        middle_item = populated_db[2]
        
        response = client.delete(f"/items/{middle_item}")
        assert response.status_code == 200
        
        # Verify remaining items are in correct order
        response = client.get("/items")
        data = response.json()
        expected_items = [item for item in populated_db if item != middle_item]
        assert data["original_order"] == expected_items


class TestItemsIntegration:
    """Integration tests for item management workflows."""

    def test_full_crud_workflow(self, client):
        """Test complete CRUD workflow."""
        # Create
        response = client.post("/items", json={"name": "Apple"})
        assert response.status_code == 200
        
        # Read
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert "Apple" in data["original_order"]
        
        # Update
        response = client.put("/items/Apple", json={"name": "Green Apple"})
        assert response.status_code == 200
        
        # Read again
        response = client.get("/items")
        data = response.json()
        assert "Green Apple" in data["original_order"]
        assert "Apple" not in data["original_order"]
        
        # Delete
        response = client.delete("/items/Green%20Apple")
        assert response.status_code == 200
        
        # Verify empty
        response = client.get("/items")
        data = response.json()
        assert data["count"] == 0

    def test_concurrent_operations(self, client):
        """Test multiple operations in sequence."""
        # Add multiple items
        items = ["Item1", "Item2", "Item3"]
        for item in items:
            client.post("/items", json={"name": item})
        
        # Update one
        client.put("/items/Item2", json={"name": "Item2_Updated"})
        
        # Delete one
        client.delete("/items/Item3")
        
        # Verify state
        response = client.get("/items")
        data = response.json()
        assert data["count"] == 2
        assert "Item1" in data["original_order"]
        assert "Item2_Updated" in data["original_order"]
        assert "Item3" not in data["original_order"]

    def test_add_retrieve_shuffle_workflow(self, client, sample_items):
        """Test adding items and getting shuffled results."""
        # Add items
        for item in sample_items:
            client.post("/items", json={"name": item})
        
        # Get shuffled
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all items present in both orders
        assert set(data["original_order"]) == set(sample_items)
        assert set(data["randomized_order"]) == set(sample_items)
        
        # Verify original order is maintained
        assert data["original_order"] == sample_items
