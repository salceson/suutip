import subprocess
from docker_ovs.plugin.rand_utils import get_rand_suffix


def create_endpoint(ovs_bridge, tag):
    host_if = 'ovs-' + get_rand_suffix()
    container_if = 'tmp-' + get_rand_suffix()
    subprocess.check_output(['sudo', 'ip', 'link',
        'add', 'name', host_if,
        'type', 'veth',
        'peer', 'name', container_if,
    ])
    subprocess.check_output(['sudo', 'ip', 'link',
        'set', 'dev', host_if,
        'mtu', '1400',
    ])
    subprocess.check_output(['sudo', 'ip', 'link',
        'set', 'dev', container_if,
        'mtu', '1400',
    ])
    subprocess.check_output(['sudo', 'ip', 'link',
        'set', 'dev', host_if,
        'up',
    ])
    subprocess.check_output(['sudo', 'ovs-vsctl',
        'add-port', ovs_bridge, host_if,
        'tag=%d' % tag,
    ])
    return host_if, container_if


def delete_endpoint(ovs_bridge, host_if):
    subprocess.check_output(['sudo', 'ovs-vsctl',
        'del-port', ovs_bridge, host_if,
    ])
    subprocess.check_output(['sudo', 'ip', 'link',
        'set', 'dev', host_if,
        'down',
    ])
    subprocess.check_output(['sudo', 'ip', 'link',
        'delete', 'dev', host_if,
    ])
