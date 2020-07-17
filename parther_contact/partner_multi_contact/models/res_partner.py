from odoo import models, fields, api, _

import logging
import time

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_contact_ids = fields.One2many('partner.contact', 'partner_id')

    def _get_actual_contacts(self):
        """
        The method returns the actual contacts of the partner.
        Relevance is determined by value sequence.
        :return: dict with actual contacts
        """
        actual_contacts = {}
        sorted_contact_ids = self.partner_contact_ids.sorted(key='sequence')
        actual_contacts['phone'] = sorted_contact_ids.filtered(lambda s: s.contact_type == 'main_phone')[:1].value
        actual_contacts['mobile'] = sorted_contact_ids.filtered(lambda s: s.contact_type == 'mobile_phone')[:1].value
        actual_contacts['email'] = sorted_contact_ids.filtered(lambda s: s.contact_type == 'email')[:1].value
        return actual_contacts

    @api.onchange('partner_contact_ids')
    def _onchange_partner_contact_ids(self):
        self.ensure_one()
        partner_contact_ids = self.partner_contact_ids
        if partner_contact_ids:
            actual_contacts = self._get_actual_contacts()
            self.write(actual_contacts)
