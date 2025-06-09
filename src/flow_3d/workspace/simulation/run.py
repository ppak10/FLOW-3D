import os
import pickle
import time
import re
import wandb

from concurrent.futures import ProcessPoolExecutor
from huggingface_hub import upload_folder
from tqdm import tqdm

class WorkspaceSimulationRun:
    """
    Workspace class providing methods to run (runhyd) simulation(s).
    """

    def simulation_run(
            self,
            name,
            postprocess = True,
            visualize = True,
            upload = False,
            num_proc = 1,
            use_wandb = False,
            **kwargs
        ):
        """
        Method to run one or a list simulations within a workspace folder.
        """
        simulation_folder = os.path.join(self.workspace_path, name)

        # Initialize WandB
        if use_wandb:
            wandb.login()

            wandb.init(
                project = self.wandb_project,
                config = {
                    "workspace": self.filename,
                    # "simulations": [s.name for s in self.simulations]
                }
            )

        s_dir_path = os.path.join(self.workspace_path, simulation_folder)
        s_pkl_path = os.path.join(s_dir_path, f"simulation.pkl")
        with open(s_pkl_path, "rb") as file:
            s = pickle.load(file)
            
        # Run simulation
        status = s.runhyd(working_dir = s_dir_path)

        if status == "success":
            if postprocess:
                self.simulation_postprocess(name, num_proc=num_proc, delete_output=False)
                if visualize:
                    self.simulation_visualize(name, num_proc=num_proc)
                if upload:
                    self.simulation_generate_dataset(name)
                    self.simulation_upload_dataset(name)
        
        return status

    def simulation_run_all(
            self,
            postprocess = True,
            visualize = True,
            upload = False,
            num_proc=1,
            use_wandb = False,
            **kwargs
        ):
        """
        Runs all simulation within workspace folder sequentially,
        but handles postprocessing, visualization, and upload asynchronously.
        """
        with ProcessPoolExecutor() as executor:
            futures = []
            for root, _, files in tqdm(sorted(os.walk(self.workspace_path))):
                if "simulation.pkl" in files:
                    simulation_name = os.path.basename(root)

                    # Run simulation synchronously to respect licensed cores.
                    status = self.simulation_run(
                        simulation_name,
                        postprocess=False,
                        use_wandb=use_wandb,
                        **kwargs
                    )

                    if status == "success":
                        if postprocess:
                            # Queue postprocessing in background
                            futures.append(
                                executor.submit(
                                    self.simulation_run_post,
                                    simulation_name,
                                    visualize,
                                    upload,
                                    num_proc,
                                )
                            )

            # Optional: Wait for all background jobs to complete
            for future in futures:
                future.result()  # You could also catch exceptions here
    
    def simulation_run_post(self, name, visualize = True, upload = False, num_proc=1, **kwargs):
        """
        Initializes simulation class and runs post processing steps
        """
        print(f"Starting post processing for {name}...")
        simulation_folder = os.path.join(self.workspace_path, name)

        s_dir_path = os.path.join(self.workspace_path, simulation_folder)
        s_pkl_path = os.path.join(s_dir_path, f"simulation.pkl")
        with open(s_pkl_path, "rb") as file:
            simulation = pickle.load(file)

        simulation.guipost(working_dir = simulation_folder)
        simulation.chunk_flslnk(working_dir = simulation_folder)
        simulation.flslnk_chunk_to_npz(working_dir = simulation_folder)
        if visualize:
            simulation.prepare_views(working_dir = simulation_folder)
            simulation.generate_views(
                working_dir = simulation_folder,
                num_proc = num_proc
            )

            simulation.prepare_view_visualizations(working_dir = simulation_folder)
            simulation.generate_views_visualizations(
                working_dir = simulation_folder,
                num_proc = num_proc
            )
        if upload:
            simulation.create_flslnk_dataset(working_dir = simulation_folder, **kwargs)
            dataset_id = simulation.filename
            response = simulation.upload_flslnk_dataset(
                dataset_id,
                working_dir = simulation_folder,
                **kwargs
            )

            # Use regex to extract the dataset path
            match = re.search(r'datasets/([^/]+/[^/]+)', response)
            if match:
                repo_id = match.group(1)
                print(f"Uploading source files to repo with id: {repo_id}")
            else:
                print("Dataset path not found.")

            path_in_repo = os.path.join('source', simulation.name)
            upload_folder(
                repo_id = repo_id,
                folder_path = simulation_folder,
                path_in_repo = path_in_repo,
                repo_type = "dataset"
            )

    # def simulations_run_all(self, use_wandb = False, **kwargs):
    #     """
    #     Method to run all simulations within a workspace folder.
    #     """

    #     # # Define Job path and check that it exists
    #     # job_dir_path = os.path.join(self.output_dir, job_name)
    #     # if not os.path.isdir(job_dir_path):
    #     #     raise Exception(f"Folder `{job_name}` not found at `{job_dir_path}`")

    #     # Only consider directories and skip over possible files.
    #     simulation_folders = sorted([s.name for s in Path(self.workspace_path).iterdir() if s.is_dir()])
    #     print(f"Simulation Folders ({len(simulation_folders)}): {simulation_folders}")

    #     # Initialize WandB
    #     if use_wandb:
    #         wandb.login()

    #         wandb.init(
    #             project = self.wandb_project,
    #             config = {
    #                 "workspace": self.filename,
    #                 # "simulations": [s.name for s in self.simulations]
    #             }
    #         )

    #     # Run simulations
    #     for simulation_folder in tqdm(simulation_folders):
    #         # Load simulation object 
    #         s_dir_path = os.path.join(self.workspace_path, simulation_folder)
    #         s_pkl_path = os.path.join(s_dir_path, f"simulation.pkl")
    #         # s_pkl_path = os.path.join(s_dir_path, f"{simulation_filename}.pkl")
    #         with open(s_pkl_path, "rb") as file:
    #             s = pickle.load(file)
            
    #         # Run simulation
    #         s.runhyd(working_dir = s_dir_path)

    #         # TODO: Implement better logging here.
    #         if use_wandb:
    #             wandb.log({
    #                 "name": s.name,
    #                 "time": time.time()
    #             })

    #     if use_wandb:
    #         wandb.finish()