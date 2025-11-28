"""Product routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from web.storage import storage
from web.models import validate_product_form
from varasto import Varasto

bp = Blueprint('products', __name__)


def _flash_errors(errors):
    """Flash all errors."""
    for error in errors:
        flash(error, 'error')


def _handle_new_product_post(warehouse):
    """Handle POST for new product."""
    errors, data = validate_product_form(request.form)
    if errors:
        _flash_errors(errors)
        return render_template(
            'products/form.html',
            warehouse=warehouse,
            action='Add',
            name=data.name,
            capacity=data.capacity,
            quantity=data.initial_quantity,
            price=data.price,
            description=data.description
        )

    warehouse.add_product(data)
    flash('Product added successfully.', 'success')
    return redirect(url_for(
        'warehouses.show_warehouse',
        warehouse_id=warehouse.warehouse_id
    ))


@bp.route('/warehouses/<int:warehouse_id>/products/new',
          methods=['GET', 'POST'])
def new_product(warehouse_id):
    """Add a new product to a warehouse."""
    warehouse = storage.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found.', 'error')
        return redirect(url_for('warehouses.index'))

    if request.method == 'POST':
        return _handle_new_product_post(warehouse)

    return render_template(
        'products/form.html',
        warehouse=warehouse,
        action='Add',
        name='',
        capacity='',
        quantity='',
        price='',
        description=''
    )


def _handle_edit_product_post(warehouse, product):
    """Handle POST for edit product."""
    errors, data = validate_product_form(request.form)
    if errors:
        _flash_errors(errors)
        return render_template(
            'products/form.html',
            warehouse=warehouse,
            product=product,
            action='Update',
            name=data.name,
            capacity=data.capacity,
            quantity=data.initial_quantity,
            price=data.price,
            description=data.description
        )

    product.name = data.name
    product.price = data.price
    product.description = data.description
    product.varasto = Varasto(data.capacity, data.initial_quantity)

    flash('Product updated successfully.', 'success')
    return redirect(url_for(
        'warehouses.show_warehouse',
        warehouse_id=warehouse.warehouse_id
    ))


@bp.route('/warehouses/<int:wh_id>/products/<int:prod_id>/edit',
          methods=['GET', 'POST'])
def edit_product(wh_id, prod_id):
    """Edit a product."""
    warehouse = storage.get_warehouse(wh_id)
    if not warehouse:
        flash('Warehouse not found.', 'error')
        return redirect(url_for('warehouses.index'))

    product = warehouse.get_product(prod_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for(
            'warehouses.show_warehouse',
            warehouse_id=wh_id
        ))

    if request.method == 'POST':
        return _handle_edit_product_post(warehouse, product)

    return render_template(
        'products/form.html',
        warehouse=warehouse,
        product=product,
        action='Update',
        name=product.name,
        capacity=product.capacity,
        quantity=product.quantity,
        price=product.price,
        description=product.description
    )


@bp.route('/warehouses/<int:wh_id>/products/<int:prod_id>/delete',
          methods=['POST'])
def delete_product(wh_id, prod_id):
    """Delete a product from a warehouse."""
    warehouse = storage.get_warehouse(wh_id)
    if not warehouse:
        flash('Warehouse not found.', 'error')
        return redirect(url_for('warehouses.index'))

    if warehouse.delete_product(prod_id):
        flash('Product deleted successfully.', 'success')
    else:
        flash('Product not found.', 'error')

    return redirect(url_for('warehouses.show_warehouse', warehouse_id=wh_id))
