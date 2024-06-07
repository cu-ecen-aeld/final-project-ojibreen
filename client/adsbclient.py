import pyModeS as pms
import threading
from pyModeS.extra.tcpclient import TcpClient
from datetime import datetime
import time
from rich.live import Live
from rich.table import Table

class ADSBClient(TcpClient):
    adsb_dict = {}
    table = Table()
    table.add_column("ICAO")
    table.add_column("Callsign")
    table.add_column("Velocity")
    table.add_column("Altitude")

    def __init__(self, host, port, rawtype):
        super(ADSBClient, self).__init__(host, port, rawtype)
        threading.Thread(target=self._live_display).start()

    def _live_display(self):
        with Live(self.table, refresh_per_second=0.4) as live:
            while True:
                time.sleep(0.5)
                
                self.table = Table()
                self.table.add_column("ICAO")
                self.table.add_column("Callsign")
                self.table.add_column("Velocity")
                self.table.add_column("Heading")
                self.table.add_column("Altitude")
                del_keys = []
                for icao, vals in self.adsb_dict.items():
                    now = datetime.now()

                    # If there has been no activity on this flight, skip and mark for deletion.
                    if(((now - vals["updated"]).total_seconds()) / 60 > 2):
                       del_keys.append(icao)
                       continue
                    if(("call" in vals) and ("velocity" in vals) and ("alt" in vals)):
                        self.table.add_row(f"{icao}", f"{vals['call']}", f"{vals['velocity']}", f"{vals['hdg']}", f"{vals['alt']}")
                
                for k in del_keys:
                    del self.adsb_dict[k]
                live.update(self.table)

    def handle_messages(self, messages):
            for msg, ts in messages:

                df = pms.df(msg)

                if pms.crc(msg) !=0:  # CRC fail
                    continue

                icao = pms.adsb.icao(msg)
                tc = pms.adsb.typecode(msg)
                now = datetime.now()

                if(icao not in self.adsb_dict):
                    self.adsb_dict[icao] = {"updated" : now, "call": "--", "velocity" : "--", "hdg" : "--", "alt" : "--"}
        
                if(tc in range(1,5)):
                    callsign = pms.adsb.callsign(msg)
                    callsign = callsign.replace("_", "")
                    self.adsb_dict[icao]["call"] = callsign
                    self.adsb_dict[icao]["updated"] = now

                if(tc == 19):
                    vel = pms.adsb.velocity(msg)          # Handles both surface & airborne messages
                    self.adsb_dict[icao]["velocity"] = vel[0]
                    self.adsb_dict[icao]["hdg"] = round(vel[1])
                    self.adsb_dict[icao]["updated"] = now
                
                if(tc in range(9, 19)):
                    alt = pms.adsb.altitude(msg)
                    self.adsb_dict[icao]["alt"] = alt
                    self.adsb_dict[icao]["updated"] = now
                #sh = pms.adsb.speed_heading(msg)     # Handles both surface & airborne messages
                #avel = pms.adsb.airborne_velocity(msg)
# run new client, change the host, port, and rawtype if needed
client = ADSBClient(host='10.0.0.104', port=30002, rawtype='raw')
client.run()

