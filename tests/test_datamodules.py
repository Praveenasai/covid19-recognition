from pathlib import Path

import pytest
import torch

from src.data.covid19_datamodule import Covid19DataModule


@pytest.mark.parametrize("batch_size", [32, 128])
def test_covid19_datamodule(batch_size):
    data_dir = "data/"

    dm = Covid19DataModule(data_dir=data_dir, batch_size=batch_size)
    dm.prepare_data()

    assert not dm.data_train and not dm.data_val and not dm.data_test
    assert Path(data_dir, "Covid19-dataset").exists()
    assert Path(data_dir, "Covid19-dataset", "train").exists()
    assert Path(data_dir, "Covid19-dataset", "test").exists()

    dm.setup()
    assert dm.data_train and dm.data_val and dm.data_test
    assert dm.train_dataloader() and dm.val_dataloader() and dm.test_dataloader()

    num_datapoints = len(dm.data_train) + len(dm.data_val) + len(dm.data_test)
    assert num_datapoints == 70_000

    batch = next(iter(dm.train_dataloader()))
    x, y = batch
    assert len(x) == batch_size
    assert len(y) == batch_size
    assert x.dtype == torch.float32
    assert y.dtype == torch.int64
