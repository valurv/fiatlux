import webiopi


GPIO = webiopi.GPIO


EldhusUtveggur = 17
StofaUtveggur = 18
EldhusEyja = 27
StofaGangur = 22
BordstofaGangur = 23
SjonvarpsholGangur = 24
BordstofaBord = 25
BordstofaSkapur = 4
SjonvarpsholSkapur = 10
BordstofaUtveggur = 9
SjonvarpsholUtveggur = 11


Takki1 = 8
Takki2 = 7
Takki3 = 2
Takki4 = 3


global Takki1Status, Takki2Status, Takki3Status, Takki4Status
Takki1Status = False
Takki2Status = False
Takki3Status = False
Takki4Status = False


Takki1Safn = set([EldhusUtveggur, EldhusEyja])
Takki2Safn = set([StofaUtveggur, StofaGangur])
Takki3Safn = set([BordstofaGangur, BordstofaBord, BordstofaSkapur, BordstofaUtveggur])
Takki4Safn = set([SjonvarpsholGangur, SjonvarpsholSkapur, SjonvarpsholUtveggur])


# setup function is automatically called at WebIOPi startup
def setup():
    global Takki1Status, Takki2Status, Takki3Status, Takki4Status
    GPIO.setFunction(Takki1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setFunction(Takki2, GPIO.IN, GPIO.PUD_UP)
    GPIO.setFunction(Takki3, GPIO.IN, GPIO.PUD_UP)
    GPIO.setFunction(Takki4, GPIO.IN, GPIO.PUD_UP)
    Takki1Status = GPIO.digitalRead(Takki1)
    Takki2Status = GPIO.digitalRead(Takki2)
    Takki3Status = GPIO.digitalRead(Takki3)
    Takki4Status = GPIO.digitalRead(Takki4)
    webiopi.debug(str(Takki4Status))


# loop function is repeatedly called by WebIOPi
def loop():
    global Takki1Status, Takki2Status, Takki3Status, Takki4Status
    #readStatus(Takki1,Takki1Status,Takki1Safn)
    #readStatus(Takki2,Takki2Status,Takki2Safn)
    #readStatus(Takki3,Takki3Status,Takki3Safn)
    readStatus(Takki4,Takki4Status,Takki4Safn)
    webiopi.sleep(0.3)


# destroy function is called at WebIOPi shutdown
def destroy():
    webiopi.debug("Slekk")


def readStatus(takki, takkaStada, takkaSafn):
    global Takki1Status, Takki2Status, Takki3Status, Takki4Status
    webiopi.debug("Les stöðu " + str(takki) + " " + str(takkaStada))
    Stada = GPIO.digitalRead(takki)
    webiopi.debug("Staðan var " + str(Stada))
    if (Stada != takkaStada):
        webiopi.debug("Breyti stöðu " + str(takki))
        takkaStada = Stada
        toggleLights(takkaSafn)


def toggleLights(takkaSafn):
    for light in takkaSafn:
        webiopi.debug("Breyti ljósi " + str(light))
        gildi = not GPIO.digitalRead(light)
        GPIO.digitalWrite(light, gildi)


# a simple macro without argument
# returns ON;OFF hours
@webiopi.macro
def getLightHours():
    return "%d;%d" % (HOUR_ON, HOUR_OFF)


# a macro with two arguments
# set ON, OFF hours
# returns ON;OFF hours
@webiopi.macro
def setLightHours(on, off):
    global HOUR_ON, HOUR_OFF
    HOUR_ON = int(on)
    HOUR_OFF = int(off)
    return getLightHours()
