from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        """
        Creates a Batch of stock, or inventory, which is modeled as an object. 
        
        self.reference is a Batch ID.
        self.sku is the SKU number for the product
        self.eta is the estimated time of delivery
        self.available_quantity is how much inventory of product is available
        """

        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty


    # If a string is the first thing presented in a function, by
    # default it becomes the docstring. To access, use `help(Batch.allocate)`
    def allocate(self, line: OrderLine):
        """
        remove inventory after order is placed
        """
        self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        """
        Do we have the product listed in the system?
        Do we have the item in stock?
        """
        return self.sku == line.sku and self.available_quantity >= line.qty

