import serial.tools.list_ports
from serial import Serial
import datetime
import time

millis = lambda: int(round(time.time() * 1000))


if __name__ == '__main__':
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if p.serial_number == '55632313838351214152':
            try:
                bluetooth = Serial(p.device, 115200, timeout=0.1)
                bluetooth.write('r\r\n'.encode('ascii', 'replace'))
                filename = datetime.datetime.now().strftime("./gyro_record_%Y%m%d-%H%M%S.csv")

                with open(filename, 'w') as f:
                    # f.write('time, roll, pitch\n')
                    interval = millis()

                    f.write('time,yaw,pitch,roll,acc x,acc y,acc z\n')

                    while True:
                        if millis() - interval > 1000:
                            bluetooth.write('r\r\n'.encode('ascii', 'replace'))
                            interval = millis()
                        while bluetooth.in_waiting:
                            packet = bluetooth.readline().decode('ascii', 'replace').split()
                            if len(packet) == 7:
                                f.write(datetime.datetime.now().__str__())
                                for value in packet[1:]:
                                    f.write(',' + value)
                                f.write('\n')
                            """
                            elif chr(int.from_bytes(packet[:1], byteorder='big')) == '$' and len(packet) == 14:
                                q = []
                                q.append(((packet[2] << 8) | packet[3]) / 16384)
                                q.append(((packet[4] << 8) | packet[5]) / 16384)
                                q.append(((packet[6] << 8) | packet[7]) / 16384)
                                q.append(((packet[8] << 8) | packet[9]) / 16384)
                                for i in range(4):
                                    if q[i] >= 2:
                                        q[i] = -4 + q[i]
                                gravity = [0, 0, 0]
                                ypr = [0, 0, 0]
                                gravity[0] = 2 * (q[1] * q[3] - q[0] * q[2])
                                gravity[1] = 2 * (q[0] * q[1] + q[2] * q[3])
                                gravity[2] = q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]
                                ypr[0] = math.atan2(2 * q[1] * q[2] - 2 * q[0] * q[3],
                                                    2 * q[0] * q[0] + 2 * q[1] * q[1] - 1)
                                ypr[1] = math.atan(
                                    gravity[0] / math.sqrt(gravity[1] * gravity[1] + gravity[2] * gravity[2]))
                                ypr[2] = math.atan(
                                    gravity[1] / math.sqrt(gravity[0] * gravity[0] + gravity[2] * gravity[2]))
                                print("ypr:\t", ypr[0] * 180.0 / math.pi, "\t", ypr[1] * 180.0 / math.pi, "\t",
                                      ypr[2] * 180.0 / math.pi)
                            """
            except Exception as e:
                print(e)