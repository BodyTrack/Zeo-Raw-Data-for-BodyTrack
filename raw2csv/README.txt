raw2csv.py:

Original version from chadjoan in the Zeo developer's forum:
http://blog.myzeo.com/forum/zeo-raw-data-library/recording-real-time-data-into-csv-files-and-wake-when-light/

Uses ZeoRawData-2.0 from Zeo, also modified

Modifications:
Reads data from file instead of serial port.

raw2csv.py [-f] filename
-f:  "follow" filename;  wait for more data and keep reading until
     ctrl-c. (without this flag, exit when end-of-file)

