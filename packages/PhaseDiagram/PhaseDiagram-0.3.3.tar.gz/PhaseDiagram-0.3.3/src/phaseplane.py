# PhaseDiagram main file
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


import numpy as np
import matplotlib.pyplot as plt
from .plot import *


class PhasePlane:
    # @param phase_func accepting three vectors x,y,z and returning an integer
    #                   phase_func(x,y,z) ---> int
    #                   These integers are used to index phase names
    # @param phase_names, a list of strings e,g, ['ferromagnet', 'antiferromagnet']
    # @param projection: either "azimuthal" or "mercator"
    def __init__(self, phase_func, phase_names, param_names):
        self.func = phase_func
        self.phase_names = phase_names
        self.param_names = param_names
        self.initpts = None
        self.tri=None
        self.vals=None
        self.boundary=None
        self.num_refinements = 0
        
    # If Y is provided, defines the initial grid bsed on the Cartesian product X, Y
    # Otherwise, directly uses X as a list of points 
    def set_initpts(self, X, Y=None):
        if Y is None:
            # assume X is a list of points
            assert len(np.asarray(X).shape) ==2
            self.initpts = X
        else:
            # assume it's a grid
            self.initpts= np.vstack((np.repeat(X, len(Y)), np.tile(Y, len(X)))).T
        
    # Calculates n triangular refinements of the grid.
    def refine(self, n=1):
        def pfunc(XY):
            return self.func(*(XY.T))
            
        if self.tri is None:
            if self.initpts is None:
                raise Exception("No initialisation points provided. Use PhasePlane.set_initpts() first")
            # No triangulation, need to calculate it from initpts
            self.tri, self.vals, self.boundary = phase_optimise(self.initpts, pfunc, num_refinements=n)
            self.num_refinements = n
        else:
            #refine an existing triangulation
            for i in range(n):
                self.vals, self.boundary = d_phase_optimise(self.tri, self.vals, pfunc)
            self.num_refinements += n
            
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
    def plot(self, cmap='Pastel2', show_boundary=True, show_triangulation=None):
        if self.tri is None:
            self.tri, self.vals, self.boundary = phase_optimise(self.initpts, pfunc, num_refinements=0)
            
        self.fig, self.ax = d_plot_phasedia(self.tri, self.vals, self.boundary, self.phase_names,
                                            cmap, show_boundary, show_triangulation)
        
        self.ax.set_xlabel(self.param_names[0])
        self.ax.set_ylabel(self.param_names[1])
    
    
    
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

        elif projection == "elliptical":
            raise NotImplementedException()
        else:
            print(projection)
            raise RuntimeError("No such projection is supported, try 'azimuthal', 'elliptical' or 'mercator'")
            
    # defines the initial grid
    def set_initpts(self, ntheta, nphi):
        self.set_projection(num_theta=ntheta, num_phi=nphi)
        
    # Calculates n triangular refinements of the grid.
    def refine(self, n=1):
        def pfunc(XY):
            return self.func(*self.XY_to_xyz(XY[0], XY[1]))
            
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
            
            if self.projection == "mercator":
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
    def add_text(self, x,y,z, label, text_kwargs={}, **kwargs):
        N = (x**2 + y**2 + z**2)**(-0.5)
        x *= N
        y *= N
        z *= N
        self.ax.text(*self.xyz_to_XY(x,y,z),label,**kwargs)
        
    

    
