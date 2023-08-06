from pybrary.func import memo

from setux.core.manage import Manager


class Distro(Manager):
    manager = 'net'

    @memo
    def addr(self):
        self.run('python3 -m pip install pybrary')
        ret, out, err = self.run('python3 -m pybrary get_ip_adr')
        res = out[0].strip('()')
        ok, adr = res.split(',')
        if ok.strip()=='True':
            return adr.strip(" '")
        else:
            debug(adr)
            return '!'

