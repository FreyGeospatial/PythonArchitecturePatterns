from datetime import date
from typing import Tuple

from model import Batch, OrderLine

# let's assume that we have 20 small tables in inventory and
# we allocate an order line for 2 of those.
#
# Therefore, our inventory (or batch) should have 18 remaining

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('order-ref', "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18

    # although we've written a lot of code just to subtract one value from another, modeling
    # our domain will probably pay off.

def make_batch_and_line(sku, batch_qty, line_qty) -> Tuple:
    """Create a batch object and an order"""
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty)        
    )

def test_can_allocate_if_available_greater_than_require() -> None:
    """this test should pass, as order line quantity is less than inventory (batch) quantity"""
    large_batch, small_line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=20, line_qty=2)
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_if_available_smaller_than_required() -> None:
    """this test should fail, as the order (line) quantity is larger than inventory (batch)"""
    small_batch, large_line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=2, line_qty=20)
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_available_equal_to_required() -> None:
    """This should pass as order line and batch quantities are equal"""
    batch, line = make_batch_and_line(sku="ELEGANT-LAMP", batch_qty=2, line_qty=2)
    assert batch.can_allocate(line)

def test_cannot_allocate_if_skus_do_not_match() -> None:
    """This should assert false as skus do not match"""
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(different_sku_line) is False

def test_can_only_deallocate_allocated_lines() -> None:
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20
