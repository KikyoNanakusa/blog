# アセンブリにおけるコメント記法

筆者は長らくバイナリ解析の方面からx86-64アセンブリに触れていたため, `;`がアセンブリにおける標準的なコメント記法であると思っていた．
しかしながら，実際にはそうではないということを知ったのでメモしておく．

## nasm 

nasm(Netwide Assembler)はx86 CPU architectureを対象にしたアセンブラである．
以下のリポジトリで開発されており，広く知られるアセンブラである．

- https://github.com/netwide-assembler/nasm

nasmにおける行コメントの記法は `;` である．
よって，以下のアセンブリは問題なくアセンブルすることができる．

```asm 
global _start 
section .text 

_start:
    mov rax, 60
    mov rdi, 42
    syscall ; exit(42)
```

```bash
nasm -f elf64 test_nasm.s -o test_nasm.o && ld test_nasm.o -o test_nasm
```

## gas

gas(GNU Assembler) はGNU Projectの開発するアセンブラで，GNU Binutilsパッケージの一部として配布されている．
このgasにおいて，`;`は文の区切りとして使用されている．
つまり，C言語におけるセミコロンと同じような記法として定義されている．

```asm 
mov rax, 60; mov rdi, 42; 
```

よって，以下のアセンブリはアセンブルすることができない．

```asm 
.intel_syntax noprefix 
.global _start 
.section .text 

_start:
    mov rax, 60
    mov rdi, 42
    syscall ; exit(42)
```

```bash 
$ as test_gas.s -o test_gas.o
test_gas.s: Assembler messages:
test_gas.s:8: Error: invalid character '(' in mnemonic
```

gasにおける正しい行コメント記法は`#`である．よって上記の例は正しくは以下のようになる．

```asm 
.intel_syntax noprefix 
.global _start 
.section .text 

_start: 
    mov rax, 60
    mov rdi, 42 
    syscall # exit(42)
```

この衝突は少し厄介で，nasmだと思って`;`の後にコメントとしてアセンブル可能な文を書いてしまうと，gasでアセンブルした際にはエラー無くアセンブルできてしまう．
極端な例を示すと，以下のアセンブリはgasでもnasmでもエラー無くアセンブルできるが，異なるオブジェクトファイルが生成されてしまう．
(gasなら2命令，nasmなら1命令)


```asm 
mov rax, 60; mov rax 1
```

今時アセンブリを手書きする人は少ないだろうが，世の中にはいろいろなアセンブリがあり，記法が衝突していることもあるので気を付けよう(1敗)．
