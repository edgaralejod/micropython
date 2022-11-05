from time import sleep
import led

#Class that encompasses the whole Data acquisition system logic.
#This should be rewritten as a class that receives a ADG715 object and
#a AD5934 Object.
class Waterbot:

	def __init__(self, i2c):
	
		#Address of the AD5934 chip
		self.AD5934 = 0x0D

		#Address of the ADG715 chips
		self.ADG715_1 = 0x48
		self.ADG715_2 = 0x49

		#AD5934 commands (Available in Datasheet)
		self.AD5934SetPointerCommand = 0xB0
		self.AD5934BlockWrite = 0xA0
		self.AD5934BlockRead = 0xA1

		#AD5934 Control Register Definitions
		self.AD5934_CLOCK_EXTERNAL = 0x08
		self.AD5934_CLOCK_INTERNAL = 0x00
		self.AD5934_RESET = 0x10
		self.AD5934_PGA_1 = 0x01
		self.AD5934_PGA_5 = 0x00
		self.AD5934_2V_PP = 0x00
		self.AD5934_1V_PP = 0x06
		self.AD5934_400_mV = 0x04
		self.AD5934_200_mV = 0x02

		#AD5934 Control Register commands
		self.AD5934_INIT_START_FREQ = 0x10
		self.AD5934_START_FREQ_SWP  = 0x20
		self.AD5934_INC_FREQ = 0x30
		self.AD5934_REPEAT_FREQ = 0x40
		self.AD5934_PWD_DOWN = 0xA0
		self.AD5934_STANDBY = 0xB0

		#AD5934 Status Register checks
		self.AD5934_VALID_DATA = 0x02
		self.AD5934_FREQ_SWEEP_CMPL = 0x04

		#AD5934 Address Space
		self.AD5934_REG_CONTROL_HB = 0x80 #R/W, 2 bytes
		self.AD5934_REG_CONTROL_LB = 0x81 #R/W, 2 bytes
		self.AD5934_REG_FREQ_START_HB = 0x82 #R/W, 3 bytes
		self.AD5934_REG_FREQ_START_MB = 0x83  
		self.AD5934_REG_FREQ_START_LB = 0x84  
		self.AD5934_REG_FREQ_INC_HB = 0x85 #R/W, 3 bytes
		self.AD5934_REG_FREQ_INC_MB = 0x86   
		self.AD5934_REG_FREQ_INC_LB = 0x87    
		self.AD5934_REG_INC_NUM_HB = 0x88 #R/W, 2 bytes, 9 bit
		self.AD5934_REG_INC_NUM_LB = 0x89
		self.AD5934_REG_SETTLING_CYCLES_HB = 0x8A #R/W, 2 bytes
		self.AD5934_REG_SETTLING_CYCLES_LB = 0x8B
		self.AD5934_REG_STATUS = 0x8F #R, 1 byte
		self.AD5934_REG_TEMP_DATA_HB = 0x92 #R, 2 bytes
		self.AD5934_REG_TEMP_DATA_LB = 0x93
		self.AD5934_REG_REAL_DATA_HB = 0x94 #R, 2 bytes
		self.AD5934_REG_REAL_DATA_LB = 0x95
		self.AD5934_REG_IMAG_DATA_HB = 0x96 #R, 2 bytes 
		self.AD5934_REG_IMAG_DATA_LB = 0x97

		#ADG715 Switch Definitions
		self.ADG715_YX = 0x40
		self.ADG715_THRM = 0x80
		self.ADG715_RCAL_10K = 0x20
		self.ADG715_RCAL_1K = 0x10
		self.ADG715_RCAL_100 = 0x08
		self.ADG715_RFBK_10K = 0x04
		self.ADG715_RFBK_1K = 0x02
		self.ADG715_RFBK_100 = 0x01

		#Constants used in calculations
		self.AD5934_EXT_MCLK = 16000000 #1MHz external clock

		self.readValues = []
		self.sweepData = []
		self.readSweep = {}
		self.readMagnitude = -1

		#Variables for sweeping
		self.incrementFrequency = 0
		self.currentFreq = 0
		self.incFreqSetting = 0
		self.stFreqSetting = 0
		self.voltageSetting = 0
		self.pgaSetting = 0

		#Declaring I2C bus
		self.i2c = i2c

	##################################################################################
	#-------------------------------Device Functions---------------------------------#
	##################################################################################

	# Function to clear channel
	def ADG715ClearChannel(self, channel):
		bytes_zero = [0]
		if channel == self.ADG715_1:
			self.i2c.writeto(0x48, bytes(bytes_zero))
		elif channel == self.ADG715_2:
			self.i2c.writeto(0x49, bytes(bytes_zero))
		else:
			print("Invalid Channel")

	# Set channel to a value
	def ADG715SetChannel(self, channel, value):
		value_bytes = []
		value_bytes.append(value)
		#print(bytes(value_bytes))
		if channel == self.ADG715_1:
			self.i2c.writeto(0x48, bytes(value_bytes))
		elif channel == self.ADG715_2:
			self.i2c.writeto(0x49, bytes(value_bytes))
		else:
			print("Invalid Channel")

	# Read from a channel
	def ADG715ReadChannel(self, channel):
		if channel == self.ADG715_1:
			return self.i2c.readfrom(0x48, 1)
		elif channel == self.ADG715_2:
			return self.i2c.readfrom(0x49, 1)
		else:
			print("Invalid Channel")

	# Write to 5934 chip
	def AD5934WriteRegister(self, address, data):
		add_arr = []
		data_arr = []
		add_arr.append(address)
		data_arr.append(data)
		data_bytes = bytes(data_arr)
		self.i2c.writeto_mem(self.AD5934, address, data_bytes)

	# Function to set the address pointer in the AD5934 chip
	def AD5934SetPointer(self, address):
		add_arr = []
		add_arr.append(self.AD5934SetPointerCommand)
		add_bytes = bytes(add_arr)
		self.i2c.writeto_mem(self.AD5934, address, add_bytes)

	# Retrieves one byte from where the pointer was set. Prints to console
	def AD5934ReadPointer(self):
		print(self.i2c.readfrom(self.AD5934, 1))

	# Gets values from AD5934
	def AD5934GetValues(self, init_address, numberOfBytes):
		self.AD5934SetPointer(init_address)
		#print("I am getting the values")
		for i in range(0, numberOfBytes):
			AD5934Read = self.i2c.readfrom(self.AD5934, 1)
			Hex = ord(AD5934Read)
			self.readValues.append('{0:02x}'.format(Hex))
			i = i #Dummy just to make lynt happy while I change the for loop

	#Function that sets the number of increments for the frequency sweep
	def AD5934SetIncrementNumber(self, numIncrements):
		numIncBytes = self.longToByteArray(numIncrements)
		self.AD5934WriteRegister(self.AD5934_REG_INC_NUM_HB, numIncBytes[1])
		self.AD5934WriteRegister(self.AD5934_REG_INC_NUM_LB, numIncBytes[0])

	#Function to set the start frequenct for the frequency sweep
	def AD5934SetStartFrequency(self, frequency):
		freq_calc = round((2**27)*(frequency)/(self.AD5934_EXT_MCLK/16))
		new_freq_calc = self.longToByteArray(freq_calc)
		self.AD5934WriteRegister(self.AD5934_REG_FREQ_START_HB, new_freq_calc[2])
		self.AD5934WriteRegister(self.AD5934_REG_FREQ_START_MB, new_freq_calc[1])
		self.AD5934WriteRegister(self.AD5934_REG_FREQ_START_LB, new_freq_calc[0])

	#Function that sets the increment frequency for the frequency sweep
	def AD5934SetIncrementFrequency(self, frequency):
		freq_calc = round((2**27)*(frequency)/(self.AD5934_EXT_MCLK/16))
		new_freq_calc = self.longToByteArray(freq_calc)
		self.AD5934WriteRegister(self.AD5934_REG_FREQ_INC_HB, new_freq_calc[2])
		self.AD5934WriteRegister(self.AD5934_REG_FREQ_INC_MB, new_freq_calc[1])
		self.AD5934WriteRegister(self.AD5934_REG_FREQ_INC_LB, new_freq_calc[0])

	#Function that converts rounded int of the frequency calculation to an array of 8 bytes
	def longToByteArray(self, longNum):
		byteArray = [None] * 8
		for i in range(0, len(byteArray)):	
			byte = int(longNum) & 0xff
			byteArray[i] = byte
			longNum = (longNum - byte) / 256
		return byteArray
	#This method clear the last value read from the I2C bus and then
	#continously reads the status to move towards the next state.
	def clearAndGetValue(self):
		self.readValues = [] #Clear past read values
		#print("I am here in Clear and get")
		self.AD5934GetValues(self.AD5934_REG_STATUS, 1)
		#sleep(0.2)

	##################################################################################
	#--------------------------------Sweep Process-----------------------------------#
	##################################################################################
	#Sweep init writes the appropiate registers to the sweep logic. 
	#TODO: Do I really need the sleep(0.2)? Need to test and try to determine
	#if the delays really make a difference for stability.
	def sweepInit(self):
		self.currentFreq = self.stFreqSetting

		self.AD5934WriteRegister(self.AD5934_REG_CONTROL_LB, self.AD5934_CLOCK_EXTERNAL | self.AD5934_RESET)
		#sleep(0.2)

		self.AD5934WriteRegister(self.AD5934_REG_CONTROL_HB, self.AD5934_STANDBY | self.voltageSetting | self.pgaSetting )
		#sleep(0.2)

		self.AD5934WriteRegister(self.AD5934_REG_CONTROL_HB, self.AD5934_INIT_START_FREQ | self.voltageSetting | self.pgaSetting )
		#sleep(0.2)

		self.AD5934WriteRegister(self.AD5934_REG_CONTROL_HB, self.AD5934_START_FREQ_SWP | self.voltageSetting | self.pgaSetting )	
		#sleep(0.2)

		self.clearAndGetValue()
		return self.sweepProcess()

	#This method computes the impedance and it populates and creates the
	#data structures that then get sent to the cloud.
	def sweepIncrement(self):
		led.led_toogle('yellow')
		self.AD5934GetValues(self.AD5934_REG_REAL_DATA_HB, 4)

		# print(self.readValues)
		# print("RawReal")
		# print(self.readValues[1])
		# print(self.readValues[2])
		# print("RawImg")
		# print(self.readValues[3])
		# print(self.readValues[4])
		realVal = self.readValues[1] + self.readValues[2]
		imgVal = self.readValues[3] + self.readValues[4]

		# print("Sums")
		# print(realVal)
		# print(imgVal)
		realVal = (int(self.readValues[1], 16) << 8) + int(self.readValues[2], 16)
		imgVal = (int(self.readValues[3], 16) << 8) + int(self.readValues[4], 16)		
		if (realVal & 0x8000) > 1:
			realVal = realVal - 0x10000
		if (imgVal & 0x8000) > 1:
			imgVal = imgVal - 0x10000

		# print("Real and imaginary to signed")
		# print(realVal)
		# print(imgVal)		
		self.readSweep['currentFreq'] = self.currentFreq
		self.readSweep['imgVal'] = imgVal
		self.readSweep['realVal'] = realVal
		realVal = realVal**2
		imgVal = imgVal**2	
		self.readMagnitude = (realVal + imgVal)**0.5
		self.readSweep['magnitude'] = self.readMagnitude
		self.sweepData.append(dict(self.readSweep))
		self.currentFreq = self.currentFreq + self.incFreqSetting
		cfgReg = ( self.voltageSetting | self.pgaSetting | self.AD5934_INC_FREQ )
		self.AD5934WriteRegister(self.AD5934_REG_CONTROL_HB, cfgReg)
		self.clearAndGetValue()
		self.sweepProcess()
		#sleep(0.2)
		led.led_off()

	def sweepProcess(self):
		hexcompare = self.readValues[0]
		#original = self.readValues[0]
		# print("No transformation:")
		# print(hexcompare)
		# print("Transformed")
		hexcompare = hexcompare[1]
		# print(hexcompare)
		if hexcompare == '0':
			while(hexcompare == '0'):	
				# print("I am in a loop")
				hexcompare = self.readValues[0]
				# print("No transformation:")
				# print(hexcompare)
				# print("Transformed")
				hexcompare = hexcompare[1]
				# print(hexcompare)
				self.clearAndGetValue()
		
		if hexcompare == '2':
			self.sweepIncrement()
			
		elif hexcompare == '6':
			pass
			#print("done")		
		else :
			raise OSError ("Analog Subsystem Failure")

	def ad5934Init(self):
		self.AD5934SetStartFrequency(1000)
		self.AD5934SetIncrementFrequency(500)
		self.AD5934SetIncrementNumber(1)
		self.AD5934WriteRegister(self.AD5934_REG_CONTROL_LB, self.AD5934_CLOCK_EXTERNAL | self.AD5934_RESET)
		#sleep(0.2)
		self.AD5934WriteRegister(self.AD5934_REG_CONTROL_LB, self.AD5934_CLOCK_EXTERNAL)
		#sleep(0.2)
		self.AD5934WriteRegister(self.AD5934_REG_CONTROL_HB, self.AD5934_STANDBY | self.AD5934_2V_PP | self.AD5934_PGA_1)
		#sleep(0.2)
		self.ADG715ClearChannel(self.ADG715_1)
		self.ADG715ClearChannel(self.ADG715_2)
		#print("AD5934 Init method")

	def setAnalogSwitch(self, swNum, afeGain, portSetting ):
		self.ADG715ClearChannel(self.ADG715_1)
		self.ADG715ClearChannel(self.ADG715_2)
		self.ADG715SetChannel(swNum, afeGain | portSetting )
		#print("Setting Analog Switch")

	def sweepCommand(self, gain, startFreq, incFreq, voltage, incNum):
		led.led_off()
		led.led_color('yellow')
		#print("On sweep Command")
		self.AD5934SetStartFrequency(startFreq)
		self.AD5934SetIncrementFrequency(incFreq)
		self.AD5934SetIncrementNumber(incNum)	
		self.voltageSetting = voltage
		self.pgaSetting = gain
		self.stFreqSetting = startFreq
		self.incFreqSetting = incFreq
		self.sweepInit()
		led.led_color('green')
		#print(self.sweepData)
		return self.sweepData

	def clearSweepObject(self):
		self.sweepData = []
		return
    		
