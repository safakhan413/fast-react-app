from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta

from .database import SessionLocal, engine
from . import models, schemas
from .auth import router as auth_router, get_current_user
from .models import User as UserModel, Phone, Voicemail
from .utils import get_logger

logger = get_logger(__name__)

# Create the database tables (if not already created)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Data API")

# Include the authentication router
app.include_router(auth_router)

# Configure CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows API requests from frontend

    # allow_origins=["*"],  # For testing; specify origins in production
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

# Protected Endpoint to Retrieve Users
# Protected Endpoint to Retrieve Users
@app.get("/users/", response_model=List[schemas.User])
async def get_users(
    start_time: int = Query(..., description="Start time in Unix timestamp"),
    end_time: int = Query(..., description="End time in Unix timestamp"),
    parameter: Optional[str] = Query(None, description="One of 'user_id', 'phone', 'voicemail', 'cluster'"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"User {current_user['username']} requested users with filters.")

    query = db.query(UserModel).filter(
        UserModel.originationTime.between(start_time, end_time)
    )

    if parameter == 'user_id':
        # No additional filtering needed; include all users with user IDs
        pass
    elif parameter == 'phone':
        query = query.join(UserModel.phones)
    elif parameter == 'voicemail':
        query = query.join(UserModel.voicemails)
    elif parameter == 'cluster':
        # No additional filtering needed; include all clusters
        pass

    users = query.all()
    logger.info(f"Retrieved {len(users)} users.")
    return users

# @app.get("/users/", response_model=List[schemas.User])
# async def get_users(
#     start_time: int = Query(..., description="Start time in Unix timestamp"),
#     end_time: int = Query(..., description="End time in Unix timestamp"),
#     user_id: Optional[str] = Query(None),
#     phone: Optional[str] = Query(None),
#     voicemail: Optional[str] = Query(None),
#     cluster: Optional[str] = Query(None),
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     logger.info(f"User {current_user['username']} requested users with filters.")

#     query = db.query(UserModel).filter(
#         UserModel.originationTime.between(start_time, end_time)
#     )

#     if user_id:
#         query = query.filter(UserModel.userId == user_id)
#     if cluster:
#         query = query.filter(UserModel.clusterId == cluster)
#     if phone:
#         query = query.join(UserModel.phones).filter(Phone.identifier == phone)
#     if voicemail:
#         query = query.join(UserModel.voicemails).filter(Voicemail.identifier == voicemail)

#     users = query.all()
#     logger.info(f"Retrieved {len(users)} users.")
#     return users

# Endpoint to Download Users as CSV
@app.get("/users/download")
async def download_users_csv(
    start_time: int = Query(..., description="Start time in Unix timestamp"),
    end_time: int = Query(..., description="End time in Unix timestamp"),
    user_id: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    voicemail: Optional[str] = Query(None),
    cluster: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    import csv
    from fastapi.responses import StreamingResponse
    from io import StringIO

    logger.info(f"User {current_user['username']} requested CSV download.")

    query = db.query(UserModel).filter(
        UserModel.originationTime.between(start_time, end_time)
    )

    if user_id:
        query = query.filter(UserModel.userId == user_id)
    if cluster:
        query = query.filter(UserModel.clusterId == cluster)
    if phone:
        query = query.join(UserModel.phones).filter(Phone.identifier == phone)
    if voicemail:
        query = query.join(UserModel.voicemails).filter(Voicemail.identifier == voicemail)

    users = query.all()
    logger.info(f"Retrieved {len(users)} users for CSV download.")

    # Create CSV in memory
    def iter_csv():
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "UserID", "OriginationTime", "ClusterID", "Phones", "Voicemails"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for user in users:
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
