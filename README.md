# Android Broadcom Firmware Finder

This docker image finds broadcom firmware files inside of an Android image.

The input file is the Android image, e.g. **lineage-14.1-20180325-nightly-zerofltexx-signed.zip**

## Run the docker image

```
$ docker run -it --rm --privileged -v /home/neonew/Downloads/lineage-14.1-20180325-nightly-zerofltexx-signed.zip:/opt/android-broadcom-firmware-finder/image.zip:ro andreas-mausch/android-broadcom-firmware-finder image.zip

Unzipping system.transfer.list and system.new.dat from image file "image.zip"..
done
Building system.img via sdat2img..
done
Searching for files which match pattern "*bcmdhd*.bin"

Found broadcom firmware: ./image.zip-image/etc/wifi/bcmdhd_apsta.bin
4358a3-roml/pcie-ag-pktctx-txbf-lpc-clm_ss_mimo-txpwr-apcs-proptxstatus-ampduhostreorder-pspretend-sarctrl-amsdutx5g-btcdyn-mfp-xorcsum-fpl2g Version: 7.112.48 (A3 SoftAP feature) CRC: 9b486866 Date: Thu 2016-12-22 17:46:49 KST Ucode Ver: 963.323 FWID: 01-1b267cca

Found broadcom firmware: ./image.zip-image/etc/wifi/bcmdhd_ibss.bin
4358a3-roml/pcie-ag-p2p-pktctx-aibss-relmcast-proptxstatus-ampduhostreorder-sr-aoe-pktfilter-keepalive-clm_ss_mimo-sarctrl-sstput-xorcsum-fpl2g Version: 7.112.17.23 CRC: f956ac3b Date: Tue 2016-08-09 15:16:27 KST Ucode Ver: 986.11001 FWID: 01-14205a46

Found broadcom firmware: ./image.zip-image/etc/wifi/bcmdhd_mfg.bin
4358a3-roml/pcie-ag-pktctx-mfgtest-seqcmds-txbf-sr-srfast-sarctrl-xorcsum-clm_ss_mimo-proptxstatus-phydbg-fpl2g Version: 7.112.48 (A3 WLTEST) CRC: 6dffc350 Date: Thu 2016-12-22 17:51:25 KST Ucode Ver: 963.323 FWID: 01-fa047ce2

Found broadcom firmware: ./image.zip-image/etc/wifi/bcmdhd_sta.bin
4358a3-roml/pcie-ag-p2p-pno-aoe-pktfilter-keepalive-sr-mchan-pktctx-hostpp-lpc-pwropt-txbf-wl11u-mfp-wnm-betdls-amsdutx5g-okc-ccx-ve-clm_ss_mimo-txpwr-rcc-fmc-wepso-noccxaka-sarctrl-btcdyn-xorcsum-dpm-shif-idsup-ndoe-fpl2g-hthrot-apf Version: 7.112.48 (A3 Station/P2P feature) CRC: d32609fb Date: Thu 2016-12-22 17:42:28 KST Ucode Ver: 963.323 FWID: 01-9bf0b5ec
```

Android image on your local hard drive in this case is here: _/home/neonew/Downloads/lineage-14.1-20180325-nightly-zerofltexx-signed.zip_
(Adjust it to point to your image)

You can adjust the pattern by passing a parameter *--pattern=xyz* right before *image.zip*.
The default pattern is _*bcmdhd*.bin_.

You can hide verbose logging via parameter *--log-level=ERROR*.

## Building the docker image

Clone this repository and call inside the directory:

```
docker build -t andreas-mausch/android-broadcom-firmware-finder .
```

## More details on how to extract files from a LineageOS image

[https://wiki.lineageos.org/extracting_blobs_from_zips.html](https://wiki.lineageos.org/extracting_blobs_from_zips.html)
