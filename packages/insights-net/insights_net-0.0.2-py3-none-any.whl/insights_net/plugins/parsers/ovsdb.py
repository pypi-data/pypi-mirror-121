import glob
import uuid
import json
import logging
import os
import os.path
import stat

from insights import CommandParser, parser, Parser, datasource
from insights.core import dr
from insights.core.context import SosArchiveContext, HostArchiveContext
from insights.core.spec_factory import simple_file, ContentProvider
from insights.parsers import SkipException

from ovsdbapp.backend.ovs_idl import Backend
from ovsdbapp.backend.ovs_idl import connection

log = logging.getLogger(__name__)


class OVSDBMixin(object):
    """
    Base class for OVSDB data parsers and combiners.

    Subclasses must populate two attributes:
        _name(str): the name of the database
        _tables(dict): Must have the following format:
            {
                "TableName0": {
                    "uuid0": {
                        "column1": value01,
                        "column2": value02,
                        ...
                    }
                    "uuid1": {
                        "column1": value11,
                        "column2": value12,
                    }
                    ...
                }
                "TableName1": {
                ...
                }
            }
    """

    @property
    def tables(self):
        """
        Returns all the tables
        """
        return self._tables

    @property
    def name(self):
        """
        Returns the database name
        """
        return self._name

    def table_list(self):
        """
        Returns all the tables
        """
        return list(self._tables.keys())

    def columns(self, table):
        """
        Returns the list columns in a particular table
        """
        first = self._tables.get(next(list(self._tables.get(table).keys())))
        return first.keys()

    def table(self, name):
        """
        Returns the table with the given name
        """
        return self._tables.get(name)

    def row(self, table, uuid):
        """
        Finds the row that with the given uuid
        """
        table = self._tables.get(table)
        if table:
            return table.get(uuid)
        return None

    def find_uuid(self, table, uuid):
        """
        Finds the row that in the table that matches the column's value
        """
        return self.filter(table, lambda x: x.get("_uuid").startswith(uuid))

    def find(self, table, column, value):
        """
        Finds the row that in the table that matches the column's value
        """
        table = self._tables.get(table)
        if table:
            return list((row for row in table.values() if row.get(column) == value))
        return []

    def filter(self, table, function):
        """
        Filters the table based on the given callable filter
        """
        table = self._tables.get(table)
        if table:
            return list(filter(function, table.values()))
        return []


class OVSDBParser(OVSDBMixin, Parser):
    """
    Base class for Parsers that implement OVSDB instances
    """

    def __init__(self, *args, **kwargs):
        super(OVSDBParser, self).__init__(*args, **kwargs)


class OVSDBListParser(OVSDBParser):
    """
    OVSDBListParser tries to parse the output of commands that use the "--list"
    format. Examples: ovs-vsctl, ovn-nbcl, ovn-sbctl

    Input example:
    ==============
    AutoAttach table

    Bridge table
    _uuid               : 45711587-9496-4d14-8dfe-67a8c273e610
    auto_attach         : []
    controller          : [65c7f516-5bef-41f1-b633-94d6375fa356]
    datapath_id         : "000048df37ce6d70"
    datapath_type       : system
    datapath_version    : "<unknown>"
    external_ids        : {bridge-id=br-link}
    fail_mode           : secure
    flood_vlans         : []
    flow_tables         : {}
    ipfix               : []
    mcast_snooping_enable: false
    mirrors             : []
    name                : br-link
    netflow             : []
    other_config        : {mac-table-size="50000"}
    ports               : [8918bf51-abfa-4b2e-961f-2dca931bf2a8, acb08497-7deb-4ca7-bc9d-d1119dc2d85f, dcf4d708-b4d8-4948-8570-d2a6a05e7949]
    """

    def __init__(self, *args, **kwargs):
        super(OVSDBListParser, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        self._tables = dict()
        current_table = dict()
        current_table_name = ""
        current_uuid = ""
        current_row = dict()
        for line in content:
            line = line.strip()
            if not line:
                continue

            table_name, _, keyword = line.partition(" ")
            if keyword == "table":
                # New Table, save old row and table
                if current_uuid != "":
                    current_table[current_row["_uuid"]] = current_row
                    current_uuid = ""

                if current_table_name != "":
                    self._tables[current_table_name] = current_table

                current_table_name = table_name
                current_table = dict()

            else:
                column, _, value = line.partition(":")
                column = column.strip()
                value = value.strip()
                converted = self._convert_value(value)

                if not value or not column:
                    raise SkipException("Wrong format")

                if column == "_uuid":
                    # New rowect, save old row if any
                    if current_uuid != "":
                        current_table[current_row["_uuid"]] = current_row

                    current_uuid = converted
                    current_row = dict()

                current_row[column] = converted

    def _convert_dict(self, value):
        """
        Convert a dictionary field value
        e.g:
        {classless_static_route="{169.254.169.254/32,192.168.199.2, 0.0.0.0/0,192.168.199.1}", dns_server="{172.16.0.1, 10.0.0.1}", domain_name="\"openstackgate.local\"", lease_time="43200", mtu="1442", router="192.168.199.1", server_id="192.168.199.1", server_mac="fa:16:3e:0b:ba:9d"}
        """
        dict_value = value.strip("{")
        result = {}
        while True:
            (key, found, rest) = dict_value.partition("=")
            if not found:
                break

            key = key.strip('"')

            item = None
            new_dict_value = ""

            if rest[0] == '"':
                start = 1
                while True:
                    pos = rest.find('"', start)
                    if pos == len(rest):
                        # Error, we did not find the end of the string
                        raise Exception("Wrong format %s" % value)

                    if rest[pos - 1] != "\\":
                        # found a non escaped "
                        item = rest[1:pos]
                        new_dict_value = rest[pos + 1 :].strip(", ")
                        break

                    start = pos + 1
            else:
                (item, comma, new_dict_value) = rest.partition(", ")
                if not comma:
                    (item, curly, new_dict_value) = rest.partition("}")
                    if not curly:
                        raise Exception("Wrong format %s" % value)

            result[key] = self._convert_single_value(item)
            dict_value = new_dict_value

        return result

    def _convert_value(self, value):
        if value[0] == "[":
            converted = []
            for val in value.strip("[]").split(", "):
                if val:
                    converted.append(self._convert_single_value(val))
            return converted
        elif value[0] == "{":
            converted = self._convert_dict(value)
        else:
            converted = self._convert_single_value(value)

        return converted

    def _convert_single_value(self, value):
        value = value.strip('\\"')
        try:
            int_val = int(value)
            return int_val
        except ValueError:
            pass

        try:
            float_val = float(value)
            return float_val
        except ValueError:
            pass

        if value == "true":
            return True
        elif value == "false":
            return False

        return value


class OVSDBDumpParser(OVSDBParser):
    """
    A parser that reads a OVSDB Dump file.

    Note that as OVSDB is transactional, if the dump has not been compacted,
    some information will be lost.

    Only the fist database will be parsed. Further databases or transactions will be ignored
    """

    def parse_content(self, content):
        if len(content) < 2:
            # raise SkipException("Wrong format")
            raise Exception("Wrong format")

        # First line should be OVSDB CLUSTER {} {}
        header = content[0]
        if header[0:13] != "OVSDB CLUSTER":
            # raise SkipException("Wrong format")
            raise Exception("Wrong format: {} ".format(header))

        dump = json.loads(content[1])
        name = dump.get("name")
        if not name:
            # raise SkipException("Wrong format")
            raise Exception("Wrong format")

        prev_data = dump.get("prev_data")
        if not prev_data or len(prev_data) != 2:
            # raise SkipException("Wrong format")
            raise Exception("Wrong format")

        self._tables = prev_data[1]
        for table_name, table in self._tables.items():
            if not isinstance(table, dict):
                continue
            for uuid, row in table.items():
                for column, data in row.items():
                    # in place replacement
                    row[column] = self.process_single_field(data)

    def process_single_field(self, data):
        """
        Process a single field that can be a map, set or uuid
        """
        if isinstance(data, list) and len(data) > 1:
            if data[0] == "set":
                return data[1]
            elif data[0] == "map":
                return {item[0]: self.process_single_field(item[1]) for item in data[1]}
            elif data[0] == "uuid":
                return data[1]
            else:
                return data
        else:
            return data


class ovsdb_servers(object):
    """For each valid OVSDB connection found, creates a datasource that
    connects to such server and dumps all its content into a dictionary

    Metadata:
        extra_patters: extra patterns can be provided as metadata

    Args:
        patterns (str or [str]): file patterns of unix sockets
        schema

    """

    def __init__(self, patterns, schema, context=None, deps=[], **kwargs):
        if not isinstance(patterns, (list, set)):
            patterns = [patterns]
        self.patterns = patterns

        self.schema = schema
        self.context = context or HostArchiveContext
        self.__name__ = self.__class__.__name__
        datasource(self.context, *deps, **kwargs)(self)

    def __call__(self, broker):
        """
        Called by the plugin to extract the data

        Find all the matched patterns and return the data
        """
        if isinstance(self.context, list):
            ctx = dr.first_of(self.context, broker)
        else:
            ctx = broker.get(self.context)

        results = []
        root = ctx.root

        for pattern in self.patterns:
            pattern = ctx.locate_path(pattern)
            for path in sorted(glob.glob(os.path.join(root, pattern.lstrip("/")))):
                if os.path.isdir(path) or not stat.S_ISSOCK(os.stat(path).st_mode):
                    continue
                log.debug("ovsdb socket found at %s" % path)

                try:
                    client = OVSDBClient(path, self.schema)
                except Exception as e:
                    log.debug(
                        "ovsdb does not contain a database with schema %s", self.schema
                    )
                    continue
                results.append(client)

        return results


class OVSDBClient:
    """OVSDBClient is a Datasource that connects to a running ovsdb-server,
    dumps all its tables. Unlike other Datasources, OVSDBClient is does not
    expose its content as a list of strings, but as a dictionary of tables.
    This is because the internal use of ovsdbapp who already parses the content

    In order to be used by a Parser it has the following attributes:
        relative_path: the relative_path to the ovsdb socket that is used to
            interact with the ovsdb server
        path: full path of the socket file
        content: the dictionary of tables with the following format:
            {
                "TableName_1" {
                    "uuid_0" : {
                        "column_name_1": _value_,
                        "column_name_2": _value_
                        ...
                    }
                    "uuid_1" : {
                        "column_name_1": _value_,
                        "column_name_2": _value_
                        ...
                    }
                    ...
                }
                "TableName_2" {
                ...
                }
            }

    Args:
        relative_path: relative_path to the db socket file
        schema: the database name which shall be dumped

    Raises:
        Exception if the database is not pressent in the ovsdb-server
        instance
    """

    def __init__(self, relative_path, schema, root="/"):
        self._relative_path = relative_path
        self._root = root
        self.idl = connection.OvsdbIdl.from_server("unix:" + self.path, schema)
        self.conn = connection.Connection(idl=self.idl, timeout=3)
        self.api = Backend(self.conn)
        self._name = schema
        self._content = None
        self._exception = None

    @property
    def path(self):
        return os.path.join(self._root, self.relative_path)

    @property
    def relative_path(self):
        return self._relative_path

    @property
    def content(self):
        if self._exception:
            raise self._exception

        if self._content is None:
            try:
                self._content = self._dump_tables()
            except Exception as ex:
                self._exception = ex
                raise

        return self._content

    def _dump_tables(self):
        result = {}
        for table, rows in self.api.idl.tables.items():
            # Extract rows and placed them as
            # "tableName" : {
            #    "uuid" : { rowData }
            # }

            result[table] = {
                str(row["_uuid"]): self._process_row(row)
                for row in self.api.db_list(table).execute()
            }
        return result

    def _process_row(self, row):
        """Ensure all of items are native types.
        In practice this just means converting UUIDs to strings
        """
        for col, value in row.items():
            if (
                isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], uuid.UUID)
            ):
                row[col] = [str(uuid) for uuid in value]
            elif (
                isinstance(value, dict)
                and len(value) > 0
                and isinstance(list(value.values())[0], uuid.UUID)
            ):
                row[col] = {k: str(v) for k, v in value.items()}
            elif isinstance(value, uuid.UUID):
                row[col] = str(value)
        return row
