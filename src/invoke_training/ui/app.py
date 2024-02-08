from pathlib import Path

import gradio as gr
from fastapi import FastAPI
from fastapi.responses import FileResponse

from invoke_training.ui.pages.data_page import DataPage
from invoke_training.ui.pages.training_page import TrainingPage


def build_app():
    training_page = TrainingPage()
    data_page = DataPage()

    app = FastAPI()

    @app.get("/")
    async def root():
        index_path = Path(__file__).parent / "index.html"
        return FileResponse(index_path)

    app = gr.mount_gradio_app(app, training_page.app(), "/train")
    app = gr.mount_gradio_app(app, data_page.app(), "/data")
    return app