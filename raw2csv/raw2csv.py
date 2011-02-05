#!/usr/bin/python -d
# -*- coding: utf-8 -*-
# DataRecorder.pyw
#
# Streams the real-time data coming from a Zeo unit into .csv files.
import sys
import time
import csv
import os

# from serial import *

from glob import glob


sys.path.append("/Users/rsargent/projects/bodytrack/zeo/raw-data/raw2csv/ZeoRawData-2.0");

from ZeoRawData import BaseLink, Parser

global done
done = False

def scanPorts():
    portList = []
    
    # Helps find USB>Serial converters on linux
    for p in glob('/dev/ttyUSB*'):
        portList.append(p)
    #Linux and Windows
    for i in range(256):
        try:
            ser = Serial(i)
            if ser.isOpen():
                #Check that the port is actually valid
                #Otherwise invalid /dev/ttyS* ports may be added
                portList.append(ser.portstr)
            ser.close()
        except SerialException:
            pass
    return portList


class HexFileReader:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        # skip 5 lines
        for i in range(5):
            self.file.readline()

    def read(self, num):
        ret = ""
        for i in range(num):
            ret += self.read1()
        return ret

    def read1(self):
        c = self.file.read(1)
        if (c == ' '):
            c = self.file.read(1)
        c += self.file.read(1)
        if (len(c) < 2):
            print "DONE"
            sys.exit(0)
        return chr(int(c,16))

    def flushInput(self):
        pass

class FileReader:
    def __init__(self, filename, follow):
        self.follow = follow
        self.file = open(filename, 'r')

    def read(self, num):
        global done
        ret = self.file.read(num)
        while len(ret) < num:
            if not self.follow:
                print "Done reading"
                done = True
                sys.exit(0)
            time.sleep(1);
            self.file.seek(0,1) # seek to current location to update buffer
            ret += self.file.read(num - len(ret))
        return ret

    def flushInput(self):
        pass


class ZeoToCSV:
    def __init__(self, basename):
        samplesFileName = basename + '.raw_samples.csv'
        sgramFileName = basename + '.spectrogram.csv'
        hgramFileName = basename + '.hypnogram.csv'
        eventsFileName = basename + '.events.csv'
        
        self.hypToHeight = {'Undefined' : 0,
                            'Deep'      : 1,
                            'Light'     : 2,
                            'REM'       : 3,
                            'Awake'     : 4}
        
        # Only create headers when the files are being created for the first time.
        # After that, all new data should be appended to the existing files.
        samplesNeedHeader = False
        sgramNeedHeader = False
        hgramNeedHeader = False
        eventsNeedHeader = False
        
        self.rawSamplesFile = open(samplesFileName, 'wb')
        self.rawSamples = csv.writer(self.rawSamplesFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        self.spectrogramFile = open(sgramFileName, 'wb')
        self.spectrogram = csv.writer(self.spectrogramFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        self.hypnogramFile = open(hgramFileName, 'wb')
        self.hypnogram = csv.writer(self.hypnogramFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        self.eventsOutFile = open(eventsFileName, 'wb')
        self.eventsOut = csv.writer(self.eventsOutFile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        self.rawSamples.writerow(["Time Stamp","Version","SQI","Impedance","Bad Signal (Y/N)","Voltage (uV)"])
        
        self.spectrogram.writerow(["Time Stamp","Version","SQI","Impedance","Bad Signal (Y/N)",
                                   "2-4 Hz","4-8 Hz","8-13 Hz","11-14 Hz","13-18 Hz","18-21 Hz","30-50 Hz"])
        
        self.hypnogram.writerow(["Time Stamp","Version","SQI","Impedance","Bad Signal (Y/N)","State (0-4)","State (named)"])
        
        self.eventsOut.writerow(["Time Stamp","Version","Event"])
    
    def updateSlice(self, slice):
        
        timestamp = slice['ZeoTimestamp']
        ver = slice['Version']
                                        
        if not slice['SQI'] == None:
            sqi = str(slice['SQI'])
        else:
            sqi = '–'
                                        
        if not slice['Impedance'] == None:
            imp = str(int(slice['Impedance']))
        else:
            imp = '–'
        if slice['BadSignal']:
            badSignal = 'Y'
        else:
            badSignal = 'N'
        if not slice['Waveform'] == []:
            self.rawSamples.writerow([timestamp,ver,sqi,imp,badSignal] + slice['Waveform'])
            self.rawSamplesFile.flush()
        if len(slice['FrequencyBins'].values()) == 7:
            f = slice['FrequencyBins']
            bins = [f['2-4'],f['4-8'],f['8-13'],f['11-14'],f['13-18'],f['18-21'],f['30-50']]
            self.spectrogram.writerow([timestamp,ver,sqi,imp,badSignal] + bins)
            self.spectrogramFile.flush()
        if not slice['SleepStage'] == None:
            stage = slice['SleepStage']
            self.hypnogram.writerow([timestamp,ver,sqi,imp,badSignal] +
                                     [self.hypToHeight[stage],str(stage)])
            self.hypnogramFile.flush()
    
    def updateEvent(self, timestamp, version, event):
        self.eventsOut.writerow([timestamp,version,event])
        self.eventsOutFile.flush()

if __name__ == '__main__':

    follow = False
    zeofile = ""
    
    for arg in sys.argv[1:]:
        if arg == "-f":
            follow = True
        else:
            zeofile = arg

    # Find ports.
    # TODO: offer a command line option for selecting ports.

#    ports = scanPorts()
#    if len(ports) > 0 :
#        print "Found the following ports:"
#        for port in ports:
#            print port
#        print ""
#        print "Using port "+ports[0]
#        print ""
#        portStr = ports[0]
#    else:
#        sys.exit("No serial ports found.")
    

    print "Generating CSV files from " + zeofile + ", follow=", follow
    # Initialize
    output = ZeoToCSV(os.path.splitext(zeofile)[0])
    
    reader = FileReader(zeofile, follow)

    link = BaseLink.BaseLink(reader)

    parser = Parser.Parser()
    # Add callbacks
    link.addCallback(parser.update)
    parser.addEventCallback(output.updateEvent)
    parser.addSliceCallback(output.updateSlice)
    # Start Link
    link.start()
    
    # TODO: perhaps use a more forgiving key?  This would require polling the keyboard without blocking.
    if follow:
        print "Following; hit ctrl-C at any time to stop."
    while not done:
        time.sleep(.2)
    print "Exiting"

    sys.exit()
