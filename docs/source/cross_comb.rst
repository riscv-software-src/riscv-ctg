************************************************
Test Generation using Cross Coverage Coverpoints
************************************************

Coverpoints constituting multiple instructions can help identify interesting instruction
sequences which have architectural significance such as structural hazards and data hazards.
The coverpoint node associated with the test generation is ``cross_comb`` defined here.

The test generator employs a constraint solver to generate relevant instruction sequence for a
``cross_comb`` coverpoint.

Example
#######

Consider a cross combination coverpoint defined as:

code ::

    
