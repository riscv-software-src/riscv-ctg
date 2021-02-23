# CHANGELOG

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

