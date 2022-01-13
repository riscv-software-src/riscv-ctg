# See LICENSE.incore for details
import random
from collections import defaultdict
from constraint import *
import re
from riscv_ctg.constants import *
from riscv_ctg.log import logger
import time
from math import *
import struct
import sys
import itertools

one_operand_finstructions = ["fsqrt.s","fmv.x.w","fcvt.wu.s","fcvt.w.s","fclass.s","fcvt.l.s","fcvt.lu.s","fcvt.s.l","fcvt.s.lu"]
two_operand_finstructions = ["fadd.s","fsub.s","fmul.s","fdiv.s","fmax.s","fmin.s","feq.s","flt.s","fle.s","fsgnj.s","fsgnjn.s","fsgnjx.s"]
three_operand_finstructions = ["fmadd.s","fmsub.s","fnmadd.s","fnmsub.s"]

one_operand_dinstructions = ["fsqrt.d","fclass.d","fcvt.w.d","fcvt.wu.d","fcvt.d.w","fcvt.d.wu"]
two_operand_dinstructions = ["fadd.d","fsub.d","fmul.d","fdiv.d","fmax.d","fmin.d","feq.d","flt.d","fle.d","fsgnj.d","fsgnjn.d","fsgnjx.d"]
three_operand_dinstructions = ["fmadd.d","fmsub.d","fnmadd.d","fnmsub.d"]
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

class Generator():
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
    def __init__(self,fmt,opnode,opcode,randomization, xl, fl,base_isa_str):
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
        xlen = xl
        flen = fl
        base_isa = base_isa_str
        self.fmt = fmt
        self.opcode = opcode

        self.op_vars = OPS[fmt]

        self.val_vars = eval(VALS[fmt])

        if opcode in ['sw', 'sh', 'sb', 'lw', 'lhu', 'lh', 'lb', 'lbu', 'ld', 'lwu', 'sd',"jal","beq","bge","bgeu","blt","bltu","bne","jalr","flw","fsw","fld","fsd"]:
            self.val_vars = self.val_vars + ['ea_align']
        self.template = opnode['template']
        self.opnode = opnode
        self.stride = opnode['stride']
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
        self.default_regs = get_default_registers(self.op_vars, self.datasets)

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

        :param cgf: a covergroup in cgf format containing the set of coverpoints to be satisfied.

        :type cgf: dict

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

        :param cgf: a covergroup in cgf format containing the set of coverpoints to be satisfied.

        :type cgf: dict

        :return: a dictionary of solutions for the various value combinations specified in the CGF file.
        '''
        logger.debug(self.opcode + ' : Generating ValComb')
        if 'val_comb' not in cgf:
            return []
        val_comb = []

        conds = list(cgf['val_comb'].keys())
        inds = set(range(len(conds)))
        while inds:
            req_val_comb = conds[inds.pop()]
            if("#nosat" in req_val_comb):
                d={}
                soln = []
                req_val_comb_minus_comm = req_val_comb.split("#")[0]
                x = req_val_comb_minus_comm.split(" and ")

                if self.opcode[0] == 'f' and 'fence' not in self.opcode:
	                # fs + fe + fm -> Combiner Script
                    if (flen == 32):
                        e_sz = 8
                        m_sz = 23
                    else:
                        e_sz = 11
                        m_sz = 52
                    e_sz_string = '{:0'+str(e_sz)+'b}'
                    m_sz_string = '{:0'+str(m_sz)+'b}'
                    size_string = '{:0'+str(int(flen/4))+'x}'

                    if len(x) == (1*3 + 1):																# 1 Operand Instructions
                        fs1 = x[0].split(" == ")[1]
                        fe1 = x[1].split(" == ")[1]
                        fm1 = x[2].split(" == ")[1]
                        rm = x[-1].split(" == ")[1]
                        bin_val1 = fs1 + e_sz_string.format(int(fe1,16)) + m_sz_string.format(int(fm1,16))
                        hex_val1 = '0x' + size_string.format(int(bin_val1, 2))
                        x = ["rs1_val == " + hex_val1, "rm_val == " + rm]

                    elif len(x) == (2*3 + 1):															# 2 Operand Instructions
                        fs1 = x[0].split(" == ")[1]
                        fe1 = x[1].split(" == ")[1]
                        fm1 = x[2].split(" == ")[1]
                        fs2 = x[3].split(" == ")[1]
                        fe2 = x[4].split(" == ")[1]
                        fm2 = x[5].split(" == ")[1]
                        rm = x[-1].split(" == ")[1]
                        bin_val1 = fs1 + e_sz_string.format(int(fe1,16)) + m_sz_string.format(int(fm1,16))
                        bin_val2 = fs2 + e_sz_string.format(int(fe2,16)) + m_sz_string.format(int(fm2,16))
                        hex_val1 = '0x' + size_string.format(int(bin_val1, 2))
                        hex_val2 = '0x' + size_string.format(int(bin_val2, 2))
                        x = ["rs1_val == " + hex_val1, "rs2_val == " + hex_val2, "rm_val == " + rm]

                    elif len(x) == (3*3 + 1):															# 3 Operand Instructions
                        fs1 = x[0].split(" == ")[1]
                        fe1 = x[1].split(" == ")[1]
                        fm1 = x[2].split(" == ")[1]
                        fs2 = x[3].split(" == ")[1]
                        fe2 = x[4].split(" == ")[1]
                        fm2 = x[5].split(" == ")[1]
                        fs3 = x[6].split(" == ")[1]
                        fe3 = x[7].split(" == ")[1]
                        fm3 = x[8].split(" == ")[1]
                        rm = x[-1].split(" == ")[1]
                        bin_val1 = fs1 + e_sz_string.format(int(fe1,16)) + m_sz_string.format(int(fm1,16))
                        bin_val2 = fs2 + e_sz_string.format(int(fe2,16)) + m_sz_string.format(int(fm2,16))
                        bin_val3 = fs3 + e_sz_string.format(int(fe3,16)) + m_sz_string.format(int(fm3,16))
                        hex_val1 = '0x' + size_string.format(int(bin_val1, 2))
                        hex_val2 = '0x' + size_string.format(int(bin_val2, 2))
                        hex_val3 = '0x' + size_string.format(int(bin_val3, 2))
                        x = ["rs1_val == " + hex_val1, "rs2_val == " + hex_val2, "rs3_val == " + hex_val3, "rm_val == " + rm]

                for i in self.val_vars:
                    for j in x:
                        if i in j:
                            if(d.get(i,"None") == "None"):
                                d[i] = j.split("==")[1]
                            else:
                                logger.error("Invalid Coverpoint: More than one value of "+ i +" found!")
                                sys.exit(1)
                if(list(d.keys()) != self.val_vars):
                    logger.error("Invalid Coverpoint: Cannot bypass SAT Solver for partially defined coverpoints!")
                    sys.exit(1)
                for y in d:
                    if("0x" in d[y]):
                        soln.append(int(d[y],16))
                    elif("0b" in d[y]):
                        soln.append(int(d[y],2))
                    else:
                        soln.append(int(d[y]))
                soln.append(req_val_comb_minus_comm)
                val_tuple = soln

            else:
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
                problem.reset()
            val_comb.append( tuple(val_tuple) )
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
                if self.opcode[0] == 'f' and 'fence' not in self.opcode:
                    if self.opnode[var+'_op_data'][2] == 'f':
                        instr[var] = 'f'+str(i+10)
                    else:
                        instr[var] = 'x'+str(i+10)
                else:
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
                instr[var]=self.default_regs[var]
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

        :param op_comb: list containing the operand combination solutions
        :param val_comb: list containing the value combination solutions
        :param cgf: a covergroup in cgf format containing the set of coverpoints to be satisfied.

        :type cgf: dict
        :type op_comb: list
        :type val_comb: list

        :return: list of dictionaries containing the various values necessary for the macro.
        '''
        instr_dict = []
        cont = []
        if len(op_comb) < len(val_comb):
            op_comb = list(op_comb) + [[]] * (len(val_comb) - len(op_comb))
        elif len(val_comb) < len(op_comb):
            val_comb = list(val_comb) + [[self.datasets[var][0] for var in self.val_vars] + [""]] * (len(op_comb) - len(val_comb))

        x = dict([(y,x) for x,y in enumerate(self.val_vars)])

        ind_dict = {}
        for ind,var in enumerate(self.op_vars):
            if var+"_val" in x:
                ind_dict[ind] = x[var+"_val"]

        for op,val_soln in zip(op_comb,val_comb):
            val = [x for x in val_soln]
            if any([x=='x0' for x in op]) or not (len(op) == len(set(op))):
                cont.append(val_soln)
                op_inds = list(ind_dict.keys())
                for i,x in enumerate(op_inds):
                    if op[x] == 'x0':
                        val[ind_dict[x]] = 0
                    for y in op_inds[i:]:
                        if op[y] == op[x]:
                            val[ind_dict[y]] = val[ind_dict[x]]
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
            elif self.fmt == 'jformat' or self.fmt == 'cjformat':
                instr_dict.append(self.__jfmt_instr__(op,val))
            else:
                instr_dict.append(self.__instr__(op,val))
        op = None
        for val in cont:
            if self.opcode == 'c.lui':
                instr_dict.append(self.__clui_instr__(op,val))
            elif self.opcode in ['c.beqz', 'c.bnez']:
                instr_dict.append(self.__cb_instr__(op,val))
            elif self.opcode in ['c.lwsp', 'c.swsp', 'c.ldsp', 'c.sdsp']:
                instr_dict.append(self.__cmemsp_instr__(op,val))
            elif self.fmt == 'bformat' or self.opcode in ['c.j']:
                instr_dict.append(self.__bfmt_instr__(op,val))
            elif self.opcode in ['c.jal', 'c.jalr']:
                instr_dict.append(self.__cj_instr__(op,val))
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
            if 'rs3_val' in instr:
                rs3_val = int(instr['rs3_val'])
            if 'rm_val' in instr:
                rm_val = int(instr['rm_val'])
            if 'rs1_b0_val' in instr:
                rs1_b0_val = int(instr['rs1_b0_val'])
            if 'rs1_b1_val' in instr:
                rs1_b1_val = int(instr['rs1_b1_val'])
            if 'rs1_b2_val' in instr:
                rs1_b2_val = int(instr['rs1_b2_val'])
            if 'rs1_b3_val' in instr:
                rs1_b3_val = int(instr['rs1_b3_val'])
            if 'rs1_b4_val' in instr:
                rs1_b4_val = int(instr['rs1_b4_val'])
            if 'rs1_b5_val' in instr:
                rs1_b5_val = int(instr['rs1_b5_val'])
            if 'rs1_b6_val' in instr:
                rs1_b6_val = int(instr['rs1_b6_val'])
            if 'rs1_b7_val' in instr:
                rs1_b7_val = int(instr['rs1_b7_val'])
            if 'rs2_b0_val' in instr:
                rs2_b0_val = int(instr['rs2_b0_val'])
            if 'rs2_b1_val' in instr:
                rs2_b1_val = int(instr['rs2_b1_val'])
            if 'rs2_b2_val' in instr:
                rs2_b2_val = int(instr['rs2_b2_val'])
            if 'rs2_b3_val' in instr:
                rs2_b3_val = int(instr['rs2_b3_val'])
            if 'rs2_b4_val' in instr:
                rs2_b4_val = int(instr['rs2_b4_val'])
            if 'rs2_b5_val' in instr:
                rs2_b5_val = int(instr['rs2_b5_val'])
            if 'rs2_b6_val' in instr:
                rs2_b6_val = int(instr['rs2_b6_val'])
            if 'rs2_b7_val' in instr:
                rs2_b7_val = int(instr['rs2_b7_val'])
            if 'rs1_h0_val' in instr:
                rs1_h0_val = int(instr['rs1_h0_val'])
            if 'rs1_h1_val' in instr:
                rs1_h1_val = int(instr['rs1_h1_val'])
            if 'rs1_h2_val' in instr:
                rs1_h2_val = int(instr['rs1_h2_val'])
            if 'rs1_h3_val' in instr:
                rs1_h3_val = int(instr['rs1_h3_val'])
            if 'rs2_h0_val' in instr:
                rs2_h0_val = int(instr['rs2_h0_val'])
            if 'rs2_h1_val' in instr:
                rs2_h1_val = int(instr['rs2_h1_val'])
            if 'rs2_h2_val' in instr:
                rs2_h2_val = int(instr['rs2_h2_val'])
            if 'rs2_h3_val' in instr:
                rs2_h3_val = int(instr['rs2_h3_val'])
            if 'rs1_w0_val' in instr:
                rs1_w0_val = int(instr['rs1_w0_val'])
            if 'rs1_w1_val' in instr:
                rs1_w1_val = int(instr['rs1_w1_val'])
            if 'rs2_w0_val' in instr:
                rs2_w0_val = int(instr['rs2_w0_val'])
            if 'rs2_w1_val' in instr:
                rs2_w1_val = int(instr['rs2_w1_val'])
            if 'imm_val' in instr:
                if self.fmt in ['jformat','bformat'] or instr['inst'] in \
                        ['c.beqz','c.bnez','c.jal','c.j','c.jalr']:
                    imm_val = (-1 if instr['label'] == '1b' else 1) * int(instr['imm_val'])
                else:
                    imm_val = int(instr['imm_val'])
            if 'rs2' in instr:
                rs2 = instr['rs2']
            if 'rd' in instr:
                rd = instr['rd']
            if 'rs1' in instr:
                rs1 = instr['rs1']
            if 'rs3' in instr:
                rs3 = instr['rs3']
            if 'val_comb' in coverpoints:
                valcomb_hits = set([])
                for coverpoint in coverpoints['val_comb']:
	                fs1=fe1=fm1=fs2=fe2=fm2=fs3=fe3=fm3=None
	                bin_val = ''
	                e_sz = 0
	                m_sz = 0
	                if self.opcode[0] == 'f' and 'fence' not in self.opcode and 'fcvt.s.w' not in self.opcode and 'fcvt.s.wu' not in self.opcode and 'fmv.w.x' not in self.opcode and "fsw" not in self.opcode and "fcvt.s.l" not in self.opcode and 'fcvt.s.lu' not in self.opcode and 'fcvt.d.w' not in self.opcode and 'fcvt.d.wu' not in self.opcode and 'fcvt.d.l' not in self.opcode and 'fcvt.d.lu' not in self.opcode and 'fmv.d.x' not in self.opcode and "fld" not in self.opcode and "fsd" not in self.opcode:
	                    if (flen == 32):
	                        e_sz = 8
	                    else:
	                        e_sz = 11
	                    if (flen == 32):
	                        m_sz = 23
	                    else:
	                        m_sz = 52
	                    if 'rs1_val' in instr:
	                        if (flen == 32):
	                            bin_val = '{:032b}'.format(rs1_val)
	                        else:
	                            bin_val = '{:064b}'.format(rs1_val)
	                        fs1 = int(bin_val[0],2)
	                        fe1 = int(bin_val[1:e_sz+1],2)
	                        fm1 = int(bin_val[e_sz+1:],2)
	                    if 'rs2_val' in instr:
	                        if (flen == 32):
	                            bin_val = '{:032b}'.format(rs2_val)
	                        else:
	                            bin_val = '{:064b}'.format(rs2_val)
	                        fs2 = int(bin_val[0],2)
	                        fe2 = int(bin_val[1:e_sz+1],2)
	                        fm2 = int(bin_val[e_sz+1:],2)
	                    if 'rs3_val' in instr:
	                        if (flen == 32):
	                            bin_val = '{:032b}'.format(rs3_val)
	                        else:
	                            bin_val = '{:064b}'.format(rs3_val)
	                        fs3 = int(bin_val[0],2)
	                        fe3 = int(bin_val[1:e_sz+1],2)
	                        fm3 = int(bin_val[e_sz+1:],2)
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
            if 'rs3' in coverpoints:
                if rs3 in coverpoints['rs3']:
                    cover_hits['rs3'] = set([rs3])

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
                    if instr['rs1'] == 'x0' or instr['rs1'] == 'f0':
                        skip_val = True
                if 'rs2' in instr:
                    if instr['rs2'] == 'x0' or instr['rs2'] == 'f0':
                        skip_val = True
                if 'rd' in instr:
                    if instr['rd'] == 'x0' or instr['rd'] == 'f0':
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

        if self.opnode['isa'] == 'IP':
            if 'p64_profile' in self.opnode:
                gen_pair_reg_data(final_instr, xlen, self.opnode['bit_width'], self.opnode['p64_profile'])
            elif 'bit_width' in self.opnode:
                concat_simd_data(final_instr, xlen, self.opnode['bit_width'])

        return final_instr

    def swreg(self, instr_dict):
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
        :param instr_dict: list of dictionaries containing the various values necessary for the macro
        :type instr_dict: list
        :return: list of dictionaries containing the various values necessary for the macro
        '''
        if self.opcode[0] == 'f' and 'fence' not in self.opcode:
           offset = 0
           val_offset = 0
           hardcoded_regs = ['x15','x16','x17']
           flag = True
           for i in range(len(instr_dict)):
                if 'swreg' not in instr_dict[i]:
                    instr_dict[i]['swreg'] = 'x15'
                    instr_dict[i]['valaddr_reg'] = 'x16'
                    instr_dict[i]['flagreg'] = 'x17'
                    if self.opcode in ['fsw','fsd']:
                        if instr_dict[i]['rs1'] in hardcoded_regs:
                            instr_dict[i]['swreg'] = 'x19'
                            instr_dict[i]['valaddr_reg'] = 'x20'
                            instr_dict[i]['flagreg'] = 'x21'
                            if not flag:
                                offset = 0
                                flag = True
                        elif flag:
                            offset = 0
                            flag = False
                    elif instr_dict[i]['rs1'] in hardcoded_regs or instr_dict[i]['rd'] in hardcoded_regs:
                        instr_dict[i]['swreg'] = 'x19'
                        instr_dict[i]['valaddr_reg'] = 'x20'
                        instr_dict[i]['flagreg'] = 'x21'
                        if not flag:
                            flag = True
                            offset = 0
                    elif flag:
                        offset = 0
                        flag = False
                    instr_dict[i]['offset'] = str(offset)
                    instr_dict[i]['val_offset'] = str(val_offset)
                    offset += int((flen/8)+(xlen/8))
                    if self.fmt == 'frformat' or self.fmt == 'rformat':
                        val_offset += 2*(int(flen/8))
                    elif self.fmt == 'fsrformat':
                        val_offset += (int(flen/8))
                    elif self.fmt == 'fr4format':
                        val_offset += 3*(int(flen/8))
                    if offset >= 2030:
                        offset = 0
                    if val_offset >= 2030:
                        val_offset = 0
           return instr_dict

        paired_regs=0
        if xlen == 32 and 'p64_profile' in self.opnode:
            p64_profile = self.opnode['p64_profile']
            paired_regs = self.opnode['p64_profile'].count('p')

        regset = e_regset if 'e' in base_isa else default_regset
        total_instr = len(instr_dict)
        available_reg = regset.copy()
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
            if 'rs1_hi' in instr and instr['rs1_hi'] in available_reg:
                available_reg.remove(instr['rs1_hi'])
            if 'rs2_hi' in instr and instr['rs2_hi'] in available_reg:
                available_reg.remove(instr['rs2_hi'])
            if 'rd_hi' in instr and instr['rd_hi'] in available_reg:
                available_reg.remove(instr['rd_hi'])

            if len(available_reg) <= 1+len(self.op_vars)+paired_regs:
                curr_swreg = available_reg[0]
                offset = 0
                for i in range(assigned, count+1):
                    if 'swreg' not in instr_dict[i]:
                        next_offset = offset + int(xlen/8)*self.stride
                        if next_offset > 2048:
                            offset = 0
                            next_offset = 0
                        instr_dict[i]['swreg'] = curr_swreg
                        instr_dict[i]['offset'] = str(offset)
                        offset = next_offset
                        assigned += 1
                available_reg = regset.copy()
                available_reg.remove('x0')
            count += 1
        if assigned != total_instr and len(available_reg) != 0:
            curr_swreg = available_reg[0]
            offset = 0
            for i in range(len(instr_dict)):
                if 'swreg' not in instr_dict[i]:
                    next_offset = offset + int(xlen/8)*self.stride
                    if next_offset > 2048:
                        offset = 0
                        next_offset = 0
                    instr_dict[i]['swreg'] = curr_swreg
                    instr_dict[i]['offset'] = str(offset)
                    offset = next_offset
        return instr_dict

    def testreg(self, instr_dict):
        '''
        This function is responsible for identifying which register can be used
        as a test register for each instruction.

        This register is calculated by traversing the dictionary of solutions
        created so far and removing all the registers which are used as either
        operands or destination or signature. When 3 or less registers are pending, one of
        those registers is used as test register for all the solutions
        traversed so far.

        Care is taken to never use 'x0' as test register.
        :param instr_dict: list of dictionaries containing the various values necessary for the macro
        :type instr_dict: list
        :return: list of dictionaries containing the various values necessary for the macro
        '''
        if self.opcode[0] == 'f' and 'fence' not in self.opcode:
            for i in range(len(instr_dict)):
                instr_dict[i]['testreg'] = 'x18'
                if self.opcode in ['fsw','fsd']:
                    if instr_dict[i]['rs1'] == 'x18':
                        instr_dict[i]['testreg'] = 'x22'
                elif instr_dict[i]['rs1'] == 'x18' or instr_dict[i]['rd'] == 'x18':
                    instr_dict[i]['testreg'] = 'x22'
            return instr_dict

        regset = e_regset if 'e' in base_isa else default_regset
        total_instr = len(instr_dict)
        available_reg = regset.copy()
        available_reg.remove('x0')
        count = 0
        assigned = 0

        paired_regs=0
        if xlen == 32 and 'p64_profile' in self.opnode:
            p64_profile = self.opnode['p64_profile']
            paired_regs = p64_profile.count('p')

        for instr in instr_dict:
            if 'rs1' in instr and instr['rs1'] in available_reg:
                available_reg.remove(instr['rs1'])
                if 'rs1_hi' in instr and instr['rs1_hi'] in available_reg:
                    available_reg.remove(instr['rs1_hi'])
            if 'rs2' in instr and instr['rs2'] in available_reg:
                available_reg.remove(instr['rs2'])
                if 'rs2_hi' in instr and instr['rs2_hi'] in available_reg:
                    available_reg.remove(instr['rs2_hi'])
            if 'rd' in instr and instr['rd'] in available_reg:
                available_reg.remove(instr['rd'])
                if 'rd_hi' in instr and instr['rd_hi'] in available_reg:
                    available_reg.remove(instr['rd_hi'])
            if 'swreg' in instr and instr['swreg'] in available_reg:
                available_reg.remove(instr['swreg'])

            if len(available_reg) <= 1+len(self.op_vars)+paired_regs:
                curr_testreg = available_reg[0]
                for i in range(assigned, count+1):
                    if 'testreg' not in instr_dict[i]:
                        instr_dict[i]['testreg'] = curr_testreg
                        assigned += 1
                available_reg = regset.copy()
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
        :param instr_dict: list of dictionaries containing the various values necessary for the macro
        :type instr_dict: list
        :return: list of dictionaries containing the various values necessary for the macro
        '''
        if self.opcode[0] == 'f' and 'fence' not in self.opcode:
            for i in range(len(instr_dict)):
                instr_dict[i]['correctval'] = '0'
            return instr_dict
        if xlen == 32 and 'p64_profile' in self.opnode:
            p64_profile = self.opnode['p64_profile']
            if len(p64_profile) >= 3 and p64_profile[0]=='p':
                for i in range(len(instr_dict)):
                    instr_dict[i]['correctval_hi'] = '0'
        if self.fmt in ['caformat','crformat']:
            normalise = lambda x,y: 0 if y['rs1']=='x0' else x
        else:
            normalise = (lambda x,y: x) if 'rd' not in self.op_vars else (lambda x,y: 0 if y['rd']=='x0' else x)
        if self.operation:
            for i in range(len(instr_dict)):
                for var in self.val_vars:
                    locals()[var]=int(instr_dict[i][var])
                correctval = eval(self.operation)
                instr_dict[i]['correctval'] = str(normalise(correctval,instr_dict[i]))
        else:
            for i in range(len(instr_dict)):
                instr_dict[i]['correctval'] = '0x' + '0'.zfill(int(xlen/4))
        return instr_dict

    def reformat_instr(self, instr_dict):
        '''
        This function basically sanitizes the integer values to a readable
        hex values
        :param instr_dict: list of dictionaries containing the various values necessary for the macro
        :type instr_dict: list
        :return: list of dictionaries containing the various values necessary for the macro
        '''
        mydict = instr_dict.copy()

        if self.opnode['isa'] == 'IP':
            if (xlen == 32 and 'p64_profile' in self.opnode) or 'bit_width' in self.opnode:
                return mydict

        for i in range(len(instr_dict)):
            for field in instr_dict[i]:
                # if xlen == 32:
                #     if instr_dict[i]['inst'] in ['sltu', 'sltiu', 'bgeu', 'bltu']:
                #         size = '>I'
                #     else:
                #         size = '>i'
                # else:
                #     if instr_dict[i]['inst'] in ['sltu', 'sltiu', 'bgeu', 'bltu']:
                #         size = '>Q'
                #     else:
                #         size = '>q'
                if 'val' in field and field != 'correctval' and field != 'valaddr_reg' and field != 'val_offset':
                    value = instr_dict[i][field]
                    if '0x' in value:
                        value = '0x' + value[2:].zfill(int(xlen/4))
                        value = struct.unpack(size, bytes.fromhex(value[2:]))[0]
                    else:
                        value = int(value)
#                    value = '0x' + struct.pack(size,value).hex()
                    instr_dict[i][field] = hex(value)
        return instr_dict

    def write_test(self, fprefix, node, label, instr_dict, op_node, usage_str,max_inst):
        start = 0
        total = len(instr_dict)
        end = len(instr_dict)
        if max_inst:
            end = max_inst
        else:
            max_inst = total
        i = 1
        while end <= total and start<total:
            fname = fprefix+("-{:02d}.S".format(i))
            logger.debug("Writing Test to "+str(fname))
            self.__write_test__(fname,node,label,instr_dict[start:end], op_node, usage_str)
            start += max_inst
            left = total - end
            i+=1
            if left>=max_inst:
                end += max_inst
            else:
                end = total


    def __write_test__(self, file_name,node,label,instr_dict, op_node, usage_str):
        '''
        This function generates the test using various templates.

        :param file_name: path of the output file
        :param node: a covergroup in cgf format containing the set of coverpoints to be satisfied
        :param label: the label for the covergroup in the input cgf file
        :param instr_dict: list of dictionaries containing the various values necessary for the macro
        :param op_node: dictionary node from the attributes YAML that is to be used in the test generation
        :param usage_str: Banner string for the test

        :type file_name: str
        :type node: dict
        :type label: str
        :type instr_dict: list
        :type op_node: dict
        :type usage_str: str
        '''
        regs = defaultdict(lambda: 0)
        sreg = instr_dict[0]['swreg']
        vreg = 0
        code = []
        sign = [""]
        data = [".align 4","rvtest_data:",".word 0xbabecafe", \
                ".word 0xabecafeb", ".word 0xbecafeba", ".word 0xecafebab"]
        stride = self.stride
        if self.opcode[0] == 'f' and 'fence' not in self.opcode:
            vreg = instr_dict[0]['valaddr_reg']
            k = 0
            if self.opcode not in ['fsw','flw']:
                data.append("test_fp:")
            code.append("RVTEST_FP_ENABLE()")

        if xlen == 32 and 'p64_profile' in self.opnode:
            p64_profile = self.opnode['p64_profile']

        n = 0
        opcode = instr_dict[0]['inst']
        op_node_isa = ""
        extension = ""
        rvxlen = "RV"+str(xlen)
        op_node_isa = ",".join([rvxlen + isa for isa in op_node['isa']])
        op_node_isa = op_node_isa.replace("I","E") if 'e' in base_isa else op_node_isa
        extension = op_node_isa.replace('I',"").replace('E',"")
        count = 0
        neg_offset = 0
        for instr in instr_dict:
            res = '\ninst_{0}:'.format(str(count))
            res += Template(op_node['template']).safe_substitute(instr)
            if self.opcode[0] == 'f' and 'fence' not in self.opcode:
                if self.fmt == 'frformat' or self.fmt == 'rformat':
                    if flen == 32:
                        data.append(".word "+instr["rs1_val"])
                        data.append(".word "+instr["rs2_val"])
                    elif flen == 64:
                        data.append(".dword "+instr["rs1_val"])
                        data.append(".dword "+instr["rs2_val"])
                elif self.fmt == 'fsrformat':
                    if flen == 32:
                        data.append(".word "+instr["rs1_val"])
                    elif flen == 64:
                        data.append(".dword "+instr["rs1_val"])
                elif self.fmt == 'fr4format':
                    if flen == 32:
                        data.append(".word "+instr["rs1_val"])
                        data.append(".word "+instr["rs2_val"])
                        data.append(".word "+instr["rs3_val"])
                    elif flen == 64:
                        data.append(".dword "+instr["rs1_val"])
                        data.append(".dword "+instr["rs2_val"])
                        data.append(".dword "+instr["rs3_val"])
                if self.opcode not in ['fsw','flw']:
                    if instr['val_offset'] == '0' and k == 0:
                        code.append("RVTEST_VALBASEUPD("+vreg+",test_fp)")
                        k = 1;
                    elif instr['val_offset'] == '0' and k!= 0:
                        if instr['inst'] in three_operand_dinstructions + three_operand_finstructions:
                            code.append("addi "+vreg+","+vreg+","+str(2040))
                        elif instr['inst'] in one_operand_dinstructions + two_operand_dinstructions + one_operand_finstructions + two_operand_finstructions:
                            code.append("addi "+vreg+","+vreg+","+str(2032))
                        else:
                            code.append("RVTEST_VALBASEUPD("+vreg+")")
                    if instr['valaddr_reg'] != vreg:
                        code.append("RVTEST_VALBASEMOV("+instr['valaddr_reg']+", "+vreg+")")
                        vreg = instr['valaddr_reg']
            if instr['swreg'] != sreg or instr['offset'] == '0':
                sign.append(signode_template.substitute({'n':n,'label':"signature_"+sreg+"_"+str(regs[sreg])}))
                n = stride
                regs[sreg]+=1
                sreg = instr['swreg']
                code.append("RVTEST_SIGBASE("+sreg+",signature_"+sreg+"_"+str(regs[sreg])+")")
            else:
                n+=stride
            code.append(res)
            count = count + 1
        case_str = ''.join([case_template.safe_substitute(xlen=xlen,num=i,cond=cond,cov_label=label) for i,cond in enumerate(node['config'])])
        sign.append(signode_template.substitute({'n':n,'label':"signature_"+sreg+"_"+str(regs[sreg])}))
        test = part_template.safe_substitute(case_str=case_str,code='\n'.join(code))
        sign.append("#ifdef rvtest_mtrap_routine\n"+signode_template.substitute({'n':64,'label':"mtrap_sigptr"})+"\n#endif\n")
        sign.append("#ifdef rvtest_gpr_save\n"+signode_template.substitute({'n':32,'label':"gpr_save"})+"\n#endif\n")
        with open(file_name,"w") as fd:
            fd.write(usage_str + test_template.safe_substitute(data='\n'.join(data),test=test,sig='\n'.join(sign),isa=op_node_isa,opcode=opcode,extension=extension,label=label))
