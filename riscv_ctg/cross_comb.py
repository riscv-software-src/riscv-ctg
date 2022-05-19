# See LICENSE.incore for details
import random
from collections import defaultdict
from constraint import *
import re

import riscv_isac.utils as isac_utils
from riscv_ctg.constants import *
from riscv_ctg.log import logger
import riscv_ctg.utils as utils
import riscv_ctg.constants as const

import time
from math import *
import struct
import sys
import itertools

from riscv_ctg.dsp_function import *

twos_xlen = lambda x: twos(x,xlen)

OPS = {
    'rformat': ['rs1', 'rs2', 'rd'],
    'iformat': ['rs1', 'rd'],
    'sformat': ['rs1', 'rs2'],
    'bsformat': ['rs1', 'rs2', 'rd'],
    'bformat': ['rs1', 'rs2'],
    'uformat': ['rd'],
    'jformat': ['rd'],
    'crformat': ['rs1', 'rs2'],
    'cmvformat': ['rd', 'rs2'],
    'ciformat': ['rd'],
    'cssformat': ['rs2'],
    'ciwformat': ['rd'],
    'clformat': ['rd', 'rs1'],
    'csformat': ['rs1', 'rs2'],
    'caformat': ['rs1', 'rs2'],
    'cbformat': ['rs1'],
    'cjformat': [],
    'kformat': ['rs1','rd'],
    'frformat': ['rs1', 'rs2', 'rd'],
    'fsrformat': ['rs1', 'rd'],
    'fr4format': ['rs1', 'rs2', 'rs3', 'rd'],
    'pbrrformat': ['rs1', 'rs2', 'rd'],
    'phrrformat': ['rs1', 'rs2', 'rd'],
    'pbrformat': ['rs1', 'rd'],
    'phrformat': ['rs1', 'rd'],
    'pbriformat': ['rs1', 'rd'],
    'phriformat': ['rs1', 'rd'],
    'psbrrformat': ['rs1', 'rs2', 'rd'],
    'pshrrformat': ['rs1', 'rs2', 'rd'],
    'pwrrformat': ['rs1', 'rs2', 'rd'],
    'pwriformat': ['rs1', 'rd'],
    'pwrformat': ['rs1', 'rd'],
    'pswrrformat': ['rs1', 'rs2', 'rd'],
    'pwhrrformat': ['rs1', 'rs2', 'rd'],
    'pphrrformat': ['rs1', 'rs2', 'rd'],
    'ppbrrformat': ['rs1', 'rs2', 'rd'],
    'prrformat': ['rs1', 'rs2', 'rd'],
    'prrrformat': ['rs1', 'rs2', 'rs3', 'rd']
}
''' Dictionary mapping instruction formats to operands used by those formats '''

VALS = {
    'rformat': "['rs1_val', 'rs2_val']",
    'iformat': "['rs1_val', 'imm_val']",
    'sformat': "['rs1_val', 'rs2_val', 'imm_val']",
    'bsformat': "['rs1_val', 'rs2_val', 'imm_val']",
    'bformat': "['rs1_val', 'rs2_val', 'imm_val']",
    'uformat': "['imm_val']",
    'jformat': "['imm_val']",
    'crformat': "['rs1_val', 'rs2_val']",
    'cmvformat': "['rs2_val']",
    'ciformat': "['rs1_val', 'imm_val']",
    'cssformat': "['rs2_val', 'imm_val']",
    'ciwformat': "['imm_val']",
    'clformat': "['rs1_val', 'imm_val']",
    'csformat': "['rs1_val', 'rs2_val', 'imm_val']",
    'caformat': "['rs1_val', 'rs2_val']",
    'cbformat': "['rs1_val', 'imm_val']",
    'cjformat': "['imm_val']",
    'kformat': "['rs1_val']",
    'frformat': "['rs1_val', 'rs2_val', 'rm_val']",
    'fsrformat': "['rs1_val', 'rm_val']",
    'fr4format': "['rs1_val', 'rs2_val', 'rs3_val', 'rm_val']",
    'pbrrformat': 'simd_val_vars("rs1", xlen, 8) + simd_val_vars("rs2", xlen, 8)',
    'phrrformat': 'simd_val_vars("rs1", xlen, 16) + simd_val_vars("rs2", xlen, 16)',
    'pbrformat': 'simd_val_vars("rs1", xlen, 8)',
    'phrformat': 'simd_val_vars("rs1", xlen, 16)',
    'pbriformat': 'simd_val_vars("rs1", xlen, 8) + ["imm_val"]',
    'phriformat': 'simd_val_vars("rs1", xlen, 16) + ["imm_val"]',
    'psbrrformat': 'simd_val_vars("rs1", xlen, 8) + ["rs2_val"]',
    'pshrrformat': 'simd_val_vars("rs1", xlen, 16) + ["rs2_val"]',
    'pwrrformat': 'simd_val_vars("rs1", xlen, 32) + simd_val_vars("rs2", xlen, 32)',
    'pwriformat': 'simd_val_vars("rs1", xlen, 32) + ["imm_val"]',
    'pwrformat': 'simd_val_vars("rs1", xlen, 32)',
    'pswrrformat': 'simd_val_vars("rs1", xlen, 32) + ["rs2_val"]',
    'pwhrrformat': 'simd_val_vars("rs1", xlen, 32) + simd_val_vars("rs2", xlen, 16)',
    'pphrrformat': '["rs1_val"] + simd_val_vars("rs2", xlen, 16)',
    'ppbrrformat': '["rs1_val"] + simd_val_vars("rs2", xlen, 8)',
    'prrformat': '["rs1_val", "rs2_val"]',
    'prrrformat': "['rs1_val', 'rs2_val' , 'rs3_val']"
}
''' Dictionary mapping instruction formats to operand value variables used by those formats '''

def isInt(s):
    '''
    Utility function to check if the variable is an int type. Returns False if
    not.
    '''
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_default_registers(ops, datasets):
    problem = Problem()
    not_x0 = lambda x: x not in ['x0']

    for op in ops:
        dataset = datasets[op]
        # problem.addVariable(op,list(random.sample(dataset, len(dataset))))
        problem.addVariable(op,dataset)
        problem.addConstraint(not_x0,tuple([op]))
    if len(ops) > 1:
        cond = " and ".join(["!=".join(x) for x in itertools.combinations(ops,2) if x[0]!=x[1]])
    else:
        cond = 'True'
    def unique_constraint(*args):
        for var,val in zip(ops,args):
            locals()[var] = val
        return eval(cond)
    problem.addConstraint(unique_constraint,tuple(ops))
    solution = None
    count = 0
    while solution is None and count < 5:
        solution = problem.getSolution()
        count += 1
    if count == 5:
        return []
    else:
        return solution

class cross():
    '''
    A generator class to generate RISC-V assembly tests for a given instruction
    format, opcode and a set of coverpoints.

    :param fmt: the RISC-V instruction format type to be used for the test generation.
    :param opnode: dictionary node from the attributes YAML that is to be used in the test generation.
    :param opcode: name of the instruction opcode.
    :param randomization: a boolean variable indicating if the random constraint solvers must be employed.
    :param xl: an integer indicating the XLEN value to be used.
    :param base_isa_str: The base isa to be used for the tests. One of [rv32e,rv32i,rv64i]

    :type fmt: str
    :type opnode: dict
    :type opcode: str
    :type randomization: bool
    :type xl: int
    :type base_isa_str: str
    '''

    # Template dictionary
    OP_TEMPLATE = utils.load_yaml(const.template_file)
    
    def __init__(self, base_isa_str):
        '''
        This is a Constructor function which initializes various class variables
        depending on the arguments.

        The function also creates a dictionary of datasets for each operand. The
        dictionary basically indicates what registers from the register file are to be used
        when generating solutions for coverpoints. The datasets are limited to
        to reduce the time taken by solvers to arrive at a solution.

        A similar dictionary is created for the values to be used by the operand
        registers.

        '''
        global xlen
        global flen
        global base_isa

        base_isa = base_isa_str
       
    def cross_comb(cgf):
        '''
        This function finds solution for various cross-combinations defined by the coverpoints
        in the CGF under the `cross_comb` node of the covergroup.
        '''
        #logger.debug(self.opcode + ': Generating CrossComb')
        #solutions = []

        if 'cross_comb' in cgf:
            cross_comb = set(cgf['cross_comb'])
        else:
            return
        
        dntcare_instrs = isac_utils.import_instr_alias(base_isa + '_arith') + isac_utils.import_instr_alias(base_isa + '_shift')

        # This function retrieves available operands in a string
        def get_oprs(opr_str):
            opr_lst = []
            if opr_str.find('rd') != -1:
                opr_lst.append('rd')
            if opr_str.find('rs1') != -1:
                opr_lst.append('rs1')
            if opr_str.find('rs2') != -1:
                opr_lst.append('rs2')
            if opr_str.find('rs3') != -1:
                opr_lst.append('rs3')
            
            return opr_lst
            
        for each in cross_comb:
            parts = each.split('::')
        
            data = parts[0].replace(' ', '')[1:-1].split(':')
            assgn_lst = parts[1].replace(' ', '')[1:-1].split(':')
            cond_lst = parts[2].lstrip().rstrip()[1:-1].split(':')

            i = 0            
            problem = Problem()
            for i in range(len(data)):
                if data[i] == '?':
                    # When instruction is not specified,
                    #   - Gather conditions if any
                    #   - Choose instruction based on operands in condition list
                    #   - Generate assignments

                    # Get corresponding conditions and accordingly chose instruction
                    cond = cond_lst[i]
                    assgn = assgn_lst[i]
                    
                    if cond.find('?') != -1:                    # Don't care condition
                        
                        # Check variables in assignment list and generate required operand list
                        opr_lst = get_oprs(assgn)

                        # Get possible instructions based on the operand list
                        problem.reset()
                        problem.addVariable('i', dntcare_instrs)
                        problem.addConstraint(lambda i: all(item in OPS[cross.OP_TEMPLATE[i]['formattype']] for item in opr_lst))
                        instrs_sol = problem.getSolutions()
                        
                        instrs_sol = [list(each.items())[0][1] for each in instrs_sol]
                    
                    else:
                        
                        opr_lst = []
                        
                        # Extract required operands from condition list
                        opr_lst += get_oprs(cond)

                        # Extract required operands from assignment list
                        opr_lst += get_oprs(assgn)

                        # Remove redundant operands
                        opr_lst = list(set(opr_lst))

                        # Get possible instructions
                        problem.reset()
                        problem.addVariable('i', dntcare_instrs)
                        problem.addConstraint(lambda i: all(item in OPS[cross.OP_TEMPLATE[i]['formattype']] for item in opr_lst))
                        instrs_sol = problem.getSolutions()
                        
                        instrs_sol = [list(each.items())[0][1] for each in instrs_sol]

                    # Randomly choose an instruction
                    instr = random.choice(instrs_sol)
                    
                    # Choose operand values
                    formattype = cross.OP_TEMPLATE[instr]['formattype']
                    oprs = OPS[formattype]
                    instr_template = cross.OP_TEMPLATE[instr]
                    
                    problem.reset()
                    for opr in oprs:
                        opr_dom = instr_template[opr + '_op_data']
                        problem.addVariable(opr, eval(opr_dom))
                    
                    # Since rd = x0 is a trivial operation, it has to be excluded
                    if 'rd' in oprs:
                        # exclude zeros
                        def exc_rd_zero(*oprs_lst):
                            pos = oprs.index('rd')
                            if oprs_lst[pos] == 'x0':
                                return False
                            return True
                        
                        problem.addConstraint(exc_rd_zero, oprs)

                    # Add additional contraints if any
                    if cond.find('?') != -1:
                        opr_sols = problem.getSolutions()
                    else:
                        def add_cond(local_var):
                            def eval_conds(*oprs_lst):
                                i = 0
                                for opr in oprs:
                                    exec(opr + "='" +  oprs_lst[i] + "'", local_var)
                                    i = i + 1
                                return eval(cond, locals(), local_var)
                            return eval_conds

                        local_vars = locals()
                        problem.addConstraint(add_cond(local_vars), oprs)
                        opr_sols = problem.getSolutions()

                    opr_vals = random.choice(opr_sols)
                    
                    # Assign operand values to operands
                    for opr, val in opr_vals.items():
                        exec(opr + "='" + val + "'")

                    # Get assignments if any and execute them
                    if assgn_lst[i] != '?':
                        assgns = assgn_lst[i].split(';')
                        for each in assgns:
                            exec(each)
                    
                    print(instr)
                    print(opr_vals)

                else:
                    cond = cond_lst[i]
                    assgn = assgn_lst[i]
                    
                    # Gather required operands
                    opr_lst = get_oprs(cond)
                    opr_lst += get_oprs(assgn)

                    opr_lst = list(set(opr_lst))                  
                    
                    if data[i] in cross.OP_TEMPLATE:
                        instr = data[i]
                    else:
                        alias_instrs = isac_utils.import_instr_alias(data[i])
                        if alias_instrs:
                            problem.reset()
                            problem.addVariable('i', alias_instrs)
                            problem.addConstraint(lambda i: all(item in OPS[cross.OP_TEMPLATE[i]['formattype']] for item in opr_lst))
                            instrs_sol = problem.getSolutions()

                            instrs_sol = [list(each.items())[0][1] for each in instrs_sol]

                            # Randomly select an instruction
                            instr = random.choice(instrs_sol)
                            
                        else:
                            logger.error('Invalid instruction/alias in cross_comb: ' + each)
                    
                    formattype = cross.OP_TEMPLATE[instr]['formattype']
                    oprs = OPS[formattype]        
                    instr_template = cross.OP_TEMPLATE[instr]
                    
                    problem.reset()
                    for opr in oprs:
                        opr_dom = instr_template[opr + '_op_data']
                        problem.addVariable(opr, eval(opr_dom))
                    
                    # Since rd = x0 is a trivial operation, it has to be excluded
                    if 'rd' in oprs:
                        # exclude zeros
                        def exc_rd_zero(*oprs_lst):
                            pos = oprs.index('rd')
                            if oprs_lst[pos] == 'x0':
                                return False
                            return True
                        
                        problem.addConstraint(exc_rd_zero, oprs)

                    # Assign values to operands
                    if cond.find('?') != -1:
                        opr_sols = problem.getSolutions()
                    else:
                        def add_cond(local_var):
                            def eval_conds(*oprs_lst):
                                i = 0
                                for opr in oprs:
                                    exec(opr + "='" +  oprs_lst[i] + "'", local_var)
                                    i = i + 1
                                return eval(cond, locals(), local_var)
                            return eval_conds

                        local_vars = locals()
                        #problem.addConstraint(add_cond(local_vars), oprs)
                        opr_sols = problem.getSolutions()

                    # Get operand values
                    opr_vals = random.choice(opr_sols)

                    # Assign operand values to operands
                    for opr, val in opr_vals.items():
                        exec(opr + "='" + val + "'")

                    # Execute assignments
                    # Get assignments if any and execute them
                    if assgn_lst[i] != '?':
                        assgns = assgn_lst[i].split(';')
                        for each in assgns:
                            exec(each)

                    print(instr)
                    print(opr_vals)


if __name__ == '__main__':

    cross_cov = {'cross_comb' : {'[add : ? : mul : ? : rv32i_shift : sub ] :: [a = rd; a = rs1 : a=rd;a=rs1 : ? : ? : ?: ?] :: [? : rs1 != a and rd == a : rs1==a or rs2==a : ? : rs1==a or rs2==a: ?]  ' : 0}}
    cross_test = cross('rv32i')
    get_it = cross.cross_comb(cross_cov)