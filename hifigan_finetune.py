# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytorch_lightning as pl

from nemo.collections.tts.models import HifiGanModel
from nemo.core.config import hydra_runner
from nemo.utils.exp_manager import exp_manager


@hydra_runner(config_path="conf/hifigan", config_name="hifigan_")
def main(cfg):
    #cfg.model.train_ds.dataloader_params.batch_size=8
    #cfg.model.max_steps=1000
    #cfg.model.optim.lr=0.0001
    #cfg.train_dataset="Dataset/vocoder_output_train/hifigan_train_ft.json"
    #cfg.validation_datasets="Dataset/vocoder_output_valid/hifigan_train_ft.json"
    #cfg.init_from_nemo_model="tts_hifigan.nemo"
    cfg.trainer.check_val_every_n_epoch=10
    trainer = pl.Trainer(**cfg.trainer)
    exp_manager(trainer, cfg.get("exp_manager", None))
    model = HifiGanModel(cfg=cfg.model, trainer=trainer)
    model.maybe_init_from_pretrained_checkpoint(cfg=cfg)
    trainer.fit(model)


if __name__ == '__main__':
    main()  # noqa pylint: disable=no-value-for-parameter
