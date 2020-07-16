from odoo import models, fields, api, _
from odoo.exceptions import UserError

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

    @api.onchange('partner_id', 'value', 'contact_type')
    def _onchange_check_duplicates(self):
        """
        The method checks if this partner already has a similar contact.
        :return:
        """
        partner_id = self._context.get('default_partner_id', False)
        value = self.value
        contact_type = self.contact_type
        if partner_id and value and contact_type:
            search_domain = [
                ('partner_id', '=', partner_id),
                ('value', '=', value),
                ('contact_type', '=', contact_type),
            ]
            result = self.search(search_domain)
            if result:
                type_ = dict(self._fields['contact_type']._description_selection(self.env)).get(contact_type)
                message = _('{type} {value} already exists with {partner}.'.format(type=type_, value=value,
                                                                                   partner=self.partner_id.name))
                raise UserError(message)


class PartnerContactTags(models.Model):
    _name = 'partner.contact.tags'
    _description = 'Tags for contact in partner'

    name = fields.Char(string="Name", translate=True)
    color = fields.Integer(string="Color",
                           help="Odoo color index [0:9]")
