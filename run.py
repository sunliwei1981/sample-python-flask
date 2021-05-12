#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author:sunliwei1981
# date:10/05/2021


from application import app
import route_map


def main():

    app.run(
            host=app.config["SERVER_HOST"],
            port=int(app.config["SERVER_PORT"]),
            debug=app.config["DEBUG"]
            )


if __name__ == '__main__':
    main()
