# Tools for managing Open IC EDA toolchain

## `env.sh`
Source this file to gain access to installed toolchain in this directory.  **NOTE** source before `make` or update packages.

## `src/Makefile`
A set of commands to help build tools and pdks from source.

## `OICvenv/`
Python virtual environment.  `cd src && make update_pyvenv` to update.  Sourcing `env.sh` will include this venv as well.

## `util/`
Utility programs for simulating device models and plotting, etc.

## Tool usage tips

### `netgen`

  - `netgen -batch lvs "cirA.spice subckt_name_A" "cirB.spice subckt_name_B" $PDK_ROOT/sky130B/libs.tech/netgen/setup.tcl`
  - Or put `$PDK_ROOT/sky130B/libs.tech/netgen/setup.tcl` under the current directory then launch `netgen` without specifying this technology file

### `OpenLane`

  - `cd $OPENLANE_ROOT`, `. venv/bin/activate`, then `make mount` to start docker.

## Installation on macOS
Dependencies are installed via `macports`.

### xschem

  1. Run `configure --prefix=/opt/OpenICEDA`.
  2. Modify `Makefile.conf` to have `-ltcl8.6 -ltk8.6`.
  3. Modify `src/xschem.h`: `#define __unix__ 1`.

### magic

```
./configure --prefix=/opt/OpenICEDA --with-tcl=/opt/local --with-tk=/opt/local --x-includes=/opt/local/include --x-libraries=/opt/local/lib
make CFLAGS="-std=gnu90 -Wno-error=implicit-function-declaration -I/opt/local/include" -j8
```

### ngspice

```
CFLAGS="-I/opt/local/include -I/opt/local/include/freetype2 -I/opt/local/include/libomp" LDFLAGS="-L/opt/local/lib -L/opt/local/lib/libomp" LIBS="-lomp" ../configure --with-x --enable-xspice --disable-debug --enable-cider --enable-predictor --enable-osdi --enable-pss --with-readline=yes --enable-openmp --prefix=/opt/OpenICEDA
```

### netgen

```
./configure --prefix=/opt/OpenICEDA --with-tcl=/opt/local --with-tk=/opt/local --x-includes=/opt/local/include --x-libraries=/opt/local/lib
make CFLAGS="-std=gnu90 -Wno-error=implicit-function-declaration -I/opt/local/include -I../base" -j8
```

## Installation on Ubuntu
All of the dependencies via
```
sh util/Ubuntu-dependencies.sh
```

After installing magic and ngspice the libs may need to be relinked.
```
sudo update-alternatives --install /usr/bin/magic magic /opt/OpenICEDA/bin/magic 0
sudo update-alternatives --install /usr/bin/ngspice ngspice /opt/OpenICEDA/bin/ngspice 0
```
But in principle, `env.sh` should set up `PATH` properly, which makes this unnecessary.

Then xschem can be launched by
```
xschem --rcfile=/opt/OpenICEDA/share/pdk/sky130B/libs.tech/xschem/xschemrc
```

## Tools to watch out for
  - [XLS: Accelerated HW Synthesis](https://google.github.io/xls/)
  - [OpenFASOC](https://github.com/idea-fasoc/OpenFASOC)
  - [Clash](https://clash-lang.org/)
  - [JKU IIC](https://github.com/hpretl/iic-osic)
