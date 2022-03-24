	.cpu cortex-m0
	.text
	.align 4
	.global aMinB
	.global aPlusB
	.global odd
	.global even

aMinB:
	PUSH {r4, r5, r6, r7, lr}
	SUB SP, SP, #16
	STR R0, [SP, #8]
	STR R1, [SP, #12]
	LDR R0, [SP, #8]
	MOV R1, R0
	LDR R0, [SP, #12]
	MOV R2, R0
	SUB R0, R1, R2
	STR R0, [SP, #0]
	LDR R0, [SP, #0]
	MOV R0, R0
	STR R0, [SP, #4]
	LDR R0, [SP, #4]
	ADD SP, SP, #16
	POP {r4, r5, r6, r7, pc}

aPlusB:
	PUSH {r4, r5, r6, r7, lr}
	SUB SP, SP, #12
	STR R0, [SP, #4]
	STR R1, [SP, #8]
	LDR R0, [SP, #4]
	MOV R1, R0
	LDR R0, [SP, #8]
	MOV R2, R0
	ADD R0, R1, R2
	STR R0, [SP, #0]
	LDR R0, [SP, #0]
	ADD SP, SP, #12
	POP {r4, r5, r6, r7, pc}

odd:
	PUSH {r4, r5, r6, r7, lr}
	SUB SP, SP, #12
	STR R0, [SP, #8]
	LDR R0, [SP, #8]
	CMP R0, #0
	BLE odd_nble0_if
	BL odd_nble0_else

odd_nble0_if:
	MOV R0, #0
	STR R0, [SP, #4]
	BL odd_end

odd_nble0_else:
	LDR R0, [SP, #8]
	MOV R1, R0
	MOV R2, #1
	SUB R0, R1, R2
	STR R0, [SP, #0]
	LDR R0, [SP, #0]
	BL even
	bl print_int
	STR R0, [SP, #4]
	BL odd_end

odd_end:
	LDR R0, [SP, #4]
	ADD SP, SP, #12
	POP {r4, r5, r6, r7, pc}

even:
	PUSH {r4, r5, r6, r7, lr}
	SUB SP, SP, #12
	STR R0, [SP, #8]
	LDR R0, [SP, #8]
	CMP R0, #0
	BLE even_nble0_if
	BL even_nble0_else

even_nble0_if:
	MOV R0, #1
	STR R0, [SP, #4]
	BL even_end

even_nble0_else:
	LDR R0, [SP, #8]
	MOV R1, R0
	MOV R2, #1
	SUB R0, R1, R2
	STR R0, [SP, #0]
	LDR R0, [SP, #0]
	BL odd
	bl print_int
	STR R0, [SP, #4]
	BL even_end

even_end:
	LDR R0, [SP, #4]
	ADD SP, SP, #12
	POP {r4, r5, r6, r7, pc}

example:
	PUSH {r4, r5, r6, r7, lr}
	SUB SP, SP, #16
	MOV R0, #2
	STR R0, [SP, #4]
	MOV R1, #4
	LDR R0, [SP, #4]
	MOV R2, R0
	SUB R3, R1, R2
	LDR R0, [SP, #4]
	MOV R1, R0
	MOV R2, #1
	SUB R4, R1, R2
	ADD R3, R3, R4
	MOV R4, #16
	ADD R0, R3, R4
	STR R0, [SP, #0]
	LDR R0, [SP, #0]
	MOV R1, #4
	BL aMinB
	bl print_int
	STR R0, [SP, #8]
	LDR R0, [SP, #8]
	CMP R0, #0
	BGE example_cbge0_if
	BL example_cbge0_else

example_cbge0_if:
	LDR R0, [SP, #8]
	CMP R0, #2
	BGE example_cbge0_if_cbge2_if
	BL example_cbge0_if_cbge2_else

example_cbge0_if_cbge2_if:
	MOV R0, #1
	STR R0, [SP, #8]
	BL example_cbge0_if_end

example_cbge0_if_cbge2_else:
	MOV R0, #2
	STR R0, [SP, #8]
	BL example_cbge0_if_end

example_cbge0_if_end:
	BL example_end

example_cbge0_else:
	MOV R0, #3
	STR R0, [SP, #8]
	BL example_end

example_end:
	ADD SP, SP, #16
	POP {r4, r5, r6, r7, pc}
