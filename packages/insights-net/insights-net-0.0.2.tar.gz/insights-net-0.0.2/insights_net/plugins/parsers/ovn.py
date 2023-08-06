import os

from insights import parser
from insights.core.spec_factory import simple_file, simple_command

from insights_net.plugins.parsers.ovsdb import (
    OVSDBListParser,
    OVSDBParser,
    ovsdb_servers,
)

# Openstack dumps
ovn_nb_dump = simple_file(
    "sos_commands/ovn_central/podman_exec_ovn-dbs-bundle-podman-0_ovsdb-client_-f_list_dump_unix.var.run.openvswitch.ovnnb_db.sock"
)
ovn_sb_dump = simple_file(
    "sos_commands/ovn_central/podman_exec_ovn-dbs-bundle-podman-0_ovsdb-client_-f_list_dump_unix.var.run.openvswitch.ovnsb_db.sock"
)


@parser(ovn_nb_dump)
class OVNNBDump(OVSDBListParser):
    def __init__(self, *args, **kwargs):
        super(OVNNBDump, self).__init__(*args, **kwargs)
        self._name = "OVN_Northbound"


@parser(ovn_sb_dump)
class OVNSBDump(OVSDBListParser):
    def __init__(self, *args, **kwargs):
        super(OVNSBDump, self).__init__(*args, **kwargs)
        self._name = "OVN_Southbound"


# Local
ovn_nb_db = ovsdb_servers(["*.sock", "ovnnb_db.sock"], "OVN_Northbound")
ovn_sb_db = ovsdb_servers(["*.sock", "ovnsb_db.sock"], "OVN_Southbound")


@parser(ovn_nb_db)
class OVNNBLocal(OVSDBParser):
    def __init__(self, *args, **kwargs):
        super(OVNNBLocal, self).__init__(*args, **kwargs)

    def parse_content(self, data):
        self._tables = data
        self._name = "OVN_Northbound"


@parser(ovn_sb_db)
class OVNSBLocal(OVSDBParser):
    def __init__(self, *args, **kwargs):
        super(OVNSBLocal, self).__init__(*args, **kwargs)

    def parse_content(self, data):
        self._tables = data
        self._name = "OVN_Southbound"
