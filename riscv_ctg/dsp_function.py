OPS_RVP = {
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
    'pswrrformat': ['rs1', 'rs2', 'rd']
}
''' Dictionary mapping RVP instruction formats to operands used by those formats '''

VALS_RVP = {
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
    'pswrrformat': 'simd_val_vars("rs1", xlen, 32) + ["rs2_val"]'
}
''' Dictionary mapping RVP instruction formats to operand value variables used by those formats '''

def simd_val_vars(operand, xlen, bit_width):
    '''
    This function generates the operand value variables for SIMD elements of the given operand.

    :param operand: a string indicating the name of the desired operand.
    :param xlen: an integer indicating the XLEN value to be used.
    :param bit_width: an integer indicating the element bit width for the current SIMD format.

    :type operand: str
    :type xlen: int
    :type bit_width: int
    :return: a list containing the element value variables for the given operand.
    '''
    val_list = []
    nelms = xlen // bit_width
    if bit_width == 8:
        sz = "b"
    elif bit_width == 16:
        sz = "h"
    elif bit_width == 32:
        sz = "w"
    else:
        sz = "d"
    for i in range(nelms):
        val_list += [f"{operand}_{sz}{i}_val"]
    return val_list

def init_rvp_ops_vals(OPS, VALS):
    '''
    This function updates the OPS and VALS dictionaries (the dictionaries for operands and operand value variables) with the RVP counter parts.

    :param OPS: the dict mapping instruction formats to operands used by those formats.
    :param VALS: the dict mapping instruction formats to operand value variables used by those formats.

    :type OPS: dict
    :type VALS: dict
    '''
    OPS.update(OPS_RVP)
    VALS.update(VALS_RVP)
    
def concat_simd_data(instr_dict, xlen, bit_width):
    '''
    This function concatenates all element of a SIMD register into a single value in the hex format.

    :param instr_dict: a dict holding metadata and operand data for the current instruction. 
    :param xlen: an integer indicating the XLEN value to be used.
    :param bit_width: an integer indicating the element bit width of the current RVP instruction.

    :type instr_dict: dict
    :type xlen: int
    :type bit_width: int
    '''
    twocompl_offset = 1<<bit_width
    if bit_width == 8:
        fmt = f"#02x"
    elif bit_width == 16:
        fmt = f"#04x"
    elif bit_width == 32:
        fmt = f"#08x"
    else:
        fmt = f"#016x"
    if bit_width == 8:
        sz = "b"
    elif bit_width == 16:
        sz = "h"
    elif bit_width == 32:
        sz = "w"
    else:
        sz = "d"
    for instr in instr_dict:
        if 'rs1' in instr:
            if 'rs1_val' in instr:  # single element value
                rs1_val = int(instr['rs1_val'])
                if rs1_val < 0:
                    rs1_val = rs1_val + twocompl_offset
                instr['rs1_val'] = format(rs1_val, f"#0x")
            else:   # concatenates all element of a SIMD register into a single value
                rs1_val = 0
                for i in range(xlen//bit_width):
                    val_var = f"rs1_{sz}{i}_val"
                    val = int(instr[val_var])
                    if val < 0:
                        val = val + twocompl_offset
                    rs1_val += val << (i*bit_width)
                instr['rs1_val'] = format(rs1_val, f"#0{xlen//4}x")
        if 'rs2' in instr:
            if 'rs2_val' in instr:  # single element value
                rs2_val = int(instr['rs2_val'])
                if rs2_val < 0:
                    rs2_val = rs2_val + twocompl_offset
                instr['rs2_val'] = format(rs2_val, f"#0x")
            else:   # concatenates all element of a SIMD register into a single value
                rs2_val = 0
                for i in range(xlen//bit_width):
                    val_var = f"rs2_{sz}{i}_val"
                    val = int(instr[val_var])
                    if val < 0:
                        val = val + twocompl_offset
                    rs2_val += val << (i*bit_width)
                instr['rs2_val'] = format(rs2_val, f"#0{xlen//4}x")
        if 'imm_val' in instr:
            imm_val = int(instr['imm_val'])
            instr['imm_val'] = format(imm_val, f"#0x")
