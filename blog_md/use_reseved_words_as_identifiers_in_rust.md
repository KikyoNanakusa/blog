# Rustで予約語を識別子として使う(Raw Identifier)

`type`とか`match`みたいな予約語を変数名として使いたい時がある．
例えば，ELFのパーサを書いていて，`ElfHeader`構造体に`e_type`として`type`を持たせたい時など．

そんな時は`r#`を先頭に付与すると，予約語が使えるようになる．

```
struct ElfHeader {
    pub ident: EIdent, 
    pub r#type: u16, 
    pub machine: u16, 
    ...
}
```

みたいな感じ．

## 参考文献

- https://doc.rust-lang.org/rust-by-example/compatibility/raw_identifiers.html
