def get_generator(opcode):
    def fr_generator(val_vars,req_val_comb):
        def condition(*argv):
            rs1_val = argv[0]
            rs2_val = argv[1]
            rm = argv[2]
            bin_val = '{:032b}'.format(rs1_val)
            fs1 = int(bin_val[0],2)
            fe1 = int(bin_val[1:9],2)
            fm1 = int(bin_val[9:],2)
            bin_val = '{:032b}'.format(rs2_val)
            fs2 = int(bin_val[0],2)
            fe2 = int(bin_val[1:9],2)
            fm2 = int(bin_val[9:],2)
            return eval(req_val_comb)
        return condition

    def i_generator(val_vars,req_val_comb):
        def condition(*argv):
            for var,val in zip(val_vars,argv):
                locals()[var]=val
            return eval(req_val_comb)
        return condition

    if opcode[0] == 'f':
        return fr_generator
    else:
        return i_generator
