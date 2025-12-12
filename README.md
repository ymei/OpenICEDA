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

There is a `update_ngspice_macos` target in `src/Makefile`.  Use `gcc-mp-15` to be consistent with verilator.

In order to work with verilator, the script `/opt/OpenICEDA/share/ngspice/scripts/vlnggen` and `verilator_main.cpp` requires modification:

``` diff
--- ngspice/src/xspice/verilog/vlnggen	2025-11-20 00:40:30
+++ /opt/OpenICEDA/share/ngspice/scripts/vlnggen	2025-12-12 11:38:44
@@ -50,7 +50,7 @@

 if $oscompiled = 7 // MacOS
    set macos=1
-   setcs cflags="$cflags --compiler clang"
+   setcs cflags="$cflags --compiler gcc"
 else
    set macos=0
 end
@@ -318,7 +318,8 @@
    setcs tail="__ALL.a"
    setcs v_lib="$objdir/$prefix$tail"          // Like Vlng__ALL.a

-   shell g++ --shared $v_objs $v_lib -pthread -lpthread -o $soname
+   shell echo g++-mp-15 "-Wl,-undefined,dynamic_lookup" --shared $v_objs $v_lib -pthread -lpthread -o $soname
+   shell g++-mp-15 "-Wl,-undefined,dynamic_lookup" --shared $v_objs $v_lib -pthread -lpthread -o $soname
 else
    // Assume we have CL.EXE and use that.  A script avoids multiple \escapes.
```
``` diff
--- ngspice/src/xspice/verilog/verilator_main.cpp	2025-11-20 00:40:30
+++ /opt/OpenICEDA/share/ngspice/scripts/src/verilator_main.cpp	2025-12-12 15:18:03
@@ -3,6 +3,9 @@
 #include "ngspice/cmtypes.h" // For Digital_t
 #include "ngspice/cosim.h"   // For struct co_info and prototypes

+// Required so the intermediate Verilator-built executable links.
+double sc_time_stamp() { return 0.0; }
+
 int main(int argc, char** argv, char**) {
     struct co_info info = {};
```

Configuration command:

```
CFLAGS="-I/opt/local/include -I/opt/local/include/freetype2 -I/opt/local/include/libomp" LDFLAGS="-L/opt/local/lib -L/opt/local/lib/libomp" LIBS="-lomp" ../configure --with-x --enable-xspice --disable-debug --enable-cider --enable-predictor --enable-osdi --enable-pss --with-readline=yes --enable-openmp --prefix=/opt/OpenICEDA
```

### verilator

In order to work well with ngspice, do `CC=gcc-mp-15 CXX=g++-mp-15 CPPFLAGS="-I/opt/local/include" ./configure` when configuring/compiling verilator.

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
