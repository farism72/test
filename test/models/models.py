from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'sale.material'
    _description = 'Material'

    material_code = fields.Char(string='Material Code', required=True)
    name = fields.Char(string='Material Name', required=True)
    material_type = fields.Selection(
        [('fabric', 'Fabric'), ('jeans', 'Jeans'), ('cotton', 'Cotton')],
        string='Material Type', required=True
    )
    unit_price = fields.Float(string='Material Buy Price', required=True)
    partner_id = fields.Many2one('res.partner', string='Related Supplier', required=True)

    @api.constrains('unit_price')
    def _check_unit_price(self):
        for rec in self:
            if rec.unit_price < 100:
                raise ValidationError("Material buy price must be at least 100.")
