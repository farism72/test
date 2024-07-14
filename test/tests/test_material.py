from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError



class TestMaterial(TransactionCase):
    def setUp(self):
        super(TestMaterial, self).setUp()
        self.material = self.env['sale.material'].create({
            'material_code': 'M001',
            'name': 'Sample Material',
            'material_type': 'fabric',
            'unit_price': 150,
            'partner_id': self.env.ref('base.res_partner_1').id
        })

    def test_material_creation(self):
        material = self.env['sale.material'].create({
            'material_code': 'M002',
            'name': 'Test Material',
            'material_type': 'jeans',
            'unit_price': 200,
            'partner_id': self.env.ref('base.res_partner_1').id
        })
        self.assertEqual(material.material_code, 'M002')
        self.assertEqual(material.unit_price, 200)

    def test_unit_price_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['sale.material'].create({
                'material_code': 'M003',
                'name': 'Invalid Material',
                'material_type': 'cotton',
                'unit_price': 50,
                'partner_id': self.env.ref('base.res_partner_1').id
            })

    def test_material_update(self):
        self.material.write({'name': 'Updated Material'})
        self.assertEqual(self.material.name, 'Updated Material')

    def test_material_delete(self):
        self.material.unlink()
        self.assertFalse(self.material.exists())
