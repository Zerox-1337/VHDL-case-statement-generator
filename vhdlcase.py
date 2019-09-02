import numpy as np


def decToHex(x, numHex):
	string = "{0:0" + str(numHex) + "x}";
	return string.format(x);

def decToBinary(x, numBits): # If 7 for example it can't be less than the bits it takes to represent 7. 
	string = "{0:0" + str(numBits) + "b}";
	return string.format(x);
def countBits(xBinary):
	return len(xBinary);



f = open('test.txt', 'w')

currBitCount = 0

lastIndex = 1



keySignalName = "oControllerKey"
ivSignalName = "oControllerIv"
counterName = "controllerAttackCounterReg"
copyName = "controllerLfsrCopyReg" # Might not be needed in this code
caseSignal = "controllerMdmSelReg"
caseSignalLenIndex = 224; # The maximum length of the lookup table 
updateName = ivSignalName; # 0 to 95 will print out the iv update name
startSpace = "       "
ivLength = 96


bitChangeIndex = [0,0,0,0,0,0,0,0]; 

def generate_case(f, maxValue, minValue, adressMaxIndex, adressMinIndex, addressLen, defaultCase): # Might wanna remove the enable signal
	f.write(startSpace + "if (" +caseSignal + "("+ str(maxValue*8 + 7)+ ") = '1' and  " +caseSignal + "("+ str(maxValue*8 + 6) +") = '1' and " +caseSignal + "(" + str(maxValue*8 + 5)+ ") = '1') then\n") # Enable signal

	
	realIndexVal = maxValue # Just for the printed code in updatename
	if (realIndexVal >=  ivLength):
		realIndexVal = maxValue - ivLength;
	f.write(str(startSpace) + "  "+updateName + "("+ str(realIndexVal) +") <= " + copyName + "("+ str(realIndexVal) +");\n") # 
	f.write(str(startSpace) + 'else\n')
	f.write(startSpace + "  case " + caseSignal + "("+ str(adressMaxIndex) +" downto "+ str(adressMinIndex) +") is -- Index Mux " + str(i) + "\n")
	for k in range (0, maxValue + 1): # Won't generate cases for first 0
		f.write(str(startSpace) + '    when "' + decToBinary(k, addressLen)+ '" => ' + updateName + '('+ str(realIndexVal) +') <= ' + counterName +'(' +str(k) + ');\n') # Index + 1 gives max bits.
		
	if (defaultCase == 1):
		f.write(str(startSpace) + "    when others => " + updateName + "("+ str(realIndexVal) +") <= '0';\n") # Index + 1 gives max bits.
	f.write(str(startSpace) + '  end case;\n')
	
	
	
	f.write(str(startSpace) + 'end if;\n')
	



iMax = 224
for i in range(0, iMax):
	x = decToBinary(i, 0) # Binary of i
	copyName = "controllerLfsrCopyReg"
	updateName = ivSignalName;
	if (i >= 96):
		updateName = keySignalName;
		copyName = "controllerNfsrCopyReg";

	xLen = countBits(x) # length of x
	if (i == (iMax-1)):
		generate_case(f, i, 0, 8*i + xLen-1, i*8, xLen, 1) # xlen is 1 to 8 basically. Needs to be 0 to 7.
	else:
		generate_case(f, i, 0, 8*i + xLen-1, i*8, xLen, 1)
	
	


