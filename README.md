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

- 変数宣言など  
  `LET REG Imm`
- 代入操作  
  `PUT REG1 REG2`
- 演算系
    - 足し算
        - `ADD REG1 REG2 REGOut`
        - `ADD REG1 Imm REGOut`
        - `ADD Imm1 Imm2 REGOut`
    - 引き算
        - `SUB REG1 REG2 REGOut`
        - `SUB REG1 Imm REGOut`
        - `SUB Imm1 Imm2 REGOut`
    - 掛け算
        - `MULT REG1 REG2 REGOut`
        - `MULT REG1 Imm REGOut`
        - `MULT Imm1 Imm2 REGOut`

## コンパイル方法

- 読める形式で出力する場合

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