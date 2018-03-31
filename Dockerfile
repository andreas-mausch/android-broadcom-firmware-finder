FROM bitnami/minideb

RUN apt-get -qq update && \
    apt-get -qq install -y zip wget git python python-pip

RUN pip install plumbum
RUN mkdir -p /opt/android-broadcom-firmware-finder/sdat2img
RUN git clone https://github.com/xpirt/sdat2img /opt/android-broadcom-firmware-finder/sdat2img

ADD run.py /opt/android-broadcom-firmware-finder/

ENTRYPOINT ["/opt/android-broadcom-firmware-finder/run.py"]
