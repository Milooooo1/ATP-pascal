	.cpu cortex-m0
	.text
	.align 4
	.global aMinB
	.global aPlusB
	.global odd
	.global even

.thumb_func
aMinB:
	# {'c': 4, 'result': 8, 'a': 12, 'b': 16}
	SUB SP SP #16
	STR R0 [SP, #8]  	# a stored
	STR R1 [SP, #12]  	# b stored
	LDR R0 [SP, #8]  	# a loaded
	MOV R1 R0
	LDR R0 [SP, #12]  	# b loaded
	MOV R2 R0
	SUB R0 R1 R2
	STR R0 [SP, #0]  	# c stored
	LDR R0 [SP, #0]  	# c loaded
	STR R0 [SP, #4]  	# result stored
	LDR R0 [SP, #4]  	# load result val in R0
	ADD SP SP #16

.thumb_func
aPlusB:
	# {'result': 4, 'a': 8, 'b': 12}
	SUB SP SP #12
	STR R0 [SP, #4]  	# a stored
	STR R1 [SP, #8]  	# b stored
	LDR R0 [SP, #4]  	# a loaded
	MOV R1 R0
	LDR R0 [SP, #8]  	# b loaded
	MOV R2 R0
	ADD R0 R1 R2
	STR R0 [SP, #0]  	# result stored
	LDR R0 [SP, #0]  	# load result val in R0
	ADD SP SP #12

.thumb_func
odd:
	# {'nMinEen': 4, 'result': 8, 'n': 12}
	SUB SP SP #12
	STR R0 [SP, #8]  	# n stored
	LDR R0 [SP, #8]  	# n loaded
	CMP R0 #0
	BLE branchToElse
	BL branchToIf
	LDR R0 [SP, #4]  	# load result val in R0
	ADD SP SP #12

.thumb_func
even:
	# {'nMinEen': 4, 'result': 8, 'n': 12}
	SUB SP SP #12
	STR R0 [SP, #8]  	# n stored
	LDR R0 [SP, #8]  	# n loaded
	CMP R0 #0
	BLE branchToElse
	BL branchToIf
	LDR R0 [SP, #4]  	# load result val in R0
	ADD SP SP #12

example:
	SUB SP SP #16
	STR R0 [SP, #4]  	# b stored
	MOV R1 #4
	LDR R0 [SP, #4]  	# b loaded
	MOV R2 R0
	SUB R3 R1 R2
	LDR R0 [SP, #4]  	# b loaded
	MOV R1 R0
	MOV R2 #1
	SUB R4 R1 R2
	ADD R3 R3 R4
	MOV R4 #16
	ADD R0 R3 R4
	STR R0 [SP, #0]  	# a stored
	LDR R0 [SP, #8]  	# b loaded
	MOV R1 #4
	BL aMinB
	STR R0 [SP, #8]  	# c stored
	ADD SP SP #16
