from sys import argv

from pybrary.net import get_ip_adr


_, name, *arg = argv
fct = globals()[name]
res = fct(*arg)
print(res)
