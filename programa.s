	.text
	.file	"programa.ll"
	.globl	novo
	.align	16, 0x90
	.type	novo,@function
novo:                                   # @novo
	.cfi_startproc
# BB#0:                                 # %entry
	movl	$2, %eax
	retq
.Lfunc_end0:
	.size	novo, .Lfunc_end0-novo
	.cfi_endproc

	.globl	main
	.align	16, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# BB#0:                                 # %entry
	subq	$24, %rsp
.Ltmp0:
	.cfi_def_cfa_offset 32
	movss	20(%rsp), %xmm0         # xmm0 = mem[0],zero,zero,zero
	callq	printf_f
	movss	20(%rsp), %xmm0         # xmm0 = mem[0],zero,zero,zero
	addq	$24, %rsp
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc


	.section	".note.GNU-stack","",@progbits
