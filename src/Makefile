MAKE_OPTIONS      ?= -j8
PREFIX            ?= /opt/OpenICEDA
GIT               ?= git
GIT_CLONE_OPTIONS := --recurse-submodules -j8
GIT_PULL_OPTIONS  := --rebase --recurse-submodules -j8
GIT_SRC_OPEN_PDKS := https://github.com/RTimothyEdwards/open_pdks
DEST_SKY130PDK    := $(PREFIX)/share/pdks
GIT_SRC_MAGIC     := https://github.com/RTimothyEdwards/magic
GIT_SRC_XCIRCUIT  := https://github.com/RTimothyEdwards/xcircuit
GIT_SRC_YOSYS     := https://github.com/YosysHQ/yosys
GIT_SRC_GRAYWOLF  := https://github.com/rubund/graywolf
GIT_SRC_QROUTER   := https://github.com/RTimothyEdwards/qrouter
GIT_SRC_QFLOW     := https://github.com/RTimothyEdwards/qflow

.PHONY: init update_tools

update_tools: update_qflow update_xcircuit

update_qflow: update_yosys update_graywolf update_qrouter update_magic
	cd qflow/ && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# need tcsh.
update_magic:
	cd magic/ && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

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
	cd yosys/ && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	mkdir -p build && cd build/ &&\
	$(MAKE) uninstall ;\
	$(MAKE) -f ../Makefile clean &&\
	$(MAKE) -f ../Makefile config-clang && echo 'PREFIX := $(PREFIX)' >> Makefile.conf &&\
	$(MAKE) -f ../Makefile $(MAKE_OPTIONS) &&\
	$(MAKE) -f ../Makefile install

# need GSL.
update_graywolf:
	cd graywolf/ && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	mkdir -p build && cd build/ &&\
	$(MAKE) uninstall ;\
	cmake -DCMAKE_INSTALL_PREFIX=$(PREFIX) .. && $(MAKE) clean &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

update_qrouter:
	cd qrouter/ && $(GIT) pull $(GIT_PULL_OPTIONS) &&\
	$(MAKE) uninstall ;\
	$(MAKE) distclean ;\
	./configure --prefix=$(PREFIX) &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

# distclean will rm sky130 pdk under sources/, which is a big download.
install_sky130pdk: update_open_pdks
	cd open_pdks/ &&\
	$(MAKE) distclean ;\
	./configure --enable-sky130-pdk --with-sky130-local-path=$(DEST_SKY130PDK) --enable-sram-sky130 &&\
	$(MAKE) $(MAKE_OPTIONS) &&\
	$(MAKE) install

update_open_pdks:
	cd open_pdks/ && $(GIT) pull $(GIT_PULL_OPTIONS)

init:
	$(GIT) clone $(GIT_CLONE_OPTIONS) $(GIT_SRC_MAGIC)
	$(GIT) clone $(GIT_CLONE_OPTIONS) $(GIT_SRC_YOSYS)
	$(GIT) clone $(GIT_CLONE_OPTIONS) $(GIT_SRC_GRAYWOLF)
	$(GIT) clone $(GIT_CLONE_OPTIONS) $(GIT_SRC_QROUTER)
	$(GIT) clone $(GIT_CLONE_OPTIONS) $(GIT_SRC_QFLOW)
	$(GIT) clone $(GIT_CLONE_OPTIONS) $(GIT_SRC_OPEN_PDKS)
