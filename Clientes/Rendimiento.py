class Rendimiento:
    def setSO(self,so):
        self.so = so
    
    def getSO(self):
        return self.so
    
    def setTimeActivity(self,time):
        self.time = time
    
    def getTimeActivity(self):
        return self.time
    
    def setNumberInterfaces(self,interfaces):
        self.interfaces = interfaces
    
    def getNumberInterfaces(self):
        return self.interfaces
    
    def setResponseSMTP(self,responseSMTP):
        self.responseSMTP = responseSMTP
    
    def getResponseSMTP(self):
        return self.responseSMTP
    
    def setResponseIMAP(self,responseIMAP):
        self.responseIMAP = responseIMAP
    
    def getResponseIMAP(self):
        return self.responseIMAP
    
    def getResponseSmtpImap(self):
        return self.responseIMAP + self.responseSMTP
    
    def setStatusSMTP(self,statusSMTP):
        self.statusSMTP = statusSMTP
    
    def getStatusSMTP(self):
        return self.statusSMTP
    
    def setResponseHTTP(self,responseHTTP):
        self.responseHTTP = responseHTTP
    
    def getResponseHTTP(self):
        return self.responseHTTP
    
    def setBytesReceiveHTTP(self,bytesHTTP):
        self.bytesHTTP = bytesHTTP
    
    def getBytesReceiveHTTP(self):
        return self.bytesHTTP
    
    def setSpeedDownload(self,speed):
        self.speed = speed
    
    def getSpeedDownload(self):
        return self.speed

    def setStatusHTTP(self,statusHTTP):
        self.statusHTTP = statusHTTP
    
    def getStatusHTTP(self):
        return self.statusHTTP
    
    def setResponseFTP(self,responseFTP):
        self.responseFTP = responseFTP
    
    def getResponseFTP(self):
        return self.responseFTP
    
    def setTimeResponseFTP(self,timeResponseFTP):
        self.timeResponseFTP = timeResponseFTP
    
    def getTimeResponseFTP(self):
        return self.timeResponseFTP
    
    def setStatusFTP(self,statusFTP):
        self.statusFTP = statusFTP
    
    def getstatusFTP(self):
        return self.statusFTP
    
    def setServerFileCountFTP(self,serverFileCountFTP):
        self.serverFileCountFTP = serverFileCountFTP
    
    def getServerFileCountFTP(self):
        return self.serverFileCountFTP
    
    def setResponseDNS(self,responseDNS):
        self.responseDNS = responseDNS
    
    def getResponseDNS(self):
        return self.responseDNS
    
    def setStatusDNS(self,statusDNS):
        self.statusDNS = statusDNS
    
    def getStatusDNS(self):
        return self.statusDNS
    
    def setNumberConectionsSSH(self,numberConectionsSSH):
        self.numberConectionsSSH = numberConectionsSSH
    
    def getNumberConectionsSSH(self):
        return self.numberConectionsSSH
    
    def setInputTraficSSH(self,inputTraficSSH):
        self.inputTraficSSH = inputTraficSSH
    
    def getInputTraficSSH(self):
        return self.inputTraficSSH
    
    def setOutputTraficSSH(self,outputTraficSSH):
        self.outputTraficSSH = outputTraficSSH
    
    def getOutputTraficSSH(self):
        return self.outputTraficSSH
    
    def setTimeSSH(self,timeSSH):
        self.timeSSH = timeSSH
    
    def getTimeSSH(self):
        return self.timeSSH
    
    def setStatusSSH(self,statusSSH):
        self.statusSSH = statusSSH
    
    def getStatusSSH(self):
        return self.statusSSH
    
    def setPathImageRAM(self,pathImageRAM):
        self.pathImageRAM = pathImageRAM
    
    def getPatImageRAM(self):
        return self.pathImageRAM
    
    def setPathImageHDD(self,pathImageHDD):
        self.pathImageHDD = pathImageHDD
    
    def getPathImageHDD(self):
        return self.pathImageHDD
    
    def setPathImageCPU(self,pathImageCPU):
        self.pathImageCPU = pathImageCPU
    
    def getPathImageCPU(self):
        return self.pathImageCPU