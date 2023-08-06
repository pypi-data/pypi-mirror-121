from pybrary.func import memo

from setux.core.manage import Manager


class Distro(Manager):
    manager = 'net'

    @memo
    def addr(self):
        self.run('python3 -m pip install -U pybrary')
        ret, out, err = self.run('get_ip_adr')
        return out[0]

