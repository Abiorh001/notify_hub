from fastapi import status, Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from src.authentication.auth import get_current_active_user, AdminRoleChecker
from .schema import RecipientSchema, RecipientResponse
from src.database.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .service import RecipientService
from typing import Optional, List

admin_role = AdminRoleChecker()

recipient_router = APIRouter(tags=["Recipient Management"], prefix="/recipients")


@recipient_router.post(
    "/", response_model=RecipientResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_recipient(
    recipient_payload: RecipientSchema,
    recipient_service: RecipientService = Depends(RecipientService),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
    admin_user: AdminRoleChecker = Depends(admin_role),
) -> Optional[RecipientResponse]:

    try:
        current_active_user_uid = current_user.uid
        if current_active_user_uid:
            recipient_payload.created_by = current_active_user_uid
            new_recipient = await recipient_service.create_recipient(
                recipient_schema=recipient_payload, session=session
            )

        return new_recipient
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@recipient_router.get(
    "/", response_model=List[RecipientResponse], status_code=status.HTTP_200_OK
)
async def retrieve_all_recipients(
    recipient_service: RecipientService = Depends(RecipientService),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
    admin_user: AdminRoleChecker = Depends(admin_role),
) -> Optional[List[RecipientResponse]]:
    try:
        current_active_user = current_user.uid
        if current_active_user:
            recipients = await recipient_service.retrieve_all_recipient(
                created_by=current_active_user, session=session
            )
        return recipients
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@recipient_router.get(
    "/{recipient_uid}", response_model=RecipientResponse, status_code=status.HTTP_200_OK
)
async def retrieve_recipient(
    recipient_uid: str,
    recipient_service: RecipientService = Depends(RecipientService),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_active_user),
    admin_user: AdminRoleChecker = Depends(admin_role),
) -> Optional[RecipientResponse]:
    try:
        current_active_user = current_user.uid
        if current_active_user:
            recipient = await recipient_service.retrieve_recipient(recipient_uid=recipient_uid, session=session)
            if not recipient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Recipient Does not exist"
                )
            if recipient.created_by != current_active_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not allowed to view this resource"
                )
        return recipient
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

    
