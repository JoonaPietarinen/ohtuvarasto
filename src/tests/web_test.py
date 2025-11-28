"""Tests for the web application."""
import unittest
from web.app import create_app
from web.storage import storage


class WebAppTestCase(unittest.TestCase):
    """Base test case for web app tests."""

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        # Clear storage before each test
        storage._warehouses.clear()
        storage._next_warehouse_id = 1


class TestWarehouseRoutes(WebAppTestCase):
    """Test warehouse routes."""

    def test_index_empty(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouses', response.data)
        self.assertIn(b'No warehouses yet', response.data)

    def test_create_warehouse(self):
        response = self.client.post('/warehouses/new', data={
            'name': 'Test Warehouse',
            'description': 'A test warehouse'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
        self.assertIn(b'Warehouse created successfully', response.data)

    def test_create_warehouse_name_required(self):
        response = self.client.post('/warehouses/new', data={
            'name': '',
            'description': 'A test warehouse'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name is required', response.data)

    def test_show_warehouse(self):
        storage.create_warehouse('Test WH', 'Description')
        response = self.client.get('/warehouses/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test WH', response.data)

    def test_show_warehouse_not_found(self):
        response = self.client.get('/warehouses/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse not found', response.data)

    def test_edit_warehouse(self):
        storage.create_warehouse('Original', 'Original desc')
        response = self.client.post('/warehouses/1/edit', data={
            'name': 'Updated',
            'description': 'Updated desc'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated', response.data)
        self.assertIn(b'Warehouse updated successfully', response.data)

    def test_delete_warehouse(self):
        storage.create_warehouse('To Delete', 'Will be deleted')
        response = self.client.post('/warehouses/1/delete',
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse deleted successfully', response.data)
        self.assertIn(b'No warehouses yet', response.data)


class TestProductRoutes(WebAppTestCase):
    """Test product routes."""

    def setUp(self):
        super().setUp()
        self.warehouse = storage.create_warehouse('Test WH', 'Test')

    def test_add_product(self):
        response = self.client.post('/warehouses/1/products/new', data={
            'name': 'Test Product',
            'capacity': '100',
            'quantity': '50',
            'price': '9.99',
            'description': 'A test product'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)
        self.assertIn(b'Product added successfully', response.data)

    def test_add_product_validation(self):
        response = self.client.post('/warehouses/1/products/new', data={
            'name': '',
            'capacity': '-10',
            'quantity': 'invalid',
            'price': '',
            'description': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product name is required', response.data)

    def test_add_product_warehouse_not_found(self):
        response = self.client.get('/warehouses/999/products/new',
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse not found', response.data)

    def test_edit_product(self):
        from web.models import ProductData
        self.warehouse.add_product(ProductData(
            name='Original',
            capacity=100,
            initial_quantity=50,
            price=5.00
        ))
        response = self.client.post('/warehouses/1/products/1/edit', data={
            'name': 'Updated Product',
            'capacity': '200',
            'quantity': '75',
            'price': '12.50',
            'description': 'Updated'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Product', response.data)
        self.assertIn(b'Product updated successfully', response.data)

    def test_delete_product(self):
        from web.models import ProductData
        self.warehouse.add_product(ProductData(
            name='To Delete',
            capacity=50
        ))
        response = self.client.post('/warehouses/1/products/1/delete',
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product deleted successfully', response.data)


if __name__ == '__main__':
    unittest.main()
