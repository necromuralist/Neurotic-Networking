# python
import math

# pypi
import attr
import numpy


@attr.s(auto_attribs=True)
class PlanesUniverse:
    """Creates set of planes with a random mormal distribution of points


    Args:
     vector_count: number of vectors that will be hashed
     dimensions: number of columns per vector
     universes: number of universes to create
     vectors_per_bucket: how many vectors we want in each
     random_seed: value to seed the random number generator
    """
    vector_count: int
    dimensions: int
    universes: int
    vectors_per_bucket: int
    random_seed: int=0
    _plane_count: int=None
    _planes: list=None

    @property
    def plane_count(self) -> int:
        """The number of planes to create
    
        Uses the number of vectors and desired vectors per bucket
        """
        if self._plane_count is None:
            buckets = self.vector_count/self.vectors_per_bucket
            self._plane_count = math.ceil(numpy.log2(buckets))
        return self._plane_count

    @property
    def planes(self) -> list:
        """The list of planes"""
        if self._planes is None:
            numpy.random.seed(self.random_seed)
            self._planes = [numpy.random.normal(size=(self.dimensions,
                                                      self.plane_count))
                            for _ in range(self.universes)]
        return self._planes


@attr.s(auto_attribs=True)
class DocumentsEmbeddings:
    """Builds embeddings for documents from their words

    Args:
     embeddings: word-embeddings for the documents
     process: callable to pre-process documents
     documents: documents (strings) to hash
    """
    embeddings: dict
    process: object
    documents: list
    _documents_embeddings: numpy.ndarray=None
    _document_index_to_embedding: dict=None

    def document_embedding(self, document: str) -> numpy.ndarray: 
        """sums the embeddings for words in the document
        
        Args:
          - document: string to tokenize and build embedding for
        
        Returns:
          - embedding: sum of all word embeddings in the document
        """
        rows = len(next(iter(self.embeddings.values())))
        embedding = numpy.zeros(rows)
        words = self.process(document)
        # adding the zeros means you always return an array, not just the number 0
        # if none of the words in the document are in the embeddings
        return embedding + sum((self.embeddings.get(word, 0) for word in words))

    @property
    def documents_embeddings(self) -> numpy.ndarray:
        """array of embeddings for each document in documents"""
        if self._documents_embeddings is None:
            self._documents_embeddings = numpy.vstack(
                [self.document_embedding(document) for document in self.documents])
        return self._documents_embeddings

    @property
    def document_index_to_embedding(self) -> dict:
        """maps document index (from self.documents) to embedding"""
        if self._document_index_to_embedding is None:
            self._document_index_to_embedding = {
                index: embedding for index, embedding in enumerate(
                    self.documents_embeddings)}
        return self._document_index_to_embedding


@attr.s(auto_attribs=True)
class HashTable:
    """Builds the hash-table for embeddings

    Args:
     planes: matrix of planes to divide into hash table
     vectors: vectors to be hashed
    """
    planes: numpy.ndarray
    vectors: numpy.ndarray
    _hashes: list=None
    _hash_table: dict=None
    _index_table: dict=None

    def hash_value(self, vector: numpy.ndarray) -> int:
        """
        Create a hash for a vector
    
        Args:
         - vector:  vector of tweet. It's dimension is (1, N_DIMS)
    
        Returns:
          - res: a number which is used as a hash for your vector
        """
        rows, columns = self.planes.shape
        # assert vector.shape == (1, rows), vector.shape
        dot_product = numpy.dot(vector, self.planes)
        #assert dot_product.shape == (1, columns), dot_product.shape
    
        sign_of_dot_product = numpy.sign(dot_product)
        hashes = sign_of_dot_product >= 0
        assert hashes.shape == dot_product.shape
    
        # remove extra un-used dimensions (convert this from a 2D to a 1D array)
        hashes = numpy.squeeze(hashes)
        hash_value = 0
    
        for column in range(columns):
            hash_value += 2**column * hashes[column]
        return int(hash_value)

    @property
    def hashes(self) -> list:
        """Vector hashes"""
        if self._hashes is None:
            self._hashes = [self.hash_value(vector) for vector in self.vectors]
        return self._hashes

    @property
    def hash_table(self) -> dict:
        """Hash table of vectors
    
        Returns:
          hash_table: dictionary - keys are hashes, values are lists of vectors (hash buckets)
        """
        if self._hash_table is None:
            number_of_planes = self.planes.shape[1]
            number_of_buckets = 2**number_of_planes
    
            self._hash_table = {index: [] for index in range(number_of_buckets)}
    
            for index, hash_ in enumerate(self.hashes):
                self._hash_table[hash_].append(self.vectors[index])
        return self._hash_table

    @property
    def index_table(self) -> dict:
        """Tabel of document hash to index"""
        if self._index_table is None:
            number_of_planes = self.planes.shape[1]
            number_of_buckets = 2**number_of_planes
    
            self._index_table = {index: [] for index in range(number_of_buckets)}
    
            for index, hash_ in enumerate(self.hashes):            
                self._index_table[hash_].append(index)
        return self._index_table



@attr.s(auto_attribs=True)
class HashTables:
    """Builds the universes of hash tables

    Args:
     universes: how many universes
     planes: planes to hash vectors into
     vectors: vectors to hash
    """
    universes: int
    planes: list
    vectors: numpy.ndarray
    _hash_tables: list=None
    _id_tables: list=None

    @property
    def hash_tables(self) -> list:
        """Builds the list of hash tables"""
        if self._hash_tables is None: 
            self._hash_tables = [
                HashTable(vectors=self.vectors,
                          planes=self.planes[universe]).hash_table
                for universe in range(self.universes)
            ]
        return self._hash_tables

    @property
    def id_tables(self) -> list:
        """Builds the list of id tables"""
        if self._id_tables is None: 
            self._id_tables = [
                HashTable(vectors=self.vectors,
                          planes=self.planes[universe]).index_table
                for universe in range(self.universes)
            ]
        return self._id_tables
