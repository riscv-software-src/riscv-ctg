# See LICENSE.incore for details
import re

from riscv_ctg.log import logger
from riscv_ctg.constants import *

CSR_REGS = ['mvendorid', 'marchid', 'mimpid', 'mhartid', 'mstatus', 'misa', 'medeleg', 'mideleg', 'mie', 'mtvec', 'mcounteren', 'mscratch', 'mepc', 'mcause', 'mtval', 'mip', 'pmpcfg0', 'pmpcfg1', 'pmpcfg2', 'pmpcfg3', 'mcycle', 'minstret', 'mcycleh', 'minstreth', 'mcountinhibit', 'tselect', 'tdata1', 'tdata2', 'tdata3', 'dcsr', 'dpc', 'dscratch0', 'dscratch1', 'sstatus', 'sedeleg', 'sideleg', 'sie', 'stvec', 'scounteren', 'sscratch', 'sepc', 'scause', 'stval', 'sip', 'satp', 'vxsat', 'fflags', 'frm', 'fcsr']

csr_comb_covpt_regex_string = f'({"|".join(CSR_REGS)})' + r' *& *([^ ].*)== *([^ ].*)'
csr_comb_covpt_regex = re.compile(csr_comb_covpt_regex_string)

class GeneratorCSRComb():
    '''
    A class to generate RISC-V assembly tests for CSR-combination coverpoints.
    '''

    def __init__(self, base_isa, xlen, randomize):
        self.base_isa = base_isa
        self.xlen = xlen
        self.randomize = randomize

    def csr_comb(self, cgf_node):
        logger.debug('Generating tests for csr_comb')
        if 'csr_comb' in cgf_node:
            csr_comb = set(cgf_node['csr_comb'])
        else:
            return

        # This function extracts the csr register, the field mask and the field value from the coverpoint
        # The coverpoint is assumed of the format: 'csr_reg & mask == val'
        # csr_reg must be a valid csr register; mask and val are allowed to be valid python expressions
        def get_csr_reg_field_mask_and_val(coverpoint):
            regex_match = csr_comb_covpt_regex.match(coverpoint.strip())
            if regex_match is None:
                return None, None, None
            csr_reg, mask_expr, val_expr = regex_match.groups()
            mask = eval(mask_expr)
            val = eval(val_expr)
            return csr_reg, mask, val

        temp_regs = ['x28', 'x29'] # t0 and t1
        dest_reg = 'x23'

        instr_dict = []
        offset = 0
        for covpt in csr_comb:
            csr_reg, mask, val = get_csr_reg_field_mask_and_val(covpt)
            if csr_reg is None:
                logger.error(f'Invalid csr_comb coverpoint: {covpt}')
                continue
            instr_dict.append({
                'csr_reg': csr_reg, 'mask': hex(mask), 'val': hex(val), 'dest_reg': dest_reg,
                'temp_reg1': temp_regs[0], 'temp_reg2': temp_regs[1], 'offset': offset
            })
            offset += 4

        return instr_dict

    def write_test(self, fprefix, cgf_node, usage_str, cov_label, instr_dict):
        base_reg = 'x8'

        code = [""]
        data = [".align 4","rvtest_data:",".word 0xbabecafe", \
                ".word 0xabecafeb", ".word 0xbecafeba", ".word 0xecafebab"]
        sig = [""]

        sig_label = f"signature_{base_reg}_0"
        sig.append(signode_template.safe_substitute(label = sig_label, n = len(instr_dict), sz = 'XLEN/32'))
        code.append(f"RVTEST_SIGBASE({base_reg}, {sig_label})\n")

        for i, instr in enumerate(instr_dict):
            code.extend([
                f"\ninst_{i}:",
                csr_reg_write_test_template.safe_substitute({
                    'base_reg': base_reg, **instr
                })
            ])

        case_str = ''.join([case_template.safe_substitute(xlen = self.xlen, num = i, cov_label = cov_label) for i, cond in enumerate(cgf_node.get('config', []))])
        test_str = part_template.safe_substitute(case_str = case_str, code = '\n'.join(code))

        with open(fprefix + '_csr-comb.S', 'w') as fp:
            fp.write(usage_str + csr_comb_test_template.safe_substitute(
                isa = self.base_isa.upper(), # how to get the extensions?
                test = test_str,
                data = '\n'.join(data),
                sig = '\n'.join(sig),
                label = cov_label
            ))
