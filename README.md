# Explicit-Formulas Database
A (modifed) export of the [Explicit-Formulas Database](https://www.hyperelliptic.org/EFD/) (EFD) which contains
the data files and three-operand-code files for the formulas. 

Currently contains only the prime field curve models:

 - [Short Weierstrass](shortw/)
 - [Montgomery](montgom/)
 - [Edwards](edwards/)
 - [Twisted Edwards](twisted/)

This repository is used as a source of parse-able formulas in the [pyecsca](https://github.com/J08nY/pyecsca)
toolkit.

## Differences to EFD data

In order to download the EFD data and compare it to this export do this in BASH:
```bash
mkdir efd-down
cd efd-down
wget -r -np -nv -nH --cut-dirs=1 http://www.hyperelliptic.org/EFD/
find . -name "*.html" -delete
rm -r oldefd g12o precomp.pdf g1p/auto-sage
for f in shortw montgom edwards twisted; do
  rsync -a g1p/auto-code/$f .;
  rsync -a g1p/data/$f .;
done;
rm -r g1p
cd ..
```

Then you can compare the `efd-down` directory with this repository using `diff -r` or some other tool.

The main differences are:

 - **Notation**: The EFD data often does not explicitly mark multiplications by `*`, it just uses spaces, this is not
                 nice when the data needs to be parsed and so this was fixed. Also changed the single equality sign
                 used in the curve equation entry `satisfying` into a double equation sign so that it can be parsed
                 as an expression.
 - **Output indices**: Some EFD formulas like the differential addition one, use the 5 as the index of their output point
                       (e.g. output coordinates are `X5`, `Y5`, `Z5`...). This is inconsistent with the notion that the
                       output point coordinates are just after the last input point coordinates, as the differential add
                       takes three input points and should have output on the fourth index. This is fixed in this export.
 - **Unified formulas**: Formulas which claim to be unified are marked as so, using the `unified` tag in the coordinate
                         system files.
 - **Infinity point**: The infinity (or neutral) point was added to more coordinate systems.
 - **New formulas**: Added the Short Weierstrass prime order complete formulas of Renes-Costello-Batina. Added negation
                     formula for more coordinate systems as well as a scaling formula that was missing.
 - **Removed formulas**: Removed some broken formulas, for example see the formulas at:
                         [shortw/projective-1/addition/add-1986-cc.op3](https://www.hyperelliptic.org/EFD/g1p/auto-code/shortw/projective-1/addition/add-1986-cc.op3)
                         which contain lines such as: `error: not sure how to handle P*(-t5)`.
