# (C) Copyright 2019-2021 Hewlett Packard Enterprise Development LP.
# Apache License 2.0

from datetime import date

from pyaoscx.api import API


class v10_04(API):
    """
    Represents a REST API Version 10.04. It keeps all the information
    needed for the version and methods related to it.
    """

    def __init__(self):
        self.release_date = date(2019, 1, 1)
        self.version = "10.04"
        self.default_selector = "writable"
        self.default_depth = 1
        self.default_facts_depth = 2
        self.default_subsystem_facts_depth = 4
        self.valid_selectors = [
            "configuration", "status", "statistics", "writable"]
        self.configurable_selectors = ["writable"]
        self.compound_index_separator = ","
        self.valid_depths = [0, 1, 2, 3, 4]

    def _create_ospf_area(module_class, session, index_id, **kwargs):
        # Add data for correct Ospf Area creation
        other_config = {
            "stub_default_cost": 1,
            "stub_metric_type": "metric_non_comparable"
        }
        return module_class(session, index_id, other_config=other_config,
                            **kwargs)
