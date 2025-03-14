from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from repanier.const import (
    PERMANENCE_OPENED,
    PERMANENCE_SEND,
    LIMIT_ORDER_QTY_ITEM,
    DECIMAL_ZERO,
    EMPTY_STRING,
)
from repanier.models.customer import Customer
from repanier.models.invoice import ProducerInvoice, CustomerInvoice
from repanier.models.offeritem import OfferItemReadOnly
from repanier.models.purchase import PurchaseWoReceiver
from repanier.tools import sint, get_html_selected_value


@never_cache
@require_GET
@login_required
def order_select_ajax(request):
    user = request.user
    customer = (
        Customer.objects.filter(id=user.customer_id, may_order=True)
        .only("id", "vat_id", "language")
        .first()
    )
    if customer is None:
        raise Http404
    translation.activate(customer.language)
    offer_item_id = sint(request.GET.get("offer_item", 0))
    offer_item = OfferItemReadOnly.objects.filter(id=offer_item_id).first()
    if offer_item is None:
        raise Http404
    # Select one purchase
    purchase = (
        PurchaseWoReceiver.objects.filter(
            customer_id=customer.id, offer_item_id=offer_item_id
        )
        .only("quantity_ordered")
        .first()
    )
    producer_invoice = ProducerInvoice.objects.filter(
        permanence_id=offer_item.permanence_id,
        producer_id=offer_item.producer_id,
        status=PERMANENCE_OPENED,
    )
    if producer_invoice.exists():
        # The orders are opened for this producer and this permanence

        if offer_item.may_order:
            # This offer_item may be ordered
            customer_invoice = (
                CustomerInvoice.objects.filter(
                    permanence_id=offer_item.permanence_id, customer_id=customer.id
                )
                .only("status")
                .first()
            )
            if customer_invoice is None:
                status = EMPTY_STRING
            else:
                status = customer_invoice.status
            if PERMANENCE_OPENED <= status <= PERMANENCE_SEND:
                product = offer_item.product
                a_price = (
                    product.customer_unit_price.amount + product.unit_deposit.amount
                )
                q_min = product.customer_minimum_order_quantity
                if purchase is not None:
                    q_previous_order = purchase.quantity_ordered
                else:
                    q_previous_order = DECIMAL_ZERO
                if status == PERMANENCE_OPENED and product.stock > DECIMAL_ZERO:
                    q_alert = offer_item.get_q_alert() + q_previous_order
                else:
                    q_alert = offer_item.get_q_alert()
                q_step = product.customer_increment_order_quantity
                q_order_is_displayed = False
                q_select_id = 0
                selected = EMPTY_STRING
                if q_previous_order <= 0:
                    q_order_is_displayed = True
                    selected = "selected"

                q_valid = q_min
                html = EMPTY_STRING
                if q_valid <= q_alert:
                    if status == PERMANENCE_OPENED or (
                        status <= PERMANENCE_SEND and selected == "selected"
                    ):
                        html = '<option value="0" {}>---</option>'.format(selected)
                else:
                    if status == PERMANENCE_OPENED or (
                        status <= PERMANENCE_SEND and selected == "selected"
                    ):
                        html = '<option value="0" {}>{}</option>'.format(
                            selected, _("Sold out")
                        )
                q_counter = 0  # Limit to avoid too long selection list
                while q_valid <= q_alert and q_counter <= LIMIT_ORDER_QTY_ITEM:
                    q_select_id += 1
                    q_counter += 1
                    selected = EMPTY_STRING
                    if not q_order_is_displayed:
                        if q_previous_order <= q_valid:
                            q_order_is_displayed = True
                            selected = "selected"
                    if status == PERMANENCE_OPENED or (
                        status <= PERMANENCE_SEND and selected == "selected"
                    ):
                        display = product.get_display(
                            qty=q_valid,
                            order_unit=product.order_unit,
                            unit_price_amount=a_price,
                        )
                        html += '<option value="{}" {}>{}</option>'.format(
                            q_select_id, selected, display
                        )
                    if q_valid < q_step:
                        # 1; 2; 4; 6; 8 ... q_min = 1; q_step = 2
                        # 0,5; 1; 2; 3 ... q_min = 0,5; q_step = 1
                        q_valid = q_step
                    else:
                        # 1; 2; 3; 4 ... q_min = 1; q_step = 1
                        # 0,125; 0,175; 0,225 ... q_min = 0,125; q_step = 0,50
                        q_valid = q_valid + q_step

                if not q_order_is_displayed:
                    # An custom order_qty > q_alert
                    q_select_id += 1
                    display = product.get_display(
                        qty=q_previous_order,
                        order_unit=product.order_unit,
                        unit_price_amount=a_price,
                    )
                    html = '<option value="{}" selected>{}</option>'.format(
                        q_select_id, display
                    )
                if status == PERMANENCE_OPENED:
                    html += '<option value="other_qty">{}</option>'.format(
                        _("Other qty")
                    )
            else:
                html = '<option value="0" selected>---</option>'
        else:
            if purchase is not None and purchase.quantity_ordered != DECIMAL_ZERO:
                html = get_html_selected_value(
                    offer_item, purchase.quantity_ordered, is_open=True
                )
            else:
                html = '<option value="0" selected>---</option>'
    else:
        if purchase is not None and purchase.quantity_ordered != DECIMAL_ZERO:
            html = get_html_selected_value(
                offer_item, purchase.quantity_ordered, is_open=True
            )
        else:
            html = '<option value="0" selected>{}</option>'.format(_("Closed"))

    return JsonResponse({"#offer_item{}".format(offer_item.id): mark_safe(html)})
