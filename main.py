from fastapi import FastAPI, Depends, HTTPException, Request, Form, UploadFile, File
from fastapi import FastAPI, Depends, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware
from datetime import date
import os




Base.metadata.create_all(bind=engine)

print(">>> Table creation finished")

#models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TraceItem")
@app.on_event("startup")
def create_default_users():
    db = SessionLocal()

    if not db.query(models.User).first():
        teacher = models.User(
            username="teacher1",
            password_hash=pwd_context.hash("admin123"),
            role="Teacher"
        )

        student = models.User(
            username="student1",
            password_hash=pwd_context.hash("1234"),
            role="Student"
        )

        db.add_all([teacher, student])
        db.commit()

    db.close()


app.add_middleware(SessionMiddleware, secret_key="traceitem-secret-key")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid username or password!"
            }
        )

    request.session["user"] = {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }

    return RedirectResponse("/dashboard", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=303)

    items = db.query(models.Item).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "items": items,
            "user": user
        }
    )


@app.post("/return-item/{item_id}")
def return_item(
    request: Request,
    item_id: int,
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user or user["role"].lower() != "teacher":
        return RedirectResponse("/dashboard", status_code=303)

    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        item.status = "Returned"
        db.commit()

    return RedirectResponse("/dashboard", status_code=303)

@app.post("/delete-item/{item_id}")
def delete_item(
    request: Request,
    item_id: int,
    db: Session = Depends(get_db)
):
    user = request.session.get("user")

    print("DELETE REQUEST FOR ITEM:", item_id)
    print("USER:", user)

    if not user or user["role"].lower() != "teacher":
        print("DELETE BLOCKED: NOT TEACHER")
        return RedirectResponse("/dashboard", status_code=303)

    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item:
        print("ITEM NOT FOUND")
        return RedirectResponse("/dashboard", status_code=303)

    db.delete(item)
    db.commit()

    print("ITEM DELETED")

    return RedirectResponse("/dashboard", status_code=303)




@app.get("/add-item", response_class=HTMLResponse)
def add_item_page(request: Request):
    user = request.session.get("user")
    if not user or user["role"].lower() != "teacher":
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse("add_item.html", {"request": request})


@app.post("/add-item")
def add_item(
    request: Request,
    item_name: str = Form(...),
    color: str = Form(...),
    location_found: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user or user["role"].lower() != "teacher":
        return RedirectResponse("/dashboard", status_code=303)

    image_url = ""

    if image and image.filename:
        os.makedirs("static/uploads", exist_ok=True)
        image_path = f"static/uploads/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(image.file.read())
        image_url = f"/{image_path}"

    new_item = models.Item(
        item_name=item_name,
        color=color,
        location_found=location_found,
        image_url=image_url,
        status="Found",
        reported_by=user["id"],
        date_found=date.today()
    )

    db.add(new_item)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)



@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
