from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
import re

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
    _rec_name = 'display_name'
    _order = 'sequence asc, contact_type'

    # Related fields
    partner_id = fields.Many2one('res.partner', string='Contact', index=True, ondelete='cascade')
    contact_tag_ids = fields.Many2many('partner.contact.tags', 'partner_tags', string='Tags')
    # Base fields
    sequence = fields.Integer(string='Priority', default=0, help='The higher the record, the higher its priority!')
    value = fields.Char(string='Value')
    search_value = fields.Char(compute='_compute_search_value', store=True)
    note = fields.Text(string='Note')
    display_name = fields.Char(string='Name', compute='_compute_display_name', store=True)

    image = fields.Binary(related='partner_id.image_1920', string='Photo')
    contact_type = fields.Selection(CONTACT_TYPE_SEL, string='Type')

    @api.depends('value')
    def _compute_search_value(self):
        """
        Compute searchable value
        """
        for record in self:
            search_value = record.get_searchable_value(record.value)
            record.search_value = search_value

    @api.depends('partner_id', 'value', 'contact_type')
    def _compute_display_name(self):
        """
        Compute custom display name
        """
        for record in self:
            type_ = dict(record._fields['contact_type']._description_selection(record.env)).get(record.contact_type,
                                                                                                False)
            values = [record.partner_id.name, type_, record.value]
            filtered_values = [value for value in values if value]
            display_name = ' '.join(filtered_values)
            record.display_name = display_name

    @api.onchange('partner_id', 'value', 'contact_type')
    def _onchange_check_duplicates(self):
        """
        The method checks if this partner already has a similar contact.
        :return: None
        """
        partner_id = self._context.get('default_partner_id', False)
        if not partner_id:
            partner_id = self.partner_id.id
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

    def get_searchable_value(self, value):
        if not value:
            return value
        if self.contact_type in ['email', 'username']:
            return value.replace(' ', '')
        else:
            return re.sub(r'[^0-9]', '', value)


class PartnerContactTags(models.Model):
    _name = 'partner.contact.tags'
    _description = 'Tags for contact in partner'

    name = fields.Char(string='Name', translate=True)
    color = fields.Integer(string='Color',
                           help='Odoo color index [0:9]')
