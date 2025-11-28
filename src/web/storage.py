"""In-memory storage layer for warehouses and products."""
from typing import Optional
from web.models import Warehouse


class Storage:
    """In-memory storage for warehouses."""

    def __init__(self):
        self._warehouses: dict[int, Warehouse] = {}
        self._next_warehouse_id: int = 1

    def create_warehouse(
        self, name: str, description: str = ""
    ) -> Warehouse:
        """Create a new warehouse."""
        warehouse = Warehouse(
            warehouse_id=self._next_warehouse_id,
            name=name,
            description=description
        )
        self._warehouses[warehouse.warehouse_id] = warehouse
        self._next_warehouse_id += 1
        return warehouse

    def get_warehouse(self, warehouse_id: int) -> Optional[Warehouse]:
        """Get a warehouse by ID."""
        return self._warehouses.get(warehouse_id)

    def get_all_warehouses(self) -> list[Warehouse]:
        """Get all warehouses."""
        return list(self._warehouses.values())

    def update_warehouse(
        self,
        warehouse_id: int,
        name: str,
        description: str
    ) -> Optional[Warehouse]:
        """Update a warehouse's details."""
        warehouse = self._warehouses.get(warehouse_id)
        if warehouse:
            warehouse.name = name
            warehouse.description = description
        return warehouse

    def delete_warehouse(self, warehouse_id: int) -> bool:
        """Delete a warehouse. Returns True if deleted."""
        if warehouse_id in self._warehouses:
            del self._warehouses[warehouse_id]
            return True
        return False


# Global storage instance
storage = Storage()
