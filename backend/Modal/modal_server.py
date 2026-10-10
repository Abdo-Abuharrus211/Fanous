import modal
from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent
image = (
    modal.Image.debian_slim()
    .workdir("/app")
    .env({"PYTHONPATH": "/app"})
    # .add_local_file("./pyproject.toml", remote_path="/app")
    # .add_local_file("./uv.lock", remote_path="/app")
    .add_local_dir(str(BACKEND_DIR), "/app", copy=True)
    .uv_sync()
    .run_commands(
        "python -c \""
        "from huggingface_hub import snapshot_download; "
        "snapshot_download(repo_id='vikhyatk/moondream2', revision='2025-06-21')\""
    )
)

app = modal.App("Fanous-VL", image=image)


@app.cls(gpu="T4", scaledown_window=300, secrets=[modal.Secret.from_name("hf-token")])
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
