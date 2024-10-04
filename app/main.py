from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func, asc

from .database import SessionLocal, engine
from . import models, schemas
from .auth import router as auth_router, get_current_user

# Create the database tables (if not already created)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Data API")

# Include the authentication router
app.include_router(auth_router)

# Configure CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to fetch users with ordering
def fetch_users(
    start_time: int,
    end_time: int,
    parameter: Optional[str],
    db: Session
):
    query = db.query(models.User).filter(
        models.User.originationTime.between(start_time, end_time)
    )

    if parameter == 'user_id':
        query = query.order_by(models.User.userId)
    elif parameter == 'phone':
        # Order users by the minimum phone identifier
        query = (
            query.outerjoin(models.User.phones)
            .group_by(models.User.id)
            .order_by(func.min(models.Phone.identifier).asc())
        )
    elif parameter == 'voicemail':
        # Order users by the minimum voicemail identifier
        query = (
            query.outerjoin(models.User.voicemails)
            .group_by(models.User.id)
            .order_by(func.min(models.Voicemail.identifier).asc())
        )
    elif parameter == 'cluster':
        query = query.order_by(models.User.clusterId)
    else:
        query = query.order_by(models.User.id)

    users = query.all()

    # Sort phones and voicemails for each user
    for user in users:
        user.phones.sort(key=lambda p: p.identifier)
        user.voicemails.sort(key=lambda v: v.identifier)

    return users

# Protected Endpoint to Retrieve Users
@app.get("/users/", response_model=List[schemas.User])
async def get_users(
    start_time: int = Query(..., description="Start time in Unix timestamp"),
    end_time: int = Query(..., description="End time in Unix timestamp"),
    parameter: Optional[str] = Query(None, description="One of 'user_id', 'phone', 'voicemail', 'cluster'"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    

    if start_time >= end_time:
        raise HTTPException(status_code=400, detail="start_time must be less than end_time")
    if parameter and parameter not in {'user_id', 'phone', 'voicemail', 'cluster'}:
        raise HTTPException(status_code=400, detail="Invalid parameter value")
    
    try:
        users = fetch_users(start_time, end_time, parameter, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return users
    # users = fetch_users(start_time, end_time, parameter, db)
    # return users

# Endpoint to Download Users as CSV
@app.get("/users/download")
async def download_users_csv(
    start_time: int = Query(..., description="Start time in Unix timestamp"),
    end_time: int = Query(..., description="End time in Unix timestamp"),
    parameter: Optional[str] = Query(None, description="One of 'user_id', 'phone', 'voicemail', 'cluster'"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    users = fetch_users(start_time, end_time, parameter, db)

    import csv
    from fastapi.responses import StreamingResponse
    from io import StringIO

    def iter_csv():
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "UserID", "OriginationTime", "ClusterID", "Phones", "Voicemails"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for user in users:
            # Phones and voicemails are already sorted in fetch_users
            writer.writerow([
                user.id,
                user.userId,
                user.originationTime,
                user.clusterId,
                ";".join([phone.identifier for phone in user.phones]),
                ";".join([vm.identifier for vm in user.voicemails])
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    response = StreamingResponse(iter_csv(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=users.csv"
    return response
