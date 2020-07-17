from . import models

from odoo import api, SUPERUSER_ID


def _create_default_contact_data(cr, registry):
    """
    This hook is used to initialize model 'partner.contact' data.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    partner_ids = env['res.partner'].search([])
    PartnerContact = env['partner.contact']
    for partner_id in partner_ids:
        if partner_id.email:
            PartnerContact.create(
                {
                    'partner_id': partner_id.id,
                    'contact_type': 'email',
                    'value': partner_id.email,
                }
            )
        if partner_id.phone:
            PartnerContact.create(
                {
                    'partner_id': partner_id.id,
                    'contact_type': 'main_phone',
                    'value': partner_id.phone,

                }
            )
        if partner_id.mobile:
            PartnerContact.create(
                {
                    'partner_id': partner_id.id,
                    'contact_type': 'mobile_phone',
                    'value': partner_id.mobile,

                }
            )


