"""Flask application factory."""

from flask import Flask, jsonify

from hookrelay import auth, audit, control, events, legacy, subscriptions


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder="/app/static",
        static_url_path="",
    )
    app.register_blueprint(auth.bp)
    app.register_blueprint(audit.bp)
    app.register_blueprint(control.bp)
    app.register_blueprint(legacy.bp)
    app.register_blueprint(subscriptions.bp)

    @app.route("/health", methods=["GET"])
    def _health():
        return "ok"

    @app.route("/", methods=["GET"])
    def _index():
        return app.send_static_file("index.html")

    @app.errorhandler(404)
    def _not_found(error):
        return jsonify({
            "error": "Not Found",
            "service": "HookRelay",
            "message": "The requested endpoint does not exist on the HookRelay API.",
        }), 404

    events.start_background_loops()
    return app
