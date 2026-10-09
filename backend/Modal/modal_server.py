import modal
from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent

image = modal.Image.debian_slim().pip_install(
    "fastapi[standard]>=0.115.0",
    "moondream>=0.1.0",
    "pillow>=10.0.0",
).workdir("/app").copy_local_dir(str(BACKEND_DIR), ".")

modal_app = modal.App("Fanous-VL", image=image)


@modal_app.cls(gpu="T4", keep_warm=1, scaledown_window=300)
class FanousServer:
    @modal.enter()
    def boot_up(self):
        from driver import Driver
        from model_modes import ModelMode
        self.driver = Driver(mode=ModelMode.moondream_direct)

    @modal.asgi_app()
    def asgi(self):
        import main
        main.DRIVER = self.driver
        return main.app
