def simd_val_vars(prefix, xlen, bit_width):
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
        val_list += [f"{prefix}_{sz}{i}_val"]
    return val_list

OPS_RVP = {
    'pb4rrformat': ['rs1', 'rs2', 'rd'],
    'pb8rrformat': ['rs1', 'rs2', 'rd'],
    'ph2rrformat': ['rs1', 'rs2', 'rd'],
    'ph4rrformat': ['rs1', 'rs2', 'rd'],
    'pb4rformat': ['rs1', 'rd'],
    'pb8rformat': ['rs1', 'rd'],
    'ph2rformat': ['rs1', 'rd'],
    'ph4rformat': ['rs1', 'rd'],
    'pb4riformat': ['rs1', 'rd'],
    'pb8riformat': ['rs1', 'rd']
}

VALS_RVP = {
    'pb4rrformat': simd_val_vars("rs1", 32, 8) + simd_val_vars("rs2", 32, 8),
    'pb8rrformat': simd_val_vars("rs1", 64, 8) + simd_val_vars("rs2", 64, 8),
    'ph2rrformat': simd_val_vars("rs1", 32, 16) + simd_val_vars("rs2", 32, 16),
    'ph4rrformat': simd_val_vars("rs1", 64, 16) + simd_val_vars("rs2", 64, 16),
    'pb4rformat': simd_val_vars("rs1", 32, 8),
    'pb8rformat': simd_val_vars("rs1", 64, 8),
    'ph2rformat': simd_val_vars("rs1", 32, 16),
    'ph4rformat': simd_val_vars("rs1", 64, 16),
    'pb4riformat': simd_val_vars("rs1", 32, 8) + ['imm_val'],  
    'pb8riformat': simd_val_vars("rs1", 64, 8) + ['imm_val']
}

def init_rvp_ops_vals(OPS, VALS):
    OPS.update(OPS_RVP)
    VALS.update(VALS_RVP)
    
def concat_simd_data(val_vars, instr_dict, xlen, bit_width):
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
            rs1_val = 0
            for i in range(xlen//bit_width):
                val_var = f"rs1_{sz}{i}_val"
                val = int(instr[val_var])
                if val < 0:
                    val = val + twocompl_offset
                rs1_val += val << (i*bit_width)
            instr['rs1_val'] = format(rs1_val, f"#0{xlen//4}x")
        if 'rs2' in instr:
            rs2_val = 0
            for i in range(xlen//bit_width):
                val_var = f"rs2_{sz}{i}_val"
                val = int(instr[val_var])
                if val < 0:
                    val = val + twocompl_offset
                rs2_val += val << (i*bit_width)
            instr['rs2_val'] = format(rs2_val, f"#0{xlen//4}x")
