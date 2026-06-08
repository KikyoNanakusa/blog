# gdb使い方メモ1 (catch syscall)

gdbの使い方を毎回忘れているのでメモっておく. 多分今後もメモるので1. 

## syscall にbreak pointを張りたい

`catch syscall [syscall name]` で張れる. 

こんな感じ
```
(gdb) catch syscall write
r 
Catchpoint 1 (call to syscall write), 0x00007ffff7d1c5a4 in __GI___libc_write (fd=1, buf=0x555555579500, nbytes=48)
```

条件も指定できる 
```
(gdb) catch syscall write 
(gdb) condition 1 $rax < 0 # raxが負だったら止める
```

便利だね
