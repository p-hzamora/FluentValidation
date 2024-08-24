from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, override


class IEnumerable[T](ABC):
    """
    Interface to emulate list type in Python
    """

    @abstractmethod
    def append(self, __object: T): ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __getitem__(self, index: int) -> T: ...

    @abstractmethod
    def __iter__(self): ...


class IDisposable(ABC):
    @abstractmethod
    def Dispose(self): ...

    @abstractmethod
    def __enter__(self): ...

    @abstractmethod
    def __exit__(self, *args, **kwargs): ...


class EventDisposable[T](IDisposable):
    def __init__(self, parent: TrackingCollection[T], handler: Callable[[T], None]):
        self.parent: TrackingCollection[T] = parent
        self.handler: Callable[[T], None] = handler

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.Dispose()

    @override
    def Dispose(self) -> None:
        self.parent.ItemAdded.remove(self.handler)


class CaptureDisposable[T](IDisposable):
    def __init__(self, parent: TrackingCollection[T], _old: Callable[[T], None]):
        self._parent: TrackingCollection[T] = parent
        self._old: Callable[[T], None] = _old

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.Dispose()

    @override
    def Dispose(self) -> None:
        self._parent._capture = self._old


class TrackingCollection[T](IEnumerable[T]):
    def __init__(self):
        self._innerCollection: list[T] = []
        self.ItemAdded: list[Callable[[T], None]] = []
        self._capture: Callable[[T], None] = None

    @override
    def append(self, item: T) -> None:
        if self._capture is None:
            self._innerCollection.append(item)
        else:
            self._capture(item)

        self._invoke_item_added(item)

    def _invoke_item_added(self, item: T):
        # due to ItemAdded is an event we need to loop over all items inside ->   ItemAdded?.Invoke(item)
        for handler in self.ItemAdded:
            handler(item)

    @override
    def __len__(self) -> int:
        return len(self._innerCollection)

    @override
    def __getitem__(self, index: int) -> T:
        return self._innerCollection[index]

    @override
    def __iter__(self):
        return iter(self._innerCollection)

    def OnItemAdded(self, onItemAdded: Callable[[T], None]) -> IDisposable:
        self.ItemAdded.append(onItemAdded)
        return EventDisposable(self, onItemAdded)

    def Capture(self, onItemAdded: Callable[[T], None]) -> IDisposable:
        return CaptureDisposable(self, onItemAdded)


if __name__ == "__main__":

    def item_added_handler(item: str):
        print(f"Item added: {item}")

    def capture_handler(item: str):
        print(f"Captured: {item}")

    collection = TrackingCollection()

    with collection.OnItemAdded(item_added_handler):
        collection.append("Item 1")
        collection.append("Item 2")

    with collection.Capture(capture_handler):
        collection.append("Item 3")

    collection.append("Item 4")

    for item in collection:
        print(item)

    print(f"Count: {len(collection)}")
