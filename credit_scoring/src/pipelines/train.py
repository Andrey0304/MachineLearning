from src.pipelines.pipeline import define_steps, Pipeline

def run_training(data, labels, pipe_path: str):
    """The function which runs training and saves the results and the pipe."""
    steps = define_steps()
    pipe = Pipeline(steps)
    model = pipe.fit(data, labels)
    model.save(pipe_path)