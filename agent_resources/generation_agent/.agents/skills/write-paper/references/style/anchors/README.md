# Optional Style Anchors

The generic `STYLE_GUIDE.md` and `PAPER_STRUCTURE.md` are sufficient to produce a
complete paper. Anchors are optional examples supplied by the operator.

Place operator-owned examples under the paper workspace, not in the installed
skill package:

```text
paper/style/anchors/
  example-paper/
    main.tex
    paper.pdf
```

LaTeX source is most useful; a PDF alone can still show structure. The style
distiller reads all anchors and proposes recurring voice rules. It never applies
those proposals automatically. `PROJECT_BRIEF.md` may name exactly one anchor as
the `structural_exemplar`; that example controls structure only, while voice comes
from the accepted style guide.

Anchors are local inputs. Do not publish them accidentally, and never let their
private labels or bibliography keys leak into the generated paper merely because
they appeared in an example.
