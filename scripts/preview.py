"""Serve a built site on localhost, over both IPv4 and IPv6.

    python scripts/preview.py .live/site --port 8012

Why this exists rather than `python -m http.server --bind localhost`:
that binds *one* address family. On macOS `localhost` resolves to `::1` first,
so the server ends up IPv6-only and `http://127.0.0.1:<port>` is refused
outright. A browser usually recovers, but a bookmark, a curl, a script or a
second browser profile that prefers IPv4 just fails, and the failure looks like
"the preview server is down" rather than "it is up on the other stack".

So: two listeners on the same port, one per family, both loopback-only. Nothing
is exposed beyond this machine - deliberately, since the in-progress site shows
every unpublished week.
"""

from __future__ import annotations

import argparse
import socket
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class V4(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class V6(V4):
    address_family = socket.AF_INET6

    def server_bind(self):
        # Loopback only, and do not let this socket also claim the IPv4 port:
        # the two listeners would then race for it.
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        super().server_bind()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("directory")
    ap.add_argument("--port", type=int, default=8012)
    args = ap.parse_args()

    root = Path(args.directory)
    if not root.is_dir():
        raise SystemExit(f"Nothing to serve: {root} does not exist. Build it first.")

    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    servers = []
    for cls, addr, label in ((V6, "::1", "[::1]"), (V4, "127.0.0.1", "127.0.0.1")):
        try:
            servers.append((cls((addr, args.port), handler), label))
        except OSError as e:
            # One family missing is survivable; both is not.
            print(f"warning  could not listen on {label}:{args.port} ({e})", file=sys.stderr)
    if not servers:
        raise SystemExit(f"Could not listen on port {args.port} at all. Something else is using it.")

    for srv, label in servers[:-1]:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        print(f"serving {root} on http://{label}:{args.port}/")
    last, label = servers[-1]
    print(f"serving {root} on http://{label}:{args.port}/  (and http://localhost:{args.port}/)")
    try:
        last.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
