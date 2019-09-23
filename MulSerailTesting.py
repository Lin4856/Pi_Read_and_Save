"""
For long-term testing device. Use serial(converted to USB) to receive data and use U disk to save it.
Support up to 3 at same time. Can be upgraded to 4(if without USB instead).
Author: Lin
Date: 2019/09/19
Coding: utf-8
Python3.7
"""

import serial
import time
import threading
import os


# create multi thread.
class MyThread (threading.Thread):
    def __init__(self, device_id):
        threading.Thread.__init__(self)
        self.device_id = device_id

    def run(self):
        threading.Lock().acquire()
        main(self.device_id)
        threading.Lock().release()


def serial_select(port_name='ttyUSB0', baud_rate=57600, time_out=0.5):
    """
    Select the right serial.
    :param port_name: check on raspberry pi: ls /dev/ttyUSB*
    :param baud_rate: device default baud-rate
    :param time_out: serial timeout parameter
    :return: return selected port
    """
    return serial.Serial("/dev/" + port_name, baudrate=baud_rate, timeout=time_out)
    

def print_local_time():
    """
    Print time info.
    :return: return the local time for storage purpose.
    """
    localtime = time.strftime("%Y %b %d %H:%M:%S ", time.localtime())
    return localtime


def write_file(write_data, file_name="fdata.txt", folder_path="/media/pi/2766-0661/temp_folder/"):
    """
    Write the write_data to selected file.
    :param write_data: serial.read_line() data received from serial port
    :param file_name: choose selected file name.
    :param folder_path: folder path stored in pi
    :return: None
    """
    fdata = open(folder_path + file_name, 'ab')
    fdata.write(write_data)


def mkdir(localtime):
    """
    Create new folder for convenience. If create goes wrong, use default path.
    :param folder_path: generated folder path
    :param localtime: print local time in terminal
    :return: folder_path
    """
    try:
        localtimelist = localtime.split()
        folder_path = "/media/pi/2766-0661/" + localtimelist[0] + "_" + localtimelist[1] + "_" + localtimelist[2]
        default_path = "/media/pi/2766-0661/temp_folder/"
        folder_exist = os.path.exists(folder_path)
        if not folder_exist:
            os.mkdir(folder_path)
            print("Folder created on", localtime)
            folder_path += "/"
            return folder_path
    except:
        return default_path
    else:
        folder_path += "/"
        return folder_path


def main(device_id="ttyUSB0"):
    '''
    Use main function to do the read and save stuff. 
    :param device_id: indicate different device.
    :return: None
    '''
    time_label = 0
    while True:
        ser = serial_select(port_name=device_id, baud_rate=57600, time_out=15)
        line_data = ser.readline()
        localtime = print_local_time()
        folder_path = mkdir(localtime)
        write_file(write_data=line_data, file_name=device_id + ".txt", folder_path=folder_path)
        time_label += 1
        if time_label >= 72:
            print(device_id + "is working at " + localtime)
            time_label = 0


if __name__ == "__main__":

    try:
        thread1_run = MyThread("ttyUSB0").start()
    except:
        print("ttyUSB0 not working")
    else:
        print("ttyUSB0 start recording")


    try:
        thread2_run = MyThread("ttyUSB1").start()
    except:
        print("ttyUSB1 not working")
    else:
        print("ttyUSB1 start recording")


    try:
        thread3_run = MyThread("ttyUSB2").start()
    except:
        print("ttyUSB2 not working")
    else:
        print("ttyUSB2 start recording")
        