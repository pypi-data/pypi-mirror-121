"""Contains all of the available models for customization. 
"""

from torch import nn

from .custom_models.inceptionv4 import InceptionV4
from .custom_models.mobilenetv2 import MobileNetV2
from .custom_models.resnext import ResNeXt101_32x4d
from .custom_models.vggm import VGGM
from .custom_models.xception import Xception

# from torchvision.models import alexnet
# from torchvision.models import densenet121, densenet161, densenet169, densenet201
# from torchvision.models import inception_v3
# from torchvision.models import resnet18, resnet34, resnet50, resnet101, resnet152
# from torchvision.models import squeezenet1_0, squeezenet1_1
# from torchvision.models import vgg11, vgg11_bn, vgg13, vgg13_bn, vgg16, vgg16_bn, vgg19, vgg19_bn

_model_names = ["inceptionv4",
                "mobilenetv2", 
                "resnext101_32x4d",
                "vggm",
                "xception"]

_models = [InceptionV4,
           MobileNetV2,
           ResNeXt101_32x4d,
           VGGM,
           Xception]

avail_models = dict(zip(_model_names, _models))
