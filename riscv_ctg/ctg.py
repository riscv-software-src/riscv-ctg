# See LICENSE.incore file for details

from riscv_ctg.log import logger
import riscv_ctg.utils as utils
import riscv_ctg.constants as const
from riscv_ctg.iformat import *
from riscv_ctg.rformat import *
from riscv_ctg.uformat import *
from riscv_ctg.bformat import *
from collections import defaultdict
from riscv_isac.cgf_normalize import expand_cgf

def create_test(file_name,node,label,instr_dict, op_node):
    regs = defaultdict(lambda: 0)
    sreg = instr_dict[0]['swreg']
    code = ["la "+sreg+",signature_"+sreg+"_"+str(regs[sreg])]
    sign = [".align 4"]
    data = [".align 4"]
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
        fd.write(const.test_template.safe_substitute(data='\n'.join(data),test=test,sig='\n'.join(sign),isa="RV32I"))

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
        op_comb = eval(formattype+'_opcomb(node,randomize)')
        val_comb = eval(formattype+'_valcomb(node, op_node,randomize)')

        instr_dict = eval(formattype+'_inst(op_comb, val_comb, node, op_node)')
        append_swreg = eval(formattype+'_swreg(instr_dict)')
        append_testreg = eval(formattype+'_testreg(append_swreg)')
        instr_dict = eval(formattype+'_correct_val(append_testreg, op_node)')

        logger.info("Writing test to "+str(fname))
        create_test(fname,node,label,instr_dict, op_node)
