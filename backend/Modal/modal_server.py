import modal
from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent

image = (
    modal.Image.debian_slim()
    .workdir("/app")
    # .add_local_file(str(BACKEND_DIR/"pyproject.toml"), remote_path="/app", copy=True)
    # .add_local_file(str(BACKEND_DIR/"uv.lock"), remote_path="/app", copy=True)
    .add_local_dir(str(BACKEND_DIR), "/app", copy=True)
    .uv_sync()
    .env({"PYTHONPATH": "/app"})
)
# Modal necessitates this be called "app"
app = modal.App("Fanous-VL", image=image)


@app.cls(gpu="T4", scaledown_window=300)
class FanousServer:
    @modal.enter()
    def boot_up(self):
        from driver import Driver
        from model_modes import ModelMode
        self.driver = Driver(mode=ModelMode.huggingface)

    @modal.asgi_app()
    def asgi(self):
        import main
        main.DRIVER = self.driver
        return main.app
