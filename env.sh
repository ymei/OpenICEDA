PREFIX=/opt/OpenICEDA
PYVENV=${PREFIX}/OICvenv
test -r ${PYVENV}/bin/activate && . ${PYVENV}/bin/activate
# for xschem_sky130
export PDK_ROOT=${PREFIX}/share/pdk
export VERILATOR_ROOT=${PREFIX}/src/verilator
export PATH=${PREFIX}/bin:${PREFIX}/src/klayout/bin-release:${PATH}
export LD_LIBRARY_PATH=${PREFIX}/lib:${PREFIX}/src/klayout/bin-release:${LD_LIBRARY_PATH}
export MANPATH=${PREFIX}/share/man:${MANPATH}
