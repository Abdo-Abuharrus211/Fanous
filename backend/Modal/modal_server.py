import modal
modal_app = modal.App("Fanous-VL")

@modal_app.server(unauthenticated=True)
class FanousOnModal:

    @modal_app.enter()
    def boot_up(self):

        import subprocess
        subprocess.Popen( "uvicorn main:app --host 0.0.0.0 --port 8000",
            shell=True)

