# Tools for managing Open IC EDA toolchain

## `env.sh`
Source this file to gain access to installed toolchain in this directory.

## `src/Makefile`
A set of commands to help build tools and pdks from source.

## `OICvenv/`
Python virtual environment.  `cd src && make update_pyvenv` to update.  Sourcing `env.sh` will include this venv as well.

## `util/`
Utility programs such as simulating device models and plotting.

## Tools to watch out for
  - [XLS: Accelerated HW Synthesis](https://google.github.io/xls/)
  - [OpenFASOC](https://github.com/idea-fasoc/OpenFASOC)
  - [Clash](https://clash-lang.org/)
