#!/usr/bin/python
import subprocess
import sys
import textwrap
import yaml

class MkBootISO(object):
    """ 
    Makes a static IP per host boot iso for easier network host creation when 
    PXE booting or DHCP networks are not an option.
    """

    def __init__(self):
        self.mkisofs = '/usr/bin/genisoimage'
        self.isodir = '/mnt/newiso'
        self.outdir = '/tmp/'


    def updateiso(self, **kwargs):
        """
        Update iso image with host specific parameters.
        All kickstart options will be added from a yaml file.
        """
        
        label = """
                default vesamenu.c32
                display boot.msg
                timeout 5
                label iso created by %s
                menu default
                kernel vmlinuz
                append initrd=initrd.img %s %s

                """ % ( sys.argv[0],
                       ' '.join("%s=%s" % (key,val) for (key,val) in kwargs['kickstart'].iteritems()),
                       ' '.join("%s=%s" % (key,val) for (key,val) in kwargs['options'].iteritems())
                )

        with open(self.isodir + '/isolinux/isolinux.cfg', 'w') as file:
            file.write(textwrap.dedent(label).strip())


    def createiso(self, isofile):
        """create iso image."""
        cmd = [self.mkisofs, 
               '-J', 
               '-T',
               '-o', self.outdir + isofile,
               '-b', 'isolinux/isolinux.bin', 
               '-c', 'isolinux/boot.cat', 
               '-no-emul-boot', 
               '-boot-load-size', '4', 
               '-boot-info-table', '-R', 
               '-m', 'TRANS.TBL', 
               '-graft-points', self.isodir,
        ]

        subprocess.call(cmd)

    def main(self):
        self.updateiso(**yaml.load(open(sys.argv[1])))
        self.createiso(sys.argv[2])

if __name__ == '__main__':
    mkiso = MkBootISO()
    sys.exit(mkiso.main())

