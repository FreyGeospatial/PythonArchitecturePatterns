from dataclasses import dataclass
from datetime import date
from typing import Optional, Set

# to note:
# a set is an unordered, unchangeable, unindexed collection. No duplicates are accepted

@dataclass(frozen=True) # frozen dataclasses mean that an object cannot be modified!
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
        self._purchased_quantity is how much inventory of product is available
        self._allocations is a set of OrderLines for the batch
        """

        self.reference: str = ref
        self.sku: str = sku
        self.eta: Optional[date] = eta
        self._purchased_quantity: int = qty # the amount of inventory available
        self._allocations: Set[OrderLine] = set() # of type set, which can contain OderLines

    # If a string is the first thing presented in a function, by
    # default it becomes the docstring. To access, use `help(Batch.allocate)`
    def allocate(self, line: OrderLine) -> None:
        """
        add the orderline to the set
        """
        if self.can_allocate(line):
            self._allocations.add(line) # .add() is a method available to sets
    
    def deallocate(self, line: OrderLine) -> None:
        """
        remove the allocation / orderline from the set (maybe order was cancelled?)
        """
        if line in self._allocations:
            self._allocations._allocations.remove(line) # .remove() is a method available to sets

    @property
    def allocated_quantity(self) -> int:
        """sums the quantity of allocations"""
        return sum(line.qty for line in self._allocations)
    
    @property # by setting the @property decorator, we can access this function as a class attribute, without paranetheses!
    def available_quantity(self) -> int:
        """finds the remaining batch inventory after order lines have been placed"""
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        """
        Do we have the product listed in the system?
        Do we have the item in stock?
        """
        return self.sku == line.sku and self.available_quantity >= line.qty # see here how no parantheses were used for available_quantity method.
                                                                            # note that if we tried, paranetheses would no longer work

