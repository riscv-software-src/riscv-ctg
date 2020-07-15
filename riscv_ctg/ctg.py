# See LICENSE.incore file for details

from riscv_ctg.log import logger
import riscv_ctg.utils as utils
import riscv_ctg.constants as const
from riscv_ctg.iformat import *
from riscv_ctg.rformat import *

def create_test(file_name,node,label,instr_dict, op_node):
    sreg = instr_dict[0]['swreg']
    code = ["la "+sreg+",signature_"+sreg]
    sign = [".align 4"]
    data = [".align 4"]
    n = 0
    for instr in instr_dict:
        res = op_node['template']
        for value in sorted(instr.keys(), key = len, reverse = True):
            res = re.sub(value, instr[value], res)
        if instr['swreg'] != sreg:
            sign.append(const.signode_template.substitute({'n':n,'label':"signature_"+sreg}))
            n = 1
            sreg = instr['swreg']
            code.append("la "+sreg+",signature_"+sreg)
        else:
            n+=1
        code.append(res)
    sign.append(const.signode_template.substitute({'n':n,'label':"signature_"+sreg}))
    test = const.case_template.safe_substitute(num=1,cond=node['config'],code='\n'.join(code),cov_label=label)
    with open(file_name,"w") as fd:
        fd.write(const.test_template.safe_substitute(data='\n'.join(data),test=test,sig='\n'.join(sign),isa="RV32I"))

def ctg(verbose, out_dir, randomize ,xlen, cgf_file):

    cgf_op = utils.load_yaml(const.template_file)
    cgf = utils.load_yaml(cgf_file)
    for label,node in cgf.items():
        opcode = node['opcode']
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
