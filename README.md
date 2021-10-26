# lc-compiler

論理回路演習のコンパイラ

## 動作構築

- Python 3.8以上

```bash
python -m venv lcenv
source lcenv/bin/activate
pip install -r requirement.txt
```

## テスト実行方法

```bash
pytest
```

## 使用できる命令

- 変数初期化  
  レジスタを数値で初期化 `LET REG Imm`
- 代入操作  
  レジスタ2の値をレジスタ1に代入 `PUT REG1 REG2`
- 演算系
    - 足し算
        - レジスタ同士の足し算 `ADD REG1 REG2 REGOut`
        - レジスタと数値の足し算 `ADD REG1 Imm REGOut`
        - 数値同士の足し算 `ADD Imm1 Imm2 REGOut`
    - 引き算
        - レジスタ同士の引き算 `SUB REG1 REG2 REGOut`
        - レジスタと数値の引き算 `SUB REG1 Imm REGOut`
        - 数値同士の引き算 `SUB Imm1 Imm2 REGOut`
    - 掛け算
        - レジスタ同士の掛け算 `MULT REG1 REG2 REGOut`
        - レジスタと数値の掛け算 `MULT REG1 Imm REGOut`
        - 数値同士の掛け算 `MULT Imm1 Imm2 REGOut`

## コンパイル方法

- 人間が読める形式で出力する場合

```bash
python compile.py ./example/sample.das
```

- hex形式で出力する場合

```bash
python compile.py ./example/sample.das --hex
```

ファイル名に`.out`がついて出力されます．

## デコード方法
hex形式を人間が読める形式に変換することもできます．  
```bash
python decode_hex.py ./example/sample1.hex 
```
ファイル名に`.out`がついて出力されます．

## CPU命令セット
論理回路設計演習に準拠しています．
- MOV A, Imm
- ADD A, Imm
- MOV A, B
- MOV A, IN
- MOV B, Imm
- ADD B, Imm
- MOV B, A
- MOV B, IN
- MOV OUT, Imm
- MOV OUT, B
- MOV B, GPR
- MOV GPR, B
- SUB A, B
- MULT A, B
- JNC Imm
- JMP Imm