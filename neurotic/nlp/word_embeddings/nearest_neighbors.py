# pypi
import attr
import numpy

@attr.s(auto_attribs=True)
class NearestNeighbors:
    """Finds the nearest neighbor(s) to a vector

    Args:
     candidates: set of vectors that are potential neighbors
     k: number of neighbors to find
    """
    candidates: numpy.ndarray    
    k: int=1

    def cosine_similarity(self, vector_1: numpy.ndarray, vector_2: numpy.ndarray) -> float:
        """Calculates the similarity between two vectors
    
        Args:
         vector_1: array to compare
         vector_2: array to compare to vector_1
    
        Returns:
         cosine similarity between the two vectors
        """
        return numpy.dot(vector_1, vector_2)/(numpy.linalg.norm(vector_1) *
                                              numpy.linalg.norm(vector_2))

    def nearest_neighbors(self, vector: numpy.ndarray) -> numpy.ndarray:
        """Find the nearest neghbor(s) to a vector
    
        Args:
          - vector, the vector you are going find the nearest neighbor for
    
        Returns:
          - k_idx: the indices of the top k closest vectors in sorted form
        """
        return numpy.argsort([self.cosine_similarity(vector, row)
                              for row in self.candidates])[-self.k:]

    def __call__(self, vector: numpy.ndarray) -> numpy.ndarray:
        """Alias for the `nearest_neighbors` method
    
        Args:
          - vector, the vector you are going find the nearest neighbor for
    
        Returns:
          - k_idx: the indices of the top k closest vectors in sorted form
        """
        return self.nearest_neighbors(vector)
