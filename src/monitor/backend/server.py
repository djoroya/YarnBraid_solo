# server python flask app

from flask import Flask, request, jsonify
from settings.simulations import simulations
from tools.basic.loadsavejson import loadjson_plain
# cors
from tools.step.deletesim import delete_sim_key
from flask_cors import CORS

import glob,os
join = os.path.join
simulations_path = simulations()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Monitor API!'})

@app.route('/simulations', methods=['GET'])
def simulations():
    simulations_key = glob.glob(join(simulations_path,'*', 'init.json'))
    
    simulations_key = [loadjson_plain(i) for i in simulations_key]
    for i in simulations_key:
        i["simulation_path_abs"] = join(simulations_path,i["simulation_path"])
    return jsonify(simulations_key)

@app.route('/simulations/<simulation_path>', methods=['DELETE'])
def delete_simulation(simulation_path):
    
    delete_sim_key(simulation_path)
    return jsonify({'message': 'Simulation deleted'})

if __name__ == '__main__':
    app.run(debug=True)