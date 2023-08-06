# TEXTA CRF Extractor

Installation:

```
pip install texta-crf-extractor
```

Usage:

```
from texta_crf_extractor.crf_extractor import CRFExtractor
from texta_mlp.mlp import MLP

mlp = MLP(language_codes=["en"], default_language_code="en")

# prepare data
texts = ["foo", "bar"]
mlp_docs = [mlp.process(text) for text in texts]

# create extractor
extractor = CRFExtractor(mlp=mlp)

# train the CRF model
extractor.train(mlp_docs)

# tag something
extractor.tag("Tere maailm!")

```
