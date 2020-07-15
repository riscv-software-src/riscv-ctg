# See LICENSE.incore file for details

from riscv_ctg.log import logger
import riscv_ctg.utils as utils
import riscv_ctg.constants as const
from riscv_ctg.iformat import *
from riscv_ctg.rformat import *

def create_instr(instr_dict, op_node):
    for instr in instr_dict:
        res = op_node['template']
        for value in sorted(instr.keys(), key = len, reverse = True):
            res = re.sub(value, instr[value], res)
        print(res)
    return instr_dict

def ctg(verbose, out_dir, randomize ,xlen, cgf_file):

    cgf_op = utils.load_yaml(const.template_file)
    cgf = utils.load_yaml(cgf_file)
    for label,node in cgf.items():
        opcode = node['opcode']
        op_node = cgf_op[opcode]
        print('Generating Test for :' + opcode )
        formattype  = cgf_op[opcode]['formattype']
        op_comb = eval(formattype+'_opcomb(node,randomize)')
        val_comb = eval(formattype+'_valcomb(node, op_node,randomize)')

        instr_dict = eval(formattype+'_inst(op_comb, val_comb, node, op_node)')
        append_swreg = eval(formattype+'_swreg(instr_dict)')
        append_testreg = eval(formattype+'_testreg(append_swreg)')
        instr_dict = eval(formattype+'_correct_val(append_testreg, op_node)')

        create_instr(instr_dict, op_node)
