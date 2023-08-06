"""FASTGenomics base library"""

__version__ = "3.3.0"

from .fg import (
    FASTGenomicsClient,
    FASTGenomicsLargeFileStorageClient,
    FASTGenomicsDatasetClient,
    ToolConfiguration,
    run_zip,
)
