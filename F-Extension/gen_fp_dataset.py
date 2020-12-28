def opcode_to_sign(opcode):
	opcode_dict = {
		'fadd'    : '+2',
		'fsub'    : '-2',
		'fmul'    : '*2',
		'fdiv'    : '/2',
		'fmadd'   : '*+3',
		'fsqrt'   : 'V1',
		'fmin'    : '<C',
		'fmax'    : '>C',
		'fcvt.w.s': 'cfi',
		'fcvt.s.w': 'cif',
		'fmv.x.w' : 'cp',
		'fmv.w.x' : 'cp'
	}
	return(opcode_dict.get(opcode,"Invalid Opcode"))

def rounding_mode(rm):
	rm_dict = {
		'=0' : '000',
		'>'  : '011',
		'<'  : '010',
		'0'  : '001',
		'=^' : '100'
	}
	return(rm_dict.get(rm))

def gen_fp_dataset(flen, opcode):
	opcode=opcode.lower()
	rs1_dataset=[]								# Declaring empty datasets
	rs2_dataset=[]
	rs3_dataset=[]
	rm_dataset=[]
	rd_dataset=[]
	te_dataset=[]
	flags_dataset=[]
	
	f=open("Basic-Types-Inputs.fptest","r")
	for i in range(5):
		a=f.readline()
	
	i=0									# Initializing count of datapoints
	sign_ops=opcode_to_sign(opcode)
	if(sign_ops=="Invalid Opcode"):
		print("Invalid Opcode!!!")
		exit()
	sign=sign_ops[0:len(sign_ops)-1]
	ops=int(sign_ops[len(sign_ops)-1])
	if(flen!=32 and flen!=64):
		print("Invalid flen value!!!")
		exit()
	
	while a!="":
		l=a.split()							#['b32?f', '=0', 'i', '-1.7FFFFFP127', '->', '0x1']
		d_sign=l[0][3:]
		d_flen=int(l[0][1:3])
		d_rm=l[1]
		
		if(sign==d_sign and flen==d_flen):			
			rm_dataset.append(rounding_mode(d_rm))
			if(ops==2):					
				if(l[4]!='->'):				#b32+ =0 i +0.000001P-126 -1.7FFFFFP127 -> -1.7FFFFFP127 x
					rs2_dataset.append(l[4])
					rs1_dataset.append(l[3])
					rd_dataset.append(l[6])
					te_dataset.append(l[2])
					if(len(l)-1==6):			#b32+ =0 i +0.000001P-126 -1.7FFFFFP127 -> -1.7FFFFFP127
						flags_dataset.append("")
					else:					#b32+ =0 i +0.000001P-126 -1.7FFFFFP127 -> -1.7FFFFFP127 x
						flags_dataset.append(l[len(l)-1])
				else:						#b32+ =0 +0.000001P-126 -1.7FFFFFP127 -> -1.7FFFFFP127 x
					rs2_dataset.append(l[3])
					rs1_dataset.append(l[2])
					rd_dataset.append(l[5])
					te_dataset.append("")
					if(len(l)-1==5):			#b32+ =0 +0.000001P-126 -1.7FFFFFP127 -> -1.7FFFFFP127
						flags_dataset.append("")
					else:					#b32+ =0 +0.000001P-126 -1.7FFFFFP127 -> -1.7FFFFFP127 x
						flags_dataset.append(l[len(l)-1])					
			elif(ops==1):
				if(l[3]!='->'):				#b32V =0 i +1.7FFFFFP127 -> +1.7FFFFFP63 x
					rs1_dataset.append(l[3])
					rd_dataset.append(l[5])
					te_dataset.append(l[2])
					if(len(l)-1==5):			#b32V =0 i +1.7FFFFFP127 -> +1.7FFFFFP63
						flags_dataset.append("")
					else:					#b32V =0 i +1.7FFFFFP127 -> +1.7FFFFFP63 x
						flags_dataset.append(l[len(l)-1])
				else:						#b32V =0 +0.7FFFFFP-126 -> +1.7FFFFFP-64 x
					rs1_dataset.append(l[2])
					rd_dataset.append(l[4])
					te_dataset.append("")
					if(len(l)-1==4):			#b32V =0 +1.7FFFFFP127 -> +1.7FFFFFP63
						flags_dataset.append("")
					else:					#b32V =0 +1.7FFFFFP127 -> +1.7FFFFFP63 x
						flags_dataset.append(l[len(l)-1])
			elif(ops==3): 
				if(l[5]!='->'):				#b32*+ =0 i -1.000000P-126 -1.19BD32P52 -Inf -> -Inf
					rs3_dataset.append(l[5])
					rs2_dataset.append(l[4])
					rs1_dataset.append(l[3])
					rd_dataset.append(l[7])
					te_dataset.append(l[2])
					if(len(l)-1==7):			#b32*+ =0 i -1.000000P-126 -1.19BD32P52 -Inf -> -Inf
						flags_dataset.append("")
					else:					#b32*+ =0 i -1.000000P-126 -1.19BD32P52 -Inf -> -Inf x
						flags_dataset.append(l[len(l)-1])
				else:						#b32*+ =0 -1.000000P-126 -1.19BD32P52 -Inf -> -Inf 
					rs3_dataset.append(l[4])
					rs2_dataset.append(l[3])
					rs1_dataset.append(l[2])
					rd_dataset.append(l[6])
					te_dataset.append("")
					if(len(l)-1==6):			#b32*+ =0 -1.000000P-126 -1.19BD32P52 -Inf -> -Inf
						flags_dataset.append("")
					else:					#b32*+ =0 -1.000000P-126 -1.19BD32P52 -Inf -> -Inf x
						flags_dataset.append(l[len(l)-1])
		i=i+1
		a=f.readline()
	print("Iterated through",i,"lines of Test Cases!")
	if(ops==2):
		return rs1_dataset,rs2_dataset,rd_dataset,rm_dataset,te_dataset,flags_dataset
	elif(ops==1):
		return rs1_dataset,rd_dataset,rm_dataset,te_dataset,flags_dataset
	elif(ops==3):
		return rs1_dataset,rs2_dataset,rs3_dataset,rd_dataset,rm_dataset,te_dataset,flags_dataset

X,Y,Z,D,Rm,Te,F=gen_fp_dataset(32,"fMADD")
print("X Dataset=>")
print(X)
print("-----------------------------------------------------------------------------------------------------------------------------",)
print("Y Dataset=>")
print(Y)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("Z Dataset=>")
print(Z)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("Destination Dataset=>")
print(D)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("Rounding Mode=>")
print(Rm)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("Trapped Exceptions=>")
print(Te)
print("-----------------------------------------------------------------------------------------------------------------------------")
print("Flags=>")
print(F)
print("-----------------------------------------------------------------------------------------------------------------------------")
#print(len(X),len(D),len(Rm),len(Te),len(F))					#1 Operand
#print(len(X),len(Y),len(D),len(Rm),len(Te),len(F))				#2 Operands
print(len(X),len(Y),len(Z),len(D),len(Rm),len(Te),len(F))			#3 Operands

