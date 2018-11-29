import argparse
import os
import re
from datetime import datetime
from dateutil.parser import parse
import julian

RE_SPLIT = re.compile('     ')  # split on 5 spaces


def get_mjd_from_filename(fname):
    """Input is a filaname like: eim08_10_18.log
    Steps:
    1. Convert to python datetime
    2. Convert to time tuple
    3. Convert to Julian Date
    4. Convert to Modified Julian Date (MJD)
    """
    res = re.search(r'(\d+)_(\d+)_(\d+)', fname)
    if res:
        day = int(res.group(1))
        month = int(res.group(2))
        year = int('20' + res.group(3))

        dt = datetime(year, month, day, 0, 0, 0)
        return julian.to_jd(dt, fmt='mjd')


def process_input_file(fname):

    mjd = str(int(get_mjd_from_filename(fname)))
    output_filename = "EIM_%s.%s.log" % (mjd[:2], mjd[2:])
    if os.path.isfile(output_filename):
        os.unlink(output_filename)
    fi = open(output_filename, "a")

    print("METEOROLOGICAL DATA\t\t\t\t\tDATA TYPE", file=fi)
    print("HUMIDITY SENSOR", file=fi)
    print("Galltech (manufacturer)", file=fi)
    print("FK80J (model)", file=fi)
    print("A310340000 (S/N)", file=fi)
    print("SET OF FIVE THERMOELEMENTS", file=fi)
    print("Uteco (Manufac.)", file=fi)
    print("CB 1XK 0.22/6000 PVC JJ2X0.22 (model)", file=fi)
    print("", file=fi)
    print("Hellenic Institute of Metrology", file=fi)
    print("Sensor located in the Time & Frequency Laboratory", file=fi)
    print("\t\t\t\t\t\t\tEND OF HEADER", file=fi)

    def print_output_line(dt, tc1, tc2, tc3, tc4, tc5, hum):
        tc_avg = (tc1 + tc2 + tc3 + tc4 + tc5) / 5.0
        dt_str = dt.strftime(' %d %m %y %H %M %S')
        print("%s\t%.2f\t%.2f\tPRE?" % (dt_str, tc_avg, hum), file=fi)

    with open(fname) as input_file:
        for line in input_file:
            line = line.strip()
            parts = RE_SPLIT.split(line)
            if parts[0]:
                try:
                    dt = parse(parts[0])
                    tc1 = float(parts[2])
                    tc2 = float(parts[3])
                    tc3 = float(parts[4])
                    tc4 = float(parts[5])
                    tc5 = float(parts[6])
                    hum = float(parts[7])
                    print_output_line(dt, tc1, tc2, tc3, tc4, tc5, hum)
                except ValueError:
                    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename")
    args = parser.parse_args()
    process_input_file(args.input_filename)
# parse input file

# print output to STDOUT
