import shutil
import json
from traceback import print_exception
from typing import Annotated, Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, Response, Header, Cookie, Depends
from fastapi.responses import PlainTextResponse, RedirectResponse
from pycel import ExcelCompiler
import pandas as pd

from utils import (
    SessionData,
    TableData,
    generate_session_id,
    validate_session_id,
    admin_session_id,
    api_write_key,
)

src_path = Path(__file__).parent.resolve()

# initialization
spreadsheet_path_clean = src_path / "data/clean.xlsx"
spreadsheet_path = src_path / "data/dirty.xlsx"
shutil.copyfile(spreadsheet_path_clean, spreadsheet_path)

print(f"[*] Loading {spreadsheet_path}...")
excel = ExcelCompiler(filename=str(spreadsheet_path))

router = APIRouter(prefix="/api")

sessions: dict[str, SessionData] = {
    admin_session_id: SessionData(username="admin", role="admin")
}


def Session(
    response: Response, token: Annotated[str | None, Cookie()] = None
) -> SessionData:
    session_id = validate_session_id(token)

    if session_id in sessions:
        return sessions[session_id]

    session_id = generate_session_id()
    sessions[session_id] = SessionData()

    response.set_cookie("token", session_id, max_age=3600, samesite="strict")

    return sessions[session_id]


def AdminSession(session: Annotated[SessionData, Depends(Session)]) -> SessionData:
    if session.username != "admin" or session.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")

    return session


def APIKey(x_api_key: Annotated[str, Header()]) -> str:
    if x_api_key != api_write_key:
        raise HTTPException(status_code=401, detail="Unauthorized - API")

    return x_api_key


# dependency shortcuts
MustLogin = Annotated[SessionData, Depends(Session)]
MustBeAdmin = Annotated[SessionData, Depends(AdminSession)]


@router.get("/whoami")
def whoami(user: MustLogin) -> SessionData:
    return user


@router.get("/whoami/jsonp")
def whoami_jsonp(user: MustLogin, callback: str = "alert"):
    return PlainTextResponse(callback + "(" + user.model_dump_json() + ")")


@router.post("/whoami")
async def update_username(user: MustLogin, request: Request) -> SessionData:
    if user.role == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    data = json.loads(await request.body())

    if "new_username" not in data:
        raise HTTPException(status_code=400, detail="Bad Request")

    new_username = data["new_username"]

    if type(new_username) is not str or len(new_username) < 2:
        raise HTTPException(status_code=400, detail="Invalid username")

    user.username = new_username
    return user


@router.get("/key")
def get_api_key(user: MustBeAdmin):
    return {"key": api_write_key}


@router.get("/sheets")
def get_sheets(user: MustLogin):
    global excel

    if not spreadsheet_path.exists():
        shutil.copyfile(spreadsheet_path_clean, spreadsheet_path)

    excel = ExcelCompiler(filename=str(spreadsheet_path))
    try:
        sheet_header = excel.evaluate("Sheet1!A1:F1")
        sheet_rows = excel.evaluate("Sheet1!A2:F16")

        if not sheet_rows or not len(sheet_rows):
            return HTTPException(
                500, detail="Unexpected error while loading spreadsheet"
            )

    except Exception as ex:
        print_exception(ex)

        print("[*] Resetting Excel file to clean state...")
        shutil.copyfile(spreadsheet_path_clean, spreadsheet_path)
        excel = ExcelCompiler(filename=str(spreadsheet_path))
        return {"error": "Something went wrong while updating... Sheet reset."}

    return {"header": sheet_header, "rows": sheet_rows}


@router.get("/sheets/reset")
def reset_sheets(user: MustLogin):
    global excel
    shutil.copyfile(spreadsheet_path_clean, spreadsheet_path)
    excel = ExcelCompiler(filename=str(spreadsheet_path))
    return {"success": "true"}


@router.post("/sheets")
def post_sheets(
    user: MustLogin, api_key: Annotated[str, Depends(APIKey)], data: TableData
):
    global excel
    try:
        sheet_header = data.header
        rows = data.rows

        excel.set_value("Sheet1!A2:F16", rows)
        sheet_rows = excel.evaluate("Sheet1!A2:F16")

        if not sheet_rows or not len(sheet_rows):
            return HTTPException(
                500, detail="Unexpected error while loading spreadsheet"
            )

        for i in range(2, 17):
            row = [x if x else 0 for x in excel.evaluate(f"Sheet1!A{i}:D{i}")]

            if row and any(row):
                excel.set_value(f"Sheet1!E{i}", f"=AVERAGE(A{i}:D{i})")
                # sadly STDEV is not implemented :(
                excel.set_value(
                    f"Sheet1!F{i}",
                    f"=SQRT(SUMPRODUCT((A{i}:D{i}-AVERAGE(A{i}:D{i}))^2)/COUNT(A{i}:D{i}))",
                )

        sheet_rows: list[Any] = excel.evaluate("Sheet1!A2:F16")

        df = pd.DataFrame([sheet_header, *sheet_rows])
        df.to_excel(spreadsheet_path, index=False, header=False)
    except Exception as ex:
        print_exception(ex)
        print("[-] Resetting Excel file...")
        shutil.copyfile(spreadsheet_path_clean, spreadsheet_path)
        excel = ExcelCompiler(filename=str(spreadsheet_path))
        return {"error": "Something went wrong while updating... Sheet reset."}

    return {"rows": sheet_rows}


@router.get("/logout")
def logout(user: MustLogin):
    response = RedirectResponse("/")
    response.delete_cookie("token")

    return response
