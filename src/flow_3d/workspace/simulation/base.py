import os
import pickle
import shutil
import yaml

from flow_3d import data
from flow_3d.simulation import Simulation

from importlib.resources import files

class WorkspaceSimulationBase:
    """
    Workspace class providing methods for initializing simulation folders.
    """

    def simulation_initialize(self, name, config=None, **kwargs):
        """
        Create prepin file within simulation folder for a specified workspace
        """

        simulation = Simulation(name=name, **kwargs)

        # Create simulation folder within workspace path 
        simulation_path = os.path.join(self.workspace_path, simulation.name)
        if not os.path.isdir(simulation_path):
            os.makedirs(simulation_path)

        if config is None:
            # Copy over default `simulation.yml` file
            config_file = "default.yml"
            if name == "test":
                config_file = "test.yml"

            config_resource_file_path = os.path.join("simulation", "config", config_file)
            config_resource = files(data).joinpath(config_resource_file_path)

            config_file_path = os.path.join(simulation_path, "simulation.yml")
            with config_resource.open("rb") as src, open (config_file_path, "wb") as file:
                shutil.copyfileobj(src, file)
        else:
            # Generates `simulation.yml` from passed in config json object.
            config_file_path = os.path.join(simulation_path, "simulation.yml")
            with open(config_file_path, "w") as f:
                yaml.dump(config, f, sort_keys=False)

        # Save simulation class object to pickle file
        simulation_pkl_path = os.path.join(simulation_path, f"{simulation.filename}.pkl")
        with open(simulation_pkl_path, "wb") as file:
            pickle.dump(simulation, file)

        return simulation

    # Alias
    simulation_init = simulation_initialize
