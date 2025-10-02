

def test_create_job(client, job_json):
    response = client.post("/backend/deliveries/fetch", json=job_json)
    assert response.status_code == 201
    data = response.json()
    assert 'jobId' in data
    assert 'status' in data
    assert data['status'] == "created"


def test_not_create_created_job(client, sample_database_data):
    job = sample_database_data.get('created')
    response = client.post(
        "/backend/deliveries/fetch", 
        json={
            "siteId": job.site_id,
            "date": str(job.for_date)
            })
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] == str(job.id)


def test_not_create_processing_job(client, sample_database_data):
    job = sample_database_data.get('processing')
    response = client.post("/backend/deliveries/fetch", json={
        "siteId": job.site_id,
        "date": str(job.for_date)} )
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] == str(job.id)


def test_create_failed_job(client, sample_database_data,):
    job = sample_database_data.get('failed')
    response = client.post("/backend/deliveries/fetch", json={
        "siteId": job.site_id,
        "date": str(job.for_date)} )
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] != str(job.id)

def test_create_finished_jon(client, sample_database_data):
    job = sample_database_data.get('finished')
    response = client.post("/backend/deliveries/fetch", json={
        "siteId": job.site_id,
        "date": str(job.for_date)} )
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] != str(job.id)
