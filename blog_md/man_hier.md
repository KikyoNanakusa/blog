# man hierについて
`man`コマンドはみんな知ってると思う.
Manualの略であり, `man hoge`とすると, それに関するマニュアルが読めるというもので, お世話になることも多い.

manページは, 中を探してみると, 思ったよりいろんなことが書いてあっておもしろい.
そんなmanページの一つとして`hier(7)`というページがある.
これはhierarchyの略で, `NAME`のセクションには以下のように書いてある.

```
hier - description of the filesystem hierarchy
```

FSH(File System Hierarchy) について書いてあるのだ.
ちょっとだけ抜粋.
```
       A typical Linux system has, among others, the following directories:

       /      This is the root directory.  This is where the whole tree starts.

       /bin   This  directory  contains executable programs which are needed in single user mode and to bring the system
              up or repair it.

       /boot  Contains static files for the boot loader.  This directory holds only the files which  are  needed  during
              the  boot  process.  The map installer and configuration files should go to /sbin and /etc.  The operating
              system kernel (initrd for example) must be located in either / or /boot.

       /dev   Special or device files, which refer to physical devices.  See mknod(1).
```

よく知らないディレクトリに遭遇したら, このmanページから検索すると簡潔な説明が見れてよい.

manページのセクション7[^1]は, このようなかゆいところに手が届く記事が多く, 覗いてみるといいかもしれない.

[^1]: セクション7は, *Miscellaneous (including macro packages and conventions)*, 日本語にするところの,「いろんなもの」が含まれるとされている. これは`man man`で確認することができる.
