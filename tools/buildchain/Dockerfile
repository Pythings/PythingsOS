############################################################
# Dockerfile to build ESPOpen toolchain
# Based on Ubuntu 14.04
############################################################

FROM ubuntu:14.04

# Don't ask user options when installing
env DEBIAN_FRONTEND noninteractive
RUN echo APT::Install-Recommends "0"; >> /etc/apt/apt.conf
RUN echo APT::Install-Suggests "0"; >> /etc/apt/apt.conf

#-------------------
# Install toolchain
#-------------------

# multiverse is required by unrar
RUN apt-get -y update && apt-get install -y \
    git \ 
    software-properties-common \
    python-software-properties \
    && add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu precise multiverse" 
    
RUN apt-get update && apt-get install -y \
    unrar \
    make \
    autoconf \
    automake \
    libtool \
    gcc \
    g++ \ 
    gperf \
    flex \
    bison \
    texinfo \
    gawk \
    ncurses-dev \
    libexpat-dev \
    python \
    python-serial \
    sed \
    python-dev \
    unzip \
    bash \
    wget \
    nano \
    help2man

## Clean apt cache
RUN apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*

# create user xtensa - toolchain cannot be built as root...
RUN useradd -ms /bin/bash xtensa
USER xtensa
WORKDIR /home/xtensa

ENV PATH /home/xtensa/esp-open-sdk/xtensa-lx106-elf/bin:$PATH

# GIT checkout and make toolchain
RUN git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
RUN cd esp-open-sdk && git checkout e8d757b && git submodule update
WORKDIR /home/xtensa/esp-open-sdk
RUN make

# Checkout Micropython & checkout commit
WORKDIR /home/xtensa
RUN git clone --recursive https://github.com/micropython/micropython.git
RUN cd /home/xtensa/micropython && git checkout 3053748 && git submodule update

# Copy strucutre for allowing building frozen version
RUN cp -a /home/xtensa/micropython /home/xtensa/micropython-frozen

# Clone PythingsOS repo & checkout version
#RUN cd /home/xtensa/ && git clone https://github.com/Pythings/PythingsOS.git
COPY PythingsOS /home/xtensa/PythingsOS
USER root
RUN chown -R xtensa:xtensa /home/xtensa/PythingsOS
USER xtensa

#-------------------
# Set versions
#-------------------

ENV VER="4af8108"
ENV REL="v0.2"

# 4af8108 - v0.2
# 42d31ea - v0.2-rc6
# -- back comp issues in build (changed installers path and boot.py in main-frozen.c)--
# fd149dd - v0.2-rc5
# e703b59 - v0.2-rc4
# -- back comp issues--
# 1f3dc40 - v0.2-rc3
# fdf2e35 - v0.2-rc2


#-------------------
# Build Normal
#-------------------

#RUN cd /home/xtensa/PythingsOS && git pull && git checkout $VER
RUN cd /home/xtensa/PythingsOS &&  git checkout $VER

# Load edited boot.py to autostart the framework
COPY main.c /home/xtensa/micropython/esp8266/main.c

# Build mpy-cross
RUN cd /home/xtensa/micropython && make -C mpy-cross

# Prepare dir for builds
RUN mkdir /home/xtensa/builds 

# Build for esp8266 (normal)
RUN cp -L /home/xtensa/PythingsOS/installers/esp8266/installer.py /home/xtensa/micropython/esp8266/modules/
RUN cd /home/xtensa/micropython/esp8266 && make clean
RUN cd /home/xtensa/micropython/esp8266 && make axtls
RUN cd /home/xtensa/micropython/esp8266 && make all
RUN mv /home/xtensa/micropython/esp8266/build/firmware-combined.bin /home/xtensa/builds/PythingsOS_${REL}_${VER}__uPy_v1.8.6-94-gf8b71aa.esp8266.bin

# Build for esp8266_esp-12
RUN cp -L /home/xtensa/PythingsOS/installers/esp8266_esp-12/installer.py /home/xtensa/micropython/esp8266/modules/
RUN cd /home/xtensa/micropython/esp8266 && make clean
RUN cd /home/xtensa/micropython/esp8266 && make axtls
RUN cd /home/xtensa/micropython/esp8266 && make all
RUN mv /home/xtensa/micropython/esp8266/build/firmware-combined.bin /home/xtensa/builds/PythingsOS_${REL}_${VER}__uPy_v1.8.6-94-gf8b71aa.esp8266_esp-12.bin



#-------------------
# Build Frozen
#-------------------

# Copy main for loading frozen module
#RUN rm /home/xtensa/micropython/esp8266/main.c
COPY main-frozen.c /home/xtensa/micropython-frozen/esp8266/main.c

# Build mpy-cross
RUN cd /home/xtensa/micropython-frozen && make -C mpy-cross

# Build for esp8266 (frozen)
RUN cp -L /home/xtensa/PythingsOS/esp8266/* /home/xtensa/micropython-frozen/esp8266/modules/
RUN cp -a /home/xtensa/PythingsOS/common/crypto* /home/xtensa/micropython-frozen/esp8266/modules/
RUN cd /home/xtensa/micropython-frozen/esp8266 && make clean
RUN cd /home/xtensa/micropython-frozen/esp8266 && make axtls
RUN cd /home/xtensa/micropython-frozen/esp8266 && make all
RUN mv /home/xtensa/micropython-frozen/esp8266/build/firmware-combined.bin /home/xtensa/builds/PythingsOS_${REL}_${VER}__uPy_v1.8.6-94-gf8b71aa.esp8266.frozen.bin

# Build for esp8266-esp-12 (fozen)
RUN cp -L /home/xtensa/PythingsOS/esp8266_esp-12/* /home/xtensa/micropython-frozen/esp8266/modules/
RUN cp -a /home/xtensa/PythingsOS/common/crypto* /home/xtensa/micropython-frozen/esp8266/modules/
RUN cd /home/xtensa/micropython-frozen/esp8266 && make clean
RUN cd /home/xtensa/micropython-frozen/esp8266 && make axtls
RUN cd /home/xtensa/micropython-frozen/esp8266 && make all
RUN mv /home/xtensa/micropython-frozen/esp8266/build/firmware-combined.bin /home/xtensa/builds/PythingsOS_${REL}_${VER}__uPy_v1.8.6-94-gf8b71aa.esp8266_esp-12.frozen.bin

COPY build_bytecode.sh /home/xtensa/build_bytecode.sh
RUN cd /home/xtensa/PythingsOS/esp8266_esp-12 && bash /home/xtensa/build_bytecode.sh
RUN mkdir /home/xtensa/builds/bytecode && cp -a /home/xtensa/PythingsOS/esp8266_esp-12/*.mpy /home/xtensa/builds/bytecode/

#-------------------
#   Entrypoint,
#  volumes  & co
#-------------------

USER root
RUN mkdir /firmware
COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]















