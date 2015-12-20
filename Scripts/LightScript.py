import webiopi
GPIO = webiopi.GPIO


StofaGangur = 4				#p7 - 1A
StofaUtveggur = 25			#p6 - 1B
EldhusEyja = 22				#p3 - 2A
EldhusUtveggur = 23			#p4 - 2B
SjonvarpsholSkapur = 17		#p0 - 3A
SjonvarpsholUtveggur = 10	#MOSI - 3B
SjonvarpsholGangur = 18		#p1 - 3C
BordstofaBord = 9			#MISO - 4A
BordstofaUtveggur = 11		#SCLK - 4B
BordstofaGangur = 24		#p5 - 4C
BordstofaSkapur = 27		#p2 - 4D


Rofi1 = 7
Rofi2 = 8
Rofi3 = 3
Rofi4 = 2


# setup function is automatically called at WebIOPi startup
def setup():
    global switches
    switches = {Rofi1: LightControl(Rofi1, [SjonvarpsholGangur, SjonvarpsholSkapur, SjonvarpsholUtveggur, StofaGangur, StofaUtveggur]),
                Rofi2: LightControl(Rofi2, [BordstofaGangur, BordstofaUtveggur, BordstofaSkapur]),
                Rofi3: LightControl(Rofi3, [BordstofaBord]),
                Rofi4: LightControl(Rofi4, [EldhusEyja, EldhusUtveggur])}


# loop function is repeatedly called by WebIOPi
def loop():
    global switches
    for key, control in switches.items():
        control.update()
    webiopi.sleep(0.1)


# destroy function is called at WebIOPi shutdown
def destroy():
    webiopi.debug("Slekk")

	
# Classes
class LightControl:

    def __init__(self, inputBCM, lights):
        webiopi.info('LightControl has initialized for inputBCM {0} and lightsBCM {1}'.format(inputBCM, lights))
        self.inputBCM = inputBCM
        GPIO.setFunction(inputBCM, GPIO.IN, GPIO.PUD_UP)
        self.lightSet = LightSet(lights)
        self.lightSet.update()
        self.lastStatus = True

    def update(self):
        self.status = GPIO.digitalRead(self.inputBCM)
        if (not self.status):
            webiopi.debug('Switch read as {0} now and {1} last'.format(self.status, self.lastStatus))
        if (self.status != self.lastStatus and not self.status):
            self.lightSet.toggle()
        self.lastStatus = self.status
        self.lightSet.update()

    def addLight(self, light):
        self.lightSet.add(light)

    def removeLight(self, light):
        self.lightSet.remove(light)


class LightSet:

    def __init__(self, lights):
        self.lightSet = set(lights)
        self.isOn = False

    def update(self):
        self.isOn = True
        for light in self.lightSet:
            if not GPIO.digitalRead(light):
                #webiopi.debug('Light {0} is off'.format(light))
                self.isOn = False
                break
        #webiopi.debug('Light set is on set as {0}'.format(self.isOn))

    def toggle(self):
        webiopi.debug('Toggle light {0}'.format(self.lightSet))
        self.isOn = not self.isOn
        for light in self.lightSet:
            GPIO.digitalWrite(light, self.isOn)

    def add(self, light):
        self.lightSet.add(light)

    def remove(self, light):
        try:
            self.lightSet.remove(light)
        except KeyError:
            webiopi.warn('Tried to remove light {0} from set where is wasn\'t present'.format(light))


#macros
@webiopi.macro
def getLightSet(switchBCM):
    global switches
    return switches[switchBCM].lightSet