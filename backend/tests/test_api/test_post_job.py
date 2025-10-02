
def test_create_job(client, job_json):
    response = client.post("/backend/deliveries/fetch", json=job_json)
    assert response.status_code == 201
    data = response.json()
    assert 'jobId' in data
    assert 'status' in data
    assert data['status'] == "created"


def test_not_create_created_jon(client, sample_database_data, job_created):
    
    response = client.post("/backend/deliveries/fetch", json={
        "siteId": job_created.site_id,
        "date": str(job_created.for_date)} )
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] == str(job_created.id)


def test_not_create_processing_jon(client, sample_database_data, job_processing):
    
    response = client.post("/backend/deliveries/fetch", json={
        "siteId": job_processing.site_id,
        "date": str(job_processing.for_date)} )
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] == str(job_processing.id)


def test_not_create_created_jon(client, sample_database_data, job_created):
    
    response = client.post("/backend/deliveries/fetch", json={
        "siteId": job_created.site_id,
        "date": str(job_created.for_date)} )
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] == str(job_created.id)


def test_create_failed_jon(client, sample_database_data, job_failed):
    
    response = client.post("/backend/deliveries/fetch", json={
        "siteId": job_failed.site_id,
        "date": str(job_failed.for_date)} )
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] != str(job_failed.id)

def test_create_finished_jon(client, sample_database_data, job_finished):
    
    response = client.post("/backend/deliveries/fetch", json={
        "siteId": job_finished.site_id,
        "date": str(job_finished.for_date)} )
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] != str(job_finished.id)