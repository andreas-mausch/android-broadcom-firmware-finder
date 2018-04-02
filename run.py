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

    broadcomPattern = cli.SwitchAttr("--broadcom-pattern", str, default = '*bcmdhd*.bin*')
    samsungPattern = cli.SwitchAttr("--samsung-pattern", str, default = 'AP_*.tar.md5')
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
        try:
            z = zipfile.ZipFile(filename)
            list = z.namelist()
            if 'system.transfer.list' in list and 'system.new.dat' in z.namelist():
                logger.debug('Found LineageOS image')
                self.handleLineageOsImage(filename)
            elif self.findFileByPattern(list, self.samsungPattern) is not None:
                logger.debug('Found Samsung Stock image')
                self.handleSamsungStockImage(filename)
        except zipfile.BadZipfile:
            if filename == 'system.img':
                logger.debug('Found Android Sparse image')
                self.handleSystemImage(filename)
            elif filename == 'system.ext4.img':
                logger.debug('Found ext4 image')
                self.handleSystemExt4Image(filename)
            else:
                print 'Unknown input file "%s", exiting.' % filename

    def handleLineageOsImage(self, filename):
        logger.debug('Unzipping system.transfer.list and system.new.dat from image file "%s"..' % filename)
        unzip('-o', filename, 'system.transfer.list', 'system.new.dat')
        logger.debug('done')

        logger.debug('Building system.img via sdat2img..')
        python = local['python']
        sdat2img = python['sdat2img/sdat2img.py', 'system.transfer.list', 'system.new.dat', 'system.img']
        sdat2img()
        logger.debug('done')

        self.handleSystemExt4Image('system.img')

        rm('-rf', 'system.transfer.list', 'system.new.dat', 'system.img')

    def handleSamsungStockImage(self, filename):
        logger.debug('Unzipping "%s" from image file "%s"..' % (self.samsungPattern, filename))
        unzip('-o', filename, self.samsungPattern)
        apFilename = self.findFileByPattern(os.listdir('.'), self.samsungPattern)
        logger.debug('done: %s', apFilename)

        logger.debug('Extracting system.img from tarball')
        tar('xf', apFilename, 'system.img')
        logger.debug('done')

        self.handleSystemImage('system.img')
        rm('-rf', 'system.img')

    def handleSystemImage(self, filename):
        logger.debug('simg2img: convert %s to system.ext4.img' % filename)
        simg2img = local['./simg2img/simg2img']
        simg2img(filename, 'system.ext4.img')
        logger.debug('done')

        self.handleSystemExt4Image('system.ext4.img')
        rm('-rf', 'system.ext4.img')

    def handleSystemExt4Image(self, systemImageFilename):
        logger.debug('Searching for files which match pattern "%s"' % self.broadcomPattern)
        directory = './mounted-image'
        mkdir(directory)
        mount(systemImageFilename, directory)

        firmwares = find(directory, '-iname', self.broadcomPattern).splitlines()

        for firmware in firmwares:
            print 'Found firmware: %s (Size: %d)' % (firmware, os.path.getsize(firmware))
            versionCommand = strings[firmware] | tail['-1']
            print versionCommand()

        if not firmwares:
            print 'No firmwares found.'

        umount(directory)
        rm('-rf', directory)

    def findFileByPattern(self, filelist, pattern):
        for file in filelist:
            if fnmatch.fnmatch(file, pattern):
                return file
        return None

if __name__ == "__main__":
    FirmwareFinder.run()
