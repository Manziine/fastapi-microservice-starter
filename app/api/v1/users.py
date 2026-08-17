"""
Users API Router - v1
Provides CRUD operations for user management with JWT authentication.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, get_current_active_superuser
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.crud import user as crud_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def get_current_user_profile(
    current_user=Depends(get_current_user),
):
    """
    Return the profile of the currently authenticated user.
    Requires a valid JWT access token in the Authorization header.
    """
    return current_user


@router.put("/me", response_model=UserResponse, summary="Update current user profile")
async def update_current_user_profile(
    user_in: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the profile of the currently authenticated user.
    Users can update their own name, email, and password.
    """
    if user_in.email and user_in.email != current_user.email:
        existing = crud_user.get_by_email(db, email=user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email address already registered"
            )
    return crud_user.update(db, db_obj=current_user, obj_in=user_in)


@router.get(
    "/",
    response_model=UserListResponse,
    summary="List all users (admin only)",
    dependencies=[Depends(get_current_active_superuser)]
)
async def list_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    search: Optional[str] = Query(None, description="Filter by name or email"),
):
    """
    Retrieve a paginated list of all users.
    **Admin only** - requires superuser privileges.
    """
    users, total = crud_user.get_multi(db, skip=skip, limit=limit, search=search)
    return UserListResponse(users=users, total=total, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
async def get_user_by_id(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a specific user by their ID.
    Users can view their own profile; admins can view any profile.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    # Non-admins can only view their own profile
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user profile"
        )
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user (admin only)",
    dependencies=[Depends(get_current_active_superuser)]
)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user account.
    **Admin only** - requires superuser privileges.
    """
    existing = crud_user.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )
    return crud_user.create(db, obj_in=user_in)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user (admin only)",
    dependencies=[Depends(get_current_active_superuser)]
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Permanently delete a user account.
    **Admin only** - requires superuser privileges.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    crud_user.remove(db, id=user_id)