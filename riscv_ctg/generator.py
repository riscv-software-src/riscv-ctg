from constraint import *
import random
import re
from riscv_ctg.constants import *

ops = {
    'rformat': ['rs1','rs2','rd'],
    'iformat': ['rs1','rd'],
    'sformat': ['rs1','rs2'],
    'bformat': ['rs1','rs2'],
    'uformat': ['rd'],
    'jformat': ['rd'],
}
vals = {
    'rformat': ['rs1_val','rs2_val'],
    'iformat': ['rs1_val','imm_val'],
    'sformat': ['rs1_val','rs2_val','imm_val'],
    'bformat': ['rs1_val','rs2_val','imm_val'],
    'uformat': ['imm_val'],
    'jformat': ['imm_val'],
}
class Generator():
    def __init__(self,fmt,opnode,opcode,randomization):
        self.fmt = fmt
        self.opcode = opcode
        self.op_vars = ops[fmt]
        self.val_vars = vals[fmt]
        self.template = opnode['template']
        self.opnode = opnode
        if 'operation' in opnode:
            self.operation = opnode['operation']
        else:
            self.operation = None
        datasets = {}
        for entry in self.val_vars:
            key = entry+"_data"
            if key in opnode:
                datasets[entry] = eval(opnode[key])
            else:
                datasets[entry] = [0]
        self.datasets = datasets
        self.random=randomization

    def opcomb(self,cgf):
        op_picked = []
        op_comb = []
        op_datasets = []
        i = 10
        for var in self.op_vars:
            if var in cgf:
                op_datasets.append(list(cgf[var].keys()))
            else:
                op_datasets.append(['x'+str(i)])
                i+=1
            op_picked.append([])

        combination_num = max([len(x) for x in op_datasets])

        for i in range(combination_num):
            if self.random:
                problem = Problem(MinConflictsSolver())
            else:
                problem = Problem()

            for i,var in enumerate(self.op_vars):
                problem.addVariable(var, op_datasets[i])

            def condition(*argv):
                res = True
                temp = []
                for j,val in enumerate(argv):
                    if len(op_picked[j]) == len(op_datasets[j]):
                        continue
                    res = res and val not in op_picked[j] and val not in temp
                    temp.append(val)
                return res
            problem.addConstraint(condition, tuple(self.op_vars))
            count = 0
            solution = problem.getSolution()
            while (solution is None and count < 5):
                solution = problem.getSolution()
                count = count + 1
            if solution is None:
                print("Can't find a solution - 1")
                exit(0)

            op_tuple = []
            for ind,key in enumerate(self.op_vars):
                op_tuple.append(solution[key])
                op_picked[ind].append(solution[key])
            op_comb.append( tuple(op_tuple) )

        if 'op_comb' in cgf:

            for req_op_comb in cgf['op_comb']:
                satisfied = False
                for comb in op_comb:
                    for var,val in zip(self.op_vars,comb):
                        locals()[var]=val
                    if eval(req_op_comb):
                        satisfied = True
                        break;
                if not satisfied:
                    if self.random:
                        problem = Problem(MinConflictsSolver())
                    else:
                        problem = Problem()
                    for i,var in enumerate(self.op_vars):
                        problem.addVariable(var, op_datasets[i])
                    def condition(*argv):
                        for var,val in zip(self.op_vars,argv):
                            locals()[var]=val
                        return eval(req_op_comb)
                    problem.addConstraint(condition, tuple(self.op_vars))
                    count = 0
                    solution = problem.getSolution()
                    while (solution is None and count < 5):
                        solution = problem.getSolution()
                        count = count + 1
                    if solution is None:
                        print("Can't find a solution - 2")
                        exit(0)
                    op_tuple = []
                    for i,key in enumerate(self.op_vars):
                        op_tuple.append(solution[key])
                    op_comb.append( tuple(op_tuple) )
                    problem.reset()
        return op_comb


    def valcomb(self, cgf):
        val_comb = []

        if self.opcode in ['lw','lb','lhu','lh','lbu','sw','sb','sh']:
            size = int(self.opnode['size'])
            def boundconstraint(rs1_val,imm_val):
                temp = rs1_val+imm_val-(imm_val+(1 if imm_val>0 else -1)*(rs1_val%size))+size
                if temp>=0 and temp<=4:
                    return True
                else:
                    return False
        else:
            boundconstraint=None
        conds = list(cgf['val_comb'].keys())
        inds = set(range(len(conds)))
        while inds:
            req_val_comb = conds[inds.pop()]
            if self.random:
                problem = Problem(MinConflictsSolver())
            else:
                problem = Problem()
            for var in self.val_vars:
                problem.addVariable(var, self.datasets[var])

            def condition(*argv):
                for var,val in zip(self.val_vars,argv):
                    locals()[var]=val
                return eval(req_val_comb)

            problem.addConstraint(condition,tuple(self.val_vars))
            if boundconstraint:
                problem.addConstraint(boundconstraint,tuple(['rs1_val','imm_val']))
            solution = problem.getSolution()
            count = 0
            while (solution != {} and count < 5):
                solution = problem.getSolution()
                count+=1
            if solution is None:
                print("Can't find a solution - 3")
                exit(0)
            val_tuple = []
            for i,key in enumerate(self.val_vars):
                val_tuple.append(solution[key])

            def eval_func(cond):
                for var,val in zip(self.val_vars,val_tuple):
                    locals()[var] = val
                return eval(cond)
            inds = inds - set(filter(lambda x: eval_func(conds[x]),inds))

            val_comb.append( tuple(val_tuple) )
            problem.reset()
        return val_comb

    def __jfmt_instr__(self,op=None,val=None):
        instr = {'inst':self.opcode,'index':'0'}

        labelize = lambda x: (str((-x)%2**21),'1b') if x < 0 else (str((x%2**21)),'3f')
        if op:
            for var,reg in zip(self.op_vars,op):
                instr[var] = str(reg)
        else:
            for i,var in enumerate(self.op_vars):
                instr[var] = 'x'+str(i+10)
        if val:
            for i,var in enumerate(self.val_vars):
                if var == "imm_val":
                    instr[var],instr['label'] = labelize(val[i])
                else:
                    instr[var] = str(val[i])
        else:
            for var in self.val_vars:
                if var == "imm_val":
                    instr[var],instr['label'] = '0','3f'
                else:
                    instr[var] = '0'
        return instr

    def __bfmt_instr__(self,op=None,val=None):
        instr = {'inst':self.opcode,'index':'0'}
        labelize = lambda x: (str((-x)%2048),'1b') if x < 0 else (str((x%2048)),'3f')

        if op:
            for var,reg in zip(self.op_vars,op):
                instr[var] = str(reg)
        else:
            for i,var in enumerate(self.op_vars):
                instr[var] = 'x'+str(i+10)
        if val:
            for i,var in enumerate(self.val_vars):
                if var == "imm_val":
                    instr[var],instr['label'] = labelize(val[i])
                else:
                    instr[var] = str(val[i])
        else:
            for var in self.val_vars:
                if var == "imm_val":
                    instr[var],instr['label'] = '0','3f'
                else:
                    instr[var] = '0'
        return instr


    def __instr__(self, op=None, val=None):
        instr = {'inst':self.opcode,'index':'0'}
        if op:
            for var,reg in zip(self.op_vars,op):
                instr[var] = str(reg)
        else:
            for i,var in enumerate(self.op_vars):
                instr[var] = 'x'+str(i+10)
        if val:
            for i,var in enumerate(self.val_vars):
                instr[var] = str(val[i])
        else:
            for var in self.val_vars:
                instr[var] = '0'
        return instr

    def gen_inst(self,op_comb, val_comb, cgf):
        instr_dict = []
        cont = []

        if len(op_comb) < len(val_comb):
            op_comb = list(op_comb) + [[]] * (len(val_comb) - len(op_comb))
        elif len(val_comb) < len(op_comb):
            val_comb = list(val_comb) + [[]] * (len(op_comb) - len(val_comb))

        for op,val in zip(op_comb,val_comb):
            if any([x=='x0' for x in op]) or not (len(op) == len(set(op))):
                cont.append(val)
            if self.fmt == 'bformat':
                instr_dict.append(self.__bfmt_instr__(op,val))
            elif self.fmt == 'jformat':
                instr_dict.append(self.__jfmt_instr__(op,val))
            else:
                instr_dict.append(self.__instr__(op,val))

        for val in cont:
            if self.fmt == 'bformat':
                instr_dict.append(self.__bfmt_instr__(op,val))
            elif self.fmt == 'jformat':
                instr_dict.append(self.__jfmt_instr__(op,val))
            else:
                instr_dict.append(self.__instr__(op,val))
        return instr_dict

    @staticmethod
    def swreg(instr_dict):
        total_instr = len(instr_dict)
        available_reg = default_regset.copy()
        available_reg.remove('x0')
        count = 0
        assigned = 0
        offset = 0
        for instr in instr_dict:
            if 'rs1' in instr and instr['rs1'] in available_reg:
                available_reg.remove(instr['rs1'])
            if 'rs2' in instr and instr['rs2'] in available_reg:
                available_reg.remove(instr['rs2'])
            if 'rd' in instr and instr['rd'] in available_reg:
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

    @staticmethod
    def testreg(instr_dict):
        total_instr = len(instr_dict)
        available_reg = default_regset.copy()
        available_reg.remove('x0')
        count = 0
        assigned = 0
        for instr in instr_dict:
            if 'rs1' in instr and instr['rs1'] in available_reg:
                available_reg.remove(instr['rs1'])
            if 'rs2' in instr and instr['rs2'] in available_reg:
                available_reg.remove(instr['rs2'])
            if 'rd' in instr and instr['rd'] in available_reg:
                available_reg.remove(instr['rd'])
            if 'swreg' in instr and instr['swreg'] in available_reg:
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

    def correct_val(self,instr_dict):
        if self.operation:
            for i in range(len(instr_dict)):
                for var in self.val_vars:
                    locals()[var]=int(instr_dict[i][var])
                correctval = eval(self.operation)
                instr_dict[i]['correctval'] = str(correctval)
        else:
            for i in range(len(instr_dict)):
                instr_dict[i]['correctval'] = '0'
        return instr_dict


