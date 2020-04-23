"""
Messages for the security system
"""
Restart = "system:RESTART"
TurnOff = "system:TURNOFF"
Ack = "system:ACK"


def retrieve(imgnum):
    return "system:{}".format(imgnum)
