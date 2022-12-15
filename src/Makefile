MAKE_OPTIONS       ?= -j8
PREFIX             ?= /opt/OpenICEDA
GIT                ?= git
GIT_CLONE_OPTIONS  := --recurse-submodules -j8
GIT_PULL_OPTIONS   := --rebase --recurse-submodules --prune -j8
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
GIT_SRC_TRILINOS   := https://github.com/trilinos/Trilinos
GIT_SRC_XYCE       := https://github.com/Xyce/Xyce
GIT_SRC_AMARANTH   := https://github.com/amaranth-lang/amaranth
GIT_SRC_OPENROAD   := https://github.com/The-OpenROAD-Project/OpenROAD
GIT_SRC_OPENLANE   := https://github.com/The-OpenROAD-Project/OpenLane
OPENLANE_ROOT      ?= $(PREFIX)/src/OpenLane
PYTHON             ?= python3
PYVENV             ?= $(PREFIX)/OICvenv

.PHONY: update_tools

update_tools: update_qflow update_netgen update_magic update_xschem update_ngspice update_verilator

update_xschem: update_xschem_gaw
	DIR="xschem" GIT_SRC=$(GIT_SRC_XSCHEM); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# need libgtk-3-dev
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
	../configure --with-x --enable-xspice --disable-debug --enable-cider --enable-pss --with-readline=yes --enable-openmp --prefix=$(PREFIX) &&\
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
	CPPFLAGS="-I/opt/local/include" ./configure &&\
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
	./build.sh $(MAKE_OPTIONS)

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
	$(MAKE) uninstall ;\
	$(MAKE) -f Makefile clean &&\
	$(MAKE) -f Makefile config-clang && echo 'PREFIX := $(PREFIX)' >> Makefile.conf &&\
	$(MAKE) -f Makefile $(MAKE_OPTIONS) &&\
	$(MAKE) -f Makefile install

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
install_pdks: update_open_pdks
	cd open_pdks/ &&\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) --enable-sky130-pdk --with-sky130-local-path=$(DEST_SKY130PDK) --enable-sram-sky130 --enable-gf180mcu-pdk &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

update_open_pdks:
	DIR="open_pdks" GIT_SRC=$(GIT_SRC_OPEN_PDKS); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	ls

# required by Xyce
# apt install adms libsuitesparse-dev libopenmpi-dev
update_trilinos:
	DIR="xyce" GIT_SRC=$(GIT_SRC_XYCE); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC" "$$DIR"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) && cd .. &&\
	DIR="trilinos" GIT_SRC=$(GIT_SRC_TRILINOS);\
	rm -rf "$$DIR" && $(GIT) clone $(GIT_CLONE_OPTIONS) --depth 1 --branch trilinos-release-12-12-1 $(GIT_SRC_TRILINOS) "$$DIR" &&\
	cd "$$DIR" && mkdir -p build && cd build &&\
	cmake -C ../../xyce/cmake/trilinos/trilinos-config-MPI.cmake -DCMAKE_INSTALL_PREFIX=$(PREFIX) -DAMD_INCLUDE_DIRS=/usr/include/suitesparse -DBUILD_SHARED_LIBS=ON .. &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

update_xyce:
	DIR="xyce" GIT_SRC=$(GIT_SRC_XYCE); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC" "$$DIR"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	mkdir -p build && cd build &&\
	cmake -DCMAKE_INSTALL_PREFIX=$(PREFIX) -D Trilinos_ROOT=$(PREFIX) -D Xyce_PLUGIN_SUPPORT=ON .. &&\
	cmake --build . $(MAKE_OPTIONS) -t install

update_amaranth: update_pyvenv
	DIR="amaranth" GIT_SRC=$(GIT_SRC_AMARANTH); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC" "$$DIR"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	pip install --editable .[builtin-yosys]

create_pyvenv:
	$(PYTHON) -m venv --symlinks --system-site-packages --clear $(PYVENV)
update_pyvenv:
	$(PYTHON) -m venv --symlinks --system-site-packages --upgrade --upgrade-deps $(PYVENV)

# need swig, libboost-all-dev, libspdlog-dev, libeigen3-dev, liblemon-dev tcllib
update_openroad:
	DIR="OpenROAD" GIT_SRC=$(GIT_SRC_OPENROAD); if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC" "$$DIR"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	mkdir -p build && cd build &&\
	cmake -DCMAKE_INSTALL_PREFIX=$(PREFIX) .. &&\
	cmake --build . $(MAKE_OPTIONS) -t install

# need autopoint, ninja-build
update_openlane:
	DIR="OpenLane" GIT_SRC=$(GIT_SRC_OPENLANE); rm -rf "$$DIR";\
	if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC" "$$DIR"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	export OPENLANE_ROOT=$(OPENLANE_ROOT) && echo "OPENLANE_ROOT=$$OPENLANE_ROOT" &&\
	$(PYTHON) ./env.py tool-list &&\
	$(PYTHON) ./env.py local-install

update_openlane_docker:
	DIR="OpenLane" GIT_SRC=$(GIT_SRC_OPENLANE); rm -rf "$$DIR";\
	if [ ! -e "$$DIR" ];\
	then $(GIT) clone $(GIT_CLONE_OPTIONS) "$$GIT_SRC" "$$DIR"; fi &&\
	cd "$$DIR" && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	export OPENLANE_ROOT=$(OPENLANE_ROOT) && echo "OPENLANE_ROOT=$$OPENLANE_ROOT" &&\
	make
