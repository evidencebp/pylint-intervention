from __future__ import annotations
import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from django.db.models import F, Sum, Q, DecimalField
from django.urls import reverse
from django.utils.formats import number_format
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from repanier.const import *
from repanier.fields.RepanierMoneyField import ModelMoneyField
from repanier.models.deliveryboard import DeliveryBoard
from repanier.tools import create_or_update_one_cart_item, round_gov_be


class InvoiceQuerySet(models.QuerySet):
    pass


class Invoice(models.Model):
    permanence = models.ForeignKey(
        "Permanence", verbose_name=_("Order"), on_delete=models.PROTECT, db_index=True
    )
    status = models.CharField(
        max_length=3,
        choices=LUT_PERMANENCE_STATUS,
        default=PERMANENCE_PLANNED,
        verbose_name=_("Status"),
    )
    date_previous_balance = models.DateField(
        _("Date previous balance"), default=datetime.date.today
    )
    previous_balance = ModelMoneyField(
        _("Previous balance"), max_digits=8, decimal_places=2, default=DECIMAL_ZERO
    )
    # Calculated with Purchase
    total_price_with_tax = ModelMoneyField(
        _("Invoiced TVAC"), default=DECIMAL_ZERO, max_digits=8, decimal_places=2
    )
    delta_price_with_tax = ModelMoneyField(
        _("Total amount"),
        help_text=_("Purchase to add amount w VAT"),
        default=DECIMAL_ZERO,
        max_digits=8,
        decimal_places=2,
    )
    delta_transport = ModelMoneyField(
        _("Delivery point shipping cost"),
        help_text=_("Transport to add"),
        default=DECIMAL_ZERO,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    total_vat = ModelMoneyField(
        _("VAT"), default=DECIMAL_ZERO, max_digits=9, decimal_places=4
    )
    delta_vat = ModelMoneyField(
        _("VAT to add"), default=DECIMAL_ZERO, max_digits=9, decimal_places=4
    )
    total_deposit = ModelMoneyField(
        _("Deposit"),
        help_text=_("Surcharge"),
        default=DECIMAL_ZERO,
        max_digits=8,
        decimal_places=2,
    )
    bank_amount_in = ModelMoneyField(
        _("Cash in"),
        help_text=_("Payment on the account"),
        max_digits=8,
        decimal_places=2,
        default=DECIMAL_ZERO,
    )
    bank_amount_out = ModelMoneyField(
        _("Cash out"),
        help_text=_("Payment from the account"),
        max_digits=8,
        decimal_places=2,
        default=DECIMAL_ZERO,
    )
    date_balance = models.DateField(_("Date balance"), default=datetime.date.today)
    balance = ModelMoneyField(
        _("Balance"), max_digits=8, decimal_places=2, default=DECIMAL_ZERO
    )
    price_list_multiplier = models.DecimalField(
        _("Coefficient to calculate the tariff"),
        default=DECIMAL_ONE,
        max_digits=5,
        decimal_places=4,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    invoice_sort_order = models.IntegerField(
        _("Invoice sort order"), default=None, blank=True, null=True, db_index=True
    )

    def get_delta_price_with_tax(self):
        return self.delta_price_with_tax.amount

    def get_abs_delta_price_with_tax(self):
        return abs(self.delta_price_with_tax.amount)

    def __str__(self):
        return _("Invoice")

    class Meta:
        abstract = True


class CustomerInvoiceQuerySet(InvoiceQuerySet):
    def last_customer_invoice(self, pk: int, customer_id: int, **kwargs):
        if pk == 0:
            return self.filter(
                customer_id=customer_id, invoice_sort_order__isnull=False
            ).order_by("-invoice_sort_order")
        return self.filter(
            id=pk, customer_id=customer_id, invoice_sort_order__isnull=False
        )

    def previous_customer_invoice(self, customer_invoice: CustomerInvoice):
        return self.filter(
            customer_id=customer_invoice.customer_id,
            invoice_sort_order__isnull=False,
            invoice_sort_order__lt=customer_invoice.invoice_sort_order,
        ).order_by("-invoice_sort_order")

    def next_customer_invoice(self, customer_invoice: CustomerInvoice):
        return self.filter(
            customer_id=customer_invoice.customer_id,
            invoice_sort_order__isnull=False,
            invoice_sort_order__gt=customer_invoice.invoice_sort_order,
        ).order_by("invoice_sort_order")


class CustomerInvoice(Invoice):
    customer = models.ForeignKey(
        "Customer", verbose_name=_("Customer"), on_delete=models.PROTECT
    )
    customer_charged = models.ForeignKey(
        "Customer",
        verbose_name=_("Customer"),
        related_name="invoices_paid",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True,
    )
    delivery = models.ForeignKey(
        "DeliveryBoard",
        verbose_name=_("Delivery board"),
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    is_order_confirm_send = models.BooleanField(
        _("Confirmation of the order send"), choices=settings.LUT_CONFIRM, default=False
    )

    transport = ModelMoneyField(
        _("Delivery point shipping cost"),
        help_text=_(
            "This amount is added once for groups with entitled customer or at each customer for open groups."
        ),
        default=DECIMAL_ZERO,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    min_transport = ModelMoneyField(
        _("Minimum order amount for free shipping cost"),
        help_text=_("This is the minimum order amount to avoid shipping cost."),
        default=DECIMAL_ZERO,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    is_group = models.BooleanField(_("Group"), default=False)

    @classmethod
    def get_or_create(cls, permanence_id, customer_id, delivery_board=None):
        customer_invoice = CustomerInvoice.objects.filter(
            permanence_id=permanence_id, customer_id=customer_id
        ).first()
        if customer_invoice is None:
            customer_invoice = CustomerInvoice.create(
                permanence_id, customer_id, delivery_board=delivery_board
            )
        elif customer_invoice.invoice_sort_order is None:
            # if not already invoiced, update all totals
            customer_invoice.set_total()
            # 	delta_price_with_tax
            # 	delta_vat
            # 	total_vat
            # 	total_deposit
            # 	total_price_with_tax
            # 	delta_transport = f(total_price_with_tax, transport, min_transport)
            customer_invoice.save()
        return customer_invoice

    @classmethod
    def create(cls, permanence_id, customer_id, delivery_board=None):
        customer_invoice = CustomerInvoice.objects.create(
            permanence_id=permanence_id,
            customer_id=customer_id,
            #
            #
            delta_price_with_tax=DECIMAL_ZERO,
            delta_vat=DECIMAL_ZERO,
            total_vat=DECIMAL_ZERO,
            total_deposit=DECIMAL_ZERO,
            total_price_with_tax=DECIMAL_ZERO,
            delta_transport=DECIMAL_ZERO,
            #
            #
            is_order_confirm_send=False,
            invoice_sort_order=None,
            # 	date_previous_balance = undefined (today)
            # 	previous_balance = undefined (DECIMAL_ZERO)
            # 	date_balance = undefined (today)
            # 	balance = undefined (DECIMAL_ZERO)
        )
        customer_invoice.set_delivery_context(delivery_board=delivery_board)
        #   validated delivery = f(delivery/customer, default delivery = None)
        #   status = f(permanence, validated delivery),
        # 	is_group= f(validated delivery)
        #   group =  f(validated delivery)
        # 	customer_charged_id=f(groupe)
        # 	price_list_multiplier= f(group), default 1
        # 	transport= f(validated delivery/group), default 0
        # 	min_transport= f(validated delivery/group), default 0
        customer_invoice.save()
        return customer_invoice

    def get_abs_delta_vat(self):
        return abs(self.delta_vat)

    def get_total_price_with_tax(self, customer_charged=False):
        if self.customer_id == self.customer_charged_id:
            return (
                self.total_price_with_tax
                + self.delta_price_with_tax
                + self.delta_transport
            )
        else:
            if self.status < PERMANENCE_INVOICED or not customer_charged:
                return self.total_price_with_tax
            else:
                return (
                    self.customer_charged
                )  # if self.total_price_with_tax != DECIMAL_ZERO else RepanierMoney()

    def get_total_price_wo_tax(self):
        return self.get_total_price_with_tax() - self.get_total_tax()

    def get_total_tax(self):
        # round to 2 decimals
        return RepanierMoney(self.total_vat.amount + self.delta_vat.amount)

    @property
    def has_purchase(self):
        if (
            self.total_price_with_tax.amount != DECIMAL_ZERO
            or self.is_order_confirm_send
        ):
            return True

        from repanier.models.purchase import PurchaseWoReceiver

        result_set = PurchaseWoReceiver.objects.filter(
            permanence_id=self.permanence_id, customer_invoice_id=self.id
        ).aggregate(
            qty_ordered=Sum(
                "qty_ordered",
                output_field=DecimalField(
                    max_digits=9, decimal_places=4, default=DECIMAL_ZERO
                ),
            ),
            qty_invoiced=Sum(
                "qty_invoiced",
                output_field=DecimalField(
                    max_digits=9, decimal_places=4, default=DECIMAL_ZERO
                ),
            ),
        )
        qty_ordered = (
            result_set["qty_ordered"]
            if result_set["qty_ordered"] is not None
            else DECIMAL_ZERO
        )
        qty_invoiced = (
            result_set["qty_invoiced"]
            if result_set["qty_invoiced"] is not None
            else DECIMAL_ZERO
        )
        return qty_ordered != DECIMAL_ZERO or qty_invoiced != DECIMAL_ZERO

    def get_html_my_order_confirmation(
        self, permanence, is_basket=False, basket_message=EMPTY_STRING
    ):

        if permanence.with_delivery_point:
            if self.delivery is not None:
                label = self.delivery.get_delivery_customer_display()
                delivery_id = self.delivery_id
            else:
                delivery_id = 0

                if self.customer.delivery_point is not None:
                    qs = DeliveryBoard.objects.filter(
                        Q(
                            permanence_id=permanence.id,
                            delivery_point_id=self.customer.delivery_point_id,
                            status=PERMANENCE_OPENED,
                        )
                        | Q(
                            permanence_id=permanence.id,
                            delivery_point__customer_responsible__isnull=True,
                            status=PERMANENCE_OPENED,
                        )
                    )

                else:
                    qs = DeliveryBoard.objects.filter(
                        permanence_id=permanence.id,
                        delivery_point__customer_responsible__isnull=True,
                        status=PERMANENCE_OPENED,
                    )

                if qs.exists():
                    label = "{}".format(_("Please, select a delivery point"))
                    CustomerInvoice.objects.filter(
                        permanence_id=permanence.id, customer_id=self.customer_id
                    ).update(status=PERMANENCE_OPENED)
                else:
                    label = "{}".format(
                        _("No delivery point is open for you. You can not place order.")
                    )
                    # IMPORTANT :
                    # 1 / This prohibit to place an order into the customer UI
                    # 2 / task_order.close_send_order will delete any CLOSED orders without any delivery point
                    CustomerInvoice.objects.filter(
                        permanence_id=permanence.id, customer_id=self.customer_id
                    ).update(status=PERMANENCE_CLOSED)

            if self.customer_id != self.customer_charged_id:
                msg_price = msg_transport = EMPTY_STRING
            else:
                if self.transport.amount <= DECIMAL_ZERO:
                    transport = False
                    msg_transport = EMPTY_STRING
                else:
                    transport = True
                    if self.min_transport.amount > DECIMAL_ZERO:
                        msg_transport = "{}<br>".format(
                            _(
                                "The shipping costs for this delivery point amount to %(transport)s for orders of less than %(min_transport)s."
                            )
                            % {
                                "transport": self.transport,
                                "min_transport": self.min_transport,
                            }
                        )
                    else:
                        msg_transport = "{}<br>".format(
                            _(
                                "The shipping costs for this delivery point amount to %(transport)s."
                            )
                            % {"transport": self.transport}
                        )
                if self.price_list_multiplier == DECIMAL_ONE:
                    msg_price = EMPTY_STRING
                else:
                    if transport:
                        if self.price_list_multiplier > DECIMAL_ONE:
                            msg_price = "{}<br>".format(
                                _(
                                    "In addition, a surcharge of %(increase)s %% is applied to the billed total. It does not apply to deposits or fees."
                                )
                                % {
                                    "increase": number_format(
                                        (self.price_list_multiplier - DECIMAL_ONE)
                                        * 100,
                                        2,
                                    )
                                }
                            )
                        else:
                            msg_price = "{}<br>".format(
                                _(
                                    "In addition a reduction of %(decrease)s %% is applied to the billed total. It does not apply to deposits or fees."
                                )
                                % {
                                    "decrease": number_format(
                                        (DECIMAL_ONE - self.price_list_multiplier)
                                        * 100,
                                        2,
                                    )
                                }
                            )
                    else:
                        if self.price_list_multiplier > DECIMAL_ONE:
                            msg_price = "{}<br>".format(
                                _(
                                    "For this delivery point, an overload of %(increase)s %% is applied to the billed total (out of deposit)."
                                )
                                % {
                                    "increase": number_format(
                                        (self.price_list_multiplier - DECIMAL_ONE)
                                        * 100,
                                        2,
                                    )
                                }
                            )
                        else:
                            msg_price = "{}<br>".format(
                                _(
                                    "For this delivery point, a reduction of %(decrease)s %% is applied to the invoiced total (out of deposit)."
                                )
                                % {
                                    "decrease": number_format(
                                        (DECIMAL_ONE - self.price_list_multiplier)
                                        * 100,
                                        2,
                                    )
                                }
                            )

            msg_delivery = """
            {}<b><i>
            <select name=\"delivery\" id=\"delivery\" onmouseover=\"show_select_delivery_list_ajax({})\" onchange=\"delivery_ajax()\" class=\"form-control\">
            <option value=\"{}\" selected>{}</option>
            </select>
            </i></b><br>{}{}
            """.format(
                _("Delivery point"),
                delivery_id,
                delivery_id,
                label,
                msg_transport,
                msg_price,
            )
        else:
            msg_delivery = EMPTY_STRING
        msg_confirmation1 = EMPTY_STRING
        if not is_basket and not settings.REPANIER_SETTINGS_CUSTOMER_MUST_CONFIRM_ORDER:
            # or customer_invoice.total_price_with_tax.amount != DECIMAL_ZERO:
            # If REPANIER_SETTINGS_CUSTOMER_MUST_CONFIRM_ORDER,
            # then permanence.with_delivery_point is also True
            msg_html = EMPTY_STRING
        else:
            if self.is_order_confirm_send:
                msg_confirmation2 = self.customer.my_order_confirmation_email_send_to()
                msg_html = """
                <div class="row">
                <div class="panel panel-default">
                <div class="panel-heading">
                {}
                <p><font color="#51a351">{}</font><p/>
                {}
                </div>
                </div>
                </div>
                 """.format(
                    msg_delivery, msg_confirmation2, basket_message
                )
            else:
                msg_html = None
                btn_disabled = (
                    EMPTY_STRING
                    if permanence.status == PERMANENCE_OPENED
                    else "disabled"
                )
                msg_confirmation2 = EMPTY_STRING
                if settings.REPANIER_SETTINGS_CUSTOMER_MUST_CONFIRM_ORDER:
                    if is_basket:
                        if self.status == PERMANENCE_OPENED:
                            if (
                                permanence.with_delivery_point and self.delivery is None
                            ) or not self.has_purchase:
                                btn_disabled = "disabled"
                            msg_confirmation1 = (
                                '<span style="color: red; ">{}</span><br>'.format(
                                    _("⚠ Unconfirmed orders will be canceled.")
                                )
                            )
                            msg_confirmation2 = '<span class="glyphicon glyphicon-floppy-disk"></span>&nbsp;&nbsp;{}'.format(
                                _(
                                    " ➜ Confirm this order and receive an email containing its summary."
                                )
                            )
                    else:
                        href = reverse("repanier:order_view", args=(permanence.id,))
                        if self.status == PERMANENCE_OPENED:
                            msg_confirmation1 = (
                                '<span style="color: red; ">{}</span><br>'.format(
                                    _("⚠ Unconfirmed orders will be canceled.")
                                )
                            )
                            msg_confirmation2 = _(
                                "➜ Go to the confirmation step of my order."
                            )
                            msg_html = """
                                <div class="row">
                                <div class="panel panel-default">
                                <div class="panel-heading">
                                {}
                                {}
                                <a href="{}?is_basket=yes" class="btn btn-info" {}>{}</a>
                                </div>
                                </div>
                                </div>
                                 """.format(
                                msg_delivery,
                                msg_confirmation1,
                                href,
                                btn_disabled,
                                msg_confirmation2,
                            )
                else:
                    if is_basket:
                        msg_confirmation2 = _(
                            "Receive an email containing this order summary."
                        )
                    elif permanence.with_delivery_point:
                        msg_html = """
                            <div class="row">
                            <div class="panel panel-default">
                            <div class="panel-heading">
                            {}
                            </div>
                            </div>
                            </div>
                             """.format(
                            msg_delivery
                        )
                    else:
                        msg_html = EMPTY_STRING
                if msg_html is None:
                    if msg_confirmation2 == EMPTY_STRING:
                        msg_html = """
                        <div class="row">
                        <div class="panel panel-default">
                        <div class="panel-heading">
                        {}
                        <div class="clearfix"></div>
                        {}
                        </div>
                        </div>
                        </div>
                         """.format(
                            msg_delivery, basket_message
                        )
                    else:
                        msg_html = """
                        <div class="row">
                        <div class="panel panel-default">
                        <div class="panel-heading">
                        {}
                        {}
                        <button id="btn_confirm_order" class="btn btn-info" {} onclick="btn_receive_order_email();">{}</button>
                        <div class="clearfix"></div>
                        {}
                        </div>
                        </div>
                        </div>
                         """.format(
                            msg_delivery,
                            msg_confirmation1,
                            btn_disabled,
                            msg_confirmation2,
                            basket_message,
                        )
        return {"#span_btn_confirm_order": mark_safe(msg_html)}

    @transaction.atomic
    def confirm_order(self):
        if not self.is_order_confirm_send:
            # Change of confirmation status
            from repanier.models.purchase import PurchaseWoReceiver

            PurchaseWoReceiver.objects.filter(customer_invoice__id=self.id).update(
                qty_confirmed=F("qty_ordered")
            )
        self.is_order_confirm_send = True

    def cancel_confirm_order(self):
        if self.is_order_confirm_send:
            # Change of confirmation status
            self.is_order_confirm_send = False
            return True
        else:
            # No change of confirmation status
            return False

    @transaction.atomic
    def set_delivery_context(self, delivery_board=None):
        """
        Calculate
            (1) keep a valid delivery (with default as self.customer.delivery_point) or None
            (2) based on delivery.delivery_point calculate
                self.customer_charged
                self.price_list_multiplier
                self.transport
                self.min_transport
                self.status
            (3) if needed, create an invoice for customer_charged

        :param delivery_board: Don't use delivery_board_id because it won't reload customer_invoice.delivery

        Important
        If it's an invoice of a member of a group :
          self.customer_charged_id != self.customer_id
          self.customer_charged_id == owner of the group
          price_list_multiplier = DECIMAL_ONE
        Else :
          self.customer_charged_id = self.customer_id
          price_list_multiplier may vary

        """

        if delivery_board is None:
            if self.permanence.with_delivery_point:
                if self.customer.delivery_point is None:
                    qs = DeliveryBoard.objects.filter(
                        permanence_id=self.permanence_id,
                        delivery_point__customer_responsible__isnull=True,
                        status=PERMANENCE_OPENED,
                    )
                else:
                    # The customer is member of a group
                    qs = DeliveryBoard.objects.filter(
                        Q(
                            permanence_id=self.permanence_id,
                            delivery_point_id=self.customer.delivery_point_id,
                            status=PERMANENCE_OPENED,
                        )
                        | Q(
                            permanence_id=self.permanence_id,
                            delivery_point__customer_responsible__isnull=True,
                            status=PERMANENCE_OPENED,
                        )
                    )
                valid_delivery_board = qs.first()
            else:
                valid_delivery_board = None
        else:
            assert self.permanence.with_delivery_point is True
            assert self.permanence_id == delivery_board.permanence_id
            valid_delivery_board = delivery_board

        if valid_delivery_board is None:
            status = self.permanence.status
        else:
            status = valid_delivery_board.status

        self.delivery = valid_delivery_board
        self.status = status

        if self.delivery is None:
            self.customer_charged = self.customer
            self.price_list_multiplier = DECIMAL_ONE
            self.transport = DECIMAL_ZERO
            self.min_transport = DECIMAL_ZERO
        else:
            delivery_point = self.delivery.delivery_point
            customer_responsible = delivery_point.customer_responsible
            if customer_responsible is None:
                self.customer_charged = self.customer
                self.price_list_multiplier = DECIMAL_ONE
                self.transport = delivery_point.transport
                self.min_transport = delivery_point.min_transport
            else:
                assert self.customer_id != customer_responsible.id
                self.customer_charged = customer_responsible
                self.price_list_multiplier = DECIMAL_ONE
                self.transport = REPANIER_MONEY_ZERO
                self.min_transport = REPANIER_MONEY_ZERO

                customer_invoice_charged = CustomerInvoice.objects.filter(
                    permanence_id=self.permanence_id,
                    customer_id=customer_responsible.id,
                )
                if not customer_invoice_charged.exists():
                    CustomerInvoice.objects.create(
                        permanence_id=self.permanence_id,
                        customer_id=customer_responsible.id,
                        status=status,
                        customer_charged_id=customer_responsible.id,
                        price_list_multiplier=customer_responsible.price_list_multiplier,
                        transport=delivery_point.transport,
                        min_transport=delivery_point.min_transport,
                        is_order_confirm_send=True,  # None ?
                        is_group=True,
                        delivery=self.delivery,
                    )

    def set_total(self):
        #
        # return :
        # - total_price_with_tax
        # - delta_price_with_tax
        # - total_vat
        # - delta_vat
        # - total_deposit
        # - delta_transport

        from repanier.models.purchase import PurchaseWoReceiver

        self.delta_price_with_tax.amount = DECIMAL_ZERO
        self.delta_vat.amount = DECIMAL_ZERO

        if self.customer_id == self.customer_charged_id:
            # It's an invoice of a group, or of a customer who is not member of a group :
            #   self.customer_charged_id == self.customer_id
            #   self.price_list_multiplier may vary
            if self.price_list_multiplier != DECIMAL_ONE:
                result_set = PurchaseWoReceiver.objects.filter(
                    permanence_id=self.permanence_id,
                    customer_invoice__customer_charged_id=self.customer_id,
                    is_resale_price_fixed=False,
                ).aggregate(
                    customer_vat=Sum(
                        "customer_vat",
                        output_field=DecimalField(
                            max_digits=8, decimal_places=4, default=DECIMAL_ZERO
                        ),
                    ),
                    deposit=Sum(
                        "deposit",
                        output_field=DecimalField(
                            max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                        ),
                    ),
                    selling_price=Sum(
                        "selling_price",
                        output_field=DecimalField(
                            max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                        ),
                    ),
                )

                total_vat = result_set["customer_vat"] or DECIMAL_ZERO
                total_deposit = result_set["deposit"] or DECIMAL_ZERO
                total_selling_price_with_tax = (
                    result_set["selling_price"] or DECIMAL_ZERO
                )

                total_selling_price_with_tax_wo_deposit = (
                    total_selling_price_with_tax - total_deposit
                )
                self.delta_price_with_tax.amount = (
                    total_selling_price_with_tax_wo_deposit * self.price_list_multiplier
                ).quantize(TWO_DECIMALS) - total_selling_price_with_tax_wo_deposit
                self.delta_vat.amount = -(
                    (total_vat * self.price_list_multiplier).quantize(FOUR_DECIMALS)
                    - total_vat
                )

            result_set = PurchaseWoReceiver.objects.filter(
                permanence_id=self.permanence_id,
                customer_invoice__customer_charged_id=self.customer_id,
                is_resale_price_fixed=True,
            ).aggregate(
                customer_vat=Sum(
                    "customer_vat",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=4, default=DECIMAL_ZERO
                    ),
                ),
                deposit=Sum(
                    "deposit",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                    ),
                ),
                selling_price=Sum(
                    "selling_price",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                    ),
                ),
            )
        else:
            # It's an invoice of a member of a group
            #   self.customer_charged_id != self.customer_id
            #   self.customer_charged_id == owner of the group
            #   assertion : self.price_list_multiplier always == DECIMAL_ONE

            result_set = PurchaseWoReceiver.objects.filter(
                permanence_id=self.permanence_id, customer_id=self.customer_id
            ).aggregate(
                customer_vat=Sum(
                    "customer_vat",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=4, default=DECIMAL_ZERO
                    ),
                ),
                deposit=Sum(
                    "deposit",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                    ),
                ),
                selling_price=Sum(
                    "selling_price",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                    ),
                ),
            )

        self.total_vat.amount = result_set["customer_vat"] or DECIMAL_ZERO
        self.total_deposit.amount = result_set["deposit"] or DECIMAL_ZERO
        self.total_price_with_tax.amount = result_set["selling_price"] or DECIMAL_ZERO

        if settings.REPANIER_SETTINGS_ROUND_INVOICES:
            total_price = (
                self.total_price_with_tax.amount + self.delta_price_with_tax.amount
            )
            total_price_gov_be = round_gov_be(total_price)
            self.delta_price_with_tax.amount += total_price_gov_be - total_price
        self.set_transport()

    def set_transport(self):
        if self.customer_id == self.customer_charged_id:
            # It's an invoice of a group, or of a customer who is not member of a group :
            #   self.customer_charged_id = self.customer_id
            #   self.price_list_multiplier may vary
            if self.transport.amount != DECIMAL_ZERO:
                total_price_with_tax = (
                    self.total_price_with_tax.amount + self.delta_price_with_tax.amount
                )
                if total_price_with_tax != DECIMAL_ZERO:
                    if self.min_transport.amount == DECIMAL_ZERO:
                        self.delta_transport.amount = self.transport.amount
                    elif total_price_with_tax < self.min_transport.amount:
                        self.delta_transport.amount = min(
                            self.min_transport.amount - total_price_with_tax,
                            self.transport.amount,
                        )
                else:
                    self.delta_transport.amount = DECIMAL_ZERO
            else:
                self.delta_transport.amount = DECIMAL_ZERO
        else:
            self.delta_transport.amount = DECIMAL_ZERO

    def set_invoice_context(self, payment_date):
        from repanier.models.bankaccount import BankAccount

        # is_order_confirm_send = False,
        # invoice_sort_order = None,
        self.date_previous_balance = self.customer.date_balance
        self.date_balance = payment_date
        self.balance = self.previous_balance = self.customer.balance

        delta_bank = DECIMAL_ZERO
        for bank_account in BankAccount.objects.select_for_update().filter(
            customer_invoice__isnull=True,
            producer_invoice__isnull=True,
            customer=self.customer,
            operation_date__lte=payment_date,
        ):
            bank_amount_in = bank_account.bank_amount_in
            bank_amount_out = bank_account.bank_amount_out
            self.bank_amount_in.amount += bank_amount_in
            self.bank_amount_out.amount += bank_amount_out

            delta_bank = bank_amount_in - bank_amount_out

            bank_account.customer_invoice_id = self.id
            bank_account.permanence_id = self.permanence_id
            bank_account.save()

        delta_balance = self.get_total_price_with_tax().amount + delta_bank
        self.balance.amount -= delta_balance

    def cancel_if_unconfirmed(self, permanence, send_mail=True):
        if (
            settings.REPANIER_SETTINGS_CUSTOMER_MUST_CONFIRM_ORDER
            and not self.is_order_confirm_send
            and self.has_purchase
        ):
            if send_mail:
                from repanier.email.email_order import export_order_2_1_customer

                filename = "{}-{}.xlsx".format(_("Canceled order"), permanence)

                export_order_2_1_customer(
                    self.customer, filename, permanence, cancel_order=True
                )

            from repanier.models.purchase import PurchaseWoReceiver

            purchase_qs = PurchaseWoReceiver.objects.filter(
                customer_invoice_id=self.id, is_box_content=False
            )

            for a_purchase in purchase_qs.select_related("customer"):
                create_or_update_one_cart_item(
                    customer=a_purchase.customer,
                    offer_item_id=a_purchase.offer_item_id,
                    q_order=DECIMAL_ZERO,
                    batch_job=True,
                    comment=_("Qty not confirmed : {}").format(
                        number_format(a_purchase.qty_ordered, 4)
                    ),
                )

    objects = CustomerInvoiceQuerySet.as_manager()

    def __str__(self):
        return f"{self.customer}, {self.permanence}"

    class Meta:
        verbose_name = _("Customer invoice")
        verbose_name_plural = _("Customers invoices")
        unique_together = (("permanence", "customer"),)


class ProducerInvoiceQuerySet(InvoiceQuerySet):
    def do_not_invoice(self, permanence_id: int, **kwargs):
        return self.filter(
            permanence_id=permanence_id,
            invoice_sort_order__isnull=True,
            is_to_be_paid=False,
            **kwargs,
        )

    def to_be_invoiced(self, permanence_id: int, **kwargs):
        return self.filter(
            permanence_id=permanence_id,
            invoice_sort_order__isnull=True,
            is_to_be_paid=True,
            **kwargs,
        )

    def last_producer_invoice(self, pk: int, producer_login_uuid: str, **kwargs):
        if pk == 0:
            return self.filter(
                producer__login_uuid=producer_login_uuid, invoice_sort_order__isnull=False
            ).order_by("-invoice_sort_order")
        return self.filter(
            id=pk, producer__login_uuid=producer_login_uuid, invoice_sort_order__isnull=False
        )

    def previous_producer_invoice(self, producer_invoice: ProducerInvoice):
        return self.filter(
            producer_id=producer_invoice.producer_id,
            invoice_sort_order__isnull=False,
            invoice_sort_order__lt=producer_invoice.invoice_sort_order,
        ).order_by("-invoice_sort_order")

    def next_producer_invoice(self, producer_invoice: ProducerInvoice):
        return self.filter(
            producer_id=producer_invoice.producer_id,
            invoice_sort_order__isnull=False,
            invoice_sort_order__gt=producer_invoice.invoice_sort_order,
        ).order_by("invoice_sort_order")


class ProducerInvoice(Invoice):
    producer = models.ForeignKey(
        "Producer",
        verbose_name=_("Producer"),
        # related_name='producer_invoice',
        on_delete=models.PROTECT,
    )
    is_to_be_paid = models.BooleanField(
        _("To be paid"),
        default=False,
        # db_column="to_be_paid"
    )
    balance_calculated = ModelMoneyField(
        _("Amount due to the producer as calculated by Repanier"),
        max_digits=8,
        decimal_places=2,
        default=DECIMAL_ZERO,
        # db_column="calculated_invoiced_balance"
    )
    balance_invoiced = ModelMoneyField(
        _("Amount claimed by the producer"),
        max_digits=8,
        decimal_places=2,
        default=DECIMAL_ZERO,
        # db_column="to_be_invoiced_balance"
    )
    reference = models.CharField(
        _("Invoice reference"),
        max_length=100,
        blank=True,
        default=EMPTY_STRING,
        # db_column="invoice_reference"
    )
    # TBD
    to_be_paid = models.BooleanField(
        _("To be paid"),
        default=False,
    )
    calculated_invoiced_balance = ModelMoneyField(
        _("Amount due to the producer as calculated by Repanier"),
        max_digits=8,
        decimal_places=2,
        default=DECIMAL_ZERO,
    )
    to_be_invoiced_balance = ModelMoneyField(
        _("Amount claimed by the producer"),
        max_digits=8,
        decimal_places=2,
        default=DECIMAL_ZERO,
    )
    invoice_reference = models.CharField(
        _("Invoice reference"),
        max_length=100,
        blank=True,
        default=EMPTY_STRING,
    )

    @classmethod
    def get_or_create(cls, permanence_id, producer_id):
        producer_invoice = ProducerInvoice.objects.filter(
            permanence_id=permanence_id, producer_id=producer_id
        ).first()
        if producer_invoice is None:
            producer_invoice = ProducerInvoice.create(permanence_id, producer_id)
        elif producer_invoice.invoice_sort_order is None:
            # if not already invoiced, update all totals
            producer_invoice.set_total()
            # 	delta_price_with_tax
            # 	delta_vat
            # 	total_vat
            # 	total_deposit
            # 	total_price_with_tax
            # 	delta_transport = f(total_price_with_tax, transport, min_transport)
            producer_invoice.save()
        return producer_invoice

    @classmethod
    def create(cls, permanence_id, producer_id):
        producer_invoice = ProducerInvoice.objects.create(
            permanence_id=permanence_id,
            producer_id=producer_id,
            #
            #
            is_order_confirm_send=False,
            invoice_sort_order=None,
            # 	date_previous_balance = undefined (today)
            # 	previous_balance = undefined (DECIMAL_ZERO)
            # 	date_balance = undefined (today)
            # 	balance = undefined (DECIMAL_ZERO)
        )
        return producer_invoice

    def set_total(self):
        #
        # return :
        # - total_price_with_tax
        # - delta_price_with_tax
        # - total_vat
        # - delta_vat
        # - total_deposit
        # - delta_transport

        from repanier.models.purchase import PurchaseWoReceiver

        self.delta_price_with_tax.amount = DECIMAL_ZERO
        self.delta_vat.amount = DECIMAL_ZERO

        if self.price_list_multiplier != DECIMAL_ONE:
            result_set = PurchaseWoReceiver.objects.filter(
                permanence_id=self.permanence_id,
                customer_invoice__customer_charged_id=self.customer_id,
                is_resale_price_fixed=False,
            ).aggregate(
                customer_vat=Sum(
                    "customer_vat",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=4, default=DECIMAL_ZERO
                    ),
                ),
                deposit=Sum(
                    "deposit",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                    ),
                ),
                selling_price=Sum(
                    "selling_price",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                    ),
                ),
            )

            total_vat = (
                result_set["customer_vat"]
                if result_set["customer_vat"] is not None
                else DECIMAL_ZERO
            )
            total_deposit = (
                result_set["deposit"]
                if result_set["deposit"] is not None
                else DECIMAL_ZERO
            )
            total_selling_price_with_tax = (
                result_set["selling_price"]
                if result_set["selling_price"] is not None
                else DECIMAL_ZERO
            )

            total_selling_price_with_tax_wo_deposit = (
                total_selling_price_with_tax - total_deposit
            )
            self.delta_price_with_tax.amount = (
                total_selling_price_with_tax_wo_deposit * self.price_list_multiplier
            ).quantize(TWO_DECIMALS) - total_selling_price_with_tax_wo_deposit
            self.delta_vat.amount = -(
                (total_vat * self.price_list_multiplier).quantize(FOUR_DECIMALS)
                - total_vat
            )

            result_set = PurchaseWoReceiver.objects.filter(
                permanence_id=self.permanence_id,
                customer_invoice__customer_charged_id=self.customer_id,
            ).aggregate(
                customer_vat=Sum(
                    "customer_vat",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=4, default=DECIMAL_ZERO
                    ),
                ),
                deposit=Sum(
                    "deposit",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                    ),
                ),
                selling_price=Sum(
                    "selling_price",
                    output_field=DecimalField(
                        max_digits=8, decimal_places=2, default=DECIMAL_ZERO
                    ),
                ),
            )

        self.total_vat.amount = (
            result_set["customer_vat"]
            if result_set["customer_vat"] is not None
            else DECIMAL_ZERO
        )
        self.total_deposit.amount = (
            result_set["deposit"] if result_set["deposit"] is not None else DECIMAL_ZERO
        )
        self.total_price_with_tax.amount = (
            result_set["selling_price"]
            if result_set["selling_price"] is not None
            else DECIMAL_ZERO
        )

        if settings.REPANIER_SETTINGS_ROUND_INVOICES:
            total_price = (
                self.total_price_with_tax.amount + self.delta_price_with_tax.amount
            )
            total_price_gov_be = round_gov_be(total_price)
            self.delta_price_with_tax.amount += total_price_gov_be - total_price

    def get_negative_previous_balance(self):
        return -self.previous_balance

    def get_negative_balance(self):
        return -self.balance

    def get_total_price_with_tax(self):
        return (
            self.total_price_with_tax + self.delta_price_with_tax + self.delta_transport
        )

    def get_total_tax(self):
        return self.total_vat

    def get_total_deposit(self):
        return self.total_deposit

    def set_invoice_context(self, payment_date):
        from repanier.models.producer import BankAccount

        # invoice_sort_order = None,
        self.date_previous_balance = self.producer.date_balance
        self.date_balance = payment_date
        self.balance = self.previous_balance = self.producer.balance

        delta_bank = DECIMAL_ZERO
        for bank_account in BankAccount.objects.select_for_update().filter(
            customer_invoice__isnull=True,
            producer_invoice__isnull=True,
            producer=self.producer,
            operation_date__lte=payment_date,
        ):
            bank_amount_in = bank_account.bank_amount_in
            bank_amount_out = bank_account.bank_amount_out
            self.bank_amount_in.amount += bank_amount_in
            self.bank_amount_out.amount += bank_amount_out

            delta_bank = bank_amount_in - bank_amount_out

            bank_account.producer_invoice_id = self.id
            bank_account.permanence_id = self.permanence_id
            bank_account.save()

        delta_balance = self.get_total_price_with_tax().amount + delta_bank
        self.balance.amount -= delta_balance

    def get_order_json(self):
        a_producer = self.producer
        json_dict = {}
        if a_producer.minimum_order_value.amount > DECIMAL_ZERO:
            ratio = (
                self.total_price_with_tax.amount / a_producer.minimum_order_value.amount
            )
            if ratio >= DECIMAL_ONE:
                ratio = 100
            else:
                ratio *= 100
            json_dict["#order_procent{}".format(a_producer.id)] = "{}%".format(
                number_format(ratio, 0)
            )
        return json_dict

    objects = ProducerInvoiceQuerySet.as_manager()

    def __str__(self):
        return f"{self.producer}, {self.permanence}"

    class Meta:
        verbose_name = _("Producer invoice")
        verbose_name_plural = _("Producers invoices")
        unique_together = (("permanence", "producer"),)


class CustomerProducerInvoice(models.Model):
    customer = models.ForeignKey(
        "Customer", verbose_name=_("Customer"), on_delete=models.PROTECT
    )
    producer = models.ForeignKey(
        "Producer", verbose_name=_("Producer"), on_delete=models.PROTECT
    )
    permanence = models.ForeignKey(
        "Permanence", verbose_name=_("Order"), on_delete=models.PROTECT, db_index=True
    )
    # Calculated with Purchase
    total_purchase_with_tax = ModelMoneyField(
        _("Producer amount invoiced"),
        help_text=_("Total selling amount vat included"),
        default=DECIMAL_ZERO,
        max_digits=8,
        decimal_places=2,
    )
    # Calculated with Purchase
    total_selling_with_tax = ModelMoneyField(
        _("Invoiced to the consumer w TVA"),
        help_text=_("Total selling amount vat included"),
        default=DECIMAL_ZERO,
        max_digits=8,
        decimal_places=2,
    )

    def get_html_producer_price_purchased(self):
        if self.total_purchase_with_tax != DECIMAL_ZERO:
            return format_html("<b>{}</b>", self.total_purchase_with_tax)
        return EMPTY_STRING

    get_html_producer_price_purchased.short_description = _("Producer amount invoiced")
    get_html_producer_price_purchased.admin_order_field = "total_purchase_with_tax"

    def __str__(self):
        return f"{self.producer}, {self.customer}"

    class Meta:
        unique_together = (("permanence", "customer", "producer"),)


class CustomerSend(CustomerProducerInvoice):
    def __str__(self):
        return f"{self.producer}, {self.customer}"

    class Meta:
        proxy = True
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
