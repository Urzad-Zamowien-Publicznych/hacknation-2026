from src.text_extraction.models import BBox, TextBlock, sort_reading_order


def _block(text: str, page: int, top: float | None, left: float = 50.0) -> TextBlock:
    bbox = BBox(left, top, left + 10, top + 10) if top is not None else None
    return TextBlock(text=text, label="text", page=page, bbox=bbox, layer="body")


def test_reading_order_follows_geometry_not_input_order():
    blocks = [_block("footer", 1, 800), _block("page 2", 2, 10), _block("right", 1, 100, left=400),
              _block("title", 1, 50), _block("left", 1, 101)]
    assert [b.text for b in sort_reading_order(blocks)] == ["title", "left", "right", "footer", "page 2"]


def test_blocks_without_bbox_go_to_end_of_their_page():
    blocks = [_block("p2", 2, 10), _block("no box", 1, None), _block("p1", 1, 10)]
    assert [b.text for b in sort_reading_order(blocks)] == ["p1", "no box", "p2"]


def test_table_renders_as_pipe_separated_rows():
    table = TextBlock(text="", label="table", page=1, bbox=None, layer="body",
                      table_rows=(("Wartość", "50,00 "), ("Waluta", "PLN")))
    assert table.is_table
    assert table.render() == "Wartość | 50,00\nWaluta | PLN"
