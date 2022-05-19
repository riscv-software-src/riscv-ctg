# See LICENSE.incore for details
import random
from constraint import *

import riscv_isac.utils as isac_utils
from riscv_ctg.constants import *
from riscv_ctg.log import logger
import riscv_ctg.utils as utils
import riscv_ctg.constants as const

from riscv_ctg.dsp_function import *

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

class cross():
    '''
    A cross class to genereate RISC-V assembly tests for cross-combination coverpoints.
    '''

    # Template dictionary
    OP_TEMPLATE = utils.load_yaml(const.template_file)
    
    def __init__(self, base_isa_str, xlen_in):
        global xlen
        global flen
        global base_isa
        
        xlen = xlen_in
        base_isa = base_isa_str
       
    def cross_comb(cgf):
        '''
        This function finds solution for various cross-combinations defined by the coverpoints
        in the CGF under the `cross_comb` node of the covergroup.
        '''
        logger.debug('Generating CrossComb')
        full_solution = []
        
        if 'cross_comb' in cgf:
            cross_comb = set(cgf['cross_comb'])
        else:
            return
        
        # Generate register file and variables
        reg_file = ['x'+str(x) for x in range(0,32 if 'e' not in base_isa else 16)]
        for each in reg_file:
            exec(f"{each} = '{each}'")

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

        # Add conditions mentioned in the condition list in the cross-comb coverpoint
        def add_cond(local_var):
            def eval_conds(*oprs_lst):
                i = 0
                for opr in oprs:
                    exec(opr + "='" +  oprs_lst[i] + "'", local_var)
                    i = i + 1
                return eval(cond, locals(), local_var)
            return eval_conds

        solution = []
        for each in cross_comb:
            print('')
            print(each)

            solution = []

            # Parse cross-comb coverpoint
            parts = each.split('::')

            data = parts[0].replace(' ', '')[1:-1].split(':')
            assgn_lst = parts[1].replace(' ', '')[1:-1].split(':')
            cond_lst = parts[2].lstrip().rstrip()[1:-1].split(':')
            
            # Initialize CSP
            problem = Problem()
            
            for i in range(len(data)):
                if data[i] == '?':
                    # When instruction is not specified,
                    #   - Gather conditions and assigngments if any and list requisite operands
                    #   - Choose instruction from base instruction set based on operands
                    #   - Based on conditions, choose operand values. Choose immediate value if required  
                    #   - Evaluate assignments

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
                    
                    else:                                       # If condition is specified
                        
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
                    
                    # Choose register values
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
                        local_vars = locals()
                        problem.addConstraint(add_cond(local_vars), oprs)
                        opr_sols = problem.getSolutions()

                    opr_vals = random.choice(opr_sols)

                    # Assign operand values to operands
                    for opr, val in opr_vals.items():
                        exec(opr + "='" + val + "'")

                    # Generate immediate value if required
                    if 'imm_val_data' in instr_template:
                        imm_val = eval(instr_template['imm_val_data'])
                        opr_vals['imm_val'] = random.choice(imm_val)

                    # Get assignments if any and execute them
                    if assgn_lst[i] != '?':
                        assgns = assgn_lst[i].split(';')
                        for each in assgns:
                            exec(each)
                    
                    solution += [instr, opr_vals]
                    print([instr, opr_vals])

                else:
                    # When instruction(s)/alias is specified,
                    #   - If an instruction is specified, operands are directly extracted and assigned values according to conditions 
                    #   - If a tuple of instructions is specified, one of the instruction is chosen at random
                    #   - If an alias is specified, the instruction is chosen according to assignment and condition list
                    #   - Immediate values are generated if required  
                    #   - Assignments are evaluated
                    cond = cond_lst[i]
                    assgn = assgn_lst[i]
                    
                    # Gather required operands
                    opr_lst = get_oprs(cond)
                    opr_lst += get_oprs(assgn)

                    opr_lst = list(set(opr_lst))                  

                    if data[i] in cross.OP_TEMPLATE:                                    # If single instruction
                        instr = data[i]
                    else:
                        alias_instrs = isac_utils.import_instr_alias(data[i])           # If data is an alias
                        if alias_instrs:
                            problem.reset()
                            problem.addVariable('i', alias_instrs)
                            problem.addConstraint(lambda i: all(item in OPS[cross.OP_TEMPLATE[i]['formattype']] for item in opr_lst))
                            instrs_sol = problem.getSolutions()

                            instrs_sol = [list(each.items())[0][1] for each in instrs_sol]

                            # Randomly select an instruction
                            instr = random.choice(instrs_sol)
                        
                        elif data[i].find('(') != -1:                                   # If data is a tuple of instructions
                            instrs_sol = data[i][1:-1].split(',')
                            instr = random.choice(instrs_sol)
                        else:
                            logger.error('Invalid instruction/alias in cross_comb: ' + each)
                    
                    # Gather operands
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
                        local_vars = locals()
                        problem.addConstraint(add_cond(local_vars), oprs)
                        opr_sols = problem.getSolutions()

                    # Get operand values
                    opr_vals = random.choice(opr_sols)

                    # Assign operand values to operands
                    for opr, val in opr_vals.items():
                        exec(opr + "='" + val + "'")

                    # Generate immediate value if required
                    if 'imm_val_data' in instr_template:
                        imm_val = eval(instr_template['imm_val_data'])
                        opr_vals['imm_val'] = random.choice(imm_val)

                    # Execute assignments
                    # Get assignments if any and execute them
                    if assgn_lst[i] != '?':
                        assgns = assgn_lst[i].split(';')
                        for each in assgns:
                            exec(each)

                    solution += [instr, opr_vals]
                    print([instr, opr_vals])
        
            full_solution += [solution]
        
        return full_solution

if __name__ == '__main__':

    cross_cov = {'cross_comb' : {'[(add,sub) : (add,sub) ] :: [a=rd : ? ] :: [? : rs1==a or rs2==a]' : 0,                                                                   # RAW
                                '[(add,sub) : ? : (add,sub) ] :: [a=rd : ? : ? ] :: [rd==x10 : rd!=a and rs1!=a and rs2!=a : rs1==a or rs2==a ]': 0,                        # RAW
                                '[add : ? : ? : ? : sub] :: [a=rd : ? : ? : ? : ?] :: [? : ? : ? : ? : rd==a]': 0,                                                          # WAW
                                '[(add,sub) : ? : mul : ? : (add,sub)] :: [a=rd : ? : ? : ? : ?] :: [? : rs1==a or rs2==a : rs1==a or rs2==a : rs1==a or rs2==a : rd==a]': 0, # WAW
                                '[(add,sub) : (add,sub) ] :: [a=rs1; b=rs2 : ? ] :: [? : rd==a or rd==b]': 0                                                                # WAR
                                }
                }
    cross_test = cross('rv32i', 32)
    get_it = cross.cross_comb(cross_cov)
    print(get_it)