from fastapi import APIRouter, Depends
from fastapi import Response, HTTPException
from starlette.status import HTTP_201_CREATED
from domain.account.repository import AccountRepository
from domain.account.service import IAccountCheck
from domain.account.account_check import AccountCheck
from infrastructure.mysql.account.repository import AccountRepositoryMysql
from application.account.interfaces import ICreateAccountUseCase
from application.account.create_account_use_case import CreateAccountUseCase
from presentation.dto.accounts.signup import ResponseBody, RequestBody
from config.rdb import get_connection, close_connection
from aiomysql.connection import Connection

router = APIRouter()


async def get_use_case() -> ICreateAccountUseCase:
    conn: Connection = await get_connection()
    repository: AccountRepository = AccountRepositoryMysql(conn)
    account_check: IAccountCheck = AccountCheck(repository)
    return CreateAccountUseCase(repository, account_check)


@router.post("/api/v1/accounts/signup", response_model=ResponseBody)
async def signup(
        response: Response,
        data: RequestBody,
        use_case: ICreateAccountUseCase = Depends(get_use_case),
):
    #   TODO: リクエストバリデーションを行う
    #   TODO: メールアドレスの確認用メールを送信する処理を追加する
    try:
        account_id = await use_case.execute(data.email, data.password, data.password_confirmation)
        response.status_code = HTTP_201_CREATED
        body: ResponseBody = ResponseBody(id=account_id)
        await close_connection()
        return body
    except:
        raise HTTPException(status_code=404, detail='signup failed')
