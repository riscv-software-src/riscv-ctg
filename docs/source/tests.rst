#####################
Benchmarking the Core
#####################

The max DMIPS of the Chromite core is **1.72 DMIPs/MHz.**

The max CoreMarks of the Chromite core is **2.9 CoreMarks/MHz**

The Chromite core is highly configurable and allows workload specific tuning to achieve the
maximum performance. This document will highlight some of the settings and their respective
benchmark numbers. For the following benchmarks the core has been configured using the
default.yaml available in the ``samples/`` folder.

.. note:: Make sure you are using gcc 9.2.0 or above to replicate the following results.

Benchmarking Dhrystone
======================

The following numbers have been obtained via simulation where the number of ITERATIONS
was fixed at 5000

Flags used for compilation::

  -mcmodel=medany -static -std=gnu99 -O2 -ffast-math \
  -fno-common -fno-builtin-printf -march=rv64$(march) -mabi=lp64d \
  -w -static -nostartfiles -lgcc

When ``$march`` is ``rv64imac`` the DMIPs/MHz is **1.68**::

  Microseconds for one run through Dhrystone:     10.0
  Dhrystones per Second:                       94652.0


When ``$march`` is ``rv64ima``  the DMIPs/MHz is **1.72**::

  Microseconds for one run through Dhrystone:     10.0
  Dhrystones per Second:                       96216.0

Benchmarking CoreMarks
======================

The following numbers have been obtained via simulation where the number of ITERATIONS
was fixed at 100

Flags used for compilation are available in the logs below: 

When ``$march`` is ``rv64imac`` the CoreMarks/MHz is **2.84**::

  2K performance run parameters for coremark.
  CoreMark Size    : 666
  Total ticks      : 35205197
  Total time (secs): 35
  Iterations/Sec   : 2
  Iterations       : 100
  Compiler version : riscv64-unknown-elf-9.2.0
  Compiler flags   : -mcmodel=medany -DCUSTOM -DPERFORMANCE_RUN=1 -DMAIN_HAS_NOARGC=1 \
                     -DHAS_STDIO -DHAS_PRINTF -DHAS_TIME_H -DUSE_CLOCK -DHAS_FLOAT=0 \
                     -DITERATIONS=10 -O3 -fno-common -funroll-loops -finline-functions \
                     -fselective-scheduling -falign-functions=16 -falign-jumps=4 \
                     -falign-loops=4 -finline-limit=1000 -nostartfiles -nostdlib -ffast-math \
                     -fno-builtin-printf -march=rv64imac -mexplicit-relocs
  Memory location  : STACK
  seedcrc          : 0xe9f5
  [0]crclist       : 0xe714
  [0]crcmatrix     : 0x1fd7
  [0]crcstate      : 0x8e3a
  [0]crcfinal      : 0x988c
  Correct operation validated. See README.md for run and reporting rules.


When ``$march`` is ``rv64ima`` the CoreMarks/MHz is **2.897**::

  2K performance run parameters for coremark.
  CoreMark Size    : 666
  Total ticks      : 34516277
  Total time (secs): 34
  Iterations/Sec   : 2
  Iterations       : 100
  Compiler version : riscv64-unknown-elf-9.2.0
  Compiler flags   : -mcmodel=medany -DCUSTOM -DPERFORMANCE_RUN=1 -DMAIN_HAS_NOARGC=1 \
                     -DHAS_STDIO -DHAS_PRINTF -DHAS_TIME_H -DUSE_CLOCK -DHAS_FLOAT=0 \
                     -DITERATIONS=100 -O3 -fno-common -funroll-loops -finline-functions \
                     -fselective-scheduling -falign-functions=16 -falign-jumps=4 \
                     -falign-loops=4 -finline-limit=1000 -nostartfiles -nostdlib -ffast-math \
                     -fno-builtin-printf -march=rv64ima -mexplicit-relocs
  Memory location  : STACK
  seedcrc          : 0xe9f5
  [0]crclist       : 0xe714
  [0]crcmatrix     : 0x1fd7
  [0]crcstate      : 0x8e3a
  [0]crcfinal      : 0x988c
  Correct operation validated. See README.md for run and reporting rules.



Why Compressed Binaries have reduced performance?
=================================================

If you have observed the numbers above, it is evident that for the same configuration of the branch-predictor, compressed provides a slight reduction in DMIPs.
This is because of the way the  fetch-stage (stage1) has been designed.

The fetch stage always expects the I$ to respond with a 32-bit word which is 4-byte aligned. Since it is possible that the 32-bit word can hold upto 2 16-bit compressed instructions the predictor also always presents 2 predictions one for `pc` and one for `pc+2`.
While analysing the 32-bit word from the I$ the following scenarios can occur:

* **Case-1**: entire word is a 32-bit instruction. In this case the entire word and the prediction for `pc` is sent to the decode stage.
* **Case-2**: word contains 2 16-bit instructions. in this case in the first cycle the lower 16-bits of the word and prediction of `pc` is sent to the decode stage. In the next cycle the upper 16-bits and prediction of `pc+2` is sent to the decode stage.
* **Case-3**: lower 16-bits need to be concatenated with the upper 16-bits of the previous I$ response. in this case the a new 32-bit instruction is formed and the prediction of the previous response is sent to the decode stage.
* **Case-4**" Only the upper 16-bits of the I$ needs to be analysed. If the upper 16-bits are compressed then the same and prediction of `pc+2` is sent to the decode stage. If however, the upper 16-bits are the lower part of a 32-bit instruction, then we need to wait for the next I$ response and use the Case-3 scheme then. Now one can land in this case, when there is jump to a 32-bit instruction placed at a 2-byte buondary.

Now that we understand how the fetch-stage works, assume that all the dhrystone code fits within the I$ (i.e. no misses) and predictor is also well trained to provide all correct-predictions. Consider the following sequence from dhrystone:

.. code-block:: bash

  ...
  8000106e: 0x00001797            auipc a5,0x1
  ...
  ...
  ...
  800010d8: 0xf97ff0ef            jal ra,8000106e
  ...

Now each time the ``jal`` instruction is executed the fetch-stage enters into case-4 where the upper 16-bits of the 32-bit word at ``8000106c`` is the lower part of a 32-bit instruction starting at ``0x8000106e`` and thus lead to a single-cycle stall in sending the ``auipc`` instruction into the decode stage.

Since in dhrystone the above kind of sequence occurs for 3 scenarios in each iteration, and thus there is always a single-cycle delay for each scenario - hence the reduced performance for compressed support.




