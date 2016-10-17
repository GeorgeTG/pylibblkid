import sys

from ctypes import *


class BlkId():

    def __init__(self, device):
        device = device.encode('ascii')
        self._blkid = cdll.LoadLibrary("libblkid.so")

        # specify types
        self._blkid.blkid_new_probe_from_filename.argtypes=[c_char_p]
        self._blkid.blkid_probe_lookup_value.argtypes=\
                [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_ulong)]
        # create probe
        self._probe = self._blkid.blkid_new_probe_from_filename(c_char_p(device))

        # probe
        self._blkid.blkid_do_probe(self._probe)

    def probe_lookup_value(self, arg):
        result = c_char_p() # char* result
        self._blkid.blkid_probe_lookup_value(
                self._probe,
                c_char_p(arg.encode('ascii')),
                byref(result),
                None)

        return string_at(result).decode('ascii')


a = BlkId(sys.argv[1])
print(a.probe_lookup_value('UUID'))
