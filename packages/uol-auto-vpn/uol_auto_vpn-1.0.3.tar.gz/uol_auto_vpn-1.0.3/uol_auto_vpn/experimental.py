class OpenConnectVPN:
    def __init__(self, cookie, server):
        self._cookie = cookie
        self._server = server

    @property
    def command(self):
        return f"sudo openconnect --cookie={self._cookie} {self._server}"

    def run(self):
        env = os.environ.copy()
        p = subprocess.Popen(
            f'/bin/bash -c \"{self.command}; echo \"Closing Terminal\";sleep 10\"',
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, env=env)

        import sys
        sys.stdout.write("Started Local Terminal...\r\n\r\n")

        def writeall(p):
            while True:
                # print("read data: ")
                data = p.stdout.read(1).decode("utf-8")
                if not data:
                    break
                sys.stdout.write(data)
                sys.stdout.flush()

        import threading
        writer = threading.Thread(target=writeall, args=(p,))
        writer.start()

        try:
            while True:
                d = sys.stdin.read(1)
                if not d:
                    break
                self._write(p, d.encode())
        except EOFError:
            pass

    def _write(self, process, message):
        process.stdin.write(message)
        process.stdin.flush()