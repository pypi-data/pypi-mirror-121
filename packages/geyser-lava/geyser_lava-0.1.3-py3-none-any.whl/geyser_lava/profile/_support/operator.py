from torch import nn
from torchvision.transforms import ToTensor
from geyser_lava.utility import unflatten, flatten
from geyser import Geyser

unflatten('reference', 'root', 'train', 'transform', 'download', name='cifar_unflatten')

@Geyser.functor(provides=('transform',))
def to_tensor() -> nn.Module:
    return ToTensor(),