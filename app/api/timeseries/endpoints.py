import os
import logging
import h5py
import numpy as np
from flask import jsonify, current_app as app
from flask_restplus import Resource, reqparse

from app.api.restplus import api
from app.utils import response as resp


ns = api.namespace("timeseries", description="Endpoint for time seies data")


parser = reqparse.RequestParser()
parser.add_argument("model_name", type=str, required=True)
parser.add_argument("start_date", type=int, required=True)
parser.add_argument("end_date", type=int, required=True)


@ns.route("/portfolio-performance/<item>")
class PortfolioPerformance(Resource):
    __available_item_list = ["return", "tvr", "cum_return"]

    def post(self, item):
        try:
            parsed = parser.parse_args()
        except:
            return resp.error("model_name, start_date, end_date must be specified")

        print parsed

        if item not in PortfolioPerformance.__available_item_list:
            return resp.error("Invalid item: {} ({})".format(item, PortfolioPerformance.__available_item_list))

        with h5py.File(os.path.join(app.root_path, "tmp/sample.h5")) as h5:
            date_list = h5["date_list"][:].tolist()
            try:
                start_index = date_list.index(parsed.start_date)
                end_index = date_list.index(parsed.end_date)
            except:
                return resp.error("Invalid date: {}, {}".format(parsed.start_date, parsed.end_date))

            date_list = date_list[start_index:end_index+1]
            print start_index, end_index
 
            if item == "return":
                value_list = h5["performance/{}/pnl".format(parsed.model_name)][0][start_index:end_index+1] / 20e6
            elif item == "tvr":
                value_list = h5["performance/{}/tvr".format(parsed.model_name)][start_index:end_index+1]
            elif item == "cum_return":
                value_list = h5["performance/{}/pnl".format(parsed.model_name)][start_index:end_index+1] / 20e6
                value_list[~np.isfinite(value_list)] = 0.0
                value_list[0] = 0.0
                value_list = np.cumsum(value_list)
            else:
                raise NotImplementedError
             
            return resp.sucess({
                "date_list": date_list,
                "value_list": value_list
            })
