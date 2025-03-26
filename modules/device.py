from miio import Yeelight

class DeviceController:
    def __init__(self, ip, token):
        self.lamp = Yeelight(ip, token) if ip and token else None

    def turn_on_lamp(self):
        if self.lamp:
            self.lamp.on()
            return True
        return False

    def turn_off_lamp(self):
        if self.lamp:
            self.lamp.off()
            return True
        return False