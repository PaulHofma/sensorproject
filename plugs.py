import asyncio
import os
from tapo import ApiClient

class PlugController:
    
    # note that ip_1 corresponds to plug1, etc.
    # for this project, plug1 corresponds to temp regulator; (on = temp goes up)
    # plug2 corresponds to humidity regulator. (on = humidity goes down)
    def __init__(self, username, password, ip_1, ip_2 = ""):
        self.username = username
        self.password = password
        self.ip_1 = ip_1
        self.ip_2 = ip_2
        
        self.ready = False
        self.client = None
        self.plug1 = None
        self.plug2 = None
        
        asyncio.run(self.initialize())
    
    async def initialize(self):
        # intialize client and devices
        if not self.ready:
            print("initializing client")
            self.client = ApiClient(self.username, self.password)
            self.plug1 = await self.client.p100(self.ip_1)
            # self.plug2 = await client.p100(self.ip_2)
            self.ready = True
            print("Plugcontroller ready")
        else:
            print("Plugcontroller initialize was called, but controller was already set up. Skipping.")
        
    def device_select(self, plug_number, f_name):
        device = None
        if self.ready:
            if plug_number == 1:
                device = self.plug1
            elif plug_number == 2:
                device = self.plug2
            else:
                print(f"{f_name}: invalid plug # provided: {plug_number}")
        else:
            print(f"{f_name} called but not ready yet!")
        return device

        
    async def on(self, plug_number):
        device = self.device_select(plug_number, "on()")
        await device.on()
                            
    async def off(self, plug_number):
        device = self.device_select(plug_number, "off()")
        await device.off()
        
    async def info(self, plug_number):
        device = self.device_select(plug_number, "info()")
        info = await device.get_device_info()
        return info.to_dict()
    
    async def is_on(self, plug_number):
        info = await self.info(plug_number)
        return info.get("device_on")
    
    # toggle state for given plug and return new state (true for on, false for off)
    async def toggle(self, plug_number):
        is_on = await self.is_on(plug_number)
        print(f"state pre-toggle: {is_on}")
        if is_on:
            await self.off(plug_number)
            return False
        else:
            await self.on(plug_number)
            return True
        
        
async def test():
    tapo_username = "paul_hofma@hotmail.com"
    tapo_password = "eelcopi7"
    tapo_ip = "192.168.178.95"

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p100(tapo_ip)

    print("turning on")
    await device.on()

    print("waiting a bit...")
    await asyncio.sleep(2)

    print("turning off")
    await device.off()

    d_info = await device.get_device_info()
    print(f"Device info: {d_info.to_dict()}")

    d_usage = await device.get_device_usage()
    print(f"Device usage: {d_usage.to_dict()}")
    

if __name__ == "__main__":
    tapo_username = "paul_hofma@hotmail.com"
    tapo_password = "eelcopi7"
    tapo_ip = "192.168.178.95"
    
    async def test2(pc):
        print(await pc.toggle(1))
        print(await pc.info(1))
    
    pc = PlugController(tapo_username, tapo_password, tapo_ip)
    asyncio.run(test2(pc))
    