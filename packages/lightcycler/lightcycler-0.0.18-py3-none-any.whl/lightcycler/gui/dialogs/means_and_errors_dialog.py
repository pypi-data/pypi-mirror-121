from PyQt5 import QtWidgets

from pylab import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from lightcycler.kernel.models.groups_model import GroupsModel


class MeansAndErrorsDialog(QtWidgets.QDialog):

    def __init__(self, statistics, *args, **kwargs):

        super(MeansAndErrorsDialog, self).__init__(*args, **kwargs)

        self._statistics = statistics

        self._init_ui()

    def _build_events(self):
        """Build the events related with the widget.
        """

        self._selected_gene_combobox.currentIndexChanged.connect(self.on_select_gene)
        self._selected_zone_combobox.currentIndexChanged.connect(self.on_select_zone)

    def _build_layout(self):
        """Build the layout of the widget.
        """

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(self._means_and_errors_canvas)
        main_layout.addWidget(self._means_and_errors_toolbar)

        hlayout = QtWidgets.QHBoxLayout()

        hlayout.addWidget(self._selected_gene_label)
        hlayout.addWidget(self._selected_gene_combobox)
        hlayout.addWidget(self._selected_zone_label)
        hlayout.addWidget(self._selected_zone_combobox)
        hlayout.addStretch()

        main_layout.addLayout(hlayout)

        self.setGeometry(0, 0, 600, 400)

        self.setLayout(main_layout)

    def _build_widgets(self):
        """Build the widgets of the widget.
        """

        self._means_and_errors_figure = Figure()
        self._means_and_errors_axes = self._means_and_errors_figure.add_subplot(111)
        self._means_and_errors_canvas = FigureCanvasQTAgg(self._means_and_errors_figure)
        self._means_and_errors_toolbar = NavigationToolbar2QT(self._means_and_errors_canvas, self)

        self._selected_gene_label = QtWidgets.QLabel('Gene')
        self._selected_gene_combobox = QtWidgets.QComboBox()
        self._selected_gene_combobox.addItems(self._statistics.keys())

        self._selected_zone_label = QtWidgets.QLabel('Zone')
        self._selected_zone_combobox = QtWidgets.QComboBox()
        self._selected_zone_combobox.addItems(GroupsModel.student_test_zones)

    def _init_ui(self):

        self._build_widgets()
        self._build_layout()
        self._build_events()

        self.on_select_gene(0)

    def on_select_gene(self, index):
        """Event handler which updates the means and errors plot for the selected gene.

        Args:
            index (int): the index of the select gene
        """

        gene = self._selected_gene_combobox.currentText()

        zone = self._selected_zone_combobox.currentText()

        self._plot(self._statistics[gene][zone])

    def on_select_zone(self, index):
        """Event handler which updates the means and errors plot for the selected gene.

        Args:
            index (int): the index of the select gene
        """

        gene = self._selected_gene_combobox.currentText()

        zone = self._selected_zone_combobox.currentText()

        self._plot(self._statistics[gene][zone])

    def _plot(self, df):
        """
        """

        self._means_and_errors_axes.clear()
        self._means_and_errors_axes.set_xlabel('groups')
        self._means_and_errors_axes.set_ylabel('Means')

        self._means_and_errors_axes.bar(df.columns, df.loc['mean'], yerr=df.loc['stddev'], align='center', alpha=0.5, ecolor='black', capsize=10)

        # self._means_and_errors_axes.set_xticklabels(statistics_per_gene.columns, rotation=90)
        for tick in self._means_and_errors_axes.xaxis.get_major_ticks():
            tick.label.set_fontsize(6)

        self._means_and_errors_canvas.draw()
