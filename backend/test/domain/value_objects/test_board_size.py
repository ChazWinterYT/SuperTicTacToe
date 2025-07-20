import pytest
from app.domain.value_objects.board_size import BoardSize
from app.core.exceptions import ValidationError


class TestBoardSize:
    def test_create_standard_board(self):
        board = BoardSize.create_standard()
        assert board.width == 3
        assert board.height == 3
        assert board.total_cells == 9
        assert board.is_square is True

    def test_create_square_board(self):
        board = BoardSize.create_square(5)
        assert board.width == 5
        assert board.height == 5
        assert board.total_cells == 25
        assert board.is_square is True

    def test_create_custom_board(self):
        board = BoardSize(5, 5)
        assert board.width == 5
        assert board.height == 5
        assert board.total_cells == 25
        assert board.is_square is True

    def test_create_rectangular_board(self):
        board = BoardSize(3, 5)
        assert board.width == 3
        assert board.height == 5
        assert board.total_cells == 15
        assert board.is_square is False

    def test_invalid_board_size_too_small(self):
        with pytest.raises(ValidationError):
            BoardSize(2, 2)

    def test_invalid_board_size_too_large(self):
        with pytest.raises(ValidationError):
            BoardSize(16, 16)

    def test_invalid_board_size_mixed(self):
        with pytest.raises(ValidationError):
            BoardSize(2, 5)  # Width too small

    def test_get_winning_sequences_3x3(self):
        board = BoardSize.create_standard()
        sequences = board.get_winning_sequences()
        assert len(sequences) > 0
        # Should have 8 winning combinations in 3x3 (3 rows + 3 cols + 2 diagonals)
        assert len(sequences) == 8

    def test_get_winning_sequences_5x5(self):
        board = BoardSize.create_square(5)
        sequences = board.get_winning_sequences()
        assert len(sequences) > 0
        # 5x5 should have more winning sequences than 3x3
        assert len(sequences) > 8

    def test_winning_sequences_contain_valid_positions(self):
        board = BoardSize.create_standard()
        sequences = board.get_winning_sequences()
        
        for sequence in sequences:
            assert len(sequence) == 3  # All sequences should be 3-in-a-row
            for position in sequence:
                assert 0 <= position < board.total_cells

    def test_string_representation(self):
        board = BoardSize(3, 5)
        assert str(board) == "3x5"
        assert repr(board) == "BoardSize(3, 5)" 