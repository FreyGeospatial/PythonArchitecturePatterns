from model import OrderLine
from model import Batch
from datetime import date

# let's assume that we have 20 small tables in inventory and
# we allocate an order line for 2 of those.
#
# Therefore, our inventory (or batch) should have 18 remaining

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('order-ref', "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18

