# -*- coding:utf-8 -*-
__version__ = "0.1.0"

import socket
import threading
import time
from queue import LifoQueue


class TianbotMini:
    def __init__(self, host):
        self.host = host
        self.delay = 0.1
        self.msg_queue = LifoQueue()
        self.received_cmd = False
        self._socket = socket.socket()
        self._keep_running = True
        self._receiver = threading.Thread(target=self._read_msg)

    @property
    def response_msg(self):
        time.sleep(self.delay)
        return self.msg_queue.get()

    def cmd(self, cmd):
        cmd = cmd + "\r\n"
        self._socket.send((cmd.strip() + "\r\n").encode("utf-8"))

    def begin(self, freq):
        self._socket.connect((self.host, 23))
        self._receiver.start()
        self.delay = 1.0 / freq
        self.cmd("useprog 1")
        self.cmd("r")

    def end(self):
        self.stop()
        self.cmd("useprog 0")
        self.cmd("r")
        self._keep_running = False
        self._socket.close()

    def motor(self, pwm1, pwm2):
        self.cmd("m " + str(pwm1) + " " + str(pwm2))

    def led(self, id, r, g, b):
        self.cmd("l " + str(id) + " " + str(r) + " " + str(g) + " " + str(b))

    def stop(self):
        self.motor(0, 0)

    def rstenc(self):
        self.cmd("r")

    def getenc(self):
        self.cmd("e")
        msg = self.response_msg
        if len(msg) == 2:
            return False, int(msg[0]), int(msg[1])
        return True, 0, 0

    def getpid(self):
        self.cmd("showpid")
        msg = self.response_msg
        if len(msg) == 5:
            return [float(i) for i in msg[1:]]
        return [-1, -1, -1, -1]

    def getrmip(self):
        self.cmd("showrmip")
        msg = self.response_msg
        if len(msg) == 2:
            return msg[1]
        return -1

    def getbase(self):
        self.cmd("showbase")
        msg = self.response_msg
        if len(msg) == 6:
            return [float(i) for i in msg[1:]]
        return [-1, -1, -1, -1, -1]

    def getbatt(self):
        self.cmd("showbatt")
        msg = self.response_msg
        if len(msg) == 2:
            return msg[1]
        return -1

    def _read_msg(self):
        receive_msg = ""
        while self._keep_running:
            try:
                data = self._socket.recv(1).decode()
            except OSError:
                break
            if data == "\n":
                self.received_cmd = True
                self.msg_queue.put(
                    [i.strip() for i in filter(None, receive_msg.split(" "))]
                )
                receive_msg = ""
            else:
                receive_msg += data


if __name__ == "__main__":
    tianbotMini = TianbotMini("tianbot_mini.local")  # 连接TianbotMini( hostname )
    tianbotMini.begin(10)
    LEFT = 0

    # 控制左轮转12圈
    while LEFT < 350 * 4:
        tianbotMini.motor(500, 500)  # 配置左右电机速度为500,-500
        try:
            err, LEFT, right = tianbotMini.getenc()  # 读取左右电机编码器计数
            if not err:
                print("编码器（左边，右边）：" + str(LEFT) + ", " + str(right))
                if (LEFT / 350) > 9:
                    tianbotMini.led(0, 255, 0, 0)  # 配置机器人状态指示灯为红色
                else:
                    if (LEFT / 350) > 6:
                        tianbotMini.led(0, 0, 255, 0)  # 配置机器人状态指示灯为绿色
                    else:
                        if (LEFT / 350) > 3:
                            tianbotMini.led(0, 255, 255, 255)  # 配置机器人状态指示灯为白色
        except:
            pass

    tianbotMini.led(0, 255, 255, 255)  # 配置机器人状态指示灯为蓝色
    tianbotMini.stop()  # 控制机器人停止运动

    kp, ki, kd, ko = tianbotMini.getpid()
    print("Kp " + str(kp))
    print("Ki " + str(ki))
    print("Kd " + str(kd))
    print("Ko " + str(ko))

    ws, wd, cpr, cpm, mpc = tianbotMini.getbase()
    print("Ws " + str(ws))
    print("Wd " + str(wd))
    print("CPR " + str(cpr))
    print("CPM " + str(cpm))
    print("MPC " + str(mpc))

    rmip = tianbotMini.getrmip()
    print("RMIP " + str(rmip))

    batt = tianbotMini.getbatt()
    print("BATT " + str(batt))

    tianbotMini.end()
