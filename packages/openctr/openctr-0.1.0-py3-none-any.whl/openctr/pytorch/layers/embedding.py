import torch
from torch import nn
from itertools import combinations
from . import sequence


class EmbeddingLayer(nn.Module):
    def __init__(self, feature_encoder, embedding_dim, 
                 feature_types=["numeric", "categorical", "sequence"]):
        super(EmbeddingLayer, self).__init__()
        self._feature_encoder = feature_encoder
        self._feature_types = feature_types
        self.embedding_layer = nn.ModuleDict()
        self.seq_encoder_layer = nn.ModuleDict()
        for feature, feature_spec in self._feature_encoder.feature_specs.items():
            if feature_spec["type"] == "numeric" and "numeric" in feature_types:
                self.embedding_layer.update({feature: nn.Linear(1, embedding_dim, bias=False)})
            elif feature_spec["type"] == 'categorical' and "categorical" in feature_types:
                self.embedding_layer.update({feature: nn.Embedding(feature_spec['vocab_size'], embedding_dim)})
            elif feature_spec["type"] == 'sequence' and "sequence" in feature_types:
                self.embedding_layer.update({feature: nn.Embedding(feature_spec['vocab_size'], embedding_dim, padding_idx=0)})
                if "encoder" in feature_spec:
                    try:
                        self.seq_encoder_layer.update({feature: getattr(sequence_encoder, feature_spec["encoder"])()})
                    except:
                        raise RuntimeError("Sequence encoder={} is not supported.".format(feature_spec["encoder"]))
                else:
                    self.seq_encoder_layer.update({feature: sequence_encoder.MaskedAveragePooling()})

    def forward(self, X):
        embedding_vecs = [] 
        for feature, feature_spec in self._feature_encoder.feature_specs.items():
            if feature_spec["type"] == "numeric" and "numeric" in self._feature_types:
                inp = X[:, feature_spec["index"]].float().view(-1, 1)
                embedding_vec = self.embedding_layer[feature](inp)
            elif feature_spec["type"] == "categorical" and "categorical" in self._feature_types:
                inp = X[:, feature_spec["index"]].long()
                embedding_vec = self.embedding_layer[feature](inp)
            elif feature_spec["type"] == "sequence" and "sequence" in self._feature_types:   
                inp = X[:, feature_spec["index"]].long()
                seq_embed_matrix = self.embedding_layer[feature](inp)
                embedding_vec = self.seq_encoder_layer[feature](seq_embed_matrix)
            embedding_vecs.append(embedding_vec)
        return embedding_vecs


# class EmbeddingDictLayer(nn.Module):
#     def __init__(self, output='sum'):
#         super(InnerProductLayer, self).__init__()
#         self._output_type = output


class InnerProductLayer(nn.Module):
    # output: sum (bsx1), bi_vector (bsxdim), dot_vector: (bsxfx(f-1)/2), element_wise (bsxfx(f-1)/2xdim)
    def __init__(self, output='sum'):
        super(InnerProductLayer, self).__init__()
        self._output_type = output
    
    def forward(self, embedding_vectors):
        if self._output_type in ['sum', 'bi_vector']:
            embedding_tensor = torch.stack(embedding_vectors)
            sum_of_square = torch.sum(embedding_tensor, dim=0) ** 2
            square_of_sum = torch.sum(embedding_tensor ** 2, dim=0)
            bi_interaction_vector = (sum_of_square - square_of_sum) * 0.5
            if self._output_type == 'bi_vector':
                return bi_interaction_vector
            else:
                return torch.sum(bi_interaction_vector, dim=-1).view(-1, 1)
        elif self._output_type in ['dot_vector', 'element_wise']:
            pairs = list(combinations(embedding_vectors, 2))
            emb1 = torch.stack([p for p, _ in pairs], dim=1)
            emb2 = torch.stack([q for _, q in pairs], dim=1)
            inner_product = emb1 * emb2
            if self._output_type == 'dot_vector':
                inner_product = torch.sum(inner_product, dim=2)
            return inner_product
