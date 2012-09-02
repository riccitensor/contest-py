
class Registrar(object):
    def __init__(self, domain):
        self.domain = domain


class RegistrarA(Registrar):
    @classmethod
    def is_registrar_for(cls, domain):
        return domain == 'foo.com'


class RegistrarB(Registrar):
    @classmethod
    def is_registrar_for(cls, domain):
        return domain == 'bar.com'



def Domain(domain):
    for cls in Registrar.__subclasses__():
        if cls.is_registrar_for(domain):
            return cls(domain)
    raise ValueError


print Domain('foo.com')
print Domain('bar.com')
