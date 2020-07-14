

ISA
  **Description**: Takes input a string representing the ISA supported by the implementation. All extension names
  (other than Zext) should be mentioned in upper-case. Z extensions should begin with an upper-case
  'Z' followed by lower-case extension name (without Camel casing)

  .. note:: Zicsr is enabled by default and cannot be switched off. Zifencei is controlled based on
    whether the caches are enabled or not

  **Examples**:

  .. code-block:: none

    ISA: RV32IMA
    ISA: RV64IMAFDCZifencei

iepoch_size
 **Description**: integer value indicating the size of the epochs for the
 instruction memory subsystem. Allowed value is 2 only

 **Examples**:

 .. code-block:: yaml

   iepoch_size: 2

depoch_size
 **Description**: integer value indicating the size of the epochs for the
 data memory subsystem. Allowed value is 1 only

 **Examples**:

 .. code-block:: yaml

   depoch_size: 1

dtvec_base
  **Description**: An integer address indicating where the self-loop for the
  debug module sits

  **Examples**:

  .. code-block:: yaml

    dtvec_base: 0x0

s_extension
  **Description**: Describes various supervisor and MMU related parameters.
  These parameters only take effect when "S" is present in the ISA field.

    - ``mode``: a string indicating the virtualisation mode to be implemented. Can
      be one of : sv32, sv39 or sv48. Please note for RV32 only sv32 is supported
      and for RV64 sv39 and sv48 are supported.
    - ``itlb_size``: integer indicating the size of entries in the Instruction TLB
    - ``dtlb_size``: integer indicating the size of entries in the Data TLB
    - ``asid_width``: integer indicating the size of the ASID field. For RV32 it can
      be maximum 9 and for RV64 is can be maximum 16

  **Examples**:

  .. code-block:: yaml

    s_extension:
      mode: sv39
      itlb_size: 4
      dtlb_size: 4
      asid_width: 9

.. _schema_pmp:

pmp
  **Description**: Defines the pmp configuration

    - ``enable``: boolean value indicating if pmp support should be enabled.
    - ``entries``: number of pmp regions to be supported. Max value of 16.
      Minimum value of 1
    - ``granularity``: granularity of protection in terms of bytes. Minimum is
      8 bytes for a 64-bit core and 4 bytes for a 32-bit core

  **Examples**:

  .. code-block:: yaml

    pmp:
      enable: true
      entries: 2
      granularity: 8

m_extension
  **Description**: Describes various M-extension related parameters. These
  parameters take effect only is "M" is present in the ISA field.

    - ``mul_stages``: an integer indicating the number of pipeline stages for the
      integer multiplier. Max value is limited to the XLEN defined in the ISA.
    - ``div_stages``: an integer indicating the number of cycles for a single
      division operation. Max value is limited to the XLEN defined in the ISA.

  **Examples**:

  .. code-block:: yaml

    m_extension:
      mul_stages : 2
      div_stages: 64


branch_predictor
  **Description**: Describes various branch predictor related parameters. 

    - ``instantiate``: boolean value indicating if the predictor needs to be
      instantiated
    - ``predictor``: string indicating the type of predictor to be implemented. Valid
      values are: 'gshare'
    - ``on_reset``: Indicates if the predictor should be enabled on system-reset or
      not. Valid values are : ['enable','disable']
    - ``btb_depth``: integer indicating the size of the branch target buffer
    - ``bht_depth``: integer indicating the size of the bracnh history buffer
    - ``history_len``: integer indicating the size of the global history register
    - ``history_bits``: integer indicating the number of bits used for indexing bht/btb.
    - ``ras_depth``: integer indicating the size of the return address stack.

  **Examples**:

  .. code-block:: yaml

    branch_predictor:
      instantiate: True
      predictor: gshare
      on_reset: "enable"
      btb_depth: 32
      bht_depth: 512
      history_len: 8
      history_bits: 5
      ras_depth: 8

icache_configuration
  **Description**: Describes the various instruction cache related features.

    - ``instantiate``: boolean value indicating if the predictor needs to be
      instantiated
    - ``on_reset``: Indicates if the predictor should be enabled on system-reset or
      not. Valid values are : ['enable','disable']
    - ``sets``: integer indicating the number of sets in the cache
    - ``word_size``: integer indicating the number of bytes in a word. Fixed to 4.
    - ``block_size``: integer indicating the number of words in a cache-block.
    - ``ways``: integer indicating the number of the ways in the cache
    - ``fb_size``: integer indicating the number of fill-buffer entries in the cache
    - ``replacement``: strings indicating the replacement policy. Valid values are:
      ["PLRU", "RR", "Random"]
    - ``ecc_enable``: boolean field indicating if ECC should be enabled on the
      cache.
    - ``one_hot_select``: boolean value indicating if the bsv one-hot selection
      funcion should be used of conventional for-loops to choose amongst
      lines/fb-lines. Choice of this has no affect on the functionality

  If supervisor is enabled then the max size of a single way should not exceed
  4Kilo Bytes

  **Examples**:

  .. code-block:: yaml

    icache_configuration:
      instantiate: True
      on_reset: "enable"
      sets: 4
      word_size: 4
      block_size: 16
      ways: 4
      fb_size: 4
      replacement: "PLRU"
      ecc_enable: false
      one_hot_select: false

dcache_configuration
  **Description**: Describes the various instruction cache related features.

    - ``instantiate``: boolean value indicating if the predictor needs to be
      instantiated
    - ``on_reset``: Indicates if the predictor should be enabled on system-reset or
      not. Valid values are : ['enable','disable']
    - ``sets``: integer indicating the number of sets in the cache
    - ``word_size``: integer indicating the number of bytes in a word. Fixed to 4.
    - ``block_size``: integer indicating the number of words in a cache-block.
    - ``ways``: integer indicating the number of the ways in the cache
    - ``fb_size``: integer indicating the number of fill-buffer entries in the cache
    - ``sb_size``: integer indicating the number of store-buffer entries in the cache. Fixed to 2
    - ``replacement``: strings indicating the replacement policy. Valid values are:
      ["PLRU", "RR", "Random"]
    - ``ecc_enable``: boolean field indicating if ECC should be enabled on the
      cache.
    - ``one_hot_select``: boolean value indicating if the bsv one-hot selection
      funcion should be used of conventional for-loops to choose amongst
      lines/fb-lines. Choice of this has no affect on the functionality
    - ``rwports``: number of read-write ports available on the brams. Allowed
      values are 1 and 2. Default value is 1

  If supervisor is enabled then the max size of a single way should not exceed
  4Kilo Bytes

  **Examples**:

  .. code-block:: yaml

    dcache_configuration:
      instantiate: True
      on_reset: "enable"
      sets: 4
      word_size: 4
      block_size: 16
      ways: 4
      fb_size: 4
      sb_size: 2
      replacement: "PLRU"
      ecc_enable: false
      one_hot_select: false
      rwports: 1

reset_pc
  **Description**: Integer value indicating the reset value of program counter

  **Example**:

  .. code-block: yaml

    reset_pc: 4096

physical_addr_size
  **Description**: Integer value indicating the number of physical address bits

  **Examples**:

  .. code-block:: yaml

    physical_addr_size: 32

bus_protocol
  **Description**: bus protocol for the master interfaces of the core. Fixed to
  "AXI4"

  **Examples**: 

  .. code-block:: yaml

    bus_protocol: AXI4

fpu_trap
  **Description**: Boolean value indicating if the core should trap on floating
  point exception and integer divide-by-zero conditions.

  **Examples**:

  .. code-block:: yaml

    fpu_trap: False

debugger_support
  **Description**: A boolean field indicating if the core should be implemented
  with debugger support

  **Examples**:

  .. code-block: yaml

    debugger_support : True

no_of_triggers
  **Description**: An integer field indicating the number of triggers to be
  implemented

  **Examples**:

  .. code-block:: yaml

    no_of_triggers: 4

csr_configuration
  **Description**: Captures various parameters for the csr implementation

    - ``structure``: should be fixed to "Daisy"
    - ``counters_grp4``: an integer field indicating the number of Counters
      implemented in this group. Max value is 7
    - ``counters_grp5``: an integer field indicating the number of Counters
      implemented in this group. Max value is 7
    - ``counters_grp6``: an integer field indicating the number of Counters
      implemented in this group. Max value is 7
    - ``counters_grp7``: an integer field indicating the number of Counters
      implemented in this group. Max value is 8

  **Examples**:

  .. code-block:: yaml

    csr_configuration:
      structure : "daisy"
      counters_in_grp4: 7
      counters_in_grp5: 7
      counters_in_grp6: 7
      counters_in_grp7: 8

verilator_configuration
  **Description**: describes the various configurations for verilator compilation.

    - ``coverage``: indicates the type of coverage that the user would like to
      track. Valid values are: ["none", "line", "toggle", "all"]
    - ``trace``: boolean value indicating if vcd dumping should be enabled.
    - ``threads``: an integer field indicating the number of threads to be used
      during simulation
    - ``verbosity``: a boolean field indicating of the verbose/display statements in
      the generated verilog should be compiled or not.
    - ``out_dir``: name of the directory where the final executable will be dumped.
    - ``sim_speed``: indicates if the user would prefer a fast simulation or slow
      simulation. Valid values are : ["fast","slow"]. Please selecting "fast"
      will speed up simulation but slow down compilation, while selecting "slow"
      does the opposite.

  **Examples**:

  .. code-block:: yaml

   verilator_configuration:
     coverage: "none"
     trace: False
     threads: 1
     verbosity: True
     open_ocd: False
     sim_speed: fast

bsc_compile_options
  **Description**: Describes the various bluespec compile options

    - ``test_memory_size``: size of the BRAM memory in the test-SoC in bytes.
       Default is 32MB
    - ``assertions``: boolean value indicating if assertions used in the design
      should be compiled or not
    - ``trace_dump``: boolean value indicating if the logic to generate a simple
      trace should be implemented or not. Note this is only for simulation and not
      a real trace
    - ``compile_target``: a string indicating if the bsv files are being compiled for simulation
      of for asic/fpga synthesis. The valid values are: [ 'sim', 'asic', 'fpga' ]
    - ``suppress_warnings``: List of warnings which can be suppressed during
      bluespec compilation. Valid values are: ["none", "all", "G0010", "T0054", "G0020", "G0024", "G0023", "G0096", "G0036", "G0117", "G0015"]
    - ``verilog_dir``: the directory name of where the generated verilog will be
      dumped
    - ``open_ocd``: a boolean field indicating if the test-bench should have an
      open-ocd vpi enabled.
    - ``build_dir``: the directory name where the bsv build files will be dumped
    - ``top_module``: name of the top-level bluespec module to be compiled.
    - ``top_file``: file containing the top-level module.
    - ``top_dir``: directory containing the top_file.

  **Examples**:

  .. code-block:: yaml

   bsc_compile_options:
     assertions: True
     trace_dump: True
     suppress_warnings: "none"
     top_module: mkTbSoc
     top_file: TbSoc
     top_dir: base_sim
     out_dir: bin
