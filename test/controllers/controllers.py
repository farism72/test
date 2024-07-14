from odoo import http
from odoo.http import request

class MaterialController(http.Controller):
    @http.route('/materials', type='json', auth='user', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        required_fields = ['material_code', 'name', 'material_type', 'unit_price', 'partner_id']
        if not all(field in kwargs for field in required_fields):
            return {"error": "Missing required fields"}
        
        if kwargs.get('unit_price') < 100:
            return {"error": "Material buy price must be at least 100"}
        
        material = request.env['sale.material'].create({
            'material_code': kwargs.get('material_code'),
            'name': kwargs.get('name'),
            'material_type': kwargs.get('material_type'),
            'unit_price': kwargs.get('unit_price'),
            'partner_id': kwargs.get('partner_id'),
        })
        return material.read()[0]

    @http.route('/materials', type='json', auth='user', methods=['GET'], csrf=False)
    def get_materials(self, material_type=None):
        domain = [('material_type', '=', material_type)] if material_type else []
        materials = request.env['sale.material'].search(domain)
        return materials.read()

    @http.route('/materials/<int:material_id>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        material = request.env['sale.material'].browse(material_id)
        if not material:
            return {"error": "Material not found"}
        material.write(kwargs)
        return material.read()[0]

    @http.route('/materials/<int:material_id>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id):
        material = request.env['sale.material'].browse(material_id)
        if not material:
            return {"error": "Material not found"}
        material.unlink()
        return {"success": True}
