# See LICENSE.incore file for details

import os,re
import multiprocessing as mp

import time
import shutil
from riscv_ctg.log import logger
import riscv_ctg.utils as utils
import riscv_ctg.constants as const
from riscv_isac.cgf_normalize import expand_cgf
from riscv_ctg.generator import Generator
from math import *
from riscv_ctg.__init__ import __version__

def create_test(usage_str, node,label,base_isa,max_inst):
    global op_template
    global ramdomize
    global out_dir
    global xlen

    flen = 0
    if 'opcode' not in node:
        return
    if 'ignore' in node:
        logger.info("Ignoring :" + str(label))
        if node['ignore']:
            return
    for opcode in node['opcode']:
        op_node=None
        if opcode not in op_template:
            for op,foo in op_template.items():
                if op!='metadata' and foo['std_op'] is not None and opcode==foo['std_op']:
                    op_node = foo
                    break
        else:
            op_node = op_template[opcode]

        if op_node is  None:
            logger.warning("Skipping :" + str(opcode))
            return
        if xlen not in op_node['xlen']:
            logger.warning("Skipping {0} since its not supported in current XLEN:".format(opcode))
            return
        if 'flen' in op_node:
            if '.d' in opcode:
                flen = 64
            elif '.s' in opcode:
                flen = 32
            else:
                flen = op_node['flen'][0]
            #if flen not in op_node['flen']:
            #    return
        fprefix = os.path.join(out_dir,str(label))
        logger.info('Generating Test for :' + str(label) +"-" + opcode)
        formattype  = op_node['formattype']
        gen = Generator(formattype,op_node,opcode,randomize,xlen,flen,base_isa)
        op_comb = gen.opcomb(node)
        val_comb = gen.valcomb(node)
        instr_dict = gen.correct_val(gen.testreg(gen.swreg(gen.gen_inst(op_comb, val_comb, node))))
        logger.info("Writing tests for :"+str(label))
        my_dict = gen.reformat_instr(instr_dict)
        gen.write_test(fprefix,node,label,my_dict, op_node, usage_str, max_inst)

def ctg(verbose, out, random ,xlen_arg, cgf_file,num_procs,base_isa, max_inst):
    global op_template
    global randomize
    global out_dir
    global xlen
    logger.level(verbose)
    logger.info('****** RISC-V Compliance Test Generator {0} *******'.format(__version__ ))
    logger.info('Copyright (c) 2020, InCore Semiconductors Pvt. Ltd.')
    logger.info('All Rights Reserved.')
    logger.info("Copying env folder to Output directory.")
    env_dir = os.path.join(out,"env")
    if not os.path.exists(env_dir):
        shutil.copytree(const.env,env_dir)
    xlen = int(xlen_arg)
    out_dir = out
    randomize = random
    mytime = time.asctime(time.gmtime(time.time()) ) + ' GMT'
    cgf_argument = ''
    for cf in cgf_file:
        cgf_argument += '//                  --cgf {} \\\n'.format(cf)
    randomize_argument = ''
    if random is True:
        randomize_argument = ' \\\n//                  --randomize'
    usage_str = const.usage.safe_substitute(base_isa=base_isa, \
            cgf=cgf_argument, version = __version__, time=mytime, \
            randomize=randomize_argument,xlen=str(xlen_arg))
    op_template = utils.load_yaml(const.template_file)
    cgf = expand_cgf(cgf_file,xlen)
    pool = mp.Pool(num_procs)
    results = pool.starmap(create_test, [(usage_str, node,label,base_isa,max_inst) for label,node in cgf.items()])
    pool.close()

