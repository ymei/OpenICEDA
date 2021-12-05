MAKE_OPTIONS       ?= -j8
PREFIX             ?= /opt/OpenICEDA
GIT                ?= git
GIT_CLONE_OPTIONS  := --recurse-submodules -j8
GIT_PULL_OPTIONS   := --rebase --recurse-submodules -j8
GIT_SRC_OPEN_PDKS  := https://github.com/RTimothyEdwards/open_pdks
DEST_SKY130PDK     := $(PREFIX)/share/pdk
GIT_SRC_MAGIC      := https://github.com/RTimothyEdwards/magic
GIT_SRC_KLAYOUT    := https://github.com/KLayout/klayout
GIT_SRC_XCIRCUIT   := https://github.com/RTimothyEdwards/xcircuit
GIT_SRC_YOSYS      := https://github.com/YosysHQ/yosys
GIT_SRC_GRAYWOLF   := https://github.com/rubund/graywolf
GIT_SRC_QROUTER    := https://github.com/RTimothyEdwards/qrouter
GIT_SRC_NETGEN     := https://github.com/RTimothyEdwards/netgen
GIT_SRC_QFLOW      := https://github.com/RTimothyEdwards/qflow
GIT_SRC_XSCHEM     := https://github.com/StefanSchippers/xschem
GIT_SRC_XSCHEM_GAW := https://github.com/StefanSchippers/xschem-gaw
GIT_SRC_NGSPICE    := https://github.com/imr/ngspice
GIT_SRC_VERILATOR  := https://github.com/verilator/verilator

.PHONY: update_tools

update_tools: update_qflow update_xcircuit update_xschem update_ngspice update_verilator

update_xschem: update_xschem_gaw
	DIR="xschem" GIT_SRC=$(GIT_SRC_XSCHEM); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# require libgtk-3-dev
update_xschem_gaw:
	DIR="xschem-gaw" GIT_SRC=$(GIT_SRC_XSCHEM_GAW); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# for compiling shared lib: ../configure --with-ngshared --enable-xspice --disable-debug --enable-cider --enable-openmp --prefix=$(PREFIX)
update_ngspice:
	DIR="ngspice" GIT_SRC=$(GIT_SRC_NGSPICE); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	./autogen.sh &&\
	mkdir -p build && cd build/ &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	../configure --with-x --enable-xspice --disable-debug --enable-cider --with-readline=yes --enable-openmp --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# Running will use files from `$VERILATOR_ROOT`, so no install needed
update_verilator:
	DIR="verilator" GIT_SRC=$(GIT_SRC_VERILATOR); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	export VERILATOR_ROOT=`pwd` && 	echo "$$VERILATOR_ROOT" &&\
	$(MAKE) distclean ;\
	autoconf &&\
	./configure &&\
	$(MAKE) $(MAKE_OPTIONS)

# update_yosys update_graywolf update_qrouter update_magic update_netgen
update_qflow:
	DIR="qflow" GIT_SRC=$(GIT_SRC_QFLOW); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# need tcsh.
update_magic:
	DIR="magic" GIT_SRC=$(GIT_SRC_MAGIC); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# need ruby-dev
update_klayout:
	DIR="klayout" GIT_SRC=$(GIT_SRC_KLAYOUT); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	./build.sh -qt5 -option $(MAKE_OPTIONS)

# make seems to modify git tracked files in this repo
update_xcircuit:
	rm -rf xcircuit &&\
	$(GIT) clone $(GIT_CLONE_OPTIONS) $(GIT_SRC_XCIRCUIT) &&\
	cd xcircuit/ && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# one can change to config-gcc.
update_yosys:
	DIR="yosys" GIT_SRC=$(GIT_SRC_YOSYS); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	mkdir -p build && cd build/ &&\
	$(MAKE) uninstall ;\
	$(MAKE) -f ../Makefile clean &&\
	$(MAKE) -f ../Makefile config-clang && echo 'PREFIX := $(PREFIX)' >> Makefile.conf &&\
	$(MAKE) -f ../Makefile $(MAKE_OPTIONS) &&\
	$(MAKE) -f ../Makefile install

# need GSL.
update_graywolf:
	DIR="graywolf" GIT_SRC=$(GIT_SRC_GRAYWOLF); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	mkdir -p build && cd build/ &&\
	$(MAKE) uninstall ;\
	cmake -DCMAKE_INSTALL_PREFIX=$(PREFIX) .. && $(MAKE) clean &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

update_qrouter:
	DIR="qrouter" GIT_SRC=$(GIT_SRC_QROUTER); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

update_netgen:
	DIR="netgen" GIT_SRC=$(GIT_SRC_NETGEN); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# distclean will rm sky130 pdk under sources/, which is a big download.
install_sky130pdk: update_open_pdks
	cd open_pdks/ &&\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) --enable-sky130-pdk --with-sky130-local-path=$(DEST_SKY130PDK) --enable-sram-sky130 &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

update_open_pdks:
	DIR="open_pdks" GIT_SRC=$(GIT_SRC_OPEN_PDKS); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	ls
