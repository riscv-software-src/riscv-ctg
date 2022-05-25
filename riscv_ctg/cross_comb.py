# See LICENSE.incore for details
import time
import random
from constraint import *

import riscv_isac.utils as isac_utils

import riscv_ctg.utils as utils
import riscv_ctg.constants as const
from riscv_ctg.constants import *
from riscv_ctg.log import logger
from riscv_ctg.__init__ import __version__
from riscv_ctg.generator import OPS
from riscv_ctg.dsp_function import *

INSTR_FORMAT = {
    'rformat': '$instr $rd, $rs1, $rs2',
    'iformat': '$instr $rd, $rs1, $imm_val'
}

REG_INIT = '''
LI (x1,  (0xFEEDBEADFEEDBEAD & MASK));
LI (x2,  (0xFF76DF56FF76DF56 & MASK));
LI (x3,  (0x7FBB6FAB7FBB6FAB & MASK));
LI (x4,  (0xBFDDB7D5BFDDB7D5 & MASK));
LA (x5,  (0xAB7FFB6FAB7FBB6F & MASK));
LA (x6,  (0x6FAB71BB6F7B7FBB & MASK));
LI (x7,  (0xB7FBB6FAB7FBB6FA & MASK));
LI (x8,  (0x5BFDDB7D5BFDDB7D & MASK));
LI (x9,  (0xADFEEDBEADFEEDBE & MASK));
LI (x10, (0x56FF76DF56FF76DF & MASK));
LI (x11, (0xAB7FBB6FAB7FBB6F & MASK));
LI (x12, (0xD5BFDDB7D5BFDDB7 & MASK));
LI (x13, (0xEADFEEDBEADFEEDB & MASK));
LI (x14, (0xF56FF76DF56FF76D & MASK));
LI (x15, (0xFAB7FBB6FAB7FBB6 & MASK));
#ifndef RVTEST_E
LI (x16, (0x7D5BFDDB7D5BFDDB & MASK));
LI (x17, (0xBEADFEEDBEADFEED & MASK));
LI (x18, (0xDF56FF76DF56FF76 & MASK));
LI (x19, (0x6FAB7FBB6FAB7FBB & MASK));
LI (x20, (0xB7D5BFDDB7D5BFDD & MASK));
LI (x21, (0xDBEADFEEDBEADFEE & MASK));
LI (x22, (0x6DF56FF76DF56FF7 & MASK));
LI (x23, (0xB6FAB7FBB6FAB7FB & MASK));
LI (x24, (0xDB7D5BFDDB7D5BFD & MASK));
LI (x25, (0xEDBEADFEEDBEADFE & MASK));
LI (x26, (0x76DF56FF76DF56FF & MASK));
LI (x27, (0xBB6FAB7FBB6FAB7F & MASK));
LI (x28, (0xDDB7D5BFDDB7D5BF & MASK));
LI (x29, (0xEEDBEADFEEDBEADF & MASK));
LI (x30, (0xF76DF56FF76DF56F & MASK));
LI (x31, (0xFBB6FAB7FBB6FAB7 & MASK));
#endif
'''

class cross():
    '''
    A cross class to genereate RISC-V assembly tests for cross-combination coverpoints.
    '''

    # Template dictionary
    OP_TEMPLATE = utils.load_yaml(const.template_file)
    
    def __init__(self, base_isa_str, xlen_in, randomize, label):
        global xlen
        global flen
        global base_isa
        
        xlen = xlen_in
        base_isa = base_isa_str

        self.randomize = randomize
        self.label = label
       
    def cross_comb(self, cgf_node):
        '''
        This function finds solution for various cross-combinations defined by the coverpoints
        in the CGF under the `cross_comb` node of the covergroup.
        '''
        logger.debug('Generating CrossComb')
        full_solution = []
        
        if 'cross_comb' in cgf_node:
            cross_comb = set(cgf_node['cross_comb'])
        else:
            return
        
        isa_set = []

        # Generate register file and variables
        reg_file = const.default_regset
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

            solution = []

            # Parse cross-comb coverpoint
            parts = each.split('::')

            data = parts[0].replace(' ', '')[1:-1].split(':')
            assgn_lst = parts[1].replace(' ', '')[1:-1].split(':')
            cond_lst = parts[2].lstrip().rstrip()[1:-1].split(':')
            
            # Initialize CSP
            if self.randomize:
                problem = Problem(MinConflictsSolver)
            else:
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
                    isa_set += (cross.OP_TEMPLATE[instr]['isa'])

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
                    
                    opr_vals['instr'] = instr
                    solution += [opr_vals]

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
                    
                    isa_set += (cross.OP_TEMPLATE[instr]['isa'])
                    opr_vals['instr'] = instr
                    solution += [opr_vals]
        
            full_solution += [solution]
        
        self.isa = list(set(isa_set))
        return full_solution

    def swreg(cross_comb_instrs):
        '''
        This function generates the register which can be used as a signature pointer for each instruction
        '''

        global base_isa
        
        op_vals = ['x0']
        
        for instr_dict in cross_comb_instrs:
            for key, val in instr_dict.items():
                if key != 'instr' and key != 'imm_val':
                    op_vals += val

        problem = Problem()
        problem.addVariable('o', ['x'+str(x) for x in range(0,32 if 'e' not in base_isa else 16)])
        problem.addConstraint(lambda op: op not in op_vals)

        swreg_sol = problem.getSolutions()
        swreg_sol = [list(each.items())[0][1] for each in swreg_sol]

        sreg = random.choice(swreg_sol)

        return sreg

    def write_test(self, fprefix, cgf_node, usage_str, cov_label, full_solution):
        
        code = '\n'
        data = [".align 4","rvtest_data:",".word 0xbabecafe", \
                ".word 0xabecafeb", ".word 0xbecafeba", ".word 0xecafebab"]
        sig = ['']
        sreg_dict = dict()

        # Generate ISA and extension string
        extension = ""
        rvxlen = "RV"+str(xlen)
        op_node_isa = ",".join([rvxlen + isa for isa in self.isa])
        op_node_isa = op_node_isa.replace("I","E") if 'e' in base_isa else op_node_isa
        extension = op_node_isa.replace('I',"").replace('E',"")

        # Handle solutions related to each cross combination coverpoint
        for cross_sol in full_solution:
            
            # Designate signature update register
            sreg = cross.swreg(cross_sol)
            
            # Designate count of sreg for signature label generation
            if sreg not in sreg_dict:
                sreg_dict[sreg] = 0
            else:
                count = sreg_dict[sreg] + 1
                sreg_dict[sreg] = count
            
            sig_label = "signature_" + sreg + "_" + str(sreg_dict[sreg])
            code = code + "\nRVTEST_SIGBASE(" + sreg + ", "+ sig_label + ")\n\n"
            
            rd_lst = set()
            # Generate instruction corresponding to each instruction dictionary
            # Append signature update statements to store rd value after each instruction
            code += '// Cross-combination test sequence\n'
            for each in cross_sol:
                
                if 'rd' in each:
                    rd_lst.add(each['rd'])

                instr_str_format = Template(INSTR_FORMAT[cross.OP_TEMPLATE[each['instr']]['formattype']])
                instr_str = instr_str_format.substitute(each)
                code = code + instr_str + '\n'
            
            # Append .fill assembly directives to initialize signature regions
            sig.append(sig_label + ':\n\t.fill ' + str(len(rd_lst)) + ', 4, 0xdeadbeef\n')

            offset = 0
            code += '\n// Store destination register values in the test signature region\n'    
            # Add signature update statement(s) for unique number of rds
            for rd in rd_lst:        
                sig_upd = f'RVTEST_SIGUPD({sreg}, {rd}, {offset})'
                offset = offset + int(xlen/8)
                code = code + sig_upd + '\n'
            
            # Initialize registers for next cross-comb coverpoint
            code = code + REG_INIT

        case_str = ''.join([case_template.safe_substitute(xlen = xlen,num = i, cond = cond, cov_label = cov_label) for i, cond in enumerate(cgf_node['config'])])
        test = part_template.safe_substitute(case_str = case_str, code = code)
        
        # Write test to file
        with open(fprefix + f'/{cov_label}_cross-comb.S', 'w') as fp:
            fp.write(usage_str + const.cross_test_template.safe_substitute(opcode = cov_label,
                                                        isa = op_node_isa, 
                                                        test = test, 
                                                        data = '\n'.join(data), 
                                                        sig = '\n'.join(sig),
                                                        label = cov_label,
                                                        extension = extension
                                                        )
                    )
                
if __name__ == '__main__':

    cov_node = 'add'
    isa = 'RV32I'
    cgf_arg = '/path/to/cgf/'
    rand_arg = True
    xlen = 32
    fprefix = '.'
    node = {'config': {'check ISA:=regex(.*I.*)'},
            'cross_comb' : {'[(add,sub) : (add,sub) ] :: [a=rd : ? ] :: [? : rs1==a or rs2==a]' : 0,                                                                     # RAW
                            '[(add,sub) : ? : (add,sub) ] :: [a=rd : ? : ? ] :: [rd==x10 : rd!=a and rs1!=a and rs2!=a : rs1==a or rs2==a ]': 0,                          # RAW
                            '[add : ? : rv32i_shift : ? : sub] :: [a=rd : ? : ? : ? : ?] :: [? : ? : ? : ? : rd==a]': 0,                                                  # WAW
                            '[(add,sub) : ? : mul : ? : (add,sub)] :: [a=rd : ? : ? : ? : ?] :: [? : rs1==a or rs2==a : rs1==a or rs2==a : rs1==a or rs2==a : rd==a]': 0, # WAW
                            '[(add,sub) : (add,sub) ] :: [a=rs1; b=rs2 : ? ] :: [? : rd==a or rd==b]': 0                                                                  # WAR
                            }
            }
    
    mytime = time.asctime(time.gmtime(time.time()) ) + ' GMT'
    usage_str = const.usage.safe_substitute(version = __version__, 
                                                time = mytime,
                                                xlen = xlen,
                                                cgf = cgf_arg,
                                                randomize = rand_arg
                                                )
    
    cross_test = cross('rv32i', 32, False, cov_node)
    full_solution = cross_test.cross_comb(node)
    cross_test.write_test(fprefix, node, usage_str, cov_node, full_solution)