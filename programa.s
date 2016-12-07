	.text
	.file	"programa.ll"
	.section	.rodata.cst4,"aM",@progbits,4
	.align	4
.LCPI0_0:
	.long	1073741824              # float 2
.LCPI0_1:
	.long	1065353216              # float 1
	.text
	.globl	fatorial
	.align	16, 0x90
	.type	fatorial,@function
fatorial:                               # @fatorial
	.cfi_startproc
# BB#0:                                 # %entry
	movl	%edi, -4(%rsp)
	cvtsi2ssl	%edi, %xmm0
	xorps	%xmm1, %xmm1
	ucomiss	%xmm0, %xmm1
	jae	.LBB0_2
# BB#1:                                 # %entao
	movl	$1, -8(%rsp)
	jmp	.LBB0_3
.LBB0_2:                                # %senao
	movl	$2, -8(%rsp)
.LBB0_3:                                # %fim
	xorps	%xmm0, %xmm0
	cvtsi2ssl	-8(%rsp), %xmm0
	cvttss2si	%xmm0, %eax
	retq
.Lfunc_end0:
	.size	fatorial, .Lfunc_end0-fatorial
	.cfi_endproc

	.globl	main
	.align	16, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# BB#0:                                 # %entry
	pushq	%rax
.Ltmp0:
	.cfi_def_cfa_offset 16
	callq	leiaFlutuante
	cvttss2si	%xmm0, %eax
	movl	%eax, global.n(%rip)
	cvtsi2ssl	%eax, %xmm0
	cvttss2si	%xmm0, %edi
	callq	fatorial
	movl	%eax, %edi
	callq	escrevaInteiro
	xorl	%eax, %eax
	popq	%rcx
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc


	.section	".note.GNU-stack","",@progbits
