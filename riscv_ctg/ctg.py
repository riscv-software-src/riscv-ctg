# See LICENSE.incore file for details

import os,re
import multiprocessing as mp

from riscv_ctg.log import logger
import riscv_ctg.utils as utils
import riscv_ctg.constants as const
from riscv_isac.cgf_normalize import expand_cgf
from riscv_ctg.generator import Generator
from math import *

def create_test(node,label):
    global cgf_op
    global ramdomize
    global out_dir
    global xlen
    if 'opcode' not in node:
        return
    if 'ignore' in node:
        logger.info("Ignoring :" + str(label))
        if node['ignore']:
            return
    for opcode in node['opcode']:
        if opcode not in cgf_op:
            logger.info("Skipping :" + str(opcode))
            return
        op_node = cgf_op[opcode]
        if xlen not in op_node['xlen']:
            return
        fname = os.path.join(out_dir,str(label+".S"))
        logger.info('Generating Test for :' + opcode)
        formattype  = op_node['formattype']
        gen = Generator(formattype,op_node,opcode,randomize,xlen)
        op_comb = gen.opcomb(node)
        val_comb = gen.valcomb(node)
        instr_dict = gen.correct_val(gen.testreg(gen.swreg(gen.gen_inst(op_comb, val_comb, node))))
        logger.info("Writing test to "+str(fname))
        mydict = gen.reformat_instr(instr_dict)
        gen.write_test(fname,node,label,mydict, op_node)

def ctg(verbose, out, random ,xlen_arg, cgf_file,num_procs):
    global cgf_op
    global randomize
    global out_dir
    global xlen
    xlen = int(xlen_arg)
    out_dir = out
    randomize = random
    cgf_op = utils.load_yaml(const.template_file)
    cgf = expand_cgf(utils.load_yaml(cgf_file),xlen)
    pool = mp.Pool(num_procs)
    results = pool.starmap(create_test,[(node,label) for label,node in cgf.items()])
    pool.close()
#    for label, node in cgf.items():
#        create_test(node, label)

