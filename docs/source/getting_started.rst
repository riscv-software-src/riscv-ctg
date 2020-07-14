###############
Getting Started
###############

To build a core and to simulate it on a test-soc, you will need the following tools:

1. `Bluespec Compiler <https://github.com/B-Lang-org/bsc>`_: This is required to compile the BSV 
   based soc, core, and other devices to Verilog.
2. Python3.7: Python 3.7 is required to configure compilation macros and clone dependencies.
3. `Verilator 4.08+ <https://www.veripool.org/projects/verilator/wiki/Installing>`_: Verilator is 
   required for simulation purposes.
4. `RISC-V Toolchain 9.2.0+ <https://github.com/riscv/riscv-gnu-toolchain>`_: You will need to install 
   the RISC-V GNU toolchain to be able to compile programs that can run on ChromiteM. 
5. `Modified RISC-V ISA Sim <https://gitlab.com/shaktiproject/tools/mod-spike/-/tree/bump-to-latest>`_: This is required for verification and the *elf2hex* utility.
6. `RISC-V OpenOCD <https://github.com/riscv/riscv-openocd>`_ :This is required if you would like to
   simulate through GDB uding remote-bitbang for JTAG communication.

.. note:: The user is advised to install the above tools from their respective repositories/sources.

You will need the following as well, the installation of which is presented below:

1. Python 3.6.0+: see python_
2. DTC version 1.4.7+: see dtc_

Install Dependencies
====================

.. _python:

Python
------

.. tabs::

   .. tab:: Ubuntu


      Ubuntu 17.10 and 18.04 by default come with python-3.6.9 which is sufficient for using riscv-config.
      
      If you are are Ubuntu 16.10 and 17.04 you can directly install python3.6 using the Universe
      repository
      
      .. code-block:: shell-session

        $ sudo apt-get install python3.6
        $ pip3 install --upgrade pip
      
      If you are using Ubuntu 14.04 or 16.04 you need to get python3.6 from a Personal Package Archive 
      (PPA)::
      
      .. code-block:: shell-session

        $ sudo add-apt-repository ppa:deadsnakes/ppa
        $ sudo apt-get update
        $ sudo apt-get install python3.6 -y 
        $ pip3 install --upgrade pip
      
      You should now have 2 binaries: ``python3`` and ``pip3`` available in your $PATH. 
      You can check the versions as below::
      
      .. code-block:: shell-session

        $ python3 --version
        Python 3.6.9
        $ pip3 --version
        pip 20.1 from <user-path>.local/lib/python3.6/site-packages/pip (python 3.6)

   .. tab:: CentOS7

      The CentOS 7 Linux distribution includes Python 2 by default. However, as of CentOS 7.7, Python 3 
      is available in the base package repository which can be installed using the following commands::
      
      .. code-block:: shell-session

        $ sudo yum update -y
        $ sudo yum install -y python3
        $ pip3 install --upgrade pip
      
      For versions prior to 7.7 you can install python3.6 using third-party repositories, such as the 
      IUS repository::
      
      .. code-block:: shell-session

        $ sudo yum update -y
        $ sudo yum install yum-utils
        $ sudo yum install https://centos7.iuscommunity.org/ius-release.rpm
        $ sudo yum install python36u
        $ pip3 install --upgrade pip
      
      You can check the versions::
      
      .. code-block:: shell-session

        $ python3 --version
        Python 3.6.8
        $ pip --version
        pip 20.1 from <user-path>.local/lib/python3.6/site-packages/pip (python 3.6)


.. _dtc:

Install DTC (device tree compiler)
----------------------------------

We use the DTC 1.4.7 to generate the device tree string in the boot-files. 
To install DTC follow the below commands:

.. code-block:: shell-session

  sudo wget https://git.kernel.org/pub/scm/utils/dtc/dtc.git/snapshot/dtc-1.4.7.tar.gz                
  sudo tar -xvzf dtc-1.4.7.tar.gz                                                                     
  cd dtc-1.4.7/                                                                                       
  sudo make NO_PYTHON=1 PREFIX=/usr/                                                                  
  sudo make install NO_PYTHON=1 PREFIX=/usr/                                                          

.. _build:

Building the Core
=================

The code is hosted on Gitlab and can be checked out using the following
command:

.. code-block:: shell-session

  $ git clone https://gitlab.com/incoresemi/core-generators/chromite.git

If you are cloning the chromite repo for the first time it would be best to install the dependencies
first:

.. code-block:: shell-session

  $ cd chromite/
  $ pyenv activate venv # ignore this is you are not using pyenv
  $ pip install -U -r chromite/requirements.txt

The Chromite core generator takes a specific :ref:`YAML<configure_core_label>` format as input. It makes specific checks to
validate if the user has entered valid data and none of the parameters conflict with each other.
For e.g., mentioning the 'D' extension without the 'F' will get captured by the generator as an
invalid spec. More information on the exact parameters and constraints on each field are discussed
here.

Once the input YAML has been validated, the generator then clones all the dependent repositories
which enable building a test-soc, simulating it and performing verification of the core. 
This is an alternative to maintaining the repositories as submodules, which
typically pollutes the commit history with bump commits.

At the end, the generator outputs a single ``makefile.inc`` in the same folder that it was run,
which contains definitions of paths where relevant bluespec files are present, bsc command with
macro definitions, verilator simulation commands, etc.

A sample yaml input YAML (`default.yaml`) is available in the ``sample_config`` directory of the
repository. 

To build the core with a sample test-soc using the default config do the following:

.. code-block:: shell-session

  $ python -m configure.main -ispec sample_config/default.yaml

The above step generates a ``makefile.inc`` file in the same folder and also
clones other dependent repositories to build a test-soc and carry out
verification. This should generate a log something similar to::

  [INFO]    : ************ Chromite Core Generator ************ 
  [INFO]    : ------ Copyright (c) InCore Semiconductors ------ 
  [INFO]    : ---------- Available under BSD License---------- 
  [INFO]    : 
  
  
  [INFO]    : Checking pre-requisites
  [INFO]    : Cloning "cache_subsystem" from URL "https://gitlab.com/incoresemi/blocks/cache_subsystem"
  [INFO]    : Checking out "1.0.0" for repo "cache_subsystem"
  [INFO]    : Cloning "common_bsv" from URL "https://gitlab.com/incoresemi/blocks/common_bsv"
  [INFO]    : Checking out "master" for repo "common_bsv"
  [INFO]    : Cloning "fabrics" from URL "https://gitlab.com/incoresemi/blocks/fabrics"
  [INFO]    : Checking out "1.1.1" for repo "fabrics"
  [INFO]    : Cloning "bsvwrappers" from URL "https://gitlab.com/incoresemi/blocks/bsvwrappers"
  [INFO]    : Checking out "master" for repo "bsvwrappers"
  [INFO]    : Cloning "devices" from URL "https://gitlab.com/incoresemi/blocks/devices"
  [INFO]    : Checking out "1.0.0" for repo "devices"
  [INFO]    : Cloning "verification" from URL "https://gitlab.com/shaktiproject/verification_environment/verification"
  [INFO]    : Checking out "4.0.0" for repo "verification"
  [INFO]    : Applying Patch "/scratch/git-repo/incoresemi/core-generators/chromite/verification/patches/riscv-tests-shakti-signature.patch" to "/scratch/git-repo/incoresemi/core-generators/chromite/verification/patches/riscv-tests-shakti-signature.patch"
  [INFO]    : Cloning "benchmarks" from URL "https://gitlab.com/incoresemi/core-generators/benchmarks"
  [INFO]    : Checking out "master" for repo "benchmarks"
  [INFO]    : Loading input file: /scratch/git-repo/incoresemi/core-generators/chromite/sample_config/default.yaml
  [INFO]    : Load Schema configure/schema.yaml
  [INFO]    : Initiating Validation
  [INFO]    : No Syntax errors in Input Yaml.
  [INFO]    : Performing Specific Checks
  [INFO]    : Generating BSC compile options
  [INFO]    : makefile.inc generated
  [INFO]    : Creating Dependency graph
  [WARNING] : path: .:%/Libraries:src/:src/predictors:src/m_ext:src/fpu/:src/m_ext/..........
  defines: Addr_space=25 ASSERT rtldump RV64 ibuswidth=64 dbuswidth=64 ....... 
  builddir: build/hw/intermediate
  topfile: test_soc/TbSoc.bsv
  outputfile: depends.mk
  argv: 
  generated make dependency rules for "test_soc/TbSoc.bsv" in: depends.mk
  [INFO]    : Dependency Graph Created
  [INFO]    : Cleaning previously built code
  [WARNING] : rm -rf build/hw/intermediate/* *.log bin/* obj_dir build/hw/verilog/*
  rm -f *.jou rm *.log *.mem log sim_main.h cds.lib hdl.var
  [INFO]    : Run make -j<jobs>



To compile the bluespec source and generate verilog

.. code-block:: shell-session

  $ make -j<jobs> generate_verilog

If you are using the samples/default.yaml config file, this should generate the following folders:

1. build/hw/verilog: contains the generated verilog files.
2. build/hw/intermediate: contains all the intermediate and information files generated by bsc.

To create a verilated executable: 

.. code-block:: shell-session

   $ make link_verilator

This will generate a ``bin`` folder containing the verilated ``chromite_core`` executable. This can be used
for simulation as described in :numref:`simulating_core`.

Congratulations - You have built your very first Chromite core !! :)

.. _simulating_core:

Simulating the Core
===================

The Chromite repository also contains a simple test-soc for the purpose of simulating applications
and verifying the core. 

Structure of Test-SoC
---------------------

The Test-SoC has the following structure (defined to a max of 4 levels of depth):

.. mermaid::

   graph TD;
      X[mkTbSoC] --> A(mkSoC)
      X --> B(mkbram)
      X --> C(mkbootrom)
      A --> D(mkccore_axi4)
      A --> E(mkuart)
      A --> F(mkclint)
      A --> G(mksignature_dump)
      D --> H(mkriscv)
      D --> I(mkdmem)
      D --> J(mkimem)

Description of the above modules:

.. tabularcolumns:: |l|L|

+--------------------+-----------------------------------------------------------+
| Module-Name        | Description                                               |
+--------------------+-----------------------------------------------------------+
| mkriscv            | Contains the 5-stages of the core pipeline including the  | 
|                    | execution and only the interface to the memory subsystem  |
+--------------------+-----------------------------------------------------------+
| mkdmem             | The Data memory subsystem. Includes the data-cache and    |
|                    | data-tlbs                                                 |
+--------------------+-----------------------------------------------------------+
| mkimem             | The instruction memory subsystem. Includes the            |
|                    | instruction-cache and the instruction-tlbs                |
+--------------------+-----------------------------------------------------------+
| mkccore_axi4       | Contains the above modules and the integrations across    |
|                    | them. Also provides 3 AXI-4 interfaces to be connected to | 
|                    | the Cross-bar fabric                                      |
+--------------------+-----------------------------------------------------------+
| mkuart             | UART module                                               |
+--------------------+-----------------------------------------------------------+
| mkclint            | Core Level Interrupt                                      |
+--------------------+-----------------------------------------------------------+
| mksignature_dump   | Signature dump module (for simulation only)               |
+--------------------+-----------------------------------------------------------+
| mkSoc              | contains all the above modules and instantiates the AXI-4 | 
|                    | crossbar fabric as well. The fabric has 2 additional      |
|                    | slaves, which are brought out through the interface to    |
|                    | connect to the boot-rom and bram-main-memory present in   |
|                    | the Test-bench                                            |
+--------------------+-----------------------------------------------------------+
| mkbram             | BRAM based memory acting as main-memory                   |
+--------------------+-----------------------------------------------------------+
| mkbootrom          | Bootrom slave                                             |
+--------------------+-----------------------------------------------------------+
| mkTbSoC            | Testbench that instantiates the Soc, and integrates it    |
|                    | with the bootrom and a bram memory                        |
+--------------------+-----------------------------------------------------------+

The details of the devices can be found in `devices <https://gitlab.com/incoresemi/blocks/devices/>`_

Address Map of Test SoC
^^^^^^^^^^^^^^^^^^^^^^^

  +----------------+-------------------------+
  | Module         | Address Range           |
  +----------------+-------------------------+
  | BRAM-Memory    | 0x80000000 - 0x8FFFFFFF |
  +----------------+-------------------------+
  | BootROM        | 0x00001000 - 0x00010FFF |
  +----------------+-------------------------+
  | UART           | 0x00011300 - 0x00011340 |
  +----------------+-------------------------+
  | CLINT          | 0x02000000 - 0x020BFFFF |
  +----------------+-------------------------+
  | Debug-Halt Loop| 0x00000000 - 0x0000000F |
  +----------------+-------------------------+
  | Signature Dump | 0x00002000 - 0x0000200c |
  +----------------+-------------------------+

Please note that the bram-based memory in the test-bench can only hold upto 32MB of code.
Thus the elf2hex arguments will need to applied accordingly. 

.. note:: The elf2hex program is available from the modified spike application.

.. note:: The size of the BRAM Memory can be changed by changing the configuration
   bsc_compile_options.test_memory_size in the configuration YAML.

BootRom Content
^^^^^^^^^^^^^^^

By default, on system-reset the core will always jump to ``0x1000`` which is mapped to the bootrom. 
The bootrom is initialized using the file ``boot.mem``. The bootrom after a few instructions
causes a re-direction jump to address ``0x80000000`` where the application program is expected to be. 
It is thus required that all programs are linked with text-section begining at ``0x80000000``. 
The rest of the boot-rom holds a dummy device-tree-string information.

To ``boot.mem`` file is generated in the ``bin`` folder using the following command:

.. code-block:: shell-session

   $ make generate_boot_files

.. tip:: You can skip executing the bootrom by changing the `reset_pc` field in the configuration
   YAML. However, the verilated executable will still require a dummy ``boot.mem`` file to initiate
   simulation

.. _verilated_exec:

Verilated Executable
--------------------

We use verilator to simulate the core and the test-soc described above. In order
to generate the verilated executable do the following (you can skip this is you have already
followed the steps so far)

.. code-block:: shell-session

  $ cd chromite
  $ python -m configure.main -ispec sample_config/default.yaml
  $ make -j<jobs> generate_verilog
  $ make link_verilator generate_boot_files

The above should result in following files in the ``bin`` folder:

 - `chromite_core`
 - `boot.mem`

Executing User Programs
-----------------------

Let's assume the software program that you would like to simulate on the core is called 
``prog.elf`` (compiled using standard riscv-gcc). This elf needs to be converted
to a hex file which can be provided to the verilated executable: ``chromite_core``. This
hex can be generated using the following command:

For 64-bit:

.. code-block:: shell-session

  $ elf2hex 8 4194304 bbl 2147483648 > code.mem

For 32-bit:

.. code-block:: shell-session

  $ elf2hex 4 4194304 add.elf 2147483648 > code.mem

place the ``code.mem`` file in the ``bin`` folder and execute the ``chromite_core`` binary
to initiate simulation.

.. note:: Since the boot code in the bootrom implicitly jumps to ``0x80000000`` the programs 
  should also be compiled at ``0x80000000``.

Hello World
^^^^^^^^^^^

To run hello-world first ensure the verilated executable is available
in the bin folder (use steps mentionedin in :numref:`verilated_exec`. 
After which run the following::

  $ make hello
  Hello World

Dhrystone
^^^^^^^^^

To run dhrystone first ensure the verilated executable is available
in the bin folder (use steps mentionedin in :numref:`verilated_exec`. 
After which run the following::

  $ make dhrystone ITERATIONS=10000

  Microseconds for one run through Dhrystone:     10.0
  Dhrystones per Second:                       94663.0 

.. note:: The above numbers are obtained by using the samples/default.yaml config file which has
   been configured for high performance. The performance numbers will change based on the config 
   used to generate the core instance.

CoreMarks
^^^^^^^^^

To run coremarks first ensure the verilated executable is available
in the bin folder (use steps mentionedin in :numref:`verilated_exec`. 
After which run the following::

  $ make coremarks ITERATIONS=35

  2K performance run parameters for coremark.
  CoreMark Size    : 666
  Total ticks      : 12323206
  Total time (secs): 12
  Iterations/Sec   : 2
  Iterations       : 35
  Compiler version : riscv64-unknown-elf-9.2.0
  Compiler flags   : -mcmodel=medany -DCUSTOM -DPERFORMANCE_RUN=1 -DMAIN_HAS_NOARGC=1 \
                     -DHAS_STDIO -DHAS_PRINTF -DHAS_TIME_H -DUSE_CLOCK -DHAS_FLOAT=0 \
                     -DITERATIONS=35 -O3 -fno-common -funroll-loops -finline-functions \
                     -fselective-scheduling -falign-functions=16 -falign-jumps=4 \
                     -falign-loops=4 -finline-limit=1000 -nostartfiles -nostdlib \
                     -ffast-math -fno-builtin-printf -march=rv64imafdc -mexplicit-relocs
  Memory location  : STACK
  seedcrc          : 0xe9f5
  [0]crclist       : 0xe714
  [0]crcmatrix     : 0x1fd7
  [0]crcstate      : 0x8e3a
  [0]crcfinal      : 0xcf56
  Correct operation validated. See README.md for run and reporting rules.


.. note:: The above numbers are obtained by using the samples/default.yaml config file which has
   been configured for high performance. The performance numbers will change based on the config 
   used to generate the core instance.

Notes on Simulation
-------------------

Support for PutChar
^^^^^^^^^^^^^^^^^^^

The test-soc for simulation contains a simple uart. The ``putchar`` function for the same is available 
`HERE <https://gitlab.com/shaktiproject/uncore/devices/blob/master/uart/uart_driver.c>`_. 
This has to be used in the printf functions. The output of the ``putchar`` is captured in a separate 
file app_log during simulation.

Simulation Arguments (Logger Utility)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. ``./chromite_core +rtldump``: if the core has been configured with ``trace_dump: true``
   , then a ``rtl.dump`` file is created which shows the log of instruction execution. Each line
   in the file has the following format::

   <privilege-mode> <program-counter> <instruction> <register-updated> <register value>

2. To enable printing of debug statements from the bluespec code, one can pass
   custom logger arguments to the simulation binary as follows

   - ``./out +fullverbose``: prints all the logger statements across all modules
     and all levels of verbosity
   - ``./out +mstage1 +l0``: prints all the logger statements within module
     stage1 which are at verbosity level 0. 
   - ``./out +mstage2 +mstage4 +l0 +l3``: prints all the logger statements
     within modules stage2 and stage4 which are at verbosity levels 0 and 3
     only.
      
3. An ``app_log`` file is also created which captures the output of the uart,
   typically used in the ``putchar`` function in C/C++ codes as mentioned
   above.

Connect to GDB in Simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A debugger implementation following the riscv-debug-draft-014 has been integrated with the core.
This can be instantiated in the design by configuring with: ``debugger_support: true``

Perform the following steps to connect to the core executable with a gdb terminal. 
This assumes you have installed openocd and is available as part of you `$PATH` variable.

Modify the ``sample_config/default.yaml`` to enable:  debugger_support and open_ocd. 
Generate a new executable with this config to support jtag remote-bitbang in the
test-bench

.. code-block:: shell-session

  $ python -m configure.main -ispec sample_config/default.yaml
  $ make gdb # generate executable with open-ocd vpi enabled in the test-bench

1. Simulate the RTL
   In a new terminal do the following:
   
   .. code-block:: shell-session
   
     $ cd chromite/bin/
     $ ./chromite_core > /dev/null

2. Connect to OpenOCD
   Open a new terminal and type the following:
   
   .. code-block:: shell-session
   
   
     $ cd chromite/test_soc/gdb_setup/
     $ openocd -f shakti_ocd.cfg

3. Connect to GDB
   Open yet another terminal and type the following:
   
   .. code-block:: shell-session
   
     $ cd chromite/test_soc/gdb_setup
     $ riscv64-unknown-elf-gdb -x gdb.script

In this window you can now perform gdb commands like : ``set $pc, i r, etc``

To reset the SoC via the debugger you can execute the following within the gdb shell:

.. code:: shell-session

  $ monitor reset halt
  $ monitor gdb_sync
  $ stepi
  $ i r

.. note:: The above will not reset memories like the BRAM Memory.

Synthesizing the Core
=====================

When synthesizing for an FPGA/ASIC, the top module should be ``mkccore_axi4 (mkccore_axi4.v)`` 
as the top module. 

The ``mkimem`` and ``mkdmem`` module include SRAM instances which implement the respective data 
and tag arrays. These are implemented as BRAMs and thus require no changes for FPGAs. 
However for an ASIC flow, it is strictly advised to replace the BRAMs with respective SRAMs. 

