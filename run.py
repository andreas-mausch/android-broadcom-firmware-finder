#!/usr/bin/env python

import logging
from plumbum.cmd import unzip, mkdir, mount, umount, tail, find, strings, rm
from plumbum import cli
from plumbum import local

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class FirmwareFinder(cli.Application):

    pattern = cli.SwitchAttr("--pattern", str, default = '*bcmdhd*.bin')
    logLevel = cli.SwitchAttr("--log-level", str, default = 'DEBUG')

    def main(self, *srcfiles):
        logger.setLevel(self.logLevel)

        filenames = list(srcfiles)

        if not filenames:
            logger.error("Please provide at least one zip image")
            return 1

        for filename in filenames:
            self.extractImage(filename)

    def extractImage(self, filename):
        logger.debug('Unzipping system.transfer.list and system.new.dat from image file "%s"..' % filename)
        local.cwd.chdir('/opt/android-broadcom-firmware-finder')
        unzip('-o', filename, 'system.transfer.list', 'system.new.dat')
        logger.debug('done')

        logger.debug('Building system.img via sdat2img..')
        python = local['python']
        sdat2img = python['sdat2img/sdat2img.py', 'system.transfer.list', 'system.new.dat', 'system.img']
        sdat2img()
        logger.debug('done')
        logger.debug('Searching for files which match pattern "%s"' % self.pattern)

        directory = './' + filename + '-image'
        mkdir(directory)
        mount('system.img', directory)

        firmwares = find(directory, '-iname', self.pattern).splitlines()

        for firmware in firmwares:
            print 'Found broadcom firmware: %s' % firmware
            versionCommand = strings[firmware] | tail['-1']
            print versionCommand()

        umount(directory)
        rm('-rf', directory)
        rm('-rf', 'system.transfer.list', 'system.new.dat', 'system.img')

if __name__ == "__main__":
    FirmwareFinder.run()
