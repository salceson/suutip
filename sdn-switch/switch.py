import array
import datetime
import struct
import logging

import requests
from ryu.base import app_manager
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import dpid as dpid_lib
from ryu.lib import stplib
from ryu.lib.mac import haddr_to_str
from ryu.lib.packet import packet, ipv4, tcp, udp, icmp, arp
from ryu.ofproto import ofproto_v1_0


logging.getLogger('requests').setLevel(logging.WARNING)


# noinspection PyCompatibility,PyBroadException
class SimpleSwitchStp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    _CONTEXTS = {'stplib': stplib.Stp}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitchStp, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.stp = kwargs['stplib']

        # Sample of stplib config.
        #  please refer to stplib.Stp.set_config() for details.
        """
        config = {dpid_lib.str_to_dpid('0000000000000001'):
                     {'bridge': {'priority': 0x8000,
                                 'max_age': 10},
                      'ports': {1: {'priority': 0x80},
                                2: {'priority': 0x90}}},
                  dpid_lib.str_to_dpid('0000000000000002'):
                     {'bridge': {'priority': 0x9000}}}
        self.stp.set_config(config)
        """

    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto

        wildcards = ofproto_v1_0.OFPFW_ALL
        wildcards &= ~ofproto_v1_0.OFPFW_IN_PORT
        wildcards &= ~ofproto_v1_0.OFPFW_DL_DST

        match = datapath.ofproto_parser.OFPMatch(
            wildcards, in_port, 0, dst,
            0, 0, 0, 0, 0, 0, 0, 0, 0)

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
        datapath.send_msg(mod)

    def delete_flow(self, datapath):
        ofproto = datapath.ofproto

        wildcards = ofproto_v1_0.OFPFW_ALL
        match = datapath.ofproto_parser.OFPMatch(
            wildcards, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_DELETE)
        datapath.send_msg(mod)

    @set_ev_cls(stplib.EventPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto

        dst, src, _eth_type = struct.unpack_from('!6s6sH', buffer(msg.data), 0)

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.debug("packet in %s %s %s %s",
                          dpid, haddr_to_str(src), haddr_to_str(dst),
                          msg.in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = msg.in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # Send message to dashboard
        pkt = packet.Packet(array.array('B', ev.msg.data))
        ip4pkt = pkt.get_protocol(ipv4.ipv4)
        arppkt = pkt.get_protocol(arp.arp)  # type: arp.arp
        icmppkt = pkt.get_protocol(icmp.icmp)  # type: icmp.icmp
        tcppkt = pkt.get_protocol(tcp.tcp)  # type: tcp.tcp
        udppkt = pkt.get_protocol(udp.udp)  # type: udp.udp

        if arppkt:
            protocol = 0x806
            src_port = arppkt.opcode
            dst_port = 0
        elif icmppkt:
            protocol = 1
            src_port = icmppkt.type
            dst_port = icmppkt.code or 0
        elif tcppkt:
            protocol = 6
            src_port = tcppkt.src_port
            dst_port = tcppkt.dst_port
        elif udppkt:
            protocol = 17
            src_port = udppkt.src_port
            dst_port = udppkt.dst_port
        else:
            protocol = None
            src_port = None
            dst_port = None

        if ip4pkt:
            src_ip = ip4pkt.src
            dst_ip = ip4pkt.dst
        elif arppkt:
            src_ip = arppkt.src_ip
            dst_ip = arppkt.dst_ip
        if protocol:
            self.logger.debug('Got flow: %s -> %s' % (src_ip, dst_ip))
            self.send_request_to_dashboard(src_ip, dst_ip, protocol, src_port, dst_port)

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, msg.in_port, dst, actions)

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions)
        datapath.send_msg(out)

    @set_ev_cls(stplib.EventTopologyChange, MAIN_DISPATCHER)
    def _topology_change_handler(self, ev):
        dp = ev.dp
        dpid_str = dpid_lib.dpid_to_str(dp.id)
        msg = 'Receive topology change event. Flush MAC table.'
        self.logger.debug("[dpid=%s] %s", dpid_str, msg)

        if dp.id in self.mac_to_port:
            del self.mac_to_port[dp.id]
        self.delete_flow(dp)

    @set_ev_cls(stplib.EventPortStateChange, MAIN_DISPATCHER)
    def _port_state_change_handler(self, ev):
        dpid_str = dpid_lib.dpid_to_str(ev.dp.id)
        of_state = {stplib.PORT_STATE_DISABLE: 'DISABLE',
                    stplib.PORT_STATE_BLOCK: 'BLOCK',
                    stplib.PORT_STATE_LISTEN: 'LISTEN',
                    stplib.PORT_STATE_LEARN: 'LEARN',
                    stplib.PORT_STATE_FORWARD: 'FORWARD'}
        self.logger.debug("[dpid=%s][port=%d] state=%s",
                          dpid_str, ev.port_no, of_state[ev.port_state])

    def send_request_to_dashboard(self, src_ip, dst_ip, protocol, src_port, dst_port):
        try:
            data = {
                "date": datetime.datetime.now().replace(microsecond=0).isoformat(),
                "source_ip": src_ip,
                "target_ip": dst_ip,
                "protocol": protocol,
                "source_port": int(src_port),
                "target_port": int(dst_port),
                "risk": -1
            }
            requests.post('http://127.0.0.1:8008/rest/flows/', json=data)
        except requests.RequestException as e:
            self.logger.exception('Request error')
        except Exception as e:
            self.logger.exception('Error')
