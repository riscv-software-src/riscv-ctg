# See LICENSE.incore for details

from collections import defaultdict
from constraint import *
import re
from riscv_ctg.constants import *
from riscv_ctg.log import logger
import time
from math import *
import struct

twos_xlen = lambda x: twos(x,xlen)

OPS = {
    'rformat': ['rs1', 'rs2', 'rd'],
    'iformat': ['rs1', 'rd'],
    'sformat': ['rs1', 'rs2'],
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
    'cjformat': []
}
''' Dictionary mapping instruction formats to operands used by those formats '''

VALS = {
    'rformat': ['rs1_val', 'rs2_val'],
    'iformat': ['rs1_val', 'imm_val'],
    'sformat': ['rs1_val', 'rs2_val', 'imm_val'],
    'bformat': ['rs1_val', 'rs2_val', 'imm_val'],
    'uformat': ['imm_val'],
    'jformat': ['imm_val'],
    'crformat': ['rs1_val', 'rs2_val'],
    'cmvformat': ['rs2_val'],
    'ciformat': ['rs1_val', 'imm_val'],
    'cssformat': ['rs2_val', 'imm_val'],
    'ciwformat': ['imm_val'],
    'clformat': ['rs1_val', 'imm_val'],
    'csformat': ['rs1_val', 'rs2_val', 'imm_val'],
    'caformat': ['rs1_val', 'rs2_val'],
    'cbformat': ['rs1_val', 'imm_val'],
    'cjformat': ['imm_val']
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

class Generator():
    '''
    A generator class to generate RISC-V assembly tests for a given instruction 
    format, opcode and a set of coverpoints.

    :param fmt: the RISC-V instruction format type to be used for the test generation.
    :param opnode: dictionary node from the attributes YAML that is to be used in the test generation.
    :param opcode: name of the instruction opcode.
    :param randomization: a boolean variable indicating if the random constraint solvers must be employed.
    :param xl: an integer indicating the XLEN value to be used.

    :type fmt:
    :type opnode: dict
    :type opcode: str
    :type randomization: bool
    :type xl: int
    '''
    def __init__(self,fmt,opnode,opcode,randomization, xl):
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
        xlen = xl
        self.fmt = fmt
        self.opcode = opcode
        self.op_vars = OPS[fmt]
        self.val_vars = VALS[fmt]
        if opcode in ['sw', 'sh', 'sb', 'lw', 'lhu', 'lh', 'lb', 'lbu', 'ld', 'lwu', 'sd',"jal","beq","bge","bgeu","blt","bltu","bne","jalr"]:
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
        '''
        This function finds the solutions for the various operand combinations 
        defined by the coverpoints in the CGF under the "op_comb" node of the 
        covergroup.

        Depending on the registers chosen in the datasets, a contraint is created
        to ensure that all those registers occur atleast once in the respective
        operand/destination location in the instruction. These contraints are
        then supplied to the solver for solutions

        If randomization is enabled we use the ``MinConflictsSolver`` solver to 
        find solutions. 

        :param cgf: dict

        :return: a dictionary of solutions for the various operand combinations specified in the CGF file.
        '''
        logger.debug(self.opcode + ' : Generating OpComb')
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
        while any([len(op_conds[x])!=0 for x in op_conds]+[len(op_comb)!=0]):
            cond_str = ''
            cond_vars = []
            if self.random:
                problem = Problem(MinConflictsSolver())
            else:
                problem = Problem()

            done = False
            for var in self.op_vars:
                problem.addVariable(var, list(self.datasets[var]))
                if op_conds[var] and not(individual and done):
                    cond_vars.append(var)
                    problem.addConstraint(construct_constraint(op_conds[var]),tuple([var]))
                    done = True
            if op_comb:
                cond = op_comb.pop()
                cond_str += cond+", "
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
                        logger.warn(self.opcode + " : Cannot find solution for Op combination")
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

            def eval_func(cond):
                for var,val in zip(self.op_vars,op_tuple):
                    locals()[var] = val
                return eval(cond)
            sat_set = set(filter(eval_func,op_comb))
            cond_str += ", ".join([var+"=="+solution[var] for var in cond_vars]+[op_comb[i] for i in sat_set])
            op_tuple.append(cond_str)
            op_comb = op_comb - sat_set
            problem.reset()
            solutions.append( tuple(op_tuple) )

        return solutions



    def valcomb(self, cgf):
        '''
        This function finds the solutions for the various value combinations 
        defined by the coverpoints in the CGF under the "val_comb" node of the 
        covergroup.

        The constraints here are quite simply taken as `eval` strings from the CGF val_comb
        nodes itself.

        If randomization is enabled we use the ``MinConflictsSolver`` solver to 
        find solutions. 

        :param cgf: dict

        :return: a dictionary of solutions for the various value combinations specified in the CGF file.
        '''
        logger.debug(self.opcode + ' : Generating ValComb')
        if 'val_comb' not in cgf:
            return []
        val_comb = []

        # if self.opcode in ['lw', 'lb', 'lhu', 'lh', 'lbu', 'sw', 'sb', 'sh']:
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
            #     problem.addConstraint(boundconstraint,tuple(['rs1_val', 'imm_val']))
            solution = problem.getSolution()
            count = 0
            while (solution is None and count < 5):
                solution = problem.getSolution()
                count+=1
            if solution is None:
                logger.warn(self.opcode + " : Cannot find solution for Val condition "+str(req_val_comb))
                continue
            val_tuple = []
            for i,key in enumerate(self.val_vars):
                val_tuple.append(solution[key])

            def eval_func(cond):
                for var,val in zip(self.val_vars,val_tuple):
                    locals()[var] = val
                return eval(cond)
            sat_set=set(filter(lambda x: eval_func(conds[x]),inds))
            inds = inds - sat_set
            val_tuple.append(req_val_comb+', '+', '.join([conds[i] for i in sat_set]))
            val_comb.append( tuple(val_tuple) )
            problem.reset()
        return val_comb

    def __jfmt_instr__(self,op=None,val=None):
        cond_str = ''
        if op:
            cond_str += op[-1]+', '
        if val:
            cond_str += val[-1]
        instr = {'inst':self.opcode,'index':'0', 'comment':cond_str}
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
                    instr[var],instr['label'] = '0', '3f'
                else:
                    instr[var] = '0'
        return instr

    def __bfmt_instr__(self,op=None,val=None):
        cond_str = ''
        if op:
            cond_str += op[-1]+', '
        if val:
            cond_str += val[-1]
        instr = {'inst':self.opcode,'index':'0', 'comment':cond_str}


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
                    instr[var],instr['label'] = '0', '3f'
                else:
                    instr[var] = '0'
        return instr

    def __cb_instr__(self,op=None,val=None):
        cond_str = ''
        if op:
            cond_str += op[-1]+', '
        if val:
            cond_str += val[-1]
        instr = {'inst':self.opcode,'index':'0', 'comment':cond_str}


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
                    instr[var],instr['label'] = '0', '3f'
                else:
                    instr[var] = '0'
        return instr

    def __cj_instr__(self,op=None,val=None):
        cond_str = ''
        if op:
            cond_str += op[-1]+', '
        if val:
            cond_str += val[-1]
        instr = {'inst':self.opcode,'index':'0', 'comment':cond_str}


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
                    instr[var],instr['label'] = '0', '3f'
                else:
                    instr[var] = '0'
        instr['rs2'] = 'x1'
        return instr

    def __clui_instr__(self,op=None,val=None):
        cond_str = ''
        if op:
            cond_str += op[-1]+', '
        if val:
            cond_str += val[-1]
        instr = {'inst':self.opcode,'index':'0', 'comment':cond_str}

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
        cond_str = ''
        if op:
            cond_str += op[-1]+', '
        if val:
            cond_str += val[-1]
        instr = {'inst':self.opcode,'index':'0', 'comment':cond_str}
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
        cond_str = ''
        if op:
            cond_str += op[-1]+', '
        if val:
            cond_str += val[-1]
        instr = {'inst':self.opcode,'index':'0', 'comment':cond_str}
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
        '''
        This function combines the op_comb and val_comb solution dictionaries
        to create a complete set of arguments of the instruction. 
        
        Depending on the instruction opcode other subfunctions are called to 
        create the final merged dictionary of op_comb and val_comb.

        Note however, that using the integer register x0 as either source or 
        destination does not contribute to the coverage. Hence the respective 
        val_combs are repeated again with non-x0 registers. 
        
        '''
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
            elif self.opcode in ['c.beqz', 'c.bnez']:
                instr_dict.append(self.__cb_instr__(op,val))
            elif self.opcode in ['c.lwsp', 'c.swsp', 'c.ldsp', 'c.sdsp']:
                if any([x == 'x2' for x in op]):
                    cont.append(val)
                instr_dict.append(self.__cmemsp_instr__(op,val))
            elif self.fmt == 'bformat' or self.opcode in ['c.j']:
                instr_dict.append(self.__bfmt_instr__(op,val))
            elif self.opcode in ['c.jal', 'c.jalr']:
                instr_dict.append(self.__cj_instr__(op,val))
            elif self.fmt == 'jformat':
                instr_dict.append(self.__jfmt_instr__(op,val))
            else:
                instr_dict.append(self.__instr__(op,val))
        op = None
        for val in cont:
            if self.opcode == 'c.lui':
                instr_dict.append(self.__clui_instr__(op,val))
            elif self.opcode in ['c.beqz', 'c.bneqz']:
                instr_dict.append(self.__cb_instr__(op,val))
            elif self.opcode in ['c.lwsp', 'c.swsp']:
                instr_dict.append(self.__cmemsp_instr__(op,val))
            elif self.fmt == 'bformat':
                instr_dict.append(self.__bfmt_instr__(op,val))
            elif self.fmt == 'jformat':
                instr_dict.append(self.__jfmt_instr__(op,val))
            else:
                instr_dict.append(self.__instr__(op,val))

        hits = defaultdict(lambda:set([]))
        final_instr = []
        def eval_inst_coverage(coverpoints,instr):
            cover_hits = {}
            if 'ea_align' in instr:
                ea_align = int(instr['ea_align'])
            if 'rs1_val' in instr:
                rs1_val = int(instr['rs1_val'])
            if 'rs2_val' in instr:
                rs2_val = int(instr['rs2_val'])
            if 'imm_val' in instr:
                if instr['inst'] in ['c.j','c.jal']:
                    imm_val = (-1 if instr['label'] == '1b' else 1) * int(instr['imm_val'])
                else:
                    imm_val = int(instr['imm_val'])
            if 'rs2' in instr:
                rs2 = instr['rs2']
            if 'rd' in instr:
                rd = instr['rd']
            if 'rs1' in instr:
                rs1 = instr['rs1']
            if 'val_comb' in coverpoints:
                valcomb_hits = set([])
                for coverpoint in coverpoints['val_comb']:
                    if eval(coverpoint):
                        valcomb_hits.add(coverpoint)
                cover_hits['val_comb']=valcomb_hits
            if 'op_comb' in coverpoints:
                opcomb_hits = set([])
                for coverpoint in coverpoints['op_comb']:
                    if eval(coverpoint):
                        opcomb_hits.add(coverpoint)
                cover_hits['op_comb']=opcomb_hits
            if 'rs1' in coverpoints:
                if rs1 in coverpoints['rs1']:
                    cover_hits['rs1'] = set([rs1])
            if 'rs2' in coverpoints:
                if rs2 in coverpoints['rs2']:
                    cover_hits['rs2'] = set([rs2])
            if 'rd' in coverpoints:
                if rd in coverpoints['rd']:
                    cover_hits['rd'] = set([rd])
            return cover_hits
        i = 0
        for instr in instr_dict:
            unique = False
            skip_val = False
            if instr['inst'] in cgf['opcode']:
                if 'rs1' in instr and 'rs2' in instr:
                    if instr['rs1'] == instr['rs2']:
                        skip_val = True
                if 'rs1' in instr:
                    if instr['rs1'] == 'x0':
                        skip_val = True
                if 'rs2' in instr:
                    if instr['rs2'] == 'x0':
                        skip_val = True
                if 'rd' in instr:
                    if instr['rd'] == 'x0':
                        skip_val = True
                cover_hits = eval_inst_coverage(cgf,instr)
                for entry in cover_hits:
                    if entry=='val_comb' and skip_val:
                        continue
                    over = hits[entry] & cover_hits[entry]
                    if over != cover_hits[entry]:
                        unique = unique or True
                    hits[entry] |= cover_hits[entry]
                if unique:
                    final_instr.append(instr)
                else:
                    i+=1
        return final_instr

    @staticmethod
    def swreg(instr_dict):
        '''
        This function is responsible for identifying which register can be used
        as a signature pointer for each instruction. 

        This register is calculated by traversing the dictionary of solutions 
        created so far and removing all the registers which are used as either 
        operands or destination. When 3 or less registers are pending, one of 
        those registers is used as signature pointer for all the solutions 
        traversed so far.

        Along with the register the offset is also assigned in this function. 
        The offset is incremented by xlen/8 bytes always.

        Care is taken to never use 'x0' as signature pointer.
        '''
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
        '''
        This function is responsible for identifying which register can be used
        as a test register for each instruction. 

        This register is calculated by traversing the dictionary of solutions 
        created so far and removing all the registers which are used as either 
        operands or destination or signature. When 3 or less registers are pending, one of 
        those registers is used as test register for all the solutions 
        traversed so far.

        Care is taken to never use 'x0' as test register.
        '''
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
        '''
        this function is responsible for assigning the correct-vals for all instructions. 
        The correctvals are calculated based on the `operation` field of the node
        in the attributes YAML. If the operation field is empty, then a value of 
        0 is assigned to the correctval.
        '''
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
        '''
        This function basically sanitizes the integer values to a readable
        hex values
        '''
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
#                    value = '0x' + struct.pack(size,value).hex()
                    instr_dict[i][field] = value
        return instr_dict


    @staticmethod
    def write_test(file_name,node,label,instr_dict, op_node, usage_str):
        regs = defaultdict(lambda: 0)
        sreg = instr_dict[0]['swreg']
        code = []
        sign = [""]
        data = [".align 4","rvtest_data:",".word 0xbabecafe"]
        n = 0
        opcode = instr_dict[0]['inst']
        extension = (op_node['isa']).replace('I',"") if len(op_node['isa'])>1 else op_node['isa']
        count = 0
        for instr in instr_dict:
            res = '\ninst_{0}:'.format(str(count))
            res += Template(op_node['template']).safe_substitute(instr)
            if instr['swreg'] != sreg or instr['offset'] == '0':
                sign.append(signode_template.substitute({'n':n,'label':"signature_"+sreg+"_"+str(regs[sreg])}))
                n = 1
                regs[sreg]+=1
                sreg = instr['swreg']
                code.append("RVTEST_SIGBASE( "+sreg+",signature_"+sreg+"_"+str(regs[sreg])+")")
            else:
                n+=1
            code.append(res)
            count = count + 1
        case_str = ''.join([case_template.safe_substitute(xlen=xlen,num=i,cond=cond,cov_label=label) for i,cond in enumerate(node['config'])])
        sign.append(signode_template.substitute({'n':n,'label':"signature_"+sreg+"_"+str(regs[sreg])}))
        test = part_template.safe_substitute(case_str=case_str,code='\n'.join(code))
        sign.append("#ifdef rvtest_mtrap_routine\n"+signode_template.substitute({'n':64,'label':"mtrap_sigptr"})+"\n#endif\n")
        sign.append("#ifdef rvtest_gpr_save\n"+signode_template.substitute({'n':32,'label':"gpr_save"})+"\n#endif\n")
        with open(file_name,"w") as fd:
            fd.write(usage_str + test_template.safe_substitute(data='\n'.join(data),test=test,sig='\n'.join(sign),isa="RV"+str(xlen)+op_node['isa'],opcode=opcode,extension=extension,label=label))

