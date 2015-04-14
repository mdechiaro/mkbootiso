mkbootiso
=========

Program creates a boot ISO on per host basis with static IP assigments.  This is useful for when PXE boot or DHCP is not an option, and you want to build a server in place.  This program requires an extracted iso file that can be written by the program.

Prep:
Dependencies:
  - Python 2.6+
  - python-argparse
  - python-yaml

Package Dependencies:
  - genisoimage
 
- Download ISO file from vendor.

- Mount it using the loop option:

        mount -o loop CentOS-6.5-x86_64-minimal.iso /mnt/tmp/centos6/

- Copy necessary contents to a folder.  In this example, only isolinux/ is needed.  Copying only mandatory files will keep the size down to save bandwidth and disk space.  

        cp -a /mnt/tmp/centos6/isolinux/ /mnt/isos/

Usage:

    ./mkbootiso.py -s /mnt/isos/centos6/ -n hostname.iso -f ~/hostname.yaml
