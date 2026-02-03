# RISC-Vに入門する1 環境構築

## RISC-Vに入門しよう

もろもろの事情において, RISC-Vに入門する必要がある. 
というわけで, とりあえずRISC-VをターゲットにしたCコンパイラを入手する. 

環境はWSL2のUbuntu24でホストマシンはx86-64である. 

##  コンパイラを入手

以下のコマンドでコンパイラと, glibcと, qemuをインストールできる. 

```
sudo apt update
sudo apt install -y \
  gcc-riscv64-linux-gnu \
  binutils-riscv64-linux-gnu \
  libc6-dev-riscv64-cross \
  qemu-user qemu-user-static
```

## コンパイルしてみる

適当にCプログラムを書く
```
#include<stdio.h>

int main() {
  for (int i = 0; i < 5; i++) {
    printf("Number is %d\n", i);
  }

  return 0;
}
```

コンパイルしてみる. いろいろオプションはあるようだが, 今回はとりあえず何もつけずに
```
riscv64-linux-gnu-gcc ./risc-v-test.c -o risc-v-test.o

```

## アセンブリを読む

`objdump`にrisc-v向けのバイナリがあるらしい. 
始めにインストールした`binutils-riscv64-linux-gnu`に入ってるっぽい
実行する. 
```
riscv64-linux-gnu-objdump -d risc-v-test.o
```

ディスアセンブル結果がこれ

```
0000000000000694 <main>:
 694:   1101                    addi    sp,sp,-32
 696:   ec06                    sd      ra,24(sp)
 698:   e822                    sd      s0,16(sp)
 69a:   1000                    addi    s0,sp,32
 69c:   fe042623                sw      zero,-20(s0)
 6a0:   a839                    j       6be <main+0x2a>
 6a2:   fec42783                lw      a5,-20(s0)
 6a6:   85be                    mv      a1,a5
 6a8:   00000517                auipc   a0,0x0
 6ac:   03850513                addi    a0,a0,56 # 6e0 <_IO_stdin_used+0x8>
 6b0:   ef1ff0ef                jal     5a0 <printf@plt>
 6b4:   fec42783                lw      a5,-20(s0)
 6b8:   2785                    addiw   a5,a5,1
 6ba:   fef42623                sw      a5,-20(s0)
 6be:   fec42783                lw      a5,-20(s0)
 6c2:   0007871b                sext.w  a4,a5
 6c6:   4791                    li      a5,4
 6c8:   fce7dde3                bge     a5,a4,6a2 <main+0xe>
 6cc:   4781                    li      a5,0
 6ce:   853e                    mv      a0,a5
 6d0:   60e2                    ld      ra,24(sp)
 6d2:   6442                    ld      s0,16(sp)
 6d4:   6105                    addi    sp,sp,32
 6d6:   8082                    ret
```

ちょっとまだ記法をよく知らないので, 読めない箇所が多々ある. 
内容は次回やる. 

## 実行してみる

なんか動的リンクだとめんどくさそうなので静的リンクでコンパイルしなおす. 

```
riscv64-linux-gnu-gcc ./risc-v-test.c -static  -o risc-v-test-static.o
```

qemuで動かす. 
```
qemu-riscv64 ./risc-v-test-static.o
Number is 0
Number is 1
Number is 2
Number is 3
Number is 4
```

とりあえず環境が整ったので, 次回は中身を勉強する

