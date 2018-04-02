# Android Broadcom Firmware Finder

This docker image finds broadcom firmware files inside of an Android image.  
It can be used to find firmwares which are vulnerable to [BroadPwn](https://blog.exodusintel.com/2017/07/26/broadpwn/). If the firmware files are dated before 2017-06, they are vulnerable.

The input file is the Android image, e.g. *lineage-14.1-20180325-nightly-zerofltexx-signed.zip*.

## Run the docker image

```
$ docker run -it --rm --privileged -v /home/neonew/Downloads/lineage-14.1-20180325-nightly-zerofltexx-signed.zip:/opt/android-broadcom-firmware-finder/image.zip:ro andreasmausch/android-broadcom-firmware-finder image.zip

Unzipping system.transfer.list and system.new.dat from image file "image.zip"..
done
Building system.img via sdat2img..
done
Searching for files which match pattern "*bcmdhd*.bin"

[...]
```

Android image on your local hard drive in this case is here: _/home/neonew/Downloads/lineage-14.1-20180325-nightly-zerofltexx-signed.zip_
(Adjust it to point to your image)

You can adjust the pattern by passing a parameter *--broadcom-pattern=xyz* right before *image.zip*.
The default pattern is _*bcmdhd*.bin_.

You can hide verbose logging via parameter *--log-level=ERROR*.

For example output, see the output directory.

## Building the docker image

If you want to build the image yourself instead of using the one provided on Docker Hub ([https://hub.docker.com/r/andreasmausch/android-broadcom-firmware-finder/](https://hub.docker.com/r/andreasmausch/android-broadcom-firmware-finder/)), you can clone this repository and call inside the directory:

```
docker build -t andreasmausch/android-broadcom-firmware-finder .
```

## More details on how to extract files from a LineageOS image

[https://wiki.lineageos.org/extracting_blobs_from_zips.html](https://wiki.lineageos.org/extracting_blobs_from_zips.html)
