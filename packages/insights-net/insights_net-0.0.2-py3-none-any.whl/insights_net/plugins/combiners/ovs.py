""" OVS combiners

OVN information can be obtained from lists, dumps or live database.
Combine them all into a single combiner per database type
"""
from insights.core.plugins import combiner
from insights.parsers import SkipException

from insights_net.plugins.commands import CommandMetaClass, command
from insights_net.plugins.parsers.ovs import (
    OVSDump,
    OVSLocal,
    OVSOfctlDump,
    OVSOfctlShow,
)
from insights_net.plugins.parsers.ovsdb import OVSDBMixin


class OVSDBCommandMetaClass(CommandMetaClass):
    """
    OVSDBCommandMetaClass is a CommandMetaClass taht, used by OVSDBMixin
    instances, exposes the some functions provided by such Mixin as commands.

    It accepts one argument that is a string to be prepended to all commands
    exposed.
    """

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return super().__prepare__(name, bases, **kwargs)

    def __new__(cls, name, bases, namespace, **kwargs):
        return super().__new__(cls, name, bases, namespace)

    def __init__(cls, name, bases, namespace, cmd_name="", *kwargs):
        super().__init__(name, bases, namespace)
        functions_to_commands = [
            "table_list",
            "columns",
            "table",
            "row",
            "find",
            "find_uuid",
        ]

        for cmd in functions_to_commands:
            full_name = "{db}_{cmd}".format(db=cmd_name, cmd=cmd)
            orig_func = getattr(cls, cmd)
            doc = orig_func.__doc__

            setattr(cls, full_name, cls._create_wrapper(orig_func, full_name, doc))

    @classmethod
    def _create_wrapper(cls, orig_func, name, doc):
        def func(self, *args, **kwargs):
            return orig_func(self, *args, **kwargs)

        func.__name__ = name
        func.__doc__ = doc
        return command(func)


class OVSDBCombiner(OVSDBMixin):
    """
    OVSDBCombiner is a base class for OVSDBMixin combiners that combine
    dump, local and ocp OVSDB Parsers
    """

    def __init__(self, dump, local, ocp):
        if local:
            # Prefer local
            if isinstance(local, list):
                local = local[0]
            self._tables = local.tables
            self._name = local.name
        elif dump:
            if isinstance(dump, list):
                dump = dump[0]
            self._tables = dump.tables
            self._name = dump.name
        elif ocp:
            if isinstance(ocp, list):
                ocp = ocp[0]
            self._tables = ocp.tables
            self._name = ocp.name
        else:
            raise Exception("No OVSDB data available")


@combiner([OVSDump, OVSLocal])
class OVS(OVSDBCombiner, metaclass=OVSDBCommandMetaClass, cmd_name="ovs"):
    def __init__(self, dump, local):
        super(OVS, self).__init__(dump, local, None)


# Ofproto


@combiner(OVSOfctlShow, OVSOfctlDump)
class OVSOfproto(metaclass=CommandMetaClass):
    """OVSOfproto groups all the Ofproto information in a single object
    and exposes some commands
    """

    def __init__(self, shows, dumps):
        self.bridges = {}
        if len(shows) != len(dumps):
            raise SkipException("Uncomplete data")

        for show in shows:
            if not self.bridges.get(show.bridge_name):
                self.bridges[show.bridge_name] = {}

            self.bridges[show.bridge_name]["show"] = show

        for dump in dumps:
            if not self.bridges.get(dump.bridge_name):
                raise SkipException("Uncomplete data")

            self.bridges[dump.bridge_name]["dump"] = dump

    @command
    def ofproto_summary(self):
        """Return a summary of the ofproto information"""
        return {
            name: {"ports": bridge["show"].ports, "flows": bridge["dump"].flow_list.len}
            for name, bridge in self.bridges
        }

    @command
    def find_flows(self, expr):
        """Find flows that match a certain expression (see ovs-dbg filtering)"""
        return {
            name: [str(f) for f in bridge["dump"].flow_list.find(expr)]
            for name, bridge in self.bridges
        }

    @command
    def show(self):
        """Return the openflow information ('ofctl show')"""
        return {name: bridge["show"] for name, bridge in self.bridges}

    @command
    def flows(self):
        """Return all the openflow flows"""
        return {
            name: [str(f) for f in bridge["dump"].flow_list.flows]
            for name, bridge in self.bridges
        }
