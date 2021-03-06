import numpy
from . import Algorithm


class GridAlgorithm(Algorithm):
    """
    The basic "algorithm" in which fixed points on a multi-dimensional grid
    over the parameter bounds are evaluated and the minimum value returned
    """

    BAD_FITNESS_VALUE = float('nan')

    def __init__(self, num_steps):
        self.num_steps = num_steps

    def set_tune_parameters(self, tune_parameters):
        super(GridAlgorithm, self).set_tune_parameters(tune_parameters)
        if not isinstance(self.num_steps, int):
            if len(self.num_steps) != self.num_dims:
                raise Exception("Number of tuneable parameters ({}) does not "
                                "match number num_steps provided to "
                                "GridAlgorithm constructor ({})"
                                .format(len(self.num_steps) != self.num_dims))

    @property
    def num_dims(self):
        try:
            return len(self.constraints)
        except AttributeError:
            raise Exception("Tuneable parameters have not been set for grid "
                            "algorithm so it doesn't have a dimension")

    def optimize(self, evaluator, **kwargs):  # @UnusedVariable
        # Convert number of steps into a list with a step number for each
        # dimension if it is not already
        if isinstance(self.num_steps, int):
            num_steps = numpy.empty(self.num_dims, dtype=int)
            num_steps.fill(self.num_steps)
        else:
            if len(self.num_steps) > self.num_dims:
                raise Exception("Length of the number of steps ({}) list does "
                                "not match the number of dimensions ({}) "
                                "provided "
                                .format(len(self.num_steps), self.num_dims))
            num_steps = numpy.asarray(self.num_steps, dtype=int)
        # Get the ranges of the parameters using the number of steps
        param_ranges = [numpy.linspace(l, u, n)
                        for (l, u), n in zip(self.constraints, num_steps)]
        if self.num_dims == 1:
            candidates = numpy.asarray(zip(*param_ranges))
        else:
            # Get all permutations of candidates given parameter ranges
            meshes = numpy.meshgrid(*param_ranges)
            cand_mesh = numpy.concatenate([mesh.reshape([1] + list(mesh.shape))
                                           for mesh in meshes])
            candidates = cand_mesh.reshape((self.num_dims, -1)).T
        # Evaluate fitnesses
        fitnesses = numpy.array(evaluator(candidates))
        # Check to see if multi-objective
        if fitnesses.ndim == 2:
            # Get fittest candidates for each objective
            fittest_candidate = [candidates[f.argmin(), :]
                                 for f in fitnesses.T]
            fitness_grid = numpy.reshape(fitnesses.T,
                                         [fitnesses.shape[1]] +
                                         list(num_steps))
            fittest_fitness = [f.min() for f in fitnesses.T]
        else:
            # Get fittest candidate
            fittest_fitness_i = fitnesses.argmin()
            fittest_candidate = candidates[fittest_fitness_i, :]
            fittest_fitness = fitnesses[fittest_fitness_i]
            fitness_grid = numpy.reshape(fitnesses, num_steps)
        # return fittest candidate, its fitness and grid of fitnesses (for
        # plotting potentially)
        return fittest_candidate, fittest_fitness, fitness_grid
