from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse
from app.crud import item as crud_item

router = APIRouter(prefix='/items', tags=['items'])


@router.get('/', response_model=ItemListResponse)
async def list_items(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    owner_only: bool = Query(False),
):
    owner_id = current_user.id if owner_only else None
    items, total = crud_item.get_multi(db, skip=skip, limit=limit, search=search, owner_id=owner_id)
    return ItemListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get('/{item_id}', response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    item = crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Item {item_id} not found')
    return item


@router.post('/', response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud_item.create_with_owner(db, obj_in=item_in, owner_id=current_user.id)


@router.put('/{item_id}', response_model=ItemResponse)
async def update_item(item_id: int, item_in: ItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    item = crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail='Permission denied')
    return crud_item.update(db, db_obj=item, obj_in=item_in)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    item = crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail='Permission denied')
    crud_item.remove(db, id=item_id)
