"""Warehouse routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from web.storage import storage

bp = Blueprint('warehouses', __name__)


@bp.route('/')
def index():
    """Display all warehouses."""
    warehouses_list = storage.get_all_warehouses()
    return render_template(
        'warehouses/index.html',
        warehouses=warehouses_list
    )


def _validate_warehouse_form(form):
    """Validate warehouse form and return (errors, name, description)."""
    name = form.get('name', '').strip()
    description = form.get('description', '').strip()
    errors = []
    if not name:
        errors.append('Name is required.')
    return errors, name, description


def _flash_errors(errors):
    """Flash all error messages."""
    for error in errors:
        flash(error, 'error')


def _handle_new_warehouse_post():
    """Handle POST request for creating a new warehouse."""
    errors, name, description = _validate_warehouse_form(request.form)
    if errors:
        _flash_errors(errors)
        return render_template(
            'warehouses/form.html',
            name=name,
            description=description,
            action='Create'
        )
    storage.create_warehouse(name, description)
    flash('Warehouse created successfully.', 'success')
    return redirect(url_for('warehouses.index'))


@bp.route('/warehouses/new', methods=['GET', 'POST'])
def new_warehouse():
    """Create a new warehouse."""
    if request.method == 'POST':
        return _handle_new_warehouse_post()

    return render_template(
        'warehouses/form.html',
        name='',
        description='',
        action='Create'
    )


@bp.route('/warehouses/<int:warehouse_id>')
def show_warehouse(warehouse_id):
    """Show a single warehouse with its products."""
    warehouse = storage.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found.', 'error')
        return redirect(url_for('warehouses.index'))

    products_list = list(warehouse.products.values())
    return render_template(
        'warehouses/show.html',
        warehouse=warehouse,
        products=products_list
    )


def _handle_edit_warehouse_post(warehouse):
    """Handle POST request for editing a warehouse."""
    errors, name, description = _validate_warehouse_form(request.form)
    if errors:
        _flash_errors(errors)
        return render_template(
            'warehouses/form.html',
            warehouse=warehouse,
            name=name,
            description=description,
            action='Update'
        )
    storage.update_warehouse(warehouse.warehouse_id, name, description)
    flash('Warehouse updated successfully.', 'success')
    return redirect(url_for(
        'warehouses.show_warehouse',
        warehouse_id=warehouse.warehouse_id
    ))


@bp.route('/warehouses/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit a warehouse."""
    warehouse = storage.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found.', 'error')
        return redirect(url_for('warehouses.index'))

    if request.method == 'POST':
        return _handle_edit_warehouse_post(warehouse)

    return render_template(
        'warehouses/form.html',
        warehouse=warehouse,
        name=warehouse.name,
        description=warehouse.description,
        action='Update'
    )


@bp.route('/warehouses/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    if storage.delete_warehouse(warehouse_id):
        flash('Warehouse deleted successfully.', 'success')
    else:
        flash('Warehouse not found.', 'error')
    return redirect(url_for('warehouses.index'))
