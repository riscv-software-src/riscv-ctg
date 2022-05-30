import re

num_dict = {
        'rs1_val': '1',
        'rs2_val': '2',
        'rs3_val': '3',
}
fsub_vars = ['fe','fm','fs']

val_regex = "{0}\s*==\s*(?P<{0}>[0-9abcdefx+\-\*/\|\&]*)\s*"

def extract_frs_fields(reg,cvp,iflen):
    if (iflen == 32):
        e_sz = 8
        m_sz = 23
    else:
        e_sz = 11
        m_sz = 52
    s_sz_string = '{:01b}'
    e_sz_string = '{:0'+str(e_sz)+'b}'
    m_sz_string = '{:0'+str(m_sz)+'b}'
    size_string = '{:0'+str(int(flen/4))+'x}'
    fvals = {}
    for var in fsub_vars:
        regex = val_regex.format(var+reg)
        match_obj = re.search(regex,cvp)
        if match_obj is not None:
            fvals[var+reg] = eval(match_obj.group(var+reg))
        else:
            raise Exception
    bin_val1 = s_sz_string.format(fvals['fs'+reg]) + e_sz_string.format(int(fvals['fe'+reg],16)) \
            + m_sz_string.format(int(fvals['fm'+reg],16))
    hex_val1 = '0x' + size_string.format(int(bin_val1, 2))
    return hex_val1

def merge_fields_f(val_vars,cvp,flen,iflen):
    nan_box = False
    if flen > iflen:
        nan_box = True
    fdict = {}
    for var in val_vars:
        if var in num_dict:
            fdict[var] = extract_frs_fields(num_dict['var'],cvp,iflen)
            if nan_box:
                nan_var = 'nan_box_rs'+num_dict['var']
                regex = val_regex.format(nan_var.replace("_","\\_"))
                match_obj = re.search(regex,cvp)
                if match_obj is not None:
                    fdict[nan_var] = hex(eval(match_obj.group(nan_var)))
                else:
                    fdict[nan_var] = '0x'+'f'*int((flen-iflen)/4)

        else:
            regex = val_regex.format(var.replace("_","\\_"))
            match_obj = re.search(regex,cvp)
            if match_obj is not None:
                fdict[var] = hex(eval(match_obj.group(var)))
            else:
                raise Exception


