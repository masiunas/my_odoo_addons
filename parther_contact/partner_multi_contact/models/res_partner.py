from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_contact_ids = fields.One2many('partner.contact', 'partner_id')
