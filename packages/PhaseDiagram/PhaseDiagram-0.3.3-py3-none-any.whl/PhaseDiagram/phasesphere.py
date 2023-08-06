# PhaseSphere main file
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .plot import *
   
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


# Bisection method root finding
# @param f : ndarray -> ndarray, a monotonic continuous function
# @param a : ndarray, minimum corner of hypercube
# @param b : bdarray, maximum corner of hypercube
def bisect(f, a, b, max_step = 100, xtol=1e-7):

    x0 = a
    x1 = b
    assert x0.shape == x1.shape
    assert x0.ndim == 1

    f0 = f(x0)
    f1 = f(x1)

    assert np.all(f0*f1 < 0) # i.e. all intervals see a sign change

    for step in range(max_step):
        xm = (x0 + x1) /2.
        fm = f(xm)

        mask0 = np.sign(fm) == np.sign(f0)
        mask1 = np.sign(fm) == np.sign(f1)

        x0 = np.where( mask0, xm, x0 )
        x1 = np.where( mask1, xm, x1 )
        f0 = np.where( mask0, fm, f0 )
        f1 = np.where( mask1, fm, f1 )
        
        error_max = np.amax(np.abs(x1 - x0))

        if error_max < xtol : break

    return xm
        

# Newton's method root finding
# @param f : ndarray -> ndarray, a monotonic differentiable function
# @param fp : ndarray -> ndarray, its derivative
# @param x0 : ndarray, starting guess

def newton(f, fp, x0, max_step = 100, xtol=1e-7, atol=1e-7):


    x = x0

    for step in range(max_step):

        fX = f(x)

        dx = - fX / fp(x)
        x = x + dx

        if np.max(np.abs(dx)) < xtol and np.max(np.abs(fX)) < atol:
            break
    
    return x



# cursed coordinate functions for 3D map projecitons

#TODO: add guard clauses

# azimuthal (polar) projection
# God's flat earth
def azim_XY_to_xyz(X, Y):
    lens = np.sqrt(X**2 + Y**2)
    return (np.sin(lens)*X/lens, np.sin(lens)*Y/lens, np.cos(lens))

def azim_xyz_to_XY(x,y,z):
    n = (x**2 + y**2 + z**2)**-0.5
    
    rho = np.arccos(n*z)
    srho = np.sin(rho) + 1e-6
    return (n*x*rho/srho, n*y*rho/srho)

# mercator projection
def mercator_XY_to_xyz(X, Y):
    return (np.sin(-Y)*np.cos(X), np.sin(-Y)*np.sin(X), np.cos(-Y))

def mercator_xyz_to_XY(x,y,z):
    n = (x**2 + y**2 + z**2)**-0.5
    phi = np.arctan2(y,x)
    theta = -np.arccos(n*z)
    if np.isscalar(phi):
        phi = phi*np.ones_like(theta)
    if np.isscalar(theta):
        theta = theta*np.ones_like(phi)
    return (phi, theta)

# elliptical projection (not area-preserving, but close-ish)
def ell1_XY_to_xyz(X, Y):
    assert np.all((X/2)**2 + (Y)**2 <= 1)
    return (np.sqrt(1-Y**2)*np.cos(np.pi*X/2/np.sqrt(1-Y**2)),
            np.sqrt(1-Y**2)*np.sin(np.pi*X/2/np.sqrt(1-Y**2)),
            Y
            )

def ell1_xyz_to_XY(x,y,z):
    Y = z/np.sqrt(x**2 + y**2 + z**2)
    X = np.arctan2(y,x)*2 * np.sqrt(1-Y**2) / np.pi
    if np.isscalar(Y):
        Y = Y*np.ones_like(X)
    if np.isscalar(X):
        X = X*np.ones_like(Y)
    return (X,Y)


# elliptical projection (area-preserving)

def ell2_func(Y):
    return 2*(Y*np.sqrt(1-Y**2) + np.arcsin(Y))/np.pi

def ell2_XY_to_xyz(X, Y):
    assert np.all((X/2)**2 + (Y)**2 <= 1)
    fY = ell2_func(Y)
    return (np.sqrt(1-fY**2)*np.cos(np.pi*X/2*np.sqrt(1-Y**2)),
            np.sqrt(1-fY**2)*np.sin(np.pi*X/2*np.sqrt(1-Y**2)),
            fY
            )

def ell2_xyz_to_XY(x,y,z):
    z = z/np.sqrt(x**2 + y**2 + z**2)

    def f(yy):
        return ell2_func(yy) - z
    def fp(yy):
        return 4*np.sqrt(1-yy**2)/np.pi


    Y = newton(f, fp, z)

    X = 2*np.sqrt(1-Y**2)*np.arctan2(y,x)/np.pi

    if np.isscalar(Y):
        Y = Y*np.ones_like(X)
    if np.isscalar(X):
        X = X*np.ones_like(Y)
    return(X,Y)



# cylindrical projection
def cyl_XY_to_xyz(X, Y):
    n = np.sqrt(1 - Y**2)
    return (n*np.cos(X), n*np.sin(X), Y)


def cyl_xyz_to_XY(x,y,z):
    phi = np.arctan2(y,x)
    if np.isscalar(z):
        z = np.ones_like(phi)*z
    if np.isscalar(phi):
        phi = np.ones_like(z)*phi

    return (phi, z)

    
# Plots a phase diagram over a 2D projection of the unit sphere.
class PhaseSphere:
    # @param phase_func accepting three vectors x,y,z and returning an integer
    #                   phase_func(x,y,z) ---> int
    #                   These integers are used to index phase names
    # @param phase_names, a list of strings e,g, ['ferromagnet', 'antiferromagnet']
    # @param projection: either "azimuthal" or "mercator"
    def __init__(self, phase_func, phase_names, param_names, projection = 'azimuthal'):
        self.func = phase_func
        self.phase_names = phase_names
        self.param_names = param_names
        self.set_projection(projection)
        self.tri=None
        self.vals=None
        self.boundary=None
        self.num_refinements = 0
        self.figsize = (5, 5)
        
        
    # @param num_theta, num_phi: dimensions of the grid on which to evaluate the initial (coarse) grid
    def set_projection(self,projection=None, num_theta = 5, num_phi=20):
        if projection is None:
            projection = self.projection
        else:
            self.projection = projection
        
        if projection == "azimuthal":
            self.figsize = (7.5,6)
            self.initpts = genradgrid(num_theta, num_phi, max_radius=np.pi)
            self.XY_to_xyz = azim_XY_to_xyz
            self.xyz_to_XY = azim_xyz_to_XY

            # No cuts necessary
            self.const_parameterisations = [np.append(np.linspace(0,2*np.pi,250),0)]


        elif projection == "mercator":
            self.figsize=(13.5,6)
            
            phi = np.linspace(-np.pi,np.pi,num_phi)
            theta = np.linspace(0, -np.pi, num_theta)

            self.initpts= np.vstack((np.repeat(phi, num_theta), np.tile(theta, num_phi))).T

            self.XY_to_xyz = mercator_XY_to_xyz
            self.xyz_to_XY = mercator_xyz_to_XY
            
            self.const_parameterisations = [np.linspace(j*np.pi/2+1e-2,(j+1)*np.pi/2-1e-2,50) for j in range(4)]

        elif projection == "elliptical1":
            self.figsize=(13.5,6)

            self.XY_to_xyz = ell1_XY_to_xyz
            self.xyz_to_XY = ell1_xyz_to_XY

            
            XY =  genradgrid(num_theta, num_phi, max_radius=0.99)

            self.initpts= np.vstack((XY[:,0]*2, XY[:,1])).T


            self.const_parameterisations = [np.linspace(j*np.pi/2+1e-2,(j+1)*np.pi/2-1e-2,50) for j in range(4)]

        elif projection == "elliptical2":
            
            self.figsize=(13.5,6)

            self.XY_to_xyz = ell2_XY_to_xyz
            self.xyz_to_XY = ell2_xyz_to_XY

            
            XY =  genradgrid(num_theta, num_phi, max_radius=0.99)

            self.initpts= np.vstack((XY[:,0]*2, XY[:,1])).T
            
            self.const_parameterisations = [np.linspace(j*np.pi/2+1e-2,(j+1)*np.pi/2-1e-2,50) for j in range(4)]


        elif projection == "cylindrical":
            self.figsize=(13.5,6)

            X = np.linspace(-np.pi, np.pi, num_phi)
            Y = np.linspace(-1,1, num_theta)
            
            self.initpts = np.vstack((np.repeat(X, num_theta), np.tile(Y, num_phi))).T

            self.XY_to_xyz = cyl_XY_to_xyz
            self.xyz_to_XY = cyl_xyz_to_XY
 
            self.const_parameterisations = [np.linspace(j*np.pi/2+1e-2,(j+1)*np.pi/2-1e-2,50) for j in range(4)]
        else:
            print(projection)
            raise RuntimeError("No such projection is supported, try 'azimuthal', 'elliptical' or 'mercator'")
            
    # defines the initial grid
    def set_initpts(self, ntheta, nphi):
        self.set_projection(num_theta=ntheta, num_phi=nphi)
        
    # Calculates n triangular refinements of the grid.
    def refine(self, n=1):
        def pfunc(XY):
            return self.func(*self.XY_to_xyz(XY[:, 0], XY[:, 1]))
            
        if self.tri is None:
            # No triangulation, need to calculate it from initpts
            self.tri, self.vals, self.boundary = phase_optimise(self.initpts, pfunc, num_refinements=n)
            self.num_refinements = n
        else:
            #refine an existing triangulation
            for i in range(n):
                self.vals, self.boundary = d_phase_optimise(self.tri, self.vals, pfunc)
            self.num_refinements += n
        
    # Plots a contour of constant [param] = [val]. 
    # If the total extent of the contour is too small, a single oversized dot is plotted in the same colour.
    def plot_contour(self, param, val, color, linewidth = 0.3):
        if np.abs(val)>1:
            raise Exception("val must lie on the unit sphere")
            
        rho = np.sqrt(1-val**2)
        for t in self.const_parameterisations:
            V = [0,0,0]
            V[param] = val
            V[(param+1)%3] = rho*np.cos(t)
            V[(param+2)%3] = rho*np.sin(t)

                
            
            X,Y = self.xyz_to_XY(V[0], V[1], V[2])
            if np.var(X) + np.var(Y)>1e-2:
                self.ax.plot(X, Y, lw=linewidth, color=color)
            else:
                self.ax.scatter(np.mean(X), np.mean(Y), color=color)
        
    # Use this to plot the phase diagram.
    # @param cmap - what it says on the tin. Works best when it is a qualitative colormap.
    # @param show_boundary - one of:
    #                        + dict of keyword arguments for the call to plt.plot() on how to style the phase boundary
    #                        + True to show default style
    #                        + None or False to hide phase boundary plotting
    # @param show_triangulation - one of:
    #                        + dict of keyword arguments for the call to plt.plot() on how to style the traingulation
    #                        + True to show default style
    #                        + None or False to hide traingulation
    # @param contours - the lines of constant Xparam, Yparam, Zparam to show
    
    def plot(self, cmap='Pastel2', show_boundary=True, show_triangulation=None, contours = [-1+1e-6, -0.5,0,0.5,1-1e-6]):
        if self.tri is None:
            self.tri, self.vals, self.boundary = phase_optimise(self.initpts, pfunc, num_refinements=0)
            
        self.fig, self.ax = d_plot_phasedia(self.tri, self.vals, self.boundary, self.phase_names,
                                            cmap, show_boundary, show_triangulation)
        self.fig.set_size_inches(*self.figsize)

        ax = self.ax
        
        # Plot lines of constant parameters
        for d in contours:
            rho = np.sqrt(1-d**2)
            sr2 = np.sqrt(2)
            
            ax.text(*self.xyz_to_XY(d, -rho/sr2,-rho/sr2), "%s=%.1f" % (self.param_names[0], d), color='red') 
            self.plot_contour(0, d, 'red')
            
            ax.text(*self.xyz_to_XY(rho/sr2,d,rho/sr2), "%s=%.1f" % (self.param_names[1], d), color='green') 
            self.plot_contour(1, d, 'green')
            
            if self.projection in ["mercator", "cylindrical"]:
                ax.text(*self.xyz_to_XY(-rho,0,d), "%s=%.1f" % (self.param_names[2], d), color='blue') 
            else:
                ax.text(*self.xyz_to_XY(-rho/sr2,rho/sr2,d), "%s=%.1f" % (self.param_names[2], d), color='blue') 
            self.plot_contour(2, d, 'blue')

        self.ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False) 
        self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False) 

    # plots a point on the phase diagram corresponding to x,y,z
    # note that these are projected to the unit sphere
    def add_point(self, x,y,z,**kwargs):
        N = (x**2 + y**2 + z**2)**(-0.5)
        x *= N
        y *= N
        z *= N
        self.ax.plot(*self.xyz_to_XY(x,y,z),**kwargs)
        
    # plots a labeled point on the phase diagram corresponding to x,y,z
    # note that these are projected to the unit sphere
    def add_text(self, x,y,z, label, **kwargs):
        N = (x**2 + y**2 + z**2)**(-0.5)
        x *= N
        y *= N
        z *= N
        self.ax.text(*self.xyz_to_XY(x,y,z),label,**kwargs)
        
    

    
