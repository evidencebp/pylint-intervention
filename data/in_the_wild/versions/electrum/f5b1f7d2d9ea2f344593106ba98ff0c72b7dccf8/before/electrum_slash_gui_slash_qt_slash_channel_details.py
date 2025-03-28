from typing import TYPE_CHECKING, Sequence

import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QGridLayout

from electrum.util import EventListener
from electrum.i18n import _
from electrum.util import bh2u, format_time
from electrum.lnutil import format_short_channel_id, LOCAL, REMOTE, UpdateAddHtlc, Direction
from electrum.lnchannel import htlcsum, Channel, AbstractChannel, HTLCWithStatus
from electrum.lnaddr import LnAddr, lndecode
from electrum.bitcoin import COIN
from electrum.wallet import Abstract_Wallet

from .util import Buttons, CloseButton, ShowQRLineEdit, MessageBoxMixin, WWLabel
from .util import QtEventListener, qt_event_listener

if TYPE_CHECKING:
    from .main_window import ElectrumWindow

class HTLCItem(QtGui.QStandardItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(False)

class SelectableLabel(QtWidgets.QLabel):
    def __init__(self, text=''):
        super().__init__(text)
        self.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

class LinkedLabel(QtWidgets.QLabel):
    def __init__(self, text, on_clicked):
        super().__init__(text)
        self.linkActivated.connect(on_clicked)


class ChannelDetailsDialog(QtWidgets.QDialog, MessageBoxMixin, QtEventListener):

    def make_htlc_item(self, i: UpdateAddHtlc, direction: Direction) -> HTLCItem:
        it = HTLCItem(_('Sent HTLC with ID {}' if Direction.SENT == direction else 'Received HTLC with ID {}').format(i.htlc_id))
        it.appendRow([HTLCItem(_('Amount')),HTLCItem(self.format_msat(i.amount_msat))])
        it.appendRow([HTLCItem(_('CLTV expiry')),HTLCItem(str(i.cltv_expiry))])
        it.appendRow([HTLCItem(_('Payment hash')),HTLCItem(bh2u(i.payment_hash))])
        return it

    def make_model(self, htlcs: Sequence[HTLCWithStatus]) -> QtGui.QStandardItemModel:
        model = QtGui.QStandardItemModel(0, 2)
        model.setHorizontalHeaderLabels(['HTLC', 'Property value'])
        parentItem = model.invisibleRootItem()
        folder_types = {
            'settled': _('Fulfilled HTLCs'),
            'inflight': _('HTLCs in current commitment transaction'),
            'failed': _('Failed HTLCs'),
        }
        self.folders = {}
        self.keyname_rows = {}

        for keyname, i in folder_types.items():
            myFont=QtGui.QFont()
            myFont.setBold(True)
            folder = HTLCItem(i)
            folder.setFont(myFont)
            parentItem.appendRow(folder)
            self.folders[keyname] = folder
            mapping = {}
            num = 0
            for htlc_with_status in htlcs:
                if htlc_with_status.status != keyname:
                    continue
                htlc = htlc_with_status.htlc
                it = self.make_htlc_item(htlc, htlc_with_status.direction)
                self.folders[keyname].appendRow(it)
                mapping[htlc.payment_hash] = num
                num += 1
            self.keyname_rows[keyname] = mapping
        return model

    def move(self, fro: str, to: str, payment_hash: bytes):
        assert fro != to
        row_idx = self.keyname_rows[fro].pop(payment_hash)
        row = self.folders[fro].takeRow(row_idx)
        self.folders[to].appendRow(row)
        dest_mapping = self.keyname_rows[to]
        dest_mapping[payment_hash] = len(dest_mapping)

    @qt_event_listener
    def on_event_channel(self, wallet, chan):
        if chan == self.chan:
            self.update()

    @qt_event_listener
    def on_event_htlc_added(self, chan, htlc, direction):
        if chan != self.chan:
            return
        mapping = self.keyname_rows['inflight']
        mapping[htlc.payment_hash] = len(mapping)
        self.folders['inflight'].appendRow(self.make_htlc_item(htlc, direction))

    @qt_event_listener
    def on_event_htlc_fulfilled(self, payment_hash, chan, htlc_id):
        if chan.channel_id != self.chan.channel_id:
            return
        self.move('inflight', 'settled', payment_hash)
        self.update()

    @qt_event_listener
    def on_event_htlc_failed(self, payment_hash, chan, htlc_id):
        if chan.channel_id != self.chan.channel_id:
            return
        self.move('inflight', 'failed', payment_hash)
        self.update()

    def update(self):
        self.can_send_label.setText(self.format_msat(self.chan.available_to_spend(LOCAL)))
        self.can_receive_label.setText(self.format_msat(self.chan.available_to_spend(REMOTE)))
        self.sent_label.setText(self.format_msat(self.chan.total_msat(Direction.SENT)))
        self.received_label.setText(self.format_msat(self.chan.total_msat(Direction.RECEIVED)))
        self.local_balance_label.setText(self.format_msat(self.chan.balance(LOCAL)))
        self.remote_balance_label.setText(self.format_msat(self.chan.balance(REMOTE)))

    @QtCore.pyqtSlot(str)
    def show_tx(self, link_text: str):
        funding_tx = self.wallet.db.get_transaction(self.chan.funding_outpoint.txid)
        if not funding_tx:
            self.show_error(_("Funding transaction not found."))
            return
        self.window.show_transaction(funding_tx, tx_desc=_('Funding Transaction'))

    def __init__(self, window: 'ElectrumWindow', chan_id: bytes):
        super().__init__(window)

        # initialize instance fields
        self.window = window
        self.wallet = window.wallet
        chan = self.chan = window.wallet.lnworker.channels[chan_id]
        self.format_msat = lambda msat: window.format_amount_and_units(msat / 1000)
        self.format_sat = lambda sat: window.format_amount_and_units(sat)

        # register callbacks for updating
        self.register_callbacks()

        # set attributes of QDialog
        self.setWindowTitle(_('Channel Details'))
        self.setMinimumSize(800, 400)

        # add layouts
        vbox = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout(None)
        remote_id_e = ShowQRLineEdit(chan.node_id.hex(), self.window.config, title=_("Remote Node ID"))
        form.addRow(QLabel(_('Remote Node') + ':'), remote_id_e)
        channel_id_e = ShowQRLineEdit(chan.channel_id.hex(), self.window.config, title=_("Channel ID"))
        form.addRow(QLabel(_('Channel ID') + ':'), channel_id_e)
        funding_label_text = f'<a href=click_destination>{chan.funding_outpoint.txid}</a>:{chan.funding_outpoint.output_index}'
        form.addRow(QLabel(_('Funding Outpoint') + ':'), LinkedLabel(funding_label_text, self.show_tx))
        form.addRow(QLabel(_('Short Channel ID') + ':'), QLabel(str(chan.short_channel_id)))
        form.addRow(QLabel(_('State') + ':'), SelectableLabel(chan.get_state_for_GUI()))
        self.capacity = self.format_sat(chan.get_capacity())
        form.addRow(QLabel(_('Capacity') + ':'), SelectableLabel(self.capacity))
        form.addRow(QLabel(_('Channel type:')), SelectableLabel(chan.storage['channel_type'].name_minimal))
        initiator = 'Local' if chan.constraints.is_initiator else 'Remote'
        form.addRow(QLabel(_('Initiator:')), SelectableLabel(initiator))
        vbox.addLayout(form)
        hbox_stats = QHBoxLayout()
        form_layout_left = QtWidgets.QFormLayout(None)
        form_layout_right = QtWidgets.QFormLayout(None)
        self.local_balance_label = SelectableLabel()
        self.remote_balance_label = SelectableLabel()
        form_layout_left.addRow(_('Local balance') + ':', self.local_balance_label)
        form_layout_right.addRow(_('Remote balance') + ':', self.remote_balance_label)
        self.can_send_label = SelectableLabel()
        self.can_receive_label = SelectableLabel()
        form_layout_left.addRow(_('Can send') + ':', self.can_send_label)
        form_layout_right.addRow(_('Can receive') + ':', self.can_receive_label)
        local_reserve_label = SelectableLabel("{}".format(
            self.format_sat(chan.config[LOCAL].reserve_sat),
        ))
        remote_reserve_label = SelectableLabel("{}".format(
            self.format_sat(chan.config[REMOTE].reserve_sat),
        ))
        form_layout_left.addRow(_('Local reserve') + ':', local_reserve_label)
        form_layout_right.addRow(_('Remote reserve' + ':'), remote_reserve_label)
        #self.htlc_minimum_msat = SelectableLabel(str(chan.config[REMOTE].htlc_minimum_msat))
        #form_layout_left.addRow(_('Minimum HTLC value accepted by peer (mSAT):'), self.htlc_minimum_msat)
        #self.max_htlcs = SelectableLabel(str(chan.config[REMOTE].max_accepted_htlcs))
        #form_layout_left.addRow(_('Maximum number of concurrent HTLCs accepted by peer:'), self.max_htlcs)
        #self.max_htlc_value = SelectableLabel(self.format_sat(chan.config[REMOTE].max_htlc_value_in_flight_msat / 1000))
        #form_layout_left.addRow(_('Maximum value of in-flight HTLCs accepted by peer:'), self.max_htlc_value)
        local_dust_limit_label = SelectableLabel("{}".format(
            self.format_sat(chan.config[LOCAL].dust_limit_sat),
        ))
        remote_dust_limit_label = SelectableLabel("{}".format(
            self.format_sat(chan.config[REMOTE].dust_limit_sat),
        ))
        form_layout_left.addRow(_('Local dust limit') + ':', local_dust_limit_label)
        form_layout_right.addRow(_('Remote dust limit') + ':', remote_dust_limit_label)
        self.received_label = SelectableLabel()
        self.sent_label = SelectableLabel()
        form_layout_left.addRow(_('Total sent') + ':', self.sent_label)
        form_layout_right.addRow(_('Total received') + ':', self.received_label)
        # channel stats left column
        hbox_stats.addLayout(form_layout_left, 50)
        # vertical line separator
        line_separator = QtWidgets.QFrame()
        line_separator.setFrameShape(QtWidgets.QFrame.VLine)
        line_separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_separator.setLineWidth(1)
        hbox_stats.addWidget(line_separator)
        # channel stats right column
        hbox_stats.addLayout(form_layout_right, 50)
        vbox.addLayout(hbox_stats)
        # add htlc tree view to vbox (wouldn't scale correctly in QFormLayout)
        vbox.addWidget(QLabel(_('Payments (HTLCs):')))
        w = QtWidgets.QTreeView(self)
        htlc_dict = chan.get_payments()
        htlc_list = []
        for rhash, plist in htlc_dict.items():
            for htlc_with_status in plist:
                htlc_list.append(htlc_with_status)
        w.setModel(self.make_model(htlc_list))
        w.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        vbox.addWidget(w)
        vbox.addLayout(Buttons(CloseButton(self)))
        # initialize sent/received fields
        self.update()

    def closeEvent(self, event):
        self.unregister_callbacks()
        event.accept()
