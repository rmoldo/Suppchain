from fastapi import FastAPI
import uvicorn
from fastapi_sqlalchemy import DBSessionMiddleware
import routers.usersRouter as userRouter
import routers.authRouter as authRouter
import routers.mailRouter as mailRouter
import routers.permissionRouter as permissionRouter
import routers.transactionRouter as transactionRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Create AdminSite instance



# @app.on_event("startup")
# async def startup():
#   await init_db()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(DBSessionMiddleware, db_url="postgresql://radu:raduadu@postgres:5432/ecomm_db")


app.include_router(authRouter.router)
app.include_router(userRouter.router)
app.include_router(mailRouter.router)
app.include_router(permissionRouter.router)
app.include_router(transactionRouter.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
