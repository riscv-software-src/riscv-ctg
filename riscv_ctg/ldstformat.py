from constraint import *
import random
import re
from riscv_ctg.constants import *

def ldstformat_opcomb(cgf, randomization):
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

        if len(rs1_range) == len(rs1_picked):
            opconstraint = lambda rs1,rd: True if rd not in rd_picked and rs1 != rd else False
        elif len(rd_range) == len(rd_picked):
            opconstraint = lambda rs1,rd: True if rs1 not in rs1_picked and rs1!= rd else False
        else:
            opconstraint = lambda rs1,rd: True if rs1 not in rs1_picked and rd not in rd_picked and rs1!= rd else False
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

def ldstformat_valcomb(cgf,op_node,randomization):
    val_comb = []
    rs1_val_data = eval(op_node['rs1_val_data'])
    imm_val_data = eval(op_node['imm_val_data'])
    size = eval(op_node['size'])
    def boundconstraint(rs1_val,imm_val):
        temp = rs1_val+imm_val-(imm_val+(-1 if imm_val>0 else 1)*(rs1_val%size))+size
        if temp>=0 and temp<=4:
            return True
        else:
            return False
    for req_val_comb in cgf['val_comb']:
        if randomization:
            problem = Problem(MinConflictsSolver())
        else:
            problem = Problem(RecursiveBacktrackingSolver())
        problem.addVariables(['rs1_val'], rs1_val_data)
        problem.addVariables(['imm_val'], imm_val_data)
        problem.addConstraint(lambda rs1_val, imm_val: eval(req_val_comb) ,\
                        ('rs1_val', 'imm_val'))
        problem.addConstraint(lambda rs1_val, imm_val: boundconstraint(rs1_val,imm_val)\
                        , ('rs1_val', 'imm_val'))

        solution = problem.getSolution()
        count = 0
        while (solution is None and count < 5):
            solution = problem.getSolution()
            count = count + 1
        if solution is None:
            print("Can't find a solution - 3")
            exit(0)
        print(solution)
        val_comb.append((str(solution['rs1_val']), str(solution['imm_val'])))
        problem.reset()
    return val_comb

def ldstformat_inst(op_comb, val_comb, cgf,op_node):

    instr_dict = []
    rs1_val_data = eval(op_node['rs1_val_data'])
    imm_val_data = eval(op_node['imm_val_data'])
    cont = []
    if len(op_comb) >= len(val_comb):
        for i in range(len(op_comb)):
            instr = {'index':'0'}
            instr['inst'] = cgf['opcode']
            instr['rd'] = op_comb[i][0]
            instr['rs1'] = op_comb[i][1]

            if i < len(val_comb):
                instr['rs1_val'] = val_comb[i][0]
                instr['imm_val'] = val_comb[i][1]
                if instr['rs1'] == 'x0' or instr['rd'] == 'x0':
                    cont.append(val_comb[i])
            elif cont:
                if instr['rs1'] == 'x0' or instr['rd'] == 'x0':
                    instr['rs1_val'] = str(random.choice(rs1_val_data))
                    instr['imm_val'] = str(random.choice(imm_val_data))
                else:
                    temp = cont.pop()
                    instr['rs1_val'] = temp[0]
                    instr['imm_val'] = temp[1]
            else:
                instr['rs1_val'] = '0'
                instr['imm_val'] = '0'
            instr_dict.append(instr)
    else:
        for i in range(len(val_comb)):
            instr = {'index':'0'}
            instr['inst'] = cgf['opcode']
            if i < len(op_comb):
                instr['rd'] = op_comb[i][0]
                instr['rs1'] = op_comb[i][1]

                if instr['rs1'] == 'x0' or instr['rd'] == 'x0':
                    cont.append(val_comb[i])
            else:
                instr['rd'] =  'x' + str(random.randint(1,31))
                instr['rs1'] =  'x' + str(random.randint(1,31))
            instr['rs1_val'] = val_comb[i][0]
            instr['imm_val'] = val_comb[i][1]
            instr_dict.append(instr)
    for entry in cont:
            instr = {'index':'0'}
            instr['inst'] = cgf['opcode']
            instr['rd'] =  'x' + str(random.randint(1,31))
            instr['rs1'] =  'x' + str(random.randint(1,31))
            instr['rs1_val'] = entry[0]
            instr['imm_val'] = entry[1]
            instr_dict.append(instr)
    return instr_dict

def ldstformat_swreg(instr_dict):
    total_instr = len(instr_dict)
    available_reg = default_regset.copy()
    available_reg.remove('x0')
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

def ldstformat_testreg(instr_dict):
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

def ldstformat_correct_val(instr_dict, op_node):
    return instr_dict



