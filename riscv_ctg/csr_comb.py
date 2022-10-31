# See LICENSE.incore for details
import re
from riscv_ctg.log import logger

CSR_REGS = ['mvendorid', 'marchid', 'mimpid', 'mhartid', 'mstatus', 'misa', 'medeleg', 'mideleg', 'mie', 'mtvec', 'mcounteren', 'mscratch', 'mepc', 'mcause', 'mtval', 'mip', 'pmpcfg0', 'pmpcfg1', 'pmpcfg2', 'pmpcfg3', 'mcycle', 'minstret', 'mcycleh', 'minstreth', 'mcountinhibit', 'tselect', 'tdata1', 'tdata2', 'tdata3', 'dcsr', 'dpc', 'dscratch0', 'dscratch1', 'sstatus', 'sedeleg', 'sideleg', 'sie', 'stvec', 'scounteren', 'sscratch', 'sepc', 'scause', 'stval', 'sip', 'satp', 'vxsat', 'fflags', 'frm', 'fcsr']

csr_comb_covpt_regex_string = f'({"|".join(CSR_REGS)})' + r' *& *([^ ].*)== *([^ ].*)'
csr_comb_covpt_regex = re.compile(csr_comb_covpt_regex_string)

class GeneratorCSRComb():
    '''
    A class to generate RISC-V assembly tests for CSR-combination coverpoints.
    '''

    def __init__(self, mxlen):
        self.mxlen = mxlen

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
            csr_reg, mask, val = regex_match.groups()
            return csr_reg, mask, val

        for covpt in csr_comb:
            csr, mask, val = get_csr_reg_field_mask_and_val(covpt)
            if csr is None:
                logger.error(f'Invalid csr_comb coverpoint: {covpt}')
            print(csr, mask, val)

