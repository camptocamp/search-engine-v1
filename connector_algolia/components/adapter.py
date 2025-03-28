# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import logging

from algoliasearch.search.client import SearchClientSync as SearchClient

from odoo import exceptions

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class AlgoliaAdapter(Component):
    _name = "algolia.adapter"
    _inherit = ["se.backend.adapter", "algolia.se.connector"]
    _usage = "se.backend.adapter"

    def __init__(self, work_context):
        super().__init__(work_context)
        self.index_name = self.work.index.name

    def _get_client(self):
        backend = self.backend_record
        account = backend._get_api_credentials()
        return SearchClient(backend.algolia_app_id, account["password"])

    def settings(self, force=False):
        """Push advanced settings like facettings attributes."""
        client = self._get_client()
        data = self.work.index._get_settings()
        if not force:
            # export settings if it is the first creation of the index.
            indexes = client.list_indices()
            index_names = [item.name for item in indexes.items]
            force = self.index_name not in index_names or False
        if data and force:
            client.set_settings(self.index_name, data)

    def get_settings(self):
        client = self._get_client()
        data = client.get_settings(self.index_name)
        return data

    def index(self, records):
        for record in records:
            error = self._validate_record(record)
            if error:
                raise exceptions.ValidationError(error)
        client = self._get_client()
        client.save_objects(self.index_name, records)

    def delete(self, binding_ids):
        client = self._get_client()
        client.delete_objects(self.index_name, binding_ids)

    def clear(self):
        client = self._get_client()
        client.clear_objects(self.index_name)
        self.settings(force=True)

    def iter(self):
        # `iter` is a built-in keyword -> to be replaced
        _logger.warning("DEPRECATED: use `each` instead of `iter`.")
        return self.each()

    def each(self):
        # TODO: test me
        client = self._get_client()
        return client.search_single_index(self.index_name)
