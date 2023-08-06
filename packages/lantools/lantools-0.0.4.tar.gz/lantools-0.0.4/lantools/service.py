class Service:
    def __init__(self):
        self.services = {}

    def __getattr__(self, name):
        if name not in self.services:
            try:
                method = getattr(self, "_{}".format(name))
                self.services[name] = method()
            except Exception as e:
                raise Exception('服务未找到。')

            self.services[name] = method()

        return self.services.get(name)
