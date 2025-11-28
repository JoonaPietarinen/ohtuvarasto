"""Models for the web interface that wrap the existing Varasto class."""
from dataclasses import dataclass, field
from typing import Optional, Tuple
from varasto import Varasto


def _parse_float(value, required=False):
    """Parse a float. Return (value, error) tuple."""
    if not value:
        if required:
            return None, 'is required'
        return 0.0, None
    try:
        result = float(value)
        if result < 0:
            return None, 'must be non-negative'
        return result, None
    except ValueError:
        return None, 'must be a valid number'


def validate_product_form(form) -> Tuple[list, 'ProductData']:
    """Validate product form and return (errors, ProductData)."""
    errors = []
    name = form.get('name', '').strip()
    if not name:
        errors.append('Product name is required.')

    capacity, cap_err = _parse_float(
        form.get('capacity', '').strip(),
        required=True
    )
    if cap_err:
        errors.append(f'Capacity {cap_err}.')

    quantity, qty_err = _parse_float(form.get('quantity', '').strip())
    if qty_err:
        errors.append(f'Quantity {qty_err}.')

    price, price_err = _parse_float(form.get('price', '').strip())
    if price_err:
        errors.append(f'Price {price_err}.')

    data = ProductData(
        name=name,
        capacity=capacity or 0,
        initial_quantity=quantity or 0,
        price=price or 0,
        description=form.get('description', '').strip()
    )
    return errors, data


@dataclass
class ProductData:
    """Data container for product creation/update."""

    name: str
    capacity: float
    initial_quantity: float = 0
    price: float = 0.0
    description: str = ""


@dataclass
class Product:
    """Represents a product in a warehouse, using Varasto for quantity."""

    product_id: int
    name: str
    varasto: Varasto
    price: float = 0.0
    description: str = ""

    @property
    def quantity(self):
        return self.varasto.saldo

    @property
    def capacity(self):
        return self.varasto.tilavuus


@dataclass
class Warehouse:
    """Represents a warehouse containing products."""

    warehouse_id: int
    name: str
    description: str = ""
    products: dict = field(default_factory=dict)
    _next_product_id: int = field(default=1, repr=False)

    def add_product(self, data: ProductData) -> Product:
        """Add a new product to this warehouse."""
        varasto = Varasto(data.capacity, data.initial_quantity)
        product = Product(
            product_id=self._next_product_id,
            name=data.name,
            varasto=varasto,
            price=data.price,
            description=data.description
        )
        self.products[product.product_id] = product
        self._next_product_id += 1
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID."""
        return self.products.get(product_id)

    def delete_product(self, product_id: int) -> bool:
        """Delete a product by ID. Returns True if deleted."""
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
