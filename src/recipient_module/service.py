from .schema import RecipientSchema, RecipientUpdateSchema, RecipientResponse
from .models import Recipient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Optional, List
from uuid import UUID


class RecipientService:
    async def create_recipient(
        self, recipient_schema: RecipientSchema, session: AsyncSession
    ) -> Optional[RecipientResponse]:
        try:
            recipient_dict = recipient_schema.model_dump()
            new_recipient = Recipient(**recipient_dict)
            session.add(new_recipient)
            await session.commit()
            await session.refresh(new_recipient)
            recipient_response = RecipientResponse(
                uid=new_recipient.uid,
                first_name=new_recipient.first_name,
                last_name=new_recipient.last_name,
                email=new_recipient.email,
                phone_number=new_recipient.phone_number,
                created_by=new_recipient.created_by,
            )
            return recipient_response
        except Exception as e:
            await session.rollback()
            raise e

    async def retrieve_recipient(
        self, recipient_uid: str, session: AsyncSession
    ) -> Optional[RecipientResponse]:
        try:
            UUID(recipient_uid)
            recipient = await session.get(Recipient, recipient_uid)
            if not recipient:
                return None
            recipient_response = recipient_response = RecipientResponse(
                uid=recipient.uid,
                first_name=recipient.first_name,
                last_name=recipient.last_name,
                email=recipient.email,
                phone_number=recipient.phone_number,
                created_by=recipient.created_by,
            )
            return recipient_response
        except Exception as e:
            await session.rollback()
            raise e

    async def retrieve_all_recipient(
        self, created_by: str, session: AsyncSession
    ) -> List[RecipientResponse]:
        try:
            statement = select(Recipient).where(Recipient.created_by == created_by)
            result = await session.execute(statement)
            recipients = result.scalars().all()
        
            if not recipients:
                return []
            
            recipient_responses = [
                RecipientResponse(
                    uid=recipient.uid,
                    first_name=recipient.first_name,
                    last_name=recipient.last_name,
                    email=recipient.email,
                    phone_number=recipient.phone_number,
                    created_by=recipient.created_by,
                )
                for recipient in recipients
            ]
            return recipient_responses
        
        except Exception as e:
            await session.rollback()
            raise e