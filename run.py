#!/usr/bin/env python

# docker build -t andreas-mausch/android-broadcom-firmware-finder .
# docker run -it --rm --privileged -v /home/neonew/Downloads/lineage-14.1-20180330-nightly-jfltexx-signed.zip:/opt/android-broadcom-firmware-finder/image.zip:ro andreas-mausch/android-broadcom-firmware-finder image.zip
# https://wiki.lineageos.org/extracting_blobs_from_zips.html

from plumbum.cmd import unzip, mkdir, mount, umount, tail, find, strings, rm
from plumbum import cli
from plumbum import local

class FirmwareFinder(cli.Application):

    pattern = cli.SwitchAttr("--pattern", str, default = '*bcmdhd*.bin')

    def main(self, *srcfiles):
        filenames = list(srcfiles)

        if not filenames:
            print "Please provide at least one zip image"
            return 1

        for filename in filenames:
            self.extractImage(filename)

    def extractImage(self, filename):
        print 'Unzipping system.transfer.list and system.new.dat from image file "%s"..' % filename
        local.cwd.chdir('/opt/android-broadcom-firmware-finder')
        unzip('-o', filename, 'system.transfer.list', 'system.new.dat')
        print 'done'

        print 'Building system.img via sdat2img..'
        python = local['python']
        sdat2img = python['sdat2img/sdat2img.py', 'system.transfer.list', 'system.new.dat', 'system.img']
        sdat2img()
        print 'done'
        print 'Searching for files which match pattern "%s"' % self.pattern
        print

        directory = './' + filename + '-image'
        mkdir(directory)
        mount('system.img', directory)

        firmwares = find(directory, '-iname', self.pattern).splitlines()

        for firmware in firmwares:
            print "Found broadcom firmware: %s" % firmware
            versionCommand = strings[firmware] | tail['-1']
            print versionCommand()

        umount(directory)
        rm('-rf', directory)
        rm('-rf', 'system.transfer.list', 'system.new.dat', 'system.img')

if __name__ == "__main__":
    FirmwareFinder.run()
