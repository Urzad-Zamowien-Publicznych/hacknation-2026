"""Local Docling models: downloaded once into the repo, then used offline."""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def use_local_models(models_dir: Path) -> None:
    """Point Docling at models_dir, downloading the models first if missing.

    Must be called before Docling builds a converter.
    """
    if not any(models_dir.glob("*")):
        download(models_dir)
    os.environ["DOCLING_ARTIFACTS_PATH"] = str(models_dir)
    from docling.datamodel.settings import settings

    settings.artifacts_path = models_dir


def download(models_dir: Path) -> None:
    from docling.utils.model_downloader import download_models

    logger.info("Downloading Docling models to %s", models_dir)
    download_models(
        output_dir=models_dir,
        progress=True,
        with_layout=True,
        with_tableformer=True,
        with_rapidocr=True,
        with_code_formula=False,
        with_picture_classifier=False,
    )
