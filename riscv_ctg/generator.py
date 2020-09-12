# See LICENSE.incore for details

from collections import defaultdict
from constraint import *
import random
import re
from riscv_ctg.constants import *
from riscv_ctg.log import logger
import time
from math import *
import struct

ops = {
    'rformat': ['rs1','rs2','rd'],
    'iformat': ['rs1','rd'],
    'sformat': ['rs1','rs2'],
    'bformat': ['rs1','rs2'],
    'uformat': ['rd'],
    'jformat': ['rd'],
    'crformat': ['rs1','rs2'],
    'cmvformat': ['rd', 'rs2'],
    'ciformat': ['rd'],
    'cssformat': ['rs2'],
    'ciwformat': ['rd'],
    'clformat': ['rd','rs1'],
    'csformat': ['rs1','rs2'],
    'caformat': ['rs1','rs2'],
    'cbformat': ['rs1'],
    'cjformat': []

}
vals = {
    'rformat': ['rs1_val','rs2_val'],
    'iformat': ['rs1_val','imm_val'],
    'sformat': ['rs1_val','rs2_val','imm_val'],
    'bformat': ['rs1_val','rs2_val','imm_val'],
    'uformat': ['imm_val'],
    'jformat': ['imm_val'],
    'crformat': ['rs1_val','rs2_val'],
    'cmvformat': ['rs2_val'],
    'ciformat': ['rs1_val','imm_val'],
    'cssformat': ['rs2_val','imm_val'],
    'ciwformat': ['imm_val'],
    'clformat': ['rs1_val','imm_val'],
    'csformat': ['rs1_val','rs2_val','imm_val'],
    'caformat': ['rs1_val','rs2_val'],
    'cbformat': ['rs1_val','imm_val'],
    'cjformat': ['imm_val']
}

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class Generator():
    def __init__(self,fmt,opnode,opcode,randomization, xl):
        global xlen
        xlen = xl
        self.fmt = fmt
        self.opcode = opcode
        self.op_vars = ops[fmt]
        self.val_vars = vals[fmt]
        if opcode in ['sw','sh','sb','lw','lhu','lh','lb','lbu','ld','lwu','sd']:
            self.val_vars = self.val_vars + ['ea_align']
        self.template = opnode['template']
        self.opnode = opnode
        if 'operation' in opnode:
            self.operation = opnode['operation']
        else:
            self.operation = None
        datasets = {}
        i=10
        for entry in self.op_vars:
            key = entry+"_op_data"
            if key in opnode:
                datasets[entry] = eval(opnode[key])
            else:
                datasets[entry] = ['x'+str(i)]
                i+=1
        for entry in self.val_vars:
            key = entry+"_data"
            if key in opnode:
                datasets[entry] = eval(opnode[key])
            else:
                datasets[entry] = [0]
        self.datasets = datasets
        self.random=randomization

    def opcomb(self, cgf):
        logger.debug('Generating OpComb')
        solutions = []
        op_conds = {}
        if "op_comb" in cgf:
            op_comb = set(cgf["op_comb"])
        else:
            op_comb = set([])
        for op in self.op_vars:
            if op in cgf:
                op_conds[op] = set(cgf[op])
            else:
                op_conds[op] = set([])
        individual = False
        nodiff = False
        construct_constraint = lambda val: (lambda x: bool(x in val))
        while any([len(op_conds[x])!=0 for x in op_conds]):
            if self.random:
                problem = Problem(MinConflictsSolver())
            else:
                problem = Problem()

            done = False
            for var in self.op_vars:
                problem.addVariable(var, list(self.datasets[var]))
                if op_conds[var] and not(individual and done):
                    problem.addConstraint(construct_constraint(op_conds[var]),tuple([var]))
                    done = True
            if op_comb:
                cond = op_comb.pop()
                def comb_constraint(*args):
                    for var,val in zip(self.op_vars,args):
                        locals()[var] = val
                    return eval(cond)
                problem.addConstraint(comb_constraint,tuple(self.op_vars))
            elif not nodiff:
                problem.addConstraint(AllDifferentConstraint())
            count = 0
            solution = problem.getSolution()
            while (solution is None and count < 5):
                solution = problem.getSolution()
                count = count + 1
            if solution is None:
                if individual:
                    if nodiff:
                        logger.warn("Cannot find solution for Op combination")
                        break
                    else:
                        nodiff = True
                else:
                    individual = True
                continue

            op_tuple = []
            for key in self.op_vars:
                op_tuple.append(solution[key])
                op_conds[key].discard(solution[key])
            solutions.append( tuple(op_tuple) )
            def eval_func(cond):
                for var,val in zip(self.op_vars,op_tuple):
                    locals()[var] = val
                return eval(cond)
            op_comb = op_comb - set(filter(eval_func,op_comb))
            problem.reset()
        return solutions



    def valcomb(self, cgf):
        logger.debug('Generating ValComb')
        if 'val_comb' not in cgf:
            return []
        val_comb = []

        # if self.opcode in ['lw','lb','lhu','lh','lbu','sw','sb','sh']:
        #     size = int(self.opnode['size'])
        #     def boundconstraint(rs1_val,imm_val):
        #         temp = rs1_val+imm_val-(imm_val+(1 if imm_val>0 else -1)*(rs1_val%size))+size
        #         if temp>=0 and temp<=4:
        #             return True
        #         else:
        #             return False
        # else:
        #     boundconstraint=None
        conds = list(cgf['val_comb'].keys())
        inds = set(range(len(conds)))
        while inds:
            req_val_comb = conds[inds.pop()]
            if self.random:
                problem = Problem(MinConflictsSolver())
            else:
                problem = Problem()

            for var in self.val_vars:
                if var == 'ea_align' and var not in req_val_comb:
                    problem.addVariable(var, [0])
                else:
                    problem.addVariable(var, self.datasets[var])

            def condition(*argv):
                for var,val in zip(self.val_vars,argv):
                    locals()[var]=val
                return eval(req_val_comb)

            problem.addConstraint(condition,tuple(self.val_vars))
            # if boundconstraint:
            #     problem.addConstraint(boundconstraint,tuple(['rs1_val','imm_val']))
            solution = problem.getSolution()
            count = 0
            while (solution != {} and count < 5):
                solution = problem.getSolution()
                count+=1
            if solution is None:
                logger.warn("Cannot find solution for Val condition "+str(req_val_comb))
                continue
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

    def __cb_instr__(self,op=None,val=None):
        instr = {'inst':self.opcode,'index':'0'}
        labelize = lambda x: (str((-x)%257),'1b') if x < 0 else (str((x%257)),'3f')

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

    def __cj_instr__(self,op=None,val=None):
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
        instr['rs2'] = 'x1'
        return instr

    def __clui_instr__(self,op=None,val=None):
        instr = {'inst':self.opcode,'index':'0'}
        if op:
            for var,reg in zip(self.op_vars,op):
                instr[var] = str(reg)
        else:
            for i,var in enumerate(self.op_vars):
                instr[var] = 'x'+str(i+10)
        if val:
            for i,var in enumerate(self.val_vars):
                if var == "imm_val":
                    instr[var] = str(val[i]) if val[i] < 32 else str(val[i]+1048512)
                else:
                    instr[var] = str(val[i])
        else:
            for var in self.val_vars:
                if var == "imm_val":
                    instr[var] = '16'
                else:
                    instr[var] = '0'
        return instr

    def __cmemsp_instr__(self, op=None, val=None):
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
                instr[var] = str(self.datasets[var][0])
        instr['rs1'] = 'x2'
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
                instr[var] = str(self.datasets[var][0])
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
            if self.opcode == 'c.lui':
                instr_dict.append(self.__clui_instr__(op,val))
            elif self.opcode in ['c.beqz','c.bnez']:
                instr_dict.append(self.__cb_instr__(op,val))
            elif self.opcode in ['c.lwsp','c.swsp','c.ldsp','c.sdsp']:
                if any([x == 'x2' for x in op]):
                    cont.append(val)
                instr_dict.append(self.__cmemsp_instr__(op,val))
            elif self.fmt == 'bformat' or self.opcode in ['c.j']:
                instr_dict.append(self.__bfmt_instr__(op,val))
            elif self.opcode in ['c.jal','c.jalr']:
                instr_dict.append(self.__cj_instr__(op,val))
            elif self.fmt == 'jformat':
                instr_dict.append(self.__jfmt_instr__(op,val))
            else:
                instr_dict.append(self.__instr__(op,val))
        op = None
        for val in cont:
            if self.opcode == 'c.lui':
                instr_dict.append(self.__clui_instr__(op,val))
            elif self.opcode in ['c.beqz','c.bneqz']:
                instr_dict.append(self.__cb_instr__(op,val))
            elif self.opcode in ['c.lwsp','c.swsp']:
                instr_dict.append(self.__cmemsp_instr__(op,val))
            elif self.fmt == 'bformat':
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
                        offset += int(xlen/8)
                        assigned += 1
                        if offset == 2048:
                            offset = 0
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
                    offset += int(xlen/8)
                    if offset == 2048:
                        offset = 0
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
                instr_dict[i]['correctval'] = '0x' + '0'.zfill(int(xlen/4))
        return instr_dict

    def reformat_instr(self, instr_dict):
        mydict = instr_dict.copy()
        for i in range(len(instr_dict)):
            for field in instr_dict[i]:
                if xlen == 32:
                    if instr_dict[i]['inst'] in ['sltu', 'sltiu', 'bgeu', 'bltu']:
                        size = '>I'
                    else:
                        size = '>i'
                else:
                    if instr_dict[i]['inst'] in ['sltu', 'sltiu', 'bgeu', 'bltu']:
                        size = '>Q'
                    else:
                        size = '>q'
                if 'val' in field and field != 'correctval' and field != 'imm_val':
                    value = instr_dict[i][field]
                    if '0x' in value:
                        value = '0x' + value[2:].zfill(int(xlen/4))
                        value = struct.unpack(size, bytes.fromhex(value[2:]))[0]
                    else:
                        value = int(value)
                    value = '0x' + struct.pack(size,value).hex()
                    instr_dict[i][field] = value
        return instr_dict


    @staticmethod
    def write_test(file_name,node,label,instr_dict, op_node):
        regs = defaultdict(lambda: 0)
        sreg = instr_dict[0]['swreg']
        code = []
        sign = [".align 4"]
        data = [".align 4","rvtest_data:",".word 0xbabecafe"]
        n = 0
        for instr in instr_dict:
            res = op_node['template']
            for value in sorted(instr.keys(), key = len, reverse = True):
                substitute = instr[value]
                res = re.sub(value, substitute, res)
            if instr['swreg'] != sreg or instr['offset'] == '0':
                sign.append(signode_template.substitute({'n':n,'label':"signature_"+sreg+"_"+str(regs[sreg])}))
                n = 1
                regs[sreg]+=1
                sreg = instr['swreg']
                code.append("la "+sreg+",signature_"+sreg+"_"+str(regs[sreg]))
            else:
                n+=1
            code.append(res)
        sign.append(signode_template.substitute({'n':n,'label':"signature_"+sreg+"_"+str(regs[sreg])}))
        test = case_template.safe_substitute(num=1,cond=node['config'],code='\n'.join(code),cov_label=label)
        with open(file_name,"w") as fd:
            fd.write(test_template.safe_substitute(data='\n'.join(data),test=test,sig='\n'.join(sign),isa="RV"+str(xlen)+op_node['isa']))

