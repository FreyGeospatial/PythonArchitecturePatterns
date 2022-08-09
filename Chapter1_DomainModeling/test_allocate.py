from datetime import date, timedelta

import pytest
from model import Batch, OrderLine, allocate, OutOfStock

today = date.today()
tomorrow = date.today() + timedelta(days=1)
later = date.today() + timedelta(days=10)

def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    # allocate 10 from a batch containing inventory of 10
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    # cannot allocate further, so exception will be raised
    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])