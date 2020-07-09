{
    "name": "Partner multi contacts",
    "version": "1.0",
    "author": "Masiunas Euheni",
    "license": "AGPL-3",
    "category": "Contacts",
    "summary": """
    The module adds the ability to add any number of contacts (phone numbers, mailboxes, usernames etc.) for partners.
    """,
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/partner_contact_views.xml",
    ],
    "installable": True,
}
