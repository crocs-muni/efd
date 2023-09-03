# Explicit-Formulas Database
A (modifed) export of the [Explicit-Formulas Database](https://www.hyperelliptic.org/EFD/) (EFD) which contains
the data files and three-operand-code files for the formulas. Credit goes to [Daniel J. Bernstein](https://cr.yp.to/djb.html) and [Tanja Lange](https://www.hyperelliptic.org/tanja/)
for collecting the formulas and to the formula [authors](https://www.hyperelliptic.org/EFD/bib.html). This repository is an export polished for automated use
and more documentation.

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
 - **New formulas**: Added negation formula for more coordinate systems as well as a scaling formula that was missing.
 - **Removed formulas**: Removed some broken formulas, for example see the formulas at:
                         [shortw/projective-1/addition/add-1986-cc.op3](https://www.hyperelliptic.org/EFD/g1p/auto-code/shortw/projective-1/addition/add-1986-cc.op3)
                         which contain lines such as: `error: not sure how to handle P*(-t5)`.

Last update from EFD as of 31.08.2023.


## Format

The repository contains files of four types:
 - Curve model files called `coordinates`
 - Coordinate system files called `variables`
 - Formula files called after the name of the formula (e.g. `add-2015-rcb`)
 - Formula three-operand files called after the name of the formula (e.g. `add-2015-rcb.op3`)

All of them are text files, with one "parameter" per line, with the parameter name always at it beginning.
Parameters listed below with an asterisk can appear multiple times per file with each carrying one value.

### Curve model

See for example [shortw](shortw/coordinates).
Has the following values:

 - **name**: The long name of the curve model (several words).
 - **parameter***: Name of curve parameter used in the model.
 - **coordinate***: Name of affine coordinate used in the model.
 - **satisfying**: Curve equation of the model, in parameters and coordinates listed, with `==` as the equality sign.
 - **ysquared**: "Right hand side of the curve equation" , or really what $y^2$ is equal to.
 - **addition***: Affine addition expression, for each coordinate, (of the form `<coord> = <expr in indexed coords>`).
 - **doubling***: Affine doubling expression, for each coordinate, (of the form `<coord> = <expr in indexed coords>`).
 - **negation***: Affine negation expression, for each coordinate, (of the form `<coord> = <expr in indexed coords>`).
 - **neutral***: Affine neutral point coordinates, for each coordinate.
 - **toweierstrass***: Affine transformation map to weierstrass form, for each coordinate.
 - **a0**, **a1**, **a2**, **a3**, **a4**, **a6**: The a-invariants of the curve.
 - **fromweierstrass***: Affine transformation map from weierstrass form, for each coordinate.
 
### Coordinate system

See for example [shortw/projective](shortw/projective/variables).
Has the following values:

 - **name**: The long name of the coordinate system.
 - **variable***: Name of the coordinate used in the system.
 - **neutral***: Neutral point coordinates used in the system.
 - **parameter***: Name of coordinate system parameter, can be used in formulas using this system or in affine to system map.
 - **assume***: Assumptions made by the coordinate system expressed as equalities in parameters of the curve model and coordinate system.
                Sometimes of the form `<coord parameter> = <expr in curve model parameters>` which defines the coordinate system
                parameter value.
 - **satisfying***: Equations relating the affine coordinates and the coordinate system ones. Usually with the affine
 					coordinate alone on the left hand side, but not necessarily.
 - **toaffine***: Equations converting coordinate system cooordinates to affine. Might not be available if the coordinate system
 				  does not support them. Might need variables defined in the **satisfying** parameter.
 - **tosystem***: Equations converting affine coordinates to system ones. Takes a concrete representative, most often
 				  with `Z = 1` or similar.

### Formula

Each formula is represented by two files, a base file with the name of the formula
and a three operand file with suffix `.op3`. The base file has the same format as curve model and
coordinate system files. The three operand file then contains the formula with each intermediate
value computation on one line, representing one unary or binary operation.

There are several types of formulas:
 - **addition**: A simple addition formula, `(P1, P2) - > P3`
 - **doubling**: A simple doubling formula, `(P1) -> P3`
 - **tripling**: A tripling formula, `(P1) -> P3`
 - **negation**: A negation formula, `(P1) -> P3`
 - **scaling**: A scaling formula, to scale the point back to some canonical representation (e.g. `Z = 1`), `(P1) -> P3`
 - **ladder**: A ladder formula, where the first input is the difference of third and second, `(P1, P2, P3) -> (P4, P5)` with `P1 = P3 - P2`, then `P4 = 2P2` and `P5 = P2 + P3`
 - **diffadd**: A differential addition formula, where the first input is the difference of third and second, `(P1, P2, P3) -> P4` with `P1 = P3 - P2`, then `P4 = P2 + P3`

See for example [shortw/projective/addition/add-2015-rcb](shortw/projective/addition/add-2015-rcb) and
[shortw/projective/addition/add-2015-rcb.op3](shortw/projective/addition/add-2015-rcb.op3).
The base formula file has the following values:

 - **source**: The reference to the source of the formula, usually with date, paper title and authors.
 - **parameter***: Name of formula parameter, used in the formula computation.
 - **assume***: Formula assumption, expression in curve model, coordinate system and formula parameters. Sometimes used to define
                the formula parameter, sometimes used to specify an assumption the formula needs (e.g. `Z2 = 1`).
 - **unified**: Present if the addition formula is unified.
 - **compute***: The formula intermediate values and outputs, (of the form `<IV> = <expr in previous IVs>`).

The three operand file has a simple format with one intermediate value computation per line.
For input and output coordinate indices, see the notation in the list of types of formulas above.
