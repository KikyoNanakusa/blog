# clangでコメント付きアセンブリを吐く

clangやgccといったコンパイラには `-S` オプションがあり, これを使うとリンクやオブジェクトファイルの作成を行わずアセンブリだけを出力することができる. 
clangの`-S`オプションはさらにほかのオプションと組み合わせて出力を変更することができる. 組み合わせることのできるオプションの中に `-fverbose-asm` というものがある. 
これを使うと生成されるアセンブリにコメントがついてちょっと読みやすくなる. 
helpには以下のように書いてある. 

>   -fverbose-asm           Generate verbose assembly output


例えば以下のコードを `-fverbose-asm` でコンパイルすると

```c
int main() {
  int a = 10;
  for (int i = 0; i < 10; i++) {
    printf("%d\n", a--);
  }
}

```

こうなる 

```
	.text
	.intel_syntax noprefix
	.file	"test.c"
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset rbp, -16
	mov	rbp, rsp
	.cfi_def_cfa_register rbp
	sub	rsp, 16
	mov	dword ptr [rbp - 4], 0
	mov	dword ptr [rbp - 8], 10
	mov	dword ptr [rbp - 12], 0
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	cmp	dword ptr [rbp - 12], 10
	jge	.LBB0_4
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	mov	esi, dword ptr [rbp - 8]
	mov	eax, esi
	add	eax, -1
	mov	dword ptr [rbp - 8], eax
	lea	rdi, [rip + .L.str]
	mov	al, 0
	call	printf@PLT
# %bb.3:                                #   in Loop: Header=BB0_1 Depth=1
	mov	eax, dword ptr [rbp - 12]
	add	eax, 1
	mov	dword ptr [rbp - 12], eax
	jmp	.LBB0_1
.LBB0_4:
	mov	eax, dword ptr [rbp - 4]
	add	rsp, 16
	pop	rbp
	.cfi_def_cfa rsp, 8
	ret
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.L.str,@object                  # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"%d\n"
	.size	.L.str, 4

	.ident	"Ubuntu clang version 18.1.3 (1ubuntu1)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
	.addrsig_sym printf
```

関数のはじめとか, ループのヘッダとかがコメントに書いてあって普段よりちょっとわかりやすい. 
ちなみに, `-emit-llvm` とは組み合わせられないので注意

