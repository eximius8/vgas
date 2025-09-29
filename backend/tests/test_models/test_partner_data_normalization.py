
from backend.schemas.partnera import PartnerADelivery
from backend.schemas.partnerb import PartnerBDelivery



def test_partner_a_normalization(partner_a_correct_response):
    for item in partner_a_correct_response:
        delivery = PartnerADelivery(**item)
        assert set(delivery.model_dump(by_alias=True).keys()) == {
            'ext_id', 'supplier', 'delivered_at', 'status', 'signed', 'source'}

def test_partner_b_normalization(partner_b_correct_response):
    for item in partner_b_correct_response:
        delivery = PartnerBDelivery(**item)
        assert set(delivery.model_dump(by_alias=True).keys()) == {
            'ext_id', 'supplier', 'delivered_at', 'status', 'signed', 'source'}

