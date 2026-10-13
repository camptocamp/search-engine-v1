# Copyright 2026 Camptocamp SA (http://www.camptocamp.com).
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Drop pending deletions created w/ the binding id instead of the record id.

    The binding id is useless to delete records from the index (and could even
    delete the wrong ones) and the record id cannot be recovered
    as the bindings are gone.
    Use `se.index.resynchronize_all_bindings` to cleanup leftovers in the index.
    """
    if not version:
        return
    cr.execute("DELETE FROM se_binding_todelete RETURNING index_id, binding_id")
    rows = cr.fetchall()
    if rows:
        _logger.warning(
            "Dropped %d obsolete se.binding.todelete (index_id, binding_id): %s",
            len(rows),
            rows,
        )
