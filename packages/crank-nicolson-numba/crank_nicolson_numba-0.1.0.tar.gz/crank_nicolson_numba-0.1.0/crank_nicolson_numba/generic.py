import numpy as np
import scipy as sc
from tqdm import tqdm
import scipy.integrate as integrate
import scipy.interpolate as interpolate

from .core import crank_nicolson

# Useful functions for... our situation


def action(x, p):
    """Returns action variable
    
    Parameters
    ----------
    x : ndarray
        position
    p : ndarray
        momentum
    
    Returns
    -------
    ndarray
        action
    """
    return ((p * p) + (x * x)) * 0.5


def normed_normal_distribution(I, mean_I, sigma_I):
    """Given an I value, returns the corresponding value for a normal distribution.
    
    Parameters
    ----------
    I : ndarray
        sample points
    mean_I : float
        mean of the distribution
    sigma_I : float
        sigme of the distribution
    
    Returns
    -------
    ndarray
        results of the samples
    """
    return ((1 / np.sqrt(2 * np.pi * sigma_I ** 2))
            * np.exp(-(I - mean_I) ** 2 / (2 * sigma_I ** 2)))


def normed_normal_linspace(I_min, I_max, mean_I, sigma_I, num=100):
    """Returns a normalized linspace of a normal distribution.
    
    Parameters
    ----------
    I_min : float
        starting point
    I_max : float
        stopping point
    mean_I : float
        mean of the distribution
    sigma_I : float
        sigma of the distribution
    num : int, optional
        number of samples, by default 100
    
    Returns
    -------
    ndarray
        linspace distribution
    """
    I_list = np.linspace(I_min, I_max, num)
    values = np.empty((num))
    for i, I in enumerate(I_list):
        values[i] = normed_normal_distribution(I, mean_I, sigma_I)
    normalization = integrate.simps(values, I_list)
    values /= normalization
    return values


def x_from_I_th(I, th=np.pi / 2):
    """Returns x from action-angle variables.
    
    Parameters
    ----------
    I : float
        action value
    th : float, optional
        angle value, by default np.pi/2
    
    Returns
    -------
    float
        x value
    """
    return np.sqrt(2 * I) * np.sin(th)


def p_from_I_th(I, th=0.0):
    """Returns p from action-angle variables.
    
    Parameters
    ----------
    I : float
        action value
    th : float, optional
        angle value, by default 0.0
    
    Returns
    -------
    float
        p value
    """
    return np.sqrt(2 * I) * np.cos(th)


def D_calculator(I, epsilon, x_star, delta, exponent):
    """Estimates D value by using definitions given for stochastic map.
    
    Parameters
    ----------
    I : float
        sampling point
    epsilon : float
        noise coefficient
    x_star : float
        nek parameter
    delta : float
        nek parameter
    exponent : float
        nek parameter (alpha)
    
    Returns
    -------
    float
        diffusion value
    """
    if I <= 0:
        return 0.0
    int_result = integrate.quad(
        (lambda th:
         epsilon ** 2
            * (2 * I)
            * np.cos(th) ** 2
            * np.exp(-np.power(((x_star) / (delta + np.absolute(x_from_I_th(I, th)))), exponent)) ** 2),
        0,
        np.pi / 2)
    # Check if int_result is valid, otherwise return 0.0
    #print(int_result[0], int_result[1],(int_result[1] / int_result[0] if int_result[0] != 0.0 else 0.0))
    return (int_result[0] / (np.pi / 2)
            if np.absolute(int_result[1] / int_result[0] if int_result[0] != 0.0 else 1.0) < 0.05 else 0.0)


def I_norm_sampling_to_x(mean_I, sigma_I):
    """Extracts a random action value from a normal distribution and returns a corrispective x value (assumes p=0).
    
    Parameters
    ----------
    mean_I : float
        mean of the distribution
    sigma_I : float
        sigma of the distribution
    
    Returns
    -------
    float
        extracted x
    """
    counter = 0
    while True:
        extracted_I = np.random.normal(mean_I, sigma_I)
        if extracted_I >= 0:
            break
        counter += 1
        assert counter < 100
    return x_from_I_th(extracted_I)


# The actual class to be used

class cn_generic(object):
    """wrapper for generic diffusive process"""

    def __init__(self, I_min, I_max, I0, dt, D_lambda, normalize=False):
        """init the wrapper
        
        Parameters
        ----------
        object : self
            self
        I_min : float
            starting point
        I_max : float
            absorbing point
        I0 : ndarray
            initial distribution
        dt : float
            time delta
        D_lambda : lambda
            lambda that takes an action value and returns the diffusion value
        normalize : bool, optional
            do you want to normalize the initial distribution? by default True
        """
        self.I_min = I_min
        self.I_max = I_max
        self.I0 = I0
        self.dt = dt
        self.D_lambda = D_lambda

        self.I, self.dI = np.linspace(I_min, I_max, I0.size, retstep=True, endpoint=False)
        self.samples = I0.size
        self.half_dI = self.dI * 0.5

        self.A = []
        for i in self.I:
            self.A.append(self.D_lambda(i - self.half_dI)) if (i -
                                                               self.half_dI > 0) else self.A.append(0.0)
            self.A.append(self.D_lambda(i + self.half_dI))
        self.A = np.array(self.A)
        self.B = np.zeros(self.samples)
        self.C = np.zeros(self.samples)
        self.D = np.zeros(self.samples + 2)

        self.locked_left = False
        self.locked_right = False

        # For Reference:
        self.diffusion = np.array([self.D_lambda(i) for i in self.I])

        # Normalize?
        if normalize:
            self.I0 /= integrate.trapz(self.I0, x=self.I)

        self.engine = crank_nicolson(
            self.samples, I_min, I_max, self.dt, self.I0.copy(), self.A, self.B, self.C, self.D)

    def rescale_time(self, scale):
        self.dt *= scale
        I = self.get_data()
        self.engine = crank_nicolson(
            self.samples, self.I_min, self.I_max, self.dt, I.copy(), self.A, self.B, self.C, self.D)
        if self.locked_left:
            self.lock_left()
        if self.locked_right:
            self.lock_right()

    def move_barrier_forward(self, movement, resample=False):
        assert movement > 0
    
        actual_rho = self.get_data()
        executed_iterations = self.engine.executed_iterations

        if resample:
            new_imax = self.I_max + movement
            f = interpolate.interp1d(self.I, actual_rho, kind="cubic")
            new_i, new_di = np.linspace(self.I_min, new_imax, self.samples, retstep=True, endpoint=False)
            new_i0 = np.array([
                f(x) if x <= self.I[-1] else 0.0 for x in new_i
            ])

            self.I0 = new_i0
            self.I = new_i
            self.dI = new_di
            self.half_dI = self.dI * 0.5
            self.I_max = new_imax

        else:
            movement += self.dI
            plug = np.arange(self.I_max, self.I_max + movement, self.dI)[1:]
            self.I0 = np.concatenate((actual_rho, np.zeros(len(plug))))
            self.I = np.concatenate((self.I, plug))
            self.I_max = self.I[-1]            
            self.samples = self.I0.size

        self.A = []
        for i in self.I:
            self.A.append(
                self.D_lambda(i - self.half_dI) 
                    if (i - self.half_dI > 0) 
                        else 0.0)
            self.A.append(self.D_lambda(i + self.half_dI))
        self.A = np.array(self.A)
        self.B = np.zeros(self.samples)
        self.C = np.zeros(self.samples)
        self.D = np.zeros(self.samples + 2)

        # For Reference:
        self.diffusion = np.array([self.D_lambda(i) for i in self.I])

        self.engine = crank_nicolson(
            self.samples, self.I_min, self.I_max, self.dt, self.I0.copy(), self.A, self.B, self.C, self.D)
        self.engine.set_executed_iterations(executed_iterations)
        if self.locked_left:
            self.lock_left()
        if self.locked_right:
            self.lock_right()

    def move_barrier_backward(self, movement, resample=False):
        assert movement > 0

        actual_rho = self.get_data()
        dist_before_movement = self.get_sum()
        executed_iterations = self.engine.executed_iterations
        
        if resample:
            new_imax = self.I_max - movement
            new_i, new_di = np.linspace(self.I_min, new_imax, self.samples, retstep=True, endpoint=False)
            f = interpolate.interp1d(self.I, actual_rho, kind="cubic")
            new_i0 = np.array([
                f(x) for x in new_i
            ]) / (1 + np.exp((new_i - (new_imax - new_di * 3)) / (new_di * 2)))
            self.I0 = new_i0
            self.I = new_i
            self.dI = new_di
            self.half_dI = self.dI * 0.5
            self.I_max = new_imax
        else:
            index = np.argmin(self.I <= self.I_max - movement)
            assert index > 1

            self.I = self.I[:index]
            self.I_max = self.I[-1]
            self.samples = self.I.size

            self.I0 = actual_rho[:index]
            self.I0 *= 1/(1 + np.exp((self.I - (self.I_max - self.dI * 3))/ (self.dI * 2)))

        self.A = []
        for i in self.I:
            self.A.append(self.D_lambda(i - self.half_dI)) if (i -
                                                          self.half_dI > 0) else self.A.append(0.0)
            self.A.append(self.D_lambda(i + self.half_dI))
        self.A = np.array(self.A)
        self.B = np.zeros(self.samples)
        self.C = np.zeros(self.samples)
        self.D = np.zeros(self.samples + 2)

        # For Reference:
        self.diffusion = np.array([self.D_lambda(i) for i in self.I])
        self.engine = crank_nicolson(
            self.samples, self.I_min, self.I_max, self.dt, self.I0.copy(), self.A, self.B, self.C, self.D)

        self.engine.set_executed_iterations(executed_iterations)
        if self.locked_left:
            self.lock_left()
        if self.locked_right:
            self.lock_right()
        dist_after_movement = self.get_sum()

        return dist_after_movement - dist_before_movement

    def set_source(self, source):
        """Apply a source vector to the simulation, this will overwrite all non zero values over the simulation distribution at each iteration.
        
        Parameters
        ----------
        source : ndarray
            source to apply
        """
        self.engine.set_source(source)

    def remove_source(self):
        """Remove the source vector to the simulation.
        """
        self.engine.remove_source()

    def lock_left(self):
        """Lock the left boundary to the non-zero value it has right now.
        """
        self.engine.set_lock_left()
        self.locked_left = True

    def lock_right(self):
        """Lock the right boundary to the non-zero value it has right now.
        """
        self.engine.set_lock_right()
        self.locked_right = True

    def unlock_left(self):
        """Unlock the left boundary and set it to zero.
        """
        self.engine.unlock_left()
        self.locked_left = False

    def unlock_right(self):
        """Unlock the right boundary and set it to zero.
        """
        self.engine.unlock_right()
        self.locked_right = False

    def iterate(self, n_iterations):
        """Iterates the simulation.
        
        Parameters
        ----------
        n_iterations : int
            number of iterations to perform
        """
        self.engine.iterate(n_iterations)

    def reset(self):
        """Resets the simulation to the starting condition.
        """
        self.engine.reset()

    def get_sanity(self):
        """Get sanity check flag
        
        Returns
        -------
        boolean
            sanity check flag
        """
        return self.engine.sanity_flag

    def get_data(self):
        """Get raw distribution data.
        
        Returns
        -------
        numpy 1D array
            raw distribution data
        """
        return np.array(self.engine.x)

    def get_data_with_x(self):
        """Get raw distribution data and corrispective I_linspace
        
        Returns
        -------
        (numpy 1D array, numpy 1D array)
            (I_linspace, distribution data)
        """
        return (self.I, np.array(self.engine.x))

    def get_sum(self):
        """Get integral of the distribution (i.e. number of particles)
        
        Returns
        -------
        float
            Number of particles
        """
        return integrate.trapz(self.engine.x, x=self.I)

    def get_particle_loss(self):
        """Get amount of particle loss (when compared to starting condition)
        
        Returns
        -------
        float
            Particle loss quota
        """
        return -(
            integrate.trapz(self.get_data(), x=self.I) -
            integrate.trapz(self.I0, x=self.I)
        )

    def current(self, samples=5000, it_per_sample=20, disable_tqdm=True):
        """Perform automatic iteration of the simulation 
        and compute resulting current.
        
        Parameters
        ----------
        samples : int, optional
            number of current samples, by default 5000
        it_per_sample : int, optional
            number of sim. iterations per current sample, by default 20
        
        Returns
        -------
        (numpy 1D array, numpy 1D array)
            (times of the samples, current values for those samples)
        """
        current_array = np.empty(samples)
        temp1 = self.get_sum()
        times = (np.arange(samples) * it_per_sample +
                 self.engine.executed_iterations) * self.dt
        for i in tqdm(range(samples), disable=disable_tqdm):
            self.engine.iterate(it_per_sample)
            temp2 = self.get_sum()
            current_array[i] = (temp1 - temp2) / (self.dt * it_per_sample)
            temp1 = temp2
        return times, current_array

    def analytical_sample(self):
        first_derivative = (- self.engine.x[-1]) / (self.dI * 1)
        return first_derivative

    def analytical_current(self, samples=5000, it_per_sample=20, disable_tqdm=True, the_diffusion_is_halved=True):
        """Perform automatic iteration of the simulation 
        and compute resulting current via analytical formula.
        
        Parameters
        ----------
        samples : int, optional
            number of current samples, by default 5000
        it_per_sample : int, optional
            number of sim. iterations per current sample, by default 20
        
        Returns
        -------
        (numpy 1D array, numpy 1D array)
            (times of the samples, current values for those samples)
        """
        current_array = np.empty(samples)
        times = (np.arange(samples) * it_per_sample +
                 self.engine.executed_iterations) * self.dt
        for i in tqdm(range(samples), disable=disable_tqdm):
            self.engine.iterate(it_per_sample)
            current_array[i] = self.analytical_sample()
        return times, - current_array * self.D_lambda(self.I_max) * (2 if the_diffusion_is_halved else 1)

    def double_kind_current(self, samples=5000, it_per_sample=20, disable_tqdm=True, the_diffusion_is_halved=True):
        """Perform automatic iteration of the simulation 
        and compute resulting current via the two formulas we have.
        
        Parameters
        ----------
        samples : int, optional
            number of current samples, by default 5000
        it_per_sample : int, optional
            number of sim. iterations per current sample, by default 20
        
        Returns
        -------
        (numpy 1D array, numpy 1D array, numpy 1D array)
            (times of the samples, current, current_analytic)
        """
        current_array = np.empty(samples)
        current_array_ana = np.empty(samples)
        temp1 = self.get_sum()
        times = (np.arange(samples) * it_per_sample +
                 self.engine.executed_iterations) * self.dt
        for i in tqdm(range(samples), disable=disable_tqdm):
            self.engine.iterate(it_per_sample)

            temp2 = self.get_sum()
            current_array[i] = (temp1 - temp2) / (self.dt * it_per_sample)
            temp1 = temp2

            current_array_ana[i] = self.analytical_sample()
        return times, current_array, - current_array_ana * self.D_lambda(self.I_max) * (2 if the_diffusion_is_halved else 1)
