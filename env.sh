PREFIX=/opt/OpenICEDA
PYVENV=${PREFIX}/OICvenv
test -r ${PYVENV}/bin/activate && . ${PYVENV}/bin/activate
# for xschem_sky130
export PDK_ROOT=${PREFIX}/share/pdk
export VERILATOR_ROOT=${PREFIX}/src/verilator
export OPENLANE_ROOT=${PREFIX}/src/OpenLane
export OPENRAM_HOME=${PREFIX}/src/OpenRAM/compiler
export OPENRAM_TECH=${PREFIX}/src/OpenRAM/technology
export PYTHONPATH=${PYTHONPATH}:${OPENRAM_HOME}
export PATH=${PREFIX}/bin:${PREFIX}/src/klayout/bin-release:${PATH}
export LD_LIBRARY_PATH=${PREFIX}/lib:${PREFIX}/src/klayout/bin-release:${LD_LIBRARY_PATH}
export MANPATH=${PREFIX}/share/man:${MANPATH}
