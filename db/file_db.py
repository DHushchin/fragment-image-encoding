import os
import numpy as np
from annoy import AnnoyIndex

from .base import BaseDB
from fragment import Fragment


class FileDB(BaseDB):
    def __init__(self):
        self.save_path = '/db/fragments.npy'
        self.fragments = {}
        self.target_size = 64
        self.tree = None
        if os.path.exists(self.save_path):
            self.fragments = np.load(self.save_path, allow_pickle=True).item()


    def is_empty(self):
        return len(self.fragments) == 0


    def build_tree(self):
        dims = self.fragments[0]['feature'].shape[0]
        self.tree = AnnoyIndex(dims, 'euclidean')
        for i, fragment in self.fragments.items():
            feature = fragment['feature']
            self.tree.add_item(i, feature)
        self.tree.build(100, n_jobs=-1)


    def add_fragment(self, fragment: Fragment):
        fragment_elem = {
            'image': fragment.img,
            'feature': fragment.feature
        }
        fragment_id = len(self.fragments)
        self.fragments[fragment_id] = fragment_elem
        return fragment_id


    def get_fragment_by_id(self, fragment_id: int):
        fragment = self.fragments[fragment_id]
        return fragment


    def find_similar_fragment_id(self, fragment_feature):
        if self.is_empty() or self.tree is None:
            self.build_tree()

        similar_fragment_id = self.tree.get_nns_by_vector(fragment_feature, 1)[0]
        return similar_fragment_id
    

    def save_results(self):
        np.save(self.save_path, self.fragments)