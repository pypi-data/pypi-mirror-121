import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class PyramidPooling(nn.Module):

    def __init__(self, levels, channels=1, mode="max", method='spatial'):
        """
        General Pyramid Pooling class which uses Spatial Pyramid Pooling by default and holds the static methods for both spatial and temporal pooling.
        :param levels defines the different divisions to be made in the width and (spatial) height dimension
        :param channels defines the number of "color" channels in the data (used to determine dimensionality)
        :param mode defines the underlying pooling mode to be used, can either be "max" or "avg"
        :param method defines whether spatial or temporal pyramid pooling is used

        :returns a tensor vector with shape [batch x 1 x n], where  n: sum(filter_amount*level*level) for each level in levels (spatial) or
                                                                    n: sum(filter_amount*level) for each level in levels (temporal)
                                            which is the concentration of multi-level pooling
        """
        self.levels = levels
        self.channels = channels
        self.mode = mode

        assert method.lower() in self._methods
        self.method = method.lower()


    def forward(self, x):
        assert 2 <= x.shape <= 4, "input x must be 2 dimensional (1 sample, 1 channel), 3 dimensional (1 sample, n channels | n samples, 1 channel) or 4 dimensional (n samples, n channels)"
        if len(x.shape) == 2:
            n_samples = 1
            assert self.channels == 1, "2 dimensional input passed when self.channels == %d (implicit single channel passed with 2D)" % self.channels
        elif len(x.shape) == 3:
            if self.channels == 1:
                n_samples = x.shape[0]
            else:
                assert self.channels == x.shape[0], "%d channels specified but 3D input of shape (%d, h, w) passed (implicit single sample passed with 3D)" % (self.channels, x.shape[0])
                n_samples = 1
        elif len(x.shape) == 4:
            assert x.shape[1] == self.channels, "second dimension of x input must represent the image channels but dimension == %d and self.channels = %d" % (x.shape[1], self.channels)
            n_samples = x.shape[0]
        
        n = n_samples
        c = self.channels
        h = x.shape[-2]
        w = x.shape[-1]
        
        return self.pool(x.reshape(n, c, h, w), self.levels, self.mode, self.method, n=n, c=c, h=h, w=w)

    def get_output_size(self, channels=None):
        out = 0
        for level in self.levels:
            out += (channels or self.channels) * level * level
        return out

    @staticmethod
    def pool(previous_conv, levels, mode, method, n, c, h, w):
        """
        Static Pyramid Pooling method, which divides the input Tensor vertically and horizontally
        (last 2 dimensions) according to each level in the given levels and pools its value according to the given mode.
        :param previous_conv input tensor of the previous convolutional layer
        :param levels defines the different divisions to be made in the width and height dimension
        :param mode defines the underlying pooling mode to be used, can either be "max" or "avg"
        :param method defines whether "spatial" or "temporal" pooling is used

        :returns a tensor vector with shape [batch x channel x n],
                                            where n: sum(level ** p) for each level in levels where p == 1 
                                            if temporal else 2 if spatial
        """
        for i, level in enumerate(levels):
            w_kernel = int(math.ceil(w / level))
            w_pad1 = int(math.floor((w_kernel * level - w) / 2))
            w_pad2 = int(math.ceil((w_kernel * level - w) / 2))

            if method == 'spatial':
                h_kernel = int(math.ceil(h / level))
                h_pad1 = int(math.floor((h_kernel * level - h) / 2))
                h_pad2 = int(math.ceil((h_kernel * level - h) / 2))

                assert w_pad1 + w_pad2 == (w_kernel * level - w) and \
                    h_pad1 + h_pad2 == (h_kernel * level - h)

                padded_input = F.pad(input=previous_conv, pad=[w_pad1, w_pad2, h_pad1, h_pad2],
                                    mode='constant', value=0)
            elif method == 'temporal':
                h_kernel = h

                assert w_pad1 + w_pad2 == (w_kernel * level - w)

                padded_input = F.pad(input=previous_conv, pad=[w_pad1, w_pad2],
                                    mode='constant', value=0)
            
            if mode == "max":
                pool = nn.MaxPool2d((h_kernel, w_kernel), stride=(h_kernel, w_kernel), padding=(0, 0))
            elif mode == "avg":
                pool = nn.AvgPool2d((h_kernel, w_kernel), stride=(h_kernel, w_kernel), padding=(0, 0))
            else:
                raise RuntimeError("Unknown pooling type: %s, please use \"max\" or \"avg\".")
            x = pool(padded_input)

            if i == 0:
                # spp = x.view(num_sample, -1)
                spp = x.view(n, c, -1)
            else:
                # spp = torch.cat((spp, x.view(num_sample, -1)), 1)
                spp = torch.cat((spp, x.view(n, c, -1)), 1)

        return spp


class SpatialPyramidPooling(PyramidPooling):
    def __init__(self, levels, channels=1, mode="max"):
        """
                Spatial Pyramid Pooling Module, which divides the input Tensor horizontally and horizontally
                (last 2 dimensions) according to each level in the given levels and pools its value according to the given mode.
                Can be used as every other pytorch Module and has no learnable parameters since it's a static pooling.
                In other words: It divides the Input Tensor in level*level rectangles width of roughly (previous_conv.size(3) / level)
                and height of roughly (previous_conv.size(2) / level) and pools its value. (pads input to fit)
                :param levels defines the different divisions to be made in the width dimension
                :param mode defines the underlying pooling mode to be used, can either be "max" or "avg"

                :returns (forward) a tensor vector with shape [batch x 1 x n],
                                                    where n: sum(filter_amount*level*level) for each level in levels
                                                    which is the concentration of multi-level pooling
                """
        super(SpatialPyramidPooling, self).__init__(levels, channels=channels, mode=mode)


class TemporalPyramidPooling(PyramidPooling):
    def __init__(self, levels, channels=1, mode="max"):
        """
        Temporal Pyramid Pooling Module, which divides the input Tensor horizontally (last dimensions)
        according to each level in the given levels and pools its value according to the given mode.
        Can be used as every other pytorch Module and has no learnable parameters since it's a static pooling.
        In other words: It divides the Input Tensor in "level" horizontal stripes with width of roughly (previous_conv.size(3) / level)
        and the original height and pools the values inside this stripe
        :param levels defines the different divisions to be made in the width dimension
        :param mode defines the underlying pooling mode to be used, can either be "max" or "avg"

        :returns (forward) a tensor vector with shape [batch x 1 x n],
                                            where n: sum(filter_amount*level) for each level in levels
                                            which is the concentration of multi-level pooling
        """
        super(TemporalPyramidPooling, self).__init__(levels, channels=channels, mode=mode)
