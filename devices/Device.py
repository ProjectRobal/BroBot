

class Device:
    def __init__(self,name,id,port):
        self._name=name
        self._id=id
        self._port=port
        self._data={}
        self._keys=()
        self._towrite=()
        self._toupdate=False

    def start(self):
        raise NotImplementedError()
    
    def port(self):
        return self._port

    def id(self):
        return self._id

    def name(self):
        return self._name
    
    #function to read data from device
    def download(self):
        raise NotImplementedError()

    #process readed data
    def process(self):
        raise NotImplementedError()
    
    #function to write data to device
    def upload(self):
        raise NotImplementedError()

    def write(self,data):
        self._toupdate = True

        for k in data.keys():
            if k in self._towrite:
                self._data[k]=data[k]
            

    # function to return data to device
    def read(self):
        return self._data

    # function to return keys of data readed by device
    def keysToRead(self):
        return self._keys

    def keysToWrite(self):
        return self._towrite

    # call when critical error happened
    def emergency(self):
        pass