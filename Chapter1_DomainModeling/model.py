from dataclasses import dataclass
from datetime import date
from typing import Optional, Set, List

# to note:
# a set is an unordered, unchangeable, unindexed collection. No duplicates are accepted

class OutOfStock(Exception):
    pass

@dataclass(frozen=True) # frozen dataclasses mean that an object cannot be modified!
class OrderLine:
    """
    What actually is a lne? An order can have multiple line items, where
    each line has a SKU and a quantity. While an order has a reference that
    uniquely identifies it, a line does not. Whenever we have a business concept
    that contains data but no identity, we often choose to represent it using the
    Value Object Pattern.

    A value object is any domain object that is uniquely identified by the data it holds.
    As such, we often make them ummutable.

    E.g, two lnes with the same orderid, sku, and qty are equal. See the 'money' example in
    value_object.py and its test file.
    """
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
    
    def __eq__(self, other):
        """
        It is better to be explicit here, when comparing two class objects.
        If the Batch shares a reference number, the two are the same. Allows us
        to directorly compare them using `==` operator
        """
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __hash__(self):
        """lets find out more about what this does!"""
        return hash(self.reference)

    def __gt__(self, other):
        """required when sorting. we define here how we sort!"""
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


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

def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')