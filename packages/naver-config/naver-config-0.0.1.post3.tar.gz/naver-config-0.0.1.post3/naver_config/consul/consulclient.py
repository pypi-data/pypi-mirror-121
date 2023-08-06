import consul
 


class ConsulClient():
    def __init__(self):
        self.consul = consul.Consul()
        pass

    def getValue(self, key, index=None):
        self.index, self.data = self.consul.kv.get(key, index=index)
        pass

    def setValue(self, key, value):
        self.consul.kv.put(key, value)
        pass

    def deleteValue(self, key):
        self.consul.kv.delete(key)
        pass
    
    def getIndex(self):
        return self.index
    
    def getData(self):
        return self.data

    def getConsul(self):
        return self.consul
   