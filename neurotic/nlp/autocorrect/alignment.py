# from pypi
import attr

# this repo
from neurotic.nlp.autocorrect.distance import MinimumEdits


@attr.s(auto_attribs=True)
class Aligner:
    """Create the alignment path

    Args: 
     source: the source string to align
     target: the target string to align
     empty_token: character to use to fill in alignments
    """
    source: str
    target: str
    empty_token: str="*"
    _source_alignment: list=None
    _target_alignment: list=None
    _table: str=None
    _editor: MinimumEdits=None
    _path: list=None

    @property
    def editor(self) -> MinimumEdits:
        """object to figure out the minimum edit distance"""
        if self._editor is None:
            self._editor = MinimumEdits(self.source, self.target)
        return self._editor

    @property
    def path(self) -> list:
        """An optimal path through the distance table"""
        if self._path is None:
            distances = self.editor.distance_table
            # start at the bottom right cell
            current_row, current_column = (len(distances) - 1,
                                           len(distances[0]) - 1)
            path = [(current_row, current_column)]
            while (current_row, current_column) != (0, 0):
                one_row_back = current_row - 1
                one_column_up = current_column - 1
                edits = (
                    # insert
                    (distances[one_row_back, current_column], (one_row_back, current_column)),
                    # delete
                    (distances[current_row, one_column_up], (current_row, one_column_up)),
                    # substitute
                    (distances[one_row_back, one_column_up], (one_row_back, one_column_up))
                )
                minimum_edit_distance, cell_coordinates = min(edits)
                path.append(cell_coordinates)
                current_row, current_column = cell_coordinates
            self._path = list(reversed(path))
        return self._path

    @property
    def source_alignment(self) -> list:
        """the aligned source tokens
    
        Warning:
         this doesn't create them, call the object to do that
        """
        return self._source_alignment

    @property
    def target_alignment(self) -> list:
        """The aligned target tokens
    
        Warning:
         this doesn't create them, the __call__ does
        """
        return self._target_alignment

    @property
    def table(self) -> str:
        """The alignments as an orgtable"""
        if self._table is None:
            if self.source_alignment is None or self.target_alignment is None:
                self()
            self._table = (f"|{'|'.join(self.source_alignment)}|\n"
                           f"|{'|'.join(self.target_alignment)}|")
        return self._table

    def __call__(self) -> tuple:
        """Sets the source and target token alignments
    
        Note:
         as a side-effect also sets source_alignment and target_alignment
    
        Returns:
         tuple of source and target tokens after alignment
        """
        previous_row = previous_column = None
        source_tokens = []
        target_tokens = []
        source = self.empty_token + self.source
        target = self.empty_token + self.target
        for current_row, current_column in self.path[1:]:
            source_token = (
                source[current_row] if current_row != previous_row
                else self.empty_token)
            target_token = (
                target[current_column] if current_column != previous_column
                else self.empty_token)
            
            source_tokens.append(source_token)
            target_tokens.append(target_token)
    
            previous_row, previous_column = current_row, current_column
        
        self._source_alignment = source_tokens
        self._target_alignment = target_tokens
        return source_tokens, target_tokens
    

    def __str__(self) -> str:
        """pass-through for the table"""
        return self.table
