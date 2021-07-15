** MOS I/V scan, G D S B
*.ipin G1v8
*.ipin D1v8
*.ipin B

* References:
* ngspice/examples/various/alterparam.sp
* ngspice/examples/various/nmos_out_BSIM330.sp 
* ngspice/examples/measure/mos-meas-dc-control.sp
* http://diychip.org/sky130/sky130_fd_pr/cells/
* https://skywater-pdk.readthedocs.io/en/latest/rules/device-details.html

* Units are um
.param W  = 1
.param L  = 0.35
.param NF = 1

.option Temp=27.0

* BSIM3v3.3.0 model with modified default parameters 0.18um
.model n1 nmos level=49 version=3.3.0 tox=3.5n nch=2.4e17 nsub=5e16 vth0=0.15
.model p1 pmos level=49 version=3.3.0 tox=3.5n nch=2.5e17 nsub=5e16 vth0=-0.15

* This experimental option enables mos model bin
* selection based on W/NF instead of W
.option wnflag=1
.option savecurrents

.param mc_mm_switch=0
.param mc_pr_switch=1
.lib /opt/OpenICEDA/share/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt
*.include /opt/OpenICEDA/share/pdks/sky130A/libs.tech/ngspice/../../libs.ref/sky130_fd_pr/spice/sky130_fd_pr__nfet_20v0__tt_discrete.corner.spice

Vg G1v8 0 1.8
Vs s 0 0
Vd D1v8 0 1.8
Vb b 0 0

Vd1 D1v8 net1 0
*M1 net1 G1v8 S B n1 L={L} W={W}
*XM1 net1 G1v8 S B sky130_fd_pr__nfet_01v8_lvt L={L} W={W} nf=1 sa=0 sb=0 sd=0 mult=1 m=1
*XM1 net1 G1v8 S B sky130_fd_pr__nfet_01v8 L={L} W={W} nf=1 sa=0 sb=0 sd=0 mult=1 m=1
*XM1 net1 G1v8 S B sky130_fd_pr__pfet_01v8_lvt L={L} W={W} nf=1 sa=0 sb=0 sd=0 mult=1 m=1
XM1 net1 G1v8 S B sky130_fd_pr__pfet_01v8 L={L} W={W} nf=1 sa=0 sb=0 sd=0 mult=1 m=1
+ ad='int((nf+1)/2) * W/nf * 0.29' as='int((nf+2)/2) * W/nf * 0.29'
+ pd='2*int((nf+1)/2) * (W/nf + 0.29)' ps='2*int((nf+2)/2) * (W/nf + 0.29)' nrd='0.29 / W' nrs='0.29 / W'

.control

set filetype = ascii

* Ws/Ls from grep lmin sky130_fd_pr__nfet_01v8__tt.pm3.spice | awk '{print $4*1e6}' | sort -g | uniq
* NMOS LVT
*compose Ws values 0.36 0.39 0.42 0.52 0.54 0.55 0.58 0.6 0.61 0.64 0.65 0.74 0.84 1 1.26 1.68 2 3 5 7 100
* 0.36, 0.39 don't seem to work
*compose Ws values 0.42 0.52 0.54 0.55 0.58 0.6 0.61 0.64 0.65 0.74 0.84 1 1.26 1.68 2 3 5 7 100
*compose Ls values 0.15 0.18 0.25 0.5 1 2 4 8 20 100
* PMOS LVT
compose Ws values 0.42 0.55 0.64 0.84 1 1.26 1.65 1.68 2 3 5 7 100
compose Ls values 0.35 0.5 1 2 4 8 20 100

foreach WW $&Ws
  foreach LL $&Ls
    alterparam W = $WW
    alterparam L = $LL
    reset
    echo W/L = $WW / $LL
*    dc vd 0.0 1.8 0.005 vg 0.0 1.8 0.005
    dc vd 0.0 -1.8 -0.005 vg 0.0 -1.8 -0.005
*   save @m.xm1.msky130_fd_pr__nfet_01v8_lvt[gm]
*   op
    set appendwrite
    write mos_iv.dat G1v8 D1v8 Vd1#branch
  end
end
set color0=white
plot all.Vd1#branch vs D1v8 title 'MOS I/V' xlabel 'Vds' ylabel 'Id'

.endc
.end
