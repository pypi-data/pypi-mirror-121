# Brainiac
biologically inspired neural networks

Derived from Numenta's research and directly influenced by the Nupic code base

To run all ports of the Brainiac algorithm you will need compilers or interpreters for C, Fortran, Java, Go, Oberon, and Python.

# Prerequisites on Debian
To obtain the compilers and interpreters for Debian 11 Bullseye you may do the following:

(as root)
 * apt install git wget build-essential fortran-compiler default-jre default-jdk libgc-dev libsdl1.2-dev
 * cd /usr/local; wget https://golang.org/dl/go1.17.1.linux-amd64.tar.gz; tar xvzf golang.org/dl/go1.17.1.linux-amd64.tar.gz
 * echo "export PATH=\$PATH:/usr/local/go/bin" >> /etc/profile.d/go.sh
 * cd /root/
 * wget http://miasap.se/obnc/downloads/obnc_0.16.1.tar.gz; tar xvzf obnc_0.16.1.tar.gz
 * wget http://miasap.se/obnc/downloads/obnc-libext_0.7.0.tar.gz; tar xvzf obnc-libext_0.7.0.tar.gz
 * cd obnc-0.16.1; ./build; ./install
 * cd ../obnc-libext-0.7.0; ./build; ./install
 * log out and log back in to obtain the new PATH

# Prerequisites on OSX
To obtain the compilers and interpreters for OSX you may do the following:

(as a user with administrative access)
 * /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
 * brew update
 * brew install SDL2
 * brew install gcc
 * brew install go
 * brew install wget
 * brew install bdw-gc
 * brew install oracle-jdk
 * wget http://miasap.se/obnc/downloads/obnc_0.16.1.tar.gz; tar xvzf obnc_0.16.1.tar.gz
 * wget http://miasap.se/obnc/downloads/obnc-libext_0.7.0.tar.gz; tar xvzf obnc-libext_0.7.0.tar.gz
 * cd obnc-0.16.1; ./build; sudo ./install
 * cd ../obnc-libext-0.7.0; ./build; sudo ./install


# Compiling and running Brainiac

Compiling:
 * git clone https://github.com/charlesap/Brainiac
 * cd Brainiac
 * make clean; make all

Running:
 * ./cbrainiac foo
 * ./fbrainiac foo
 * ./obrainiac foo
 * ./gobrainiac foo
 * python3 brainiac.py foo
 * java Brainiac foo

