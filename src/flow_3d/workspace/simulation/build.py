import os
import pickle

class WorkspaceSimulationBuild:
    """
    Workspace class providing methods for initializing simulation folders and
    prepin files.
    """

    def simulation_build(self, name, config_file="simulation.yml", **kwargs):
        """
        Creates prepin file from simulation.yml
        """

        simulation_path = os.path.join(self.workspace_path, name)
        simulation_pkl_path = os.path.join(simulation_path, f"simulation.pkl")
        with open(simulation_pkl_path, "rb") as file:
            simulation = pickle.load(file)

        simulation.load_config(config_file, working_dir=simulation_path)

        # Creates prepin file inside simulation job folder
        simulation_prepin_filename = f"prepin.{simulation.filename}"
        simulation_prepin_path = os.path.join(simulation_path, simulation_prepin_filename)

        # Write prepin file as "prepin.simulation"
        with open(simulation_prepin_path, "w") as file:
            file.write(simulation.prepin_file_content)

        # Save simulation class object to pickle file
        simulation_pkl_path = os.path.join(simulation_path, f"{simulation.filename}.pkl")
        with open(simulation_pkl_path, "wb") as file:
            pickle.dump(simulation, file)

    def simulation_build_all(self, **kwargs):
        """
        Builds all simulations within the workspace.
        """
        for root, _, files in os.walk(self.workspace_path):
            if "simulation.pkl" in files:
                simulation_folder = os.path.basename(root)
                self.simulation_build(simulation_folder)
