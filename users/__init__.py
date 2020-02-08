from flask import Flask, make_response


def create_app():

    app = Flask(__name__)

    # simple health check
    @app.route('/ping', methods=['GET'])
    def ping():
        # TODO: implement actual health checks here
        print("/ping")  # dumb logging
        return make_response({'status': 'healthy'})

    @app.errorhandler(404)
    def not_found(error):
        """
        not_found

        Default error handling for not found resources
        """
        print(error)  # dumb logging
        return make_response({'error': 'Not Found'}, 404)

    return app
