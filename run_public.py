import time
import threading

import ngrok
from app import app as flask_app


PORT = 5000


def start_flask():
    flask_app.run(
        host="127.0.0.1",
        port=PORT,
        debug=False,
        use_reloader=False
    )


def main():
    print("Starting Personal Finance Advisor Bot...")
    print(f"Flask will run on http://127.0.0.1:{PORT}")

    # Start Flask inside the same Python environment.
    flask_thread = threading.Thread(
        target=start_flask,
        daemon=True
    )

    flask_thread.start()

    # Give Flask a few seconds to start.
    time.sleep(3)

    try:
        # Create the public Ngrok tunnel.
        forwarder = ngrok.forward(
            f"localhost:{PORT}",
            authtoken_from_env=True
        )

        print("\n" + "=" * 60)
        print("PERSONAL FINANCE ADVISOR BOT IS LIVE")
        print("=" * 60)
        print(f"Local URL:  http://127.0.0.1:{PORT}")
        print(f"Public URL: {forwarder.url()}")
        print("=" * 60)
        print("\nKeep this PowerShell window open.")
        print("Press Ctrl+C to stop the public website.\n")

        # Keep the program running.
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping Personal Finance Advisor Bot...")

    except Exception as error:
        print("\nNgrok error:")
        print(error)

    finally:
        try:
            ngrok.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    main()