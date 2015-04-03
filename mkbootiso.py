#!/usr/bin/python
import argparse
import subprocess
import os
import sys
import textwrap
import yaml

class MkBootISO(object):
    """
    Makes a static IP per host boot iso for easier network host creation when
    PXE booting or DHCP networks are not an option.
    """

    def __init__(self):
        self.opts = None
        self.help = None
        self.mkisofs = '/usr/bin/genisoimage'


    def options(self):
        """argparse command line options."""

        parser = argparse.ArgumentParser(
            description='Creates a per host custom boot iso.'
        )

        parser.add_argument(
            '--file', '-f', metavar='',
            help='yaml file with kickstart info'
        )

        parser.add_argument(
            '--name', '-n', metavar='',
            help='name of iso file.'
        )

        parser.add_argument(
            '--output', '-o', metavar='', default='/tmp/',
            help='output directory: /tmp/ default: %(default)s'
        )

        parser.add_argument(
            '--source', '-s', metavar='',
            help='source directory: /path/to/iso/'
        )


        self.opts = parser.parse_args()
        self.help = parser.print_help


    def updateiso(self, source, **kwargs):
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

        with open(source + '/isolinux/isolinux.cfg', 'w') as iso_cfg:
            iso_cfg.write(textwrap.dedent(label).strip())


    def createiso(self, source, output, filename):
        """create iso image."""
        cmd = [self.mkisofs,
               '-J',
               '-T',
               '-o', output + filename,
               '-b', 'isolinux/isolinux.bin',
               '-c', 'isolinux/boot.cat',
               '-no-emul-boot',
               '-boot-load-size', '4',
               '-boot-info-table', '-R',
               '-m', 'TRANS.TBL',
               '-graft-points', source,
        ]

        subprocess.call(cmd)

    def main(self):
        """ main method."""
        self.options()
        self.updateiso(self.opts.source, **yaml.load(open(os.path.expanduser(self.opts.file))))
        self.createiso(self.opts.source, self.opts.output, self.opts.name)

if __name__ == '__main__':
    mkiso = MkBootISO()
    sys.exit(mkiso.main())

