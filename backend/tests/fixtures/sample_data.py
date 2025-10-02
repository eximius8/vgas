import pytest


@pytest.fixture
def job_json():

    return {
        "siteId": "test site",
        "date": "2025-12-20"
    }


@pytest.fixture
def partner_a_wrong_response():

    return [{       
        "supplier": "SupplierX",
        "timestamp": "2025-08-01T07:34:00Z",
        "status": "delivered",
        "signedBy": "Martin Schulz"
    },
    {
        "deliveryId": "DEL-002-A",
        "supplier": "SupplierY",
        "timestamp": "2025-08-01T12",
        "status": "pending",       
    },   
    {
        "deliveryId": "k",
        "supplier": "SupplierZ",
        "timestamp": "2025-08-01T09:15:00Z",
        "status": "not ok",
    }]



@pytest.fixture
def partner_a_correct_response():
    return [{
        "deliveryId": "DEL-001-A",
        "supplier": "SupplierX",
        "timestamp": "2025-08-01T07:34:00Z",
        "status": "delivered",
        "signedBy": "Martin Schulz",
        "source": "Partner D"
    },
    {
        "deliveryId": "DEL-002-A",
        "supplier": "SupplierY",
        "timestamp": "2025-08-01T12:00:00Z",
        "status": "pending",       
        "source": "Partner C"
    },
    {
        "deliveryId": "k",
        "supplier": "SupplierZ",
        "timestamp": "2025-08-01T09:15:00Z",
        "status": "cancelled",
        "source": "Partner ADVCD"
    }]

@pytest.fixture
def partner_b_wrong_response():

    return [{
        "id": "b-876543",
        "provider": "SupplierY",
        "deliveredAt": "2025-08-01T08:02:00+01:00",
        "statusCode": "OK",
        "receiver": {
            "name": "M. Schulz",            
            }
    },
    {
        "id": "b-876543",
        "provider": "SupplierY",
        "deliveredAt": "2025-08-01T08",
        "statusCode": "failed"
    },
    {
        "id": "b",
        "provider": "SuppliefasdfdasfasrY",
        "deliveredAt": "2025-08-01T08:02:00+01:00",
        "statusCode": "failed",
        "receiver": {          
            "signed": False
            }
    },]



@pytest.fixture
def partner_b_correct_response():
    return [{
        "id": "b-876543",
        "provider": "SupplierY",
        "deliveredAt": "2025-08-01T08:02:00+01:00",
        "statusCode": "OK",
        "receiver": {
            "name": "M. Schulz",
            "signed": True
            }
    },
    {
        "id": "b-876543",
        "provider": "SupplierY",
        "deliveredAt": "2025-08-01T08:02:00+01:00",
        "statusCode": "failed"
    },
    {
        "id": "b",
        "provider": "SuppliefasdfdasfasrY",
        "deliveredAt": "2025-08-01T08:02:00+01:00",
        "statusCode": "failed",
        "receiver": {
            "name": "M. Schulz",
            "signed": False
            }
    },]


