# (C) Copyright 2021 Hewlett Packard Enterprise Development LP.
# Apache License 2.0

import json
import logging

from pyaoscx.utils import util as utils
from pyaoscx.exceptions.generic_op_error import GenericOperationError
from pyaoscx.exceptions.request_error import HttpRequestError

from pyaoscx.pyaoscx_module import PyaoscxModule

class QosDscp(PyaoscxModule):
    """
    Provide configuration management for QoS DSCP trust mode on AOS-CX devices.
    """

    base_uri = "system/qos_dscp_map_entries"
    resource_uri_name = "qos_dscp_map_entries"

    indices = ["code_point"]

    def __init__(self, session, code_point):
        """
        Initialize a QoS DSCP trust mode object.
        :param session: pyaoscx.Session object used to represent logical
            connection to the device.
        :param code_point: Integer to identify a QoS DSCP configuration.
        """
        self.session = session
        self.__code_point = code_point

        # List used to determine attributes related to the QoS DSCP
        # configuration
        self.config_attrs = []
        self.materialized = False
        # Attribute dictionary used to manage the original data
        # obtained from the GET
        self._original_attributes = {}
        # Attribute used to know if object was changed recently
        self.__modified = False
        # Build path
        self.path = "{0}/{1}".format(
            self.base_uri,
            self.code_point
        )

    @property
    def code_point(self):
        """
        Method used to obtain the specific code point.
        :return: returns the code point of this QoS DSCP trust mode object.
        """
        # Use the @property decorator to make `self.code_point` read-only, and
        # return the actual value here
        return self.__code_point

    @PyaoscxModule.connected
    def get(self, depth=None, selector=None):
        """
        Perform a GET call to retrieve data for a QoS DSCP table entry and fill
            the object with the incoming attributes.
        :param depth: Integer deciding how many levels into the API JSON that
            references will be returned.
        :param selector: Alphanumeric option to select specific information
            return.
        :return: Returns True if there is not an exception raised.
        """
        logging.info(
            "Retrieving the switch %s QoS DSCP trust mode.", self.code_point)

        data = self._get_data(depth, selector)

        # Add dictionary as attributes for the object
        utils.create_attrs(self, data)

        if selector is None and self.session.api.default_selector in \
                self.session.api.configurable_selectors:
            utils.set_config_attrs(
                self, data, 'config_attrs')

        # Set original attributes
        self._original_attributes = data

        self.materialized = True

        return True

    @classmethod
    def get_all(cls, session):
        """
        Perform a GET call to retrieve all system QoS DSCP configurations from
            a switch.
        :param session: pyaoscx.Session object used to represent a logical
            connection to the device.
        :return:  containing all system QoS.
        """
        logging.info("Retrieving all the switch QoS DSCP trust mode.")

        uri = "{0}{1}".format(
            session.base_url,
            cls.base_uri
        )

        try:
            response = session.s.get(uri, verify=False, proxies=session.proxy)
        except Exception as e:
            raise HttpRequestError("GET", e)

        if not utils._response_ok(response, "GET"):
            raise GenericOperationError(response.text, response.status_code)

        qos_dscp_dict = {}

        data = json.loads(response.text)
        uri_list = session.api.get_uri_from_data(data)
        for uri in uri_list:
            code_point, qos_dscp = cls.from_uri(session, uri)
            qos_dscp_dict[code_point] = qos_dscp

        return qos_dscp_dict

    @PyaoscxModule.materialized
    @PyaoscxModule.connected
    def apply(self):
        """
        Main method used to update an existing QoS table entry.
        Checks whether the QoS DSCP entry exists in the switch.
        Calls self.update if object is being updated.
        :return modified: Boolean, True if object was modified,
            False otherwise.
        """
        self.__modified = self.update()
        return self.__modified

    @PyaoscxModule.connected
    def update(self):
        """
        Perform a PUT request to apply changes to an existing QoS DSCP table
            entry.
        :return modified: True if Object was modified and a PUT request was
            made. False otherwise.
        """
        qos_dscp_data = utils.get_attrs(self, self.config_attrs)

        return self._put_data(qos_dscp_data)

    @PyaoscxModule.connected
    def create(self):
        #TODO: Remove once abstractmethod decorator is removed from parent
        pass

    @PyaoscxModule.connected
    def delete(self):
        #TODO: Remove once abstractmethod decorator is removed from parent
        pass

    @classmethod
    def from_response(cls, session, response_data):
        """
        Create a QoS DSCP trust mode object given a response_data related to
            the QoS DSCP trust mode object.
        :param session: pyaoscx.Session object used to represent a logical
            connection to the device.
        :param response_data: The response can be either a
            dictionary:{
                "3" : "/rest/v10.08/system/qos_dscp_map_entries/3"
            }
            or a
            string: "/rest/v10.08/system/qos_dscp_map_entries/3"
        :return: QoS DSCP trust mode object.
        """
        code_points_arr = session.api.get_keys(
            response_data, cls.resource_uri_name)

        code_point = code_points_arr[0]

        return cls(session, code_point)

    @classmethod
    def from_uri(cls, session, uri):
        """
        Create a QoS DSCP object given a QoS DSCP trust mode URI.
        :param session: pyaoscx.Session object used to represent a logical
            connection to the device.
        :param uri: s String with a URI.
        :return: returns identifier and object
        """
        # Separate values from URI
        if cls.base_uri not in uri:
            raise ValueError("Expected valid QoS DSCP trust mode URI.")

        # Extract code point from URI
        code_point = uri.split("/")[-1]

        qos_dscp = cls(session, code_point)

        # Return identifier and object
        return code_point, qos_dscp

    def get_uri(self):
        """
        Method used to obtain the specific QoS DSCP trust mode URI.
        :return: Object's URI.
        """
        # Return self.path containing the object's URI
        return self.path

    def was_modified(self):
        """
        Getter method to check it object has been modified.
        :return: Boolean True if the object was recently modified.
        """
        return self.__modified

    def __str__(self):
        return "QoS DSCP trust mode {0}".format(self.code_point)

    ####################################################################
    # IMPERATIVE FUNCTIONS
    ####################################################################

    @PyaoscxModule.materialized
    def set_color(self, color):
        """
        Updates the value of the color of this QoS DSCP instance.
        :param color: String to identify the color which may be used later in
            the pipeline in packet-drop decision points. Example: "green".
        :return: Boolean True if no exception is raised.
        """
        # Verify data type
        if not isinstance(color, str):
            raise ValueError("ERROR: Color value must be on string format.")

        self.color = color

        return self.apply()

    @PyaoscxModule.materialized
    def set_description(self, description):
        """
        Updates the value of the color of this QoS DSCP instance.
        :param description: String used for customer documentation
        :return: Boolean True if no exception is raised.
        """
        # Verify data type
        if not isinstance(description, str):
            raise ValueError(
                "ERROR: Description value must be on a string format.")

        self.description = description

        return self.apply()

    @PyaoscxModule.materialized
    def set_local_priority(self, priority):
        """
        Updates the value of the local priority of this QoS DSCP instance.
        :param priority: Integer to represent an internal meta-data value that
            will be associated with the packet. This value will be used later
            to select the egress queue for the packet.
        :return: Boolean True if no exception is raised.
        """
        # Verify data type
        if not isinstance(priority, int):
            raise ValueError(
                "ERROR: Priority must be on integer format.")

        self.local_priority = priority

        return self.apply()
