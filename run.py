#!/usr/bin/env python

import fnmatch
import logging
import os.path
import time
import zipfile
from datetime import datetime
from plumbum.cmd import unzip, mkdir, mount, umount, tail, find, strings, rm, tar, ls
from plumbum import cli
from plumbum import local

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class FirmwareFinder(cli.Application):

    pattern = cli.SwitchAttr("--pattern", str, default = '*bcmdhd*.bin*')
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
        local.cwd.chdir('/opt/android-broadcom-firmware-finder')
        z = zipfile.ZipFile(filename)
        if 'system.transfer.list' in z.namelist() and 'system.new.dat' in z.namelist():
            self.extractLineageOsImage(filename)
        else:
            self.extractSamsungStockImage(filename)

    def extractLineageOsImage(self, filename):
        logger.debug('Found LineageOS image')
        logger.debug('Unzipping system.transfer.list and system.new.dat from image file "%s"..' % filename)
        unzip('-o', filename, 'system.transfer.list', 'system.new.dat')
        logger.debug('done')

        logger.debug('Building system.img via sdat2img..')
        python = local['python']
        sdat2img = python['sdat2img/sdat2img.py', 'system.transfer.list', 'system.new.dat', 'system.img']
        sdat2img()
        logger.debug('done')
        logger.debug('Searching for files which match pattern "%s"' % self.pattern)

        self.mountAndAnalyseFirmwares('system.img')

        rm('-rf', 'system.transfer.list', 'system.new.dat', 'system.img')

    def extractSamsungStockImage(self, filename):
        logger.debug('Found Samsung Stock image')
        logger.debug('Unzipping AP_*.tar.md5 from image file "%s"..' % filename)
        unzip('-o', filename, 'AP_*.tar.md5')
        apFilename = self.findFileByPattern('AP_*.tar.md5')
        logger.debug('done: %s', apFilename)

        logger.debug('Extracting system.img from tarball')
        tar('xf', apFilename, 'system.img')
        logger.debug('done')

        logger.debug('simg2img: convert system.img to system.ext4.img')
        simg2img = local['./simg2img/simg2img']
        simg2img('system.img', 'system.ext4.img')
        logger.debug('done')

        self.mountAndAnalyseFirmwares('system.ext4.img')

        rm('-rf', 'system.ext4.img', 'system.img')

    def mountAndAnalyseFirmwares(self, systemImageFilename):
        directory = './mounted-image'
        mkdir(directory)
        mount(systemImageFilename, directory)

        firmwares = find(directory, '-iname', self.pattern).splitlines()

        for firmware in firmwares:
            print 'Found firmware: %s (Size: %d)' % (firmware, os.path.getsize(firmware))
            versionCommand = strings[firmware] | tail['-1']
            print versionCommand()

        umount(directory)
        rm('-rf', directory)

    def findFileByPattern(self, pattern):
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, pattern):
                return file

if __name__ == "__main__":
    FirmwareFinder.run()
