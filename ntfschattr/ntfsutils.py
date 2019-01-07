import xattr

#: Table mapping symbolic attribute names into actual attribute masks.
NTFS_ATTRIBUTE_TABLE = {
    'readonly': 0x1,
    'hidden': 0x2,
    'system': 0x4,
    'archive': 0x20,
    'temporary': 0x100,
    'compressed': 0x800,
    'offline': 0x1000,
    'content_not_indexed': 0x2000
}


class NtfsFile(object):
    """
    NtfsFile represents a file or folder in an NTFS filesystem for which attributes can be read
    and written.
    """

    def __init__(self, path):
        self.path = path

    def __getattr__(self, key):
        if key in NTFS_ATTRIBUTE_TABLE:
            return (NTFS_ATTRIBUTE_TABLE[key] & self._raw_attributes()) != 0

        return self.__getattribute__(key)

    def set_attribute(self, attribute: str) -> None:
        """
        Sets the given attribute in the underlying NTFS path.

        :param attribute:
            a valid attribute key (as per py:const:`NTFS_ATTRIBUTE_TABLE`).
        """
        mask = NTFS_ATTRIBUTE_TABLE[attribute]
        self._write_raw_attributes(
            self._raw_attributes() | mask
        )

    def clear_attribute(self, attribute: str) -> None:
        """
        Clears the given attribute in the underlying NTFS path.

        :param attribute:
            a valid attribute key (as per py:const:`NTFS_ATTRIBUTE_TABLE`).
        """
        flip_mask = NTFS_ATTRIBUTE_TABLE[attribute] ^ 0xFFFFFFFF
        self._write_raw_attributes(
            self._raw_attributes() & flip_mask
        )

    def _raw_attributes(self) -> int:
        return int.from_bytes(
            xattr.get(self.path, 'system.ntfs_attrib'),
            'little'
        )

    def _write_raw_attributes(self, attributes: int) -> None:
        xattr.set(
            self.path,
            'system.ntfs_attrib',
            int.to_bytes(attributes, 4, 'little')
        )

    def __str__(self) -> str:
        attributes = [
            attribute for attribute in NTFS_ATTRIBUTE_TABLE.keys()
            if self.__getattr__(attribute)
        ]

        return '%s: [%s]' % (self.path, ','.join(attributes))
