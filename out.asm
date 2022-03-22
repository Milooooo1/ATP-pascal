	.cpu cortex-m0
	.text
	.align 4
	.global aMinB
	.global aPlusB
	.global odd
	.global even

.thumb_func
aMinB:
	LDR R0 [SP, #0]		# a loaded
	MOV R1 R0
	LDR R0 [SP, #4]		# b loaded
	MOV R2 R0
	SUB R0 R1 R2
	STR R0 [SP, #8]		# c stored
	LDR R0 [SP, #8]		# c loaded
	MOV R0 R0
	STR R0 [SP, #-4]		# result stored

.thumb_func
aPlusB:
	LDR R0 [SP, #0]		# a loaded
	MOV R1 R0
	LDR R0 [SP, #4]		# b loaded
	MOV R2 R0
	ADD R0 R1 R2
	STR R0 [SP, #-4]		# result stored

.thumb_func
odd:
	IfElse

.thumb_func
even:
	IfElse

example:
	SUB SP SP #12
	MOV R0 #2
	STR R0 [SP, #4]		# b stored
	LDR R0 [SP, #4]		# b loaded
	MOV R1 R0
	MOV R2 #1
	SUB R0 R1 R2
	ADD R0 R0 #2
	MOV R4 16
	ADD R0 R3 R4
	STR R0 [SP, #0]		# a stored
	ADD SP SP #12
