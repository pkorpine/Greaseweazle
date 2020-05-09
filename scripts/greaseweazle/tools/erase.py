# greaseweazle/tools/erase.py
#
# Greaseweazle control script: Erase a Disk.
#
# Written & released by Keir Fraser <keir.xen@gmail.com>
#
# This is free and unencumbered software released into the public domain.
# See the file COPYING for more details, or visit <http://unlicense.org>.

import sys, argparse

from greaseweazle.tools import util
from greaseweazle import usb as USB

import binascii
from greaseweazle.bitcell import Bitcell
from bitarray import bitarray

def erase(usb, args):

    sync = bitarray(endian="big")
    sync.frombytes(b"\x44\x89")

    gap = bitarray(endian="big")
    gap.frombytes(b"\xaa\xaa")

    bits = bitarray(endian="big")
    bits += gap * 100
    bits += sync

    bits += [0] * 16
    bits += gap * 2
    bits += sync
    
    flux_list = []
    flux_ticks = 0
    for bit in bits:
        flux_ticks += 2
        if bit:
            flux_list.append(flux_ticks)
            flux_ticks = 0
    if flux_ticks:
        flux_list.append(flux_ticks)
    
    usb.seek(80, 1)
    usb.erase_track(72 * 220000)
    
    flux_list += [25] + ([0.5]*6) + [4]
    flux_list += [4] * (16 * 1000)

    flux = []
    for x in flux_list:
        flux.append(int(x*72))
    usb.write_track(flux, False)

    for i in range(20):
        print(i)
        flux = usb.read_track(1)
        bc = Bitcell()
        bc.from_flux(flux)
        bits = bc.revolution_list[0][0]
        bits = bits[:10000]
        for j in bits.itersearch(sync):
            print(str(binascii.hexlify(bits[j:j+100].tobytes())), j)

    print()


def main(argv):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--drive", type=util.drive_letter, default='A',
                        help="drive to write (A,B,0,1,2)")
    parser.add_argument("--scyl", type=int, default=0,
                        help="first cylinder to write")
    parser.add_argument("--ecyl", type=int, default=81,
                        help="last cylinder to write")
    parser.add_argument("--single-sided", action="store_true",
                        help="single-sided write")
    parser.add_argument("device", nargs="?", default="auto",
                        help="serial device")
    parser.prog += ' ' + argv[1]
    args = parser.parse_args(argv[2:])
    args.nr_sides = 1 if args.single_sided else 2

    try:
        usb = util.usb_open(args.device)
        util.with_drive_selected(erase, usb, args)
    except USB.CmdError as error:
        print("Command Failed: %s" % error)


if __name__ == "__main__":
    main(sys.argv)

# Local variables:
# python-indent: 4
# End:
