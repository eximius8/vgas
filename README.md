# vgas

A FastAPI-based backend service for aggregating and processing delivery data from multiple logistics providers.

# Quick Start

## Configure environment
cp .env.example .env

## Build service images
```bash
docker compose build
```

## Run service
```bash
docker compose up
```

# API Documentation
http://localhost:8000/backend/docs


# Project Structure
```
backend/
├── api/
│   ├── routes/              # REST API endpoints
│   ├── schemas/             # API request/response models
│   └── filters/             # Query parameter filters
├── core/
│   ├── backgroundtasks/     # Async job processing & partner fetching
│   ├── crud/                # Database operations
│   └── database/            # SQLModel models & config
├── tests/                   # Unit & integration tests
├── main.py                  # FastAPI application
└── deps.py                  # Dependency injection
```

## API Layer (backend/api/)
### Routes (routes/deliveriesrouter.py):

```
POST /deliveries/fetch - Create fetch job 
GET /deliveries/jobs/{jobId} - Get job status 
GET /deliveries/jobs/{jobId}/results - Get job results with filters 
GET /deliveries - Query all deliveries
```

### Schemas (schemas/):

- JobCreateSerializer - Job creation request
- JobStatusSerializer - Job status response
- DeliveryGetSerializer - Delivery response
- DeliveryListSerializer - Paginated delivery list


### Filters (filters/deliveryfilter.py):

Query parameters for filtering/sorting deliveries

## Core Logic (backend/core/)
### Background Tasks (backgroundtasks/):


- fetchpartners.py - Fetch data from Partner A & B APIs in parallel
- processpartnerdata.py - Validate and transform partner data
- processjob.py - Orchestrate job processing workflow
- serializers.py - Pydantic models for partner data transformation


### CRUD Operations (crud/):

- jobs.py - Job creation, status updates, idempotency logic
- deliveries.py - Delivery storage, filtering, and queries

### Database (database/):

- models/job.py - Job model with stats and status tracking
- models/delivery.py - Delivery model with hybrid_property for scoring
- config.py - Database engine and initialization

### Data Flow

Client creates job → POST /deliveries/fetch 
Background task starts → Fetch from Partner A & B in parallel 
Transform & validate data using Pydantic serializers 
Calculate delivery scores 
Store in PostgreSQL → Update job stats/status 
Client queries results → GET /deliveries/jobs/{jobId}/results 


## Transformation & Scoring
### Transformation Layer

Pydantic models handle data transformation from partner-specific formats to unified format. 
Located in backend/core/backgroundtasks/serializers.py


### Scoring Logic
Implementation: SQLAlchemy hybrid_property in backend/core/database/models/delivery.py

Key Feature: hybrid_property allows:

- Python property for in-memory calculations 
- SQL expression for database queries and sorting
- Efficient sorting without loading all records


API Examples
1. Create Fetch Job
Request:
```bash
curl -X POST http://localhost:8000/backend/deliveries/fetch \
  -H "Content-Type: application/json" \
  -d '{"siteId":"munich-schwabing-1","date":"2025-08-01"}'
```
Response (201 Created):
```json
{
  "jobId": "c9b0d4d1-5f6a-4c88-9a28-1d88d1b4a3f7",
  "status": "created"
}
```

2. Check Job Status
Request:
```bash
curl http://localhost:8000/backend/deliveries/jobs/c9b0d4d1-5f6a-4c88-9a28-1d88d1b4a3f7
```
Response:
```json
{
  "jobId": "c9b0d4d1-5f6a-4c88-9a28-1d88d1b4a3f7",
  "status": "finished",
  "createdAt": "2025-08-01T06:00:00Z",
  "updatedAt": "2025-08-01T06:00:12Z",
  "input": {
    "siteId": "munich-schwabing-1",
    "date": "2025-08-01"
  },
  "stats": {
    "partnerA": {"fetched": 100, "transformed": 100, "errors": 0},
    "partnerB": {"fetched": 100, "transformed": 100, "errors": 0},
    "stored": 200
  },
  "error": null
}
```

3. Get Job Results
Request:
```bash
curl "http://localhost:8000/backend/deliveries/jobs/c9b0d4d1-5f6a-4c88-9a28-1d88d1b4a3f7/results?limit=10&signed=true&sortBy=delivery_score_desc"
```
Response:
```json
{
  "jobId": "c9b0d4d1-5f6a-4c88-9a28-1d88d1b4a3f7",
  "items": [
    {
      "id": "DEL-002-A",
      "supplier": "SupplierY",
      "deliveredAt": "2025-08-01T09:41:00Z",
      "status": "delivered",
      "signed": true,
      "siteId": "munich-schwabing-1",
      "source": "Partner A",
      "deliveryScore": 1.2
    },
    {
      "id": "b-1005",
      "supplier": "SupplierB4",
      "deliveredAt": "2025-08-01T08:00:00Z",
      "status": "delivered",
      "signed": true,
      "siteId": "munich-schwabing-1",
      "source": "Partner B",
      "deliveryScore": 1.2
    }
  ],
  "total": 89,
  "limit": 10,
  "offset": 0
}
```
Available Query Parameters:

- limit, offset - Pagination
- supplier - Filter by supplier
- status - delivered, cancelled, pending
- signed - true/false
- from, to - Date range
- siteId - Site ID
- sortBy - delivery_score_desc, delivered_at_asc, etc.


4. Query All Deliveries
Request:
```bash
curl "http://localhost:8000/backend/deliveries?status=delivered&limit=5"
```
Response:
```json
{
  "items": [
    {
      "id": "DEL-001-A",
      "supplier": "Innotech",
      "deliveredAt": "2025-08-01T15:54:00Z",
      "status": "delivered",
      "signed": true,
      "siteId": "munich-schwabing-1",
      "source": "Partner A",
      "deliveryScore": 1.0
    }
  ],
  "total": 200,
  "limit": 5,
  "offset": 0
}
```

# Resilience Notes
## Timeouts

- Partner APIs: 5-second timeout per request
- Implementation: httpx.AsyncClient(timeout=5.0)
- Behavior: Timeout on one partner doesn't fail entire job

## Retries

- Current State: No automatic retries for partner API calls
- Partial Success: Job succeeds if at least one partner returns data

## Caching

Current State: No caching implemented


## Idempotency

Implementation: Jobs uniquely identified by (siteId, date) pair
Behavior:

- Existing job with status created/processing → Returns existing job (202)
- Existing job with status finished/failed → Creates new job (201)
- No existing job → Creates new job (201)


# Future Improvements
1. Replace SQLModel with SQLAlchemy
Issue: SQLModel has limitations and less community support

2. Add Database Migrations


3. Expand Test Coverage
Add:

Edge case testing (invalid dates, malformed data)
Integration tests for complete job lifecycle
Performance tests for large datasets
Mock partner API failure scenarios
Database constraint testing

Current Coverage: ~70% (transformation, validation, API endpoints)
Target: 90%+

4. Implement Celery for Job Processing
Replace: FastAPI BackgroundTasks
