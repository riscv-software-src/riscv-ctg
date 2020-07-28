from constraint import *
import random
import re
from riscv_ctg.constants import *

def bformat_opcomb(cgf,randomization):
    rs1_picked = []
    rs2_picked = []
    op_comb = []
    if 'rs1' in cgf:
        rs1_range = list(cgf['rs1'].keys())
    else:
        rs1_range = ['x'+str(random.randint(1,31))]
    if 'rs2' in cgf:
        rs2_range = list(cgf['rs2'].keys())
    else:
        rs2_range = ['x'+str(random.randint(1,31))]
    variables = ['rs1', 'rs2']

    combination_num = max(len(rs1_range), len(rs2_range))
    rs1_picked = []
    rs2_picked = []

    for i in range(combination_num):
        if randomization:
            problem = Problem(MinConflictsSolver())
        else:
            problem = Problem()


        problem.addVariable('rs1', rs1_range)
        problem.addVariable('rs2', rs2_range)

        def opconstraint(rs1=0, rs2=0):
            if rs1 not in rs1_picked and rs2 not in rs2_picked and rs1 != rs2:
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
        op_tuple.append(solution['rs1'])
        op_tuple.append(solution['rs2'])
        op_comb.append( tuple(op_tuple) )
        rs1_picked.append(solution['rs1'])
        rs2_picked.append(solution['rs2'])
        problem.reset()

    if 'op_comb' in cgf:
        rs1_range = default_regset.copy()
        rs2_range = default_regset.copy()

        for req_op_comb in cgf['op_comb']:
            satisfied = False
            for comb in op_comb:
                rs1 = comb[0]
                rs2 = comb[1]
                if eval(req_op_comb):
                    satisfied = True
                    break;
            if not satisfied:
                if randomization:
                    problem = Problem(MinConflictsSolver())
                else:
                    problem = Problem()
                problem.addVariable('rs1', rs1_range)
                problem.addVariable('rs2', rs2_range)
                problem.addConstraint(lambda rs1, rs2: eval(req_op_comb) ,\
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
                op_tuple.append(solution['rs1'])
                op_tuple.append(solution['rs2'])
                op_comb.append( tuple(op_tuple) )
                problem.reset()

    return op_comb

def bformat_valcomb(cgf, op_node, randomization):
    val_comb = []
    rs1_val_data = eval(op_node['rs1_val_data'])
    rs2_val_data = eval(op_node['rs2_val_data'])
    imm_val_data = eval(op_node['imm_val_data'])
    for req_val_comb in cgf['val_comb']:
        if randomization:
            problem = Problem(MinConflictsSolver())
        else:
            problem = Problem()
        problem.addVariable('rs1_val', rs1_val_data)
        problem.addVariable('rs2_val', rs2_val_data)
        problem.addVariable('imm_val', imm_val_data)
        problem.addConstraint(lambda rs1_val, rs2_val, imm_val: eval(req_val_comb) ,\
                        ('rs1_val', 'rs2_val', 'imm_val'))
        solution = problem.getSolution()
        count = 0
        while (solution != {} and count < 5):
            solution = problem.getSolution()
            count+=1
        if solution is None:
            print("Can't find a solution - 3")
            exit(0)
        val_comb.append((str(solution['rs1_val']), str(solution['rs2_val']), str(solution['imm_val'])))
        problem.reset()
    return val_comb

def bformat_inst(op_comb, val_comb, cgf, op_node):
    instr_dict = []
    rs1_val_data = eval(op_node['rs1_val_data'])
    rs2_val_data = eval(op_node['rs2_val_data'])
    imm_val_data = eval(op_node['imm_val_data'])
    cont = []
    regs = list(range(1,31))
    labelize = lambda x: (str((-x)%2048),'1b') if x < 0 else (str((x%2048)),'3f')
    if len(op_comb) >= len(val_comb):
        for i in range(len(op_comb)):
            instr = {}
            instr['inst'] = cgf['opcode']
            instr['rs1'] = op_comb[i][0]
            instr['rs2'] = op_comb[i][1]

            if i < len(val_comb):
                instr['rs1_val'] = val_comb[i][0]
                instr['rs2_val'] = val_comb[i][1]
                instr['imm_val'], instr['label'] = labelize(int(val_comb[i][2]))
                if instr['rs1'] == 'x0' or instr['rs2'] == 'x0' or instr['rs1'] == instr['rs2']:
                    cont.append(val_comb[i])
            elif cont:
                if instr['rs1'] == 'x0' or instr['rs2'] == 'x0' or instr['rs1'] == instr['rs2']:
                    instr['rs1_val'] = str(random.choice(rs1_val_data))
                    instr['rs2_val'] = str(random.choice(rs2_val_data))
                else:
                    temp = cont.pop()
                    instr['rs1_val'] = temp[0]
                    instr['rs2_val'] = temp[1]
                    instr['imm_val'], instr['label'] = labelize(int(temp[i][2]))
            else:
                instr['rs1_val'] = str(random.choice(rs1_val_data))
                instr['rs2_val'] = str(random.choice(rs2_val_data))
                instr['label'] = '3f'
                instr['imm_val'] = '0'
            instr_dict.append(instr)
    else:
        for i in range(len(val_comb)):
            instr = {}
            instr['inst'] = cgf['opcode']
            if i < len(op_comb):
                instr['rs1'] = op_comb[i][0]
                instr['rs2'] = op_comb[i][1]

                if instr['rs1'] == 'x0' or instr['rs2'] == 'x0' or instr['rs1'] == instr['rs2']:
                    cont.append(val_comb[i])
            else:
                instr['rs1'] =  'x' + str(random.randint(1,31))
                instr['rs2'] =  'x' + str(random.randint(1,31))
                while instr['rs1'] == instr['rs2']:
                    instr['rs2'] =  'x' + str(random.randint(1,31))
            instr['rs1_val'] = val_comb[i][0]
            instr['rs2_val'] = val_comb[i][1]
            instr['imm_val'], instr['label'] = labelize(int(val_comb[i][2]))
            instr_dict.append(instr)
    for entry in cont:
            instr = {}
            instr['inst'] = cgf['opcode']
            instr['rs1'] =  'x' + str(random.randint(1,31))
            instr['rs2'] =  'x' + str(random.randint(1,31))
            while instr['rs1'] == instr['rs2']:
                instr['rs2'] =  'x' + str(random.randint(1,31))
            instr['rs1_val'] = entry[0]
            instr['rs2_val'] = entry[1]
            instr['imm_val'], instr['label'] = labelize(int(entry[2]))
            instr_dict.append(instr)
    return instr_dict

def bformat_swreg(instr_dict):
    total_instr = len(instr_dict)
    available_reg = default_regset.copy()
    available_reg.remove('x0')
    count = 0
    assigned = 0
    offset = 0
    for instr in instr_dict:
        if instr['rs1'] in available_reg:
            available_reg.remove(instr['rs1'])
        if instr['rs2'] in available_reg:
            available_reg.remove(instr['rs2'])

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

def bformat_testreg(instr_dict):
    total_instr = len(instr_dict)
    available_reg = default_regset.copy()
    available_reg.remove('x0')
    count = 0
    assigned = 0
    for instr in instr_dict:
        if instr['rs1'] in available_reg:
            available_reg.remove(instr['rs1'])
        if instr['rs2'] in available_reg:
            available_reg.remove(instr['rs2'])
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

def bformat_correct_val(instr_dict, op_node):
    return instr_dict


