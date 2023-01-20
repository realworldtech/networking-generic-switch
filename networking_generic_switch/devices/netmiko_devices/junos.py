from .juniper import Juniper
from . import check_output


class Junos(Juniper):
    """
    Junos Extension of the Juniper library class
    This is to override certain parameters that dont work in modern Junos
    """

    @check_output("unplug port")
    def delete_port(self, port, segmentation_id):
        cmds = self._format_commands(
            self.DELETE_PORT, port=port, segmentation_id=segmentation_id
        )
        ngs_port_default_vlan = self._get_port_default_vlan()
        if ngs_port_default_vlan:
            # NOTE(mgoddard): Pass network_id and segmentation_id for drivers
            # not yet using network_name.
            network_name = self._get_network_name(
                ngs_port_default_vlan, ngs_port_default_vlan
            )
            cmds += self._format_commands(
                self.PLUG_PORT_TO_NETWORK,
                port=port,
                segmentation_id=ngs_port_default_vlan,
            )
        if self._disable_inactive_ports() and self.DISABLE_PORT:
            cmds += self._format_commands(self.DISABLE_PORT, port=port)
        return self.send_commands_to_device(cmds)
