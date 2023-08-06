import copy

from PyQt5 import QtCore


class AvailableSamplesModel(QtCore.QAbstractListModel):

    def __init__(self, *args, **kwargs):
        """Constructor.
        """

        super(AvailableSamplesModel, self).__init__(*args, **kwargs)

        self._samples = []

        self._samples_default = []

    def clear(self):
        """Clear the model.
        """

        self._samples = []
        self._samples_default = []

        self.layoutChanged.emit()

    def data(self, index, role):
        """Get the data at a given index for a given role.

        Args:
            index (QtCore.QModelIndex): the index
            role (int): the role

        Returns:
            QtCore.QVariant: the data
        """

        if not index.isValid():
            return QtCore.QVariant()

        if not self._samples:
            return QtCore.QVariant()

        idx = index.row()

        if role == QtCore.Qt.DisplayRole:
            return self._samples[idx]

    def flags(self, index):
        """Return the flags of an itme with a given index.

        Args:
            index (PyQt5.QtCore.QModelIndex): the index

        Returns:
            int: the flag
        """

        if index.isValid():
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled

    def remove_items(self, items):
        """Remove samples from the model.

        Args:
            items (list of str): the sample to remove
        """

        indexes = []

        for item in items:
            try:
                indexes.append(self._samples.index(item))
            except ValueError:
                continue

        indexes.sort()
        indexes.reverse()

        for idx in indexes:
            self.beginRemoveRows(QtCore.QModelIndex(), idx, idx)
            del self._samples[idx]
            self.endRemoveRows()

    def reset(self):
        """Reset the model.
        """

        self._samples = copy.copy(self._samples_default)
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        """Returns the number of samples.

        Return:
            int: the number of samples
        """

        return len(self._samples)

    @property
    def samples(self):
        """Return the samples.

        Return:
            list of str: the samples
        """

        return self._samples

    @samples.setter
    def samples(self, samples):
        """Set the samples.

        Args:
            samples (list of str): the samples
        """

        self._samples = sorted(samples)

        self._samples_default = copy.copy(samples)

        self.layoutChanged.emit()

    def add_item(self, item):
        """Add a sample to the model.

        Args:
            item (str): the sample
        """

        if item in self._samples:
            return

        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())

        self._samples.append(item)

        self.endInsertRows()
