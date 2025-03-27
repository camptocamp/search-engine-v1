# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from urllib import parse as urlparse

from odoo import tools
from odoo.tools import file_path

from odoo.addons.component.tests.common import TransactionComponentCase

# mute `test_queue_job_no_delay` logging
logging.getLogger("odoo.addons.queue_job.models.base").setLevel("CRITICAL")


def load_xml(env, module, filepath):
    tools.convert_file(
        env,
        module,
        file_path(filepath),
        {},
        mode="init",
        noupdate=False,
        kind="test",
    )


class TestSeBackendCaseBase(TransactionComponentCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                tracking_disable=True,  # speed up tests
                queue_job__no_delay=True,  # no jobs thanks
            )
        )
        cls.se_index_model = cls.env["se.index"]

    @classmethod
    def _load_fixture(cls, fixture, module="connector_search_engine"):
        load_xml(cls.env, module, f"{module}/tests/fixtures/{fixture}")

    @staticmethod
    def parse_path(url):
        return urlparse.urlparse(url).path
