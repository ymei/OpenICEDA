# Tools for managing Open IC EDA toolchain

## `env.sh`
Source this file to gain access to installed toolchain in this directory.

## `src/Makefile`
A set of commands to help build tools and pdks from source.

## `OICvenv/`
Python virtual environment.  `cd src && make update_pyvenv` to update.  Sourcing `env.sh` will include this venv as well.

## `util/`
Utility programs such as simulating device models and plotting.

## Installation on macOS
Dependencies are installed via `macports`.

### magic

```
./configure --prefix=/opt/OpenICEDA --with-tcl=/opt/local --with-tk=/opt/local --x-includes=/opt/local/include --x-libraries=/opt/local/lib
make CFLAGS="-std=gnu90 -Wno-error=implicit-function-declaration -I/opt/local/include" -j8
```

### ngspice

```
CFLAGS="-I/opt/local/include -I/opt/local/include/freetype2 -I/opt/local/include/libomp" LDFLAGS="-L/opt/local/lib -L/opt/local/lib/libomp" LIBS="-lomp" ../configure --with-x --enable-xspice --disable-debug --enable-cider --with-readline=yes --enable-openmp --prefix=/opt/OpenICEDA
```

### netgen

```
./configure --prefix=/opt/OpenICEDA --with-tcl=/opt/local --with-tk=/opt/local --x-includes=/opt/local/include --x-libraries=/opt/local/lib
make CFLAGS="-std=gnu90 -Wno-error=implicit-function-declaration -I/opt/local/include" -j8
```

## Tools to watch out for
  - [XLS: Accelerated HW Synthesis](https://google.github.io/xls/)
  - [OpenFASOC](https://github.com/idea-fasoc/OpenFASOC)
  - [Clash](https://clash-lang.org/)
