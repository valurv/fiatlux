import webiopi
GPIO = webiopi.GPIO


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
        webiopi.debug('Switch read as {0} now and {1} last'.format(self.status, self.lastStatus))
        if (self.status != self.lastStatus && not self.status):
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
        self.isOn = false

    def update(self):
        self.isOn = true
        for light in self.lightSet:
            if not GPIO.digitalRead(light):
                webiopi.debug('Light {0} is off'.format(light))
                self.isOn = false
                break
        webiopi.debug('Light set is on set as {0}'.format(self.isOn))

    def toggle(self):
        for light in self.lightSet:
            GPIO.digitalWrite(light, self.isOn)

    def add(self, light):
        self.lightSet.add(light)

    def remove(self, light):
        try:
            self.lightSet.remove(light)
        except KeyError:
            webiopi.warn('Tried to remove light {0} from set where it wasn\'t present'.format(light))
