from typing import Text, Sequence, Optional, Union, Mapping, Any, Tuple

import torch
from geyser import Geyser
from geyser.utility import reflect
from ignite import engine
from ignite.utils import convert_tensor
from ignite.handlers import Checkpoint, DiskSaver, global_step_from_engine
from taskflow.task import Task
from torch import nn, optim
from torch.utils.data import DataLoader


@Geyser.task(
    provides=('model',),
    requires=(
            'model', 'train_loader', 'validate_loader', 'optimizer', 'device', 'loss', 'metrics_params', 'max_epochs',
            'non_blocking'
    )
)
class SupervisedTrainer(Task):
    def build_metrics(self, *args, loss: nn.Module):
        return dict(loss=loss, **dict(map(
            lambda it: (it['name'], reflect(it['reference'])(**(it['params'] if 'params' in it else {}))),
            args
        )))

    def execute(
            self, *args, logger, id, path,
            model: nn.Module, train_loader: DataLoader, validate_loader: DataLoader, optimizer: optim.Optimizer,
            loss: nn.Module, device: Text, metric_params: Sequence[Mapping[Text, Any]], max_epochs: int,
            non_blocking: bool = False, **kwargs
    ) -> Tuple[nn.Module]:
        model = model.to(device)

        trainer = engine.create_supervised_trainer(
            model, optimizer, loss, device, non_blocking, self.prepare_train_batch
        )
        evaluator = engine.create_supervised_evaluator(
            model, self.build_metrics(*metric_params, loss=loss), device, non_blocking, self.prepare_validate_batch
        )

        @evaluator.on(engine.Events.COMPLETED)
        def log_metrics(_engine: engine.Engine):
            logger.info('EVALUATE EPOCH {} | {}'.format(trainer.state.epoch, ' | '.join(map(
                lambda it: '{}: {}'.format(it[0], repr(it[1]).replace('\n', ' ')),
                _engine.state.metrics.items(),
            ))))

        evaluator.add_event_handler(engine.Events.COMPLETED, Checkpoint(
            {'model': model, 'optimizer': optimizer, 'trainer': trainer},
            DiskSaver(str(path.current('supervised_trainer', id, 'checkpoints')), create_dir=True, atomic=True),
            score_function=Checkpoint.get_default_score_fn('loss'),
            score_name='loss',
            global_step_transform=global_step_from_engine(trainer)
        ))

        @trainer.on(engine.Events.EPOCH_COMPLETED)
        def evaluate(_engine: engine.Engine):
            evaluator.run(
                validate_loader,
            )

        trainer.run(
            train_loader, max_epochs=max_epochs,
        )
        return model,

    def prepare_train_batch(
            self,
            batch: Sequence[torch.Tensor], device: Optional[Union[str, torch.device]] = None, non_blocking: bool = False
    ):
        x, y = batch
        return (
            convert_tensor(x, device=torch.device(device), non_blocking=non_blocking),
            convert_tensor(y, device=torch.device(device), non_blocking=non_blocking),
        )

    def prepare_validate_batch(
            self,
            batch: Sequence[torch.Tensor], device: Optional[Union[str, torch.device]] = None, non_blocking: bool = False
    ):
        """
        Preparing batch of samples when validating. Implement this function to
        customize.
        Args:
            profile: Runtime profile defined in TOML file.
            shared: Shared storage in the whole lifecycle.
            logger: The logger named with this Task.
            batch: Raw batch provided by the data loader.
            device: Which device of the batch.
            non_blocking: Whether the action of moving the batch is blocking.
        Returns:
            Prepared batch.
        """
        x, y = batch
        return (
            convert_tensor(x, device=torch.device(device), non_blocking=non_blocking),
            convert_tensor(y, device=torch.device(device), non_blocking=non_blocking),
        )
