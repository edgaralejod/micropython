from frozen_fmwupg import FmwUpgradeMachine

class LocalBleError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
		

class LocalBleProcess():
	def __init__(self, radioObject, attindex):
		self._FSM_INIT = 0
		self._FSM_PARSING_CMD = 1
		self._FSM_FMWUPGRADE = 2
		self._FSM_CFG_READ = 3
		self._FSM_CFG_WRITE = 4
		self._FSM_LOCAL_CONTROL = 5
		self._radio = radioObject
		self._bleattribute = attindex
		self._fmwUpgradationMachine = FmwUpgradeMachine()
		self._rcvmsg = ""
		self._state = self._FSM_PARSING_CMD
		self._txdata = {}

	def processCommand(self, command):
		print('LocalBleProcess processCommand: ' + str(command))
		if command == 'commsinit':
			self._txdata['reply'] = 'OK'
			self.sendReplySubprocess(self._txdata)
		elif command == 'ping':
			self._txdata['reply'] = 'PING'
			self.sendReplySubprocess(self._txdata)
		elif command == 'fmwupg':
			self._state = self._FSM_FMWUPGRADE
			self._fmwUpgradationMachine.start()
		elif command == 'cfgread':
			self._txdata['reply'] = str(self.readConfigFile())
			self.sendReplyProcess(self._txdata)

	def receiveData(self, data):
		print('LocalBleProcess receiveData: ' + str(data))
		if self._state == self._FSM_PARSING_CMD:
			try:	
				evaluated = eval(data)
				print('command: ' + evaluated['command'])
				self.processCommand(evaluated['command'])
			except Exception as e:
				raise LocalBleError('Error evaluating command: ' + str(e))
		elif self._state == self._FSM_FMWUPGRADE:
			try:	
				self._fmwUpgradationMachine.receiveData(data)
			except Exception as e:
				raise LocalBleError('Error Running Firmware Update: ' + str(e))			

	def sendReplyProcess(self, data):
		print('In the Send Reply Process')
		# tx_header = {}
		# tx_header['chk'] = self._fmwUpgradationMachine.calculateFileChecksum(data)
		# pass

	def sendReplySubprocess(self, data):
		if len(data) > 20:
			raise LocalBleError('Strings longer than 20 characters not supported!')
		else:
			self._radio.set_attr_value(self._bleattribute, str(data))

	def readConfigFile(self):
		f = open('config.json')
		cfg_file = f.read()
		#dec_cred = decode(dec_key, wifi_cred)
		#eval_cred = eval(dec_cred)
		eval_cred = eval(wifi_cred)
		f.close()
		return cfg_file