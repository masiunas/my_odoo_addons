from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

CONTACT_TYPE_SEL = [
    ('main_phone', 'Main phone'),
    ('mobile_phone', 'Mobile phone'),
    ('work_phone', 'Work phone'),
    ('ex_phone', 'Extension phone'),
    ('home_phone', 'Home phone'),
    ('fax', 'Fax'),
    ('other_phone', 'Other phone'),
    ('email', 'Email'),
    ('username', 'Username'),
]


class PartnerContact(models.Model):
    _name = 'partner.contact'
    _description = 'Different types of contact in partner'

    partner_id = fields.Many2one('res.partner', string='Contact', index=True, ondelete='cascade')
    image = fields.Binary(related='partner_id.image_1920', string='Photo')
    sequence = fields.Integer(string='Priority', default=0, help='The higher the record, the higher its priority!')
    value = fields.Char(string='Value')
    contact_type = fields.Selection(CONTACT_TYPE_SEL, string='Type')
    note = fields.Text(string='Note')
    contact_tag_ids = fields.Many2many('partner.contact.tags', 'partner_tags', string='Tags')


class PartnerContactTags(models.Model):
    _name = 'partner.contact.tags'
    _description = 'Tags for contact in partner'

    name = fields.Char(string="Name", translate=True)
    color = fields.Integer(string="Color",
                           help="Odoo color index [0:9]")

