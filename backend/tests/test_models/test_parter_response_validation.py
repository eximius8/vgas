import pytest
from backend.core.backgroundtasks.serializers import (
    DeliveryPartnerASerializer,
    DeliveryPartnerBSerializer,
)


def test_partner_a_delivery_validation_positive(partner_a_correct_response):
    for item in partner_a_correct_response:
        delivery = DeliveryPartnerASerializer(**item)
        assert delivery.deliveryId == item["deliveryId"]
        assert delivery.supplier == item["supplier"]
        assert (
            delivery.timestamp.isoformat().replace("+00:00", "Z") == item["timestamp"]
        )
        assert delivery.status == item["status"]
        assert delivery.signedBy == item.get("signedBy")
        assert delivery.source == "Partner A"


def test_partner_a_delivery_validation_negative(partner_a_wrong_response):
    for item in partner_a_wrong_response:
        with pytest.raises(Exception):
            DeliveryPartnerASerializer(**item)


def test_partner_b_delivery_validation_positive(partner_b_correct_response):
    for item in partner_b_correct_response:
        delivery = DeliveryPartnerBSerializer(**item)
        assert delivery.id == item["id"]
        assert delivery.provider == item["provider"]
        assert delivery.deliveredAt.isoformat() == item["deliveredAt"]
        assert delivery.statusCode == item["statusCode"]
        assert delivery.source == "Partner B"


def test_partner_b_delivery_validation_negative(partner_b_wrong_response):
    for item in partner_b_wrong_response:
        with pytest.raises(Exception):
            DeliveryPartnerBSerializer(**item)
