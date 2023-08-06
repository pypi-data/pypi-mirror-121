from locapip.dependencies import app_config
from locapip import explorer, explorer_ws
import click
import fastapi
import uvicorn
import pathlib
import os

app = fastapi.FastAPI(
    title=app_config.name,
    version=app_config.version,
    description=app_config.description,
    # contact={
    #     "name": "洛卡皮迪奥",
    #     "url": "https://locapidio.com",
    #     "email": "88172828@qq.com",
    # },
    # license_info={
    #     "name": "GPLv3+",
    #     "url": "https://jxself.org/translations/gpl-3.zh.shtml",
    # },
    openapi_tags=[
        {"name": "explorer", "description": "场景数据资源管理"},
        {"name": "explorer_ws", "description": "场景数据资源管理"},
    ]
)

app.include_router(explorer.router, prefix="/explorer", tags=["explorer"])
app.include_router(explorer_ws.router, prefix="/explorer", tags=["explorer"])


@click.command()
@click.argument("data_root_dir", type=click.Path(file_okay=False, dir_okay=True, path_type=pathlib.Path))
@click.option("--host", type=click.STRING, default="0.0.0.0", show_default=True)
@click.option("--port", type=click.IntRange(1024, 49151), default=6547, show_default=True)
def main(data_root_dir: pathlib.Path, host: str, port: int):
    if not data_root_dir.exists():
        os.makedirs(data_root_dir)

    app_config.data_root_dir = data_root_dir.resolve()
    app_config.host = host
    app_config.port = port

    print(f"{app_config.name} {app_config.version}\n"
          f"ROOT: {data_root_dir}\n"
          f"INFO: http://{host}:{port}/redoc or http://{host}:{port}/docs")

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
