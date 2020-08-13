# See LICENSE.incore file for details

import os,re

from riscv_ctg.log import logger
import riscv_ctg.utils as utils
import riscv_ctg.constants as const
from collections import defaultdict
from riscv_isac.cgf_normalize import expand_cgf
from riscv_ctg.generator import Generator

def create_test(file_name,node,label,instr_dict, op_node):
    regs = defaultdict(lambda: 0)
    sreg = instr_dict[0]['swreg']
    code = ["la "+sreg+",signature_"+sreg+"_"+str(regs[sreg])]
    sign = [".align 4"]
    data = [".align 4","rvtest_data:",".word 0xbabecafe"]
    n = 0
    for instr in instr_dict:
        res = op_node['template']
        for value in sorted(instr.keys(), key = len, reverse = True):
            res = re.sub(value, instr[value], res)
        if instr['swreg'] != sreg:
            sign.append(const.signode_template.substitute({'n':n,'label':"signature_"+sreg+"_"+str(regs[sreg])}))
            n = 1
            regs[sreg]+=1
            sreg = instr['swreg']
            code.append("la "+sreg+",signature_"+sreg+"_"+str(regs[sreg]))
        else:
            n+=1
        code.append(res)
    sign.append(const.signode_template.substitute({'n':n,'label':"signature_"+sreg+"_"+str(regs[sreg])}))
    test = const.case_template.safe_substitute(num=1,cond=node['config'],code='\n'.join(code),cov_label=label)
    with open(file_name,"w") as fd:
        fd.write(const.test_template.safe_substitute(data='\n'.join(data),test=test,sig='\n'.join(sign),isa="RV32"+op_node['isa']))

def ctg(verbose, out_dir, randomize ,xlen, cgf_file):

    cgf_op = utils.load_yaml(const.template_file)
    cgf = expand_cgf(utils.load_yaml(cgf_file),int(xlen))
    for label,node in cgf.items():
        if 'opcode' not in node:
            continue
        opcode = node['opcode']
        if opcode not in cgf_op:
            logger.info("Skipping :" + str(opcode))
            continue
        op_node = cgf_op[opcode]
        fname = os.path.join(out_dir,str(label.capitalize()+".S"))

        logger.info('Generating Test for :' + opcode)
        formattype  = cgf_op[opcode]['formattype']
        gen = Generator(formattype,op_node,opcode,randomize)
        op_comb = gen.opcomb(node)
        val_comb = gen.valcomb(node)
        instr_dict = gen.correct_val(gen.testreg(gen.swreg(gen.gen_inst(op_comb, val_comb, node))))

        logger.info("Writing test to "+str(fname))
        create_test(fname,node,label,instr_dict, op_node)
