from constraint import *
import random
import re
from riscv_ctg.constants import *

def jformat_opcomb(cgf,randomization):
    rd_picked = []
    op_comb = []
    if 'rd' in cgf:
        rd_range = list(cgf['rd'].keys())
    variables = ['rd']

    combination_num = len(rd_range)
    rd_picked = []

    for i in range(combination_num):
        if randomization:
            problem = Problem(MinConflictsSolver())
        else:
            problem = Problem()


        problem.addVariable('rd', rd_range)

        opconstraint = lambda rd: True if rd not in rd_picked else False
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
        op_comb.append( tuple(op_tuple) )
        rd_picked.append(solution['rd'])
        problem.reset()

    if 'op_comb' in cgf:
        rd_range = default_regset.copy()

        for req_op_comb in cgf['op_comb']:
            satisfied = False
            for comb in op_comb:
                rd = comb[0]
                if eval(req_op_comb):
                    satisfied = True
                    break;
            if not satisfied:
                if randomization:
                    problem = Problem(MinConflictsSolver())
                else:
                    problem = Problem()
                problem.addVariable('rd', rd_range)
                problem.addConstraint(lambda rd: eval(req_op_comb) ,\
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
                op_comb.append( tuple(op_tuple) )
                problem.reset()

    return op_comb

def jformat_valcomb(cgf, op_node, randomization):
    val_comb = []
    imm_val_data = eval(op_node['imm_val_data'])
    for req_val_comb in cgf['val_comb']:
        if randomization:
            problem = Problem(MinConflictsSolver())
        else:
            problem = Problem()
        problem.addVariable('imm_val', imm_val_data)
        problem.addConstraint(lambda imm_val: eval(req_val_comb) ,\
                        tuple(['imm_val']))
        solution = problem.getSolution()
        count = 0
        while (solution != {} and count < 5):
            solution = problem.getSolution()
            count+=1
        if solution is None:
            print("Can't find a solution - 3")
            exit(0)
        val_comb.append((str(solution['imm_val'])))
        problem.reset()
    return val_comb

def jformat_inst(op_comb, val_comb, cgf, op_node):
    instr_dict = []
    imm_val_data = eval(op_node['imm_val_data'])
    cont = []
    regs = list(range(1,31))
    labelize = lambda x: (str((-x)%2**21),'1b') if x < 0 else (str((x%2**21)),'3f')
    if len(op_comb) >= len(val_comb):
        for i in range(len(op_comb)):
            instr = {}
            instr['inst'] = cgf['opcode']
            instr['rd'] = op_comb[i][0]

            if i < len(val_comb):
                instr['imm_val'], instr['label'] = labelize(int(val_comb[i]))
                if instr['rd'] == 'x0':
                    cont.append(val_comb[i])
            elif cont:
                if instr['rd'] == 'x0':
                    instr['imm_val'], instr['label'] = 0,'1b'
                else:
                    temp = cont.pop()
                    instr['imm_val'], instr['label'] = labelize(int(temp[i]))
            else:
                instr['label'] = '3f'
                instr['imm_val'] = '0'
            instr_dict.append(instr)
    else:
        for i in range(len(val_comb)):
            instr = {}
            instr['inst'] = cgf['opcode']
            if i < len(op_comb):
                instr['rd'] = op_comb[i][0]

                if instr['rd'] == 'x0':
                    cont.append(val_comb[i])
            else:
                instr['rd'] =  'x' + str(random.randint(1,31))
            instr['imm_val'], instr['label'] = labelize(int(val_comb[i]))
            instr_dict.append(instr)
    for entry in cont:
            instr = {}
            instr['inst'] = cgf['opcode']
            instr['rd'] =  'x' + str(random.randint(1,31))
            instr['imm_val'], instr['label'] = labelize(int(entry))
            instr_dict.append(instr)
    return instr_dict

def jformat_swreg(instr_dict):
    total_instr = len(instr_dict)
    available_reg = default_regset.copy()
    available_reg.remove('x0')
    count = 0
    assigned = 0
    offset = 0
    for instr in instr_dict:
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

def jformat_testreg(instr_dict):
    total_instr = len(instr_dict)
    available_reg = default_regset.copy()
    available_reg.remove('x0')
    count = 0
    assigned = 0
    for instr in instr_dict:
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

def jformat_correct_val(instr_dict, op_node):
    return instr_dict


