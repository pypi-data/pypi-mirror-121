import dataclasses

from pycspr.types.cl import CLAccessRights


@dataclasses.dataclass
class UnforgeableReference():
    """An unforgeable reference storage key.
    
    """
    # Uref on-chain identifier.
    address: bytes
    
    # Access rights granted by issuer. 
    access_rights: CLAccessRights

    def as_string(self):
        """Returns a string representation for over the wire dispatch.
        
        """
        return f"uref-{self.address.hex()}-{self.access_rights.value:03}"


@dataclasses.dataclass
class DictionaryIdentifier():
    """A set of variants for performation dictionary item state queries.
    
    """
    pass


@dataclasses.dataclass
class DictionaryIdentifier_AccountNamedKey(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via an Account's named keys.
    
    """
    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    # The account key as a formatted string whose named keys contains dictionary_name.
    key: str


@dataclasses.dataclass
class DictionaryIdentifier_ContractNamedKey(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via a Contract's named keys.
    
    """
    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    # The contract key as a formatted string whose named keys contains dictionary_name.
    key: str


@dataclasses.dataclass
class DictionaryIdentifier_SeedURef(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via it's seed unforgeable reference.
    
    """
    # The dictionary item key.
    dictionary_item_key: str

    # The dictionary's seed URef.
    seed_uref: UnforgeableReference


@dataclasses.dataclass
class DictionaryIdentifier_UniqueKey(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via it's unique key.
    
    """
    # The globally unique dictionary key.
    key: str


@dataclasses.dataclass
class StorageKey():
    """A pointer to data within global state.
    
    """
    # 32 byte key identifier.
    identifier: bytes


@dataclasses.dataclass
class StorageKey_Account(StorageKey):
    """Represents an account identity key.
    
    """
    def as_string(self):
        """Returns a string representation for over the wire dispatch.
        
        """
        return f"account-hash-{self.identifier.hex()}"


@dataclasses.dataclass
class StorageKey_Hash(StorageKey):
    """Represents an immutable contract identifier.
    
    """
    def as_string(self):
        """Returns a string representation for over the wire dispatch.
        
        """
        return f"hash-{self.identifier.hex()}"


@dataclasses.dataclass
class StorageKey_UnforgeableReference(StorageKey):
    """Represents an unforgeable reference.
    
    """
    def as_string(self):
        """Returns a string representation for over the wire dispatch.
        
        """
        return f"uref-{self.identifier.hex()}"
