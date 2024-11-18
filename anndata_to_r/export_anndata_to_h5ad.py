import os
import tempfile

import sparrow as sp

sdata = sp.datasets.resolve_example()

OUTPUT_DIR = tempfile.tempdir

sdata["table_transcriptomics"].write(os.path.join(OUTPUT_DIR, "adata.h5ad"))
