# CHANGELOG

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.8] - 2021-10-21
- Updated and added bitmanip_real_world.py script to generate test with real world patterns.

## [0.5.7] - 2021-09-20
- Fix the generation of rv32ec/cswsp test

## [0.5.6] - 2021-09-19
- rvtest\_data section now includes 16 bytes of rotated versions of `0xbabecafe`

## [0.5.5] - 2021-09-10
- Add CGFs for F&D extensions
- Add support for F & D extension test generation
- Add support for test splitting based on number of macro instances
- Add macro based signature entry sizes

## [0.5.4] - 2021-09-02
- Updated logger to enable logging for API calls.

## [0.5.3] - 2021-08-12

- Update instruction format of aes32 and sm4 instructions for K extensions.
- Improve the coverage of S-boxes for sm4 instructions by setting overlap = "Y" in byte_count.

## [0.5.2] - 2021-08-09
- Fix sign of immediate value for branching instructions while filtering.
- Fix instruction generation while result shadowing.

## [0.5.1] - 2021-07-16
- Update the sample cgf for RV32E
- fix the generation of RV32E Tests

## [0.5.0] - 2021-05-27
- support for K extension and subextension instructions
- support for comments in coverpoints
- added std_op field in template.yaml to indicate is standard-instruction the pseudo op belongs to.
- added support for parsing #nosat in coverpoint which disables the solvers for the current resolution.
- added sample cgf files for rv64ik and rv32ik

## [0.4.5] - 2021-05-15
- Minor code restructure to support API calls.
- Fixes to include env files in pip package.

## [0.4.4] - 2021-02-23
- Added missing coverpoints for JALR
- fixed CI to run main.yml on pushes to master.
- added version check for PRs in test.yml

## [0.4.3] - 2021-02-23
- Updated CI to actions

## [0.4.2] - 2021-01-15
- Fixed header base_isa argument
- Change header configuration argument list
- Remove first empty line in assembler output
- Add header randomization argument

## [0.4.1] - 2020-12-13
- Fixed correctval generation for existing ops.
- Fixed signedness of operand values for m ext instructions.
- Added operation strings for m and c extensions.

## [0.4.0] - 2020-11-19
- Added base_isa as option in cli
- Added support for register set based on base isa.
- Reformatted output values in tests to be hex strings.
- change compliance_model to model_test

## [0.3.0] - 2020-11-18
- minor doc updates
- renamed compliance_test.h to arch_test.h
- added aliasing macros for v0.1 compliance framework
- split datasets and coverpoints into multiple cgfs
- support for multiple cgf as inputs
- added support for special datasets to relevant instructions
- adding explicit entry point label to all tests
- remove x2 as coverpoint in cswsp and csdsp

## [0.2.0] - 2020-11-10
- initial draft of CTG
- parallelization support added
- random solvers can be used
- support rv32/64imc instructions
- docs updated

## [0.1.0] - 2020-07025
- initial draft

