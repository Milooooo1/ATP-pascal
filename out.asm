	.cpu cortex-m0
	.text
	.align 4
	.global aMinB
	.global aPlusB
	.global odd
	.global even

.thumb_func
aMinB:
	push {r0, r1, r2, r3, r4, r5, r6, r7, lr}
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
	MOV R0 R0
	STR R0 [SP, #4]  	# result stored
	LDR R0 [SP, #4]  	# load result val in R0
	ADD SP SP #16
	pop {r0, r1, r2, r3, r4, r5, r6, r7, pc}

.thumb_func
aPlusB:
	push {r0, r1, r2, r3, r4, r5, r6, r7, lr}
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
	pop {r0, r1, r2, r3, r4, r5, r6, r7, pc}

.thumb_func
odd:
	push {r0, r1, r2, r3, r4, r5, r6, r7, lr}
	SUB SP SP #12
	STR R0 [SP, #8]  	# n stored
	LDR R0 [SP, #8]  	# n loaded
	CMP R0 #0
	BLE odd_nble0_if
	BL odd_nble0_else

odd_nble0_if:
	MOV R0 #0
	STR R0 [SP, #4]  	# result stored
	BL odd_end

odd_nble0_else:
	LDR R0 [SP, #8]  	# n loaded
	MOV R1 R0
	MOV R2 #1
	SUB R0 R1 R2
	STR R0 [SP, #0]  	# nMinEen stored
	LDR R0 [SP, #4]  	# nMinEen loaded
	BL even
	STR R0 [SP, #4]  	# result stored
	BL odd_end

odd_end:
	LDR R0 [SP, #4]  	# load result val in R0
	ADD SP SP #12
	pop {r0, r1, r2, r3, r4, r5, r6, r7, pc}

.thumb_func
even:
	push {r0, r1, r2, r3, r4, r5, r6, r7, lr}
	SUB SP SP #12
	STR R0 [SP, #8]  	# n stored
	LDR R0 [SP, #8]  	# n loaded
	CMP R0 #0
	BLE even_nble0_if
	BL even_nble0_else

even_nble0_if:
	MOV R0 #1
	STR R0 [SP, #4]  	# result stored
	BL even_end

even_nble0_else:
	LDR R0 [SP, #8]  	# n loaded
	MOV R1 R0
	MOV R2 #1
	SUB R0 R1 R2
	STR R0 [SP, #0]  	# nMinEen stored
	LDR R0 [SP, #4]  	# nMinEen loaded
	BL odd
	STR R0 [SP, #4]  	# result stored
	BL even_end

even_end:
	LDR R0 [SP, #4]  	# load result val in R0
	ADD SP SP #12
	pop {r0, r1, r2, r3, r4, r5, r6, r7, pc}

example:
	push {r0, r1, r2, r3, r4, r5, r6, r7, lr}
	SUB SP SP #16
	MOV R0 #2
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
	LDR R0 [SP, #8]  	# c loaded
	CMP R0 #0
	BGE example_cbge0_if
	BL example_cbge0_else

example_cbge0_if:
	LDR R0 [SP, #8]  	# c loaded
	CMP R0 #2
	BGE example_cbge0_if_cbge2_if
	BL example_cbge0_if_cbge2_else

example_cbge0_if_cbge2_if:
	MOV R0 #1
	STR R0 [SP, #8]  	# c stored
	BL example_cbge0_if_end

example_cbge0_if_cbge2_else:
	MOV R0 #2
	STR R0 [SP, #8]  	# c stored
	BL example_cbge0_if_end

example_cbge0_if_end:
	BL example_end

example_cbge0_else:
	MOV R0 #3
	STR R0 [SP, #8]  	# c stored
	BL example_end

example_end:
	ADD SP SP #16
	pop {r0, r1, r2, r3, r4, r5, r6, r7, pc}
