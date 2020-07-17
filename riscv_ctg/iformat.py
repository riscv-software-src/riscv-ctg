from constraint import *
import random
import re
from riscv_ctg.constants import *

def iformat_opcomb(cgf, randomization):
    rs1_picked = []
    rd_picked = []
    op_comb = []
    if 'rs1' in cgf:
        rs1_range = cgf['rs1']
    else:
        rs1_range = ['x'+str(random.randint(1,31))]
    if 'rd' in cgf:
        rd_range = cgf['rd']
    else:
        rd_range = ['x'+str(random.randint(1,31))]
    variables = ['rs1', 'rd']

    combination_num = max(len(rs1_range), len(rd_range))
    rs1_picked = []
    rd_picked = []

    for i in range(combination_num):
        if randomization:
            problem = Problem(MinConflictsSolver())
        else:
            problem = Problem()

        problem.addVariable('rs1', rs1_range)
        problem.addVariable('rd',  rd_range)

        def opconstraint(rs1=0, rd=0):
            if rs1 not in rs1_picked and rd not in rd_picked\
                    and rs1 != rd :
                return True

        problem.addConstraint(opconstraint, variables)

        count = 0
        solution = problem.getSolution()
        while (solution is None and count < 5):
            solution = problem.getSolution()
            count = count + 1
        if solution is None:
            print("Can't find a solution - 1")
            exit(0)

        op_tuple = []
        op_tuple.append(solution['rd'])
        op_tuple.append(solution['rs1'])
        op_comb.append( tuple(op_tuple) )
        rs1_picked.append(solution['rs1'])
        rd_picked.append(solution['rd'])
        problem.reset()

    if 'op_comb' in cgf:
        rs1_range = default_regset.copy()
        rd_range = default_regset.copy()

        for req_op_comb in cgf['op_comb']:
            satisfied = False
            for comb in op_comb:
                rd = comb[0]
                rs1 = comb[1]
                if eval(req_op_comb):
                    satisfied = True
                    break;
            if not satisfied:
                if randomization:
                    problem = Problem(MinConflictsSolver())
                else:
                    problem = Problem()
                problem.addVariable('rs1', rs1_range)
                problem.addVariable('rd', rd_range)
                problem.addConstraint(lambda rs1, rd: eval(req_op_comb) ,\
                        tuple(variables))
                count = 0
                solution = problem.getSolution()
                while (solution is None and count < 5):
                    solution = problem.getSolution()
                    count = count + 1
                if solution is None:
                    print("Can't find a solution - 2")
                    exit(0)
                op_tuple = []
                op_tuple.append(solution['rd'])
                op_tuple.append(solution['rs1'])
                op_comb.append( tuple(op_tuple) )
                problem.reset()
    return op_comb

def iformat_valcomb(cgf,op_node,randomization):
    val_comb = []
    for req_val_comb in cgf['val_comb']:
        print(req_val_comb)
        if randomization:
            problem = Problem(MinConflictsSolver())
        else:
            problem = Problem(RecursiveBacktrackingSolver())
        problem.addVariables(['rs1_val'], list(range(-50, 50))+[-2**(xlen-1),2**(xlen-1)-1])
        problem.addVariables(['imm_val'], list(range(-5, 5))+[-2**11,(2**11)-1])
        problem.addConstraint(lambda rs1_val, imm_val: eval(req_val_comb) ,\
                        ('rs1_val', 'imm_val'))
        solution = problem.getSolution()
        count = 0
        while (solution is None and count < 5):
            solution = problem.getSolution()
            count = count + 1
        if solution is None:
            print("Can't find a solution - 3")
            exit(0)
        val_comb.append((str(solution['rs1_val']), str(solution['imm_val'])))
        problem.reset()
    return val_comb

def iformat_inst(op_comb, val_comb, cgf,op_node):
    instr_dict = []
    if len(op_comb) >= len(val_comb):
        for i in range(len(op_comb)):
            instr = {}
            instr['inst'] = cgf['opcode']
            instr['rd'] = op_comb[i][0]
            instr['rs1'] = op_comb[i][1]

            if i < len(val_comb):
                instr['rs1_val'] = val_comb[i][0]
                instr['imm_val'] = val_comb[i][1]
            else:
                instr['rs1_val'] = str(random.randint(-2**32, 2**32))
                instr['imm_val'] = str(random.randint(-2**12, 2**12))
            instr_dict.append(instr)
    else:
        for i in range(len(val_comb)):
            instr = {}
            instr['inst'] = cgf['opcode']
            if i < len(op_comb):
                instr['rd'] = op_comb[i][0]
                instr['rs1'] = op_comb[i][1]
            else:
                instr['rd'] =  'x' + str(random.randint(1,31))
                instr['rs1'] = 'x' + str(random.randint(1,31))
            instr['rs1_val'] = val_comb[i][0]
            instr['imm_val'] = val_comb[i][1]
            instr_dict.append(instr)
    return instr_dict

def iformat_swreg(instr_dict):
    total_instr = len(instr_dict)
    available_reg = default_regset.copy()
    available_reg.remove('x1')
    count = 0
    assigned = 0
    offset = 0
    for instr in instr_dict:
        if instr['rs1'] in available_reg:
            available_reg.remove(instr['rs1'])
        if instr['rd'] in available_reg:
            available_reg.remove(instr['rd'])

        if len(available_reg) <= 3:
            curr_swreg = available_reg[0]
            offset = 0
            for i in range(assigned, count+1):
                if 'swreg' not in instr_dict[i]:
                    instr_dict[i]['swreg'] = curr_swreg
                    instr_dict[i]['offset'] = str(offset)
                    offset += 4
                    assigned += 1

            available_reg = default_regset.copy()
            available_reg.remove('x0')
        count += 1
    if assigned != total_instr and len(available_reg) != 0:
        curr_swreg = available_reg[0]
        offset = 0
        for i in range(len(instr_dict)):
            if 'swreg' not in instr_dict[i]:
                instr_dict[i]['swreg'] = curr_swreg
                instr_dict[i]['offset'] = str(offset)
                offset += 4
    return instr_dict

def iformat_testreg(instr_dict):
    total_instr = len(instr_dict)
    available_reg = default_regset.copy()
    available_reg.remove('x0')
    count = 0
    assigned = 0
    for instr in instr_dict:
        if instr['rs1'] in available_reg:
            available_reg.remove(instr['rs1'])
        if instr['rd'] in available_reg:
            available_reg.remove(instr['rd'])
        if instr['swreg'] in available_reg:
            available_reg.remove(instr['swreg'])

        if len(available_reg) <= 3:
            curr_testreg = available_reg[0]
            for i in range(assigned, count+1):
                if 'testreg' not in instr_dict[i]:
                    instr_dict[i]['testreg'] = curr_testreg
                    assigned += 1
            available_reg = default_regset.copy()
            available_reg.remove('x0')
        count += 1
    if assigned != total_instr and len(available_reg) != 0:
        curr_testreg = available_reg[0]
        for i in range(len(instr_dict)):
            if 'testreg' not in instr_dict[i]:
                instr_dict[i]['testreg'] = curr_testreg
    return instr_dict

def iformat_correct_val(instr_dict, op_node):
    for i in range(len(instr_dict)):
        rs1_val = int(instr_dict[i]['rs1_val'])
        imm_val = int(instr_dict[i]['imm_val'])
        correctval = eval(op_node['operation'])
        instr_dict[i]['correctval'] = str(correctval)
    return instr_dict



