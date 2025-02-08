import time
import pyvisa
import matplotlib.pyplot as plt
from netmiko import ConnectHandler
import re  # For regular expressions (iperf output parsing)

# Configuration (adjust these)
ATTENUATOR_VISA_ADDRESS = "TCPIP0::192.168.1.100::502::SOCKET"
WIRELESS_CLIENT_IP = "192.168.1.200"
WIRELESS_CLIENT_USERNAME = "your_username"
WIRELESS_CLIENT_PASSWORD = "your_password"
WIRELESS_INTERFACE = "wlan0"
IPERF_SERVER_IP = "192.168.1.101" # IP of the iperf server
TEST_RANGES_DB = range(0, 61, 5)
TEST_DURATION_SEC = 10  # Duration for iperf test at each attenuation level

class AttenuatorControl:
    # ... (same as previous example)

class WirelessClient:
    def __init__(self, ip, username, password, interface, iperf_server_ip):
        # ... (same as previous example)
        self.iperf_server_ip = iperf_server_ip

    def connect(self):
        # ... (same as previous example)

    def run_iperf(self):
        if not self.net_connect:
            raise Exception("Not connected to wireless client. Call connect() first.")

        try:
            command = f"iperf3 -c {self.iperf_server_ip} -t {TEST_DURATION_SEC} -i 1"  # Run iperf3 client
            output = self.net_connect.send_command(command)
            # Parse iperf output for bandwidth
            bandwidth = 0
            for line in output.splitlines():
                match = re.search(r"\[\s*5\]\s*(\d+\.\d+)\s*Mbits/sec", line)  # Example: [  5]   789.45 Mbits/sec
                if match:
                    bandwidth = float(match.group(1))
                    break # Stop looking after finding the rate
            if bandwidth == 0:
              print(f"Could not parse iperf output. Output was:\n{output}")
            return bandwidth
        except Exception as e:
            print(f"Error running iperf: {e}")
            return 0


    def close(self):
        # ... (same as previous example)


# Main script
if __name__ == "__main__":
    attenuator = None
    wireless_client = None
    try:
        attenuator = AttenuatorControl(ATTENUATOR_VISA_ADDRESS)
        wireless_client = WirelessClient(WIRELESS_CLIENT_IP, WIRELESS_CLIENT_USERNAME, WIRELESS_CLIENT_PASSWORD, WIRELESS_INTERFACE, IPERF_SERVER_IP)
        wireless_client.connect()

        bandwidths = []
        attenuations = []

        for db in TEST_RANGES_DB:
            attenuator.set_attenuation(db)
            time.sleep(2) # Added a small delay to ensure the attenuation is set
            bandwidth = wireless_client.run_iperf()
            bandwidths.append(bandwidth)
            attenuations.append(db)

        # Plotting
        plt.plot(attenuations, bandwidths, marker='o')
        plt.xlabel("Attenuation (dB)")
        plt.ylabel("Iperf Bandwidth (Mbits/sec)")
        plt.title("Iperf Bandwidth vs. Attenuation")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if attenuator:
            attenuator.close()
        if wireless_client:
            wireless_client.close()
