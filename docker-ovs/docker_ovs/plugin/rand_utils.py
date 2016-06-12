from random import Random
from socket import gethostname
import string


mac_oui_rand = Random(gethostname())
mac_nic_rand = Random()

suffix_chars = string.ascii_letters + string.digits


def get_rand_mac():
    mac = [0x02 + 0x42]
    mac += [mac_oui_rand.randint(0x00, 0xff) for _ in xrange(2)]
    mac += [mac_nic_rand.randint(0x00, 0xff) for _ in xrange(3)]
    return ':'.join(map(lambda x: '%02x' % x, mac))


def get_rand_suffix(n=8):
    return ''.join(mac_nic_rand.choice(suffix_chars) for _ in xrange(n))
