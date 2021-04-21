#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 17:56:47 2021

@author: frederic

# =============================================================================
#                                  CHANGELOG:
#   - Fixed Mine class, input arrays will be formatted as (x,z) for 2D and 
#     (x,y,z) for 3D. - Ethan
#   - States are now correctly working, e.g. doing state(action) will now find
#     the correct location in the mine. - Ethan
#   - Added variable self.three_dim, set to True if mine is 3D - Ethan
#   - Implemented Is_Dangerous function, seems to be working correctly - Ethan
#   - changed code in init from 0 to -2 for x_len as in 3d mind x is the second index and -2 for 2d mine will index first variable - Connor
# 
# 
# 
# 
# 
# =============================================================================

class problem with     

An open-pit mine is a grid represented with a 2D or 3D numpy array. 

The first coordinates are surface locations.

In the 2D case, the coordinates are (x,z).
In the 3D case, the coordinates are (x,y,z).
The last coordinate 'z' points down.

    
A state indicates for each surface location  how many cells 
have been dug in this pit column.

For a 3D mine, a surface location is represented with a tuple (x,y).

For a 2D mine, a surface location is represented with a tuple (x,).


Two surface cells are neighbours if they share a common border point.
That is, for a 3D mine, a surface cell has 8 surface neighbours.


An action is represented by the surface location where the dig takes place.


"""
import numpy as np
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

#Test

import itertools

import functools # @lru_cache(maxsize=32)

from numbers import Number

import search

def my_team():    

     '''    Return the list of the team members of this assignment submission 
     as a list of triplet of the form (student_number, first_name, last_name)        ''' 

     return [ (10467858, 'Ethan', 'Griffiths'), (10467874, 'Matti', 'Winsen'), (1234567, 'Connor', 'Browne') ]   
    
def convert_to_tuple(a):
    '''
    Convert the parameter 'a' into a nested tuple of the same shape as 'a'.
    
    The parameter 'a' must be array-like. That is, its elements are indexed.

    Parameters
    ----------
    a : flat array or an array of arrays

    Returns
    -------
    the conversion of 'a' into a tuple or a tuple of tuples

    '''
    if isinstance(a, Number):
        return a
    if len(a)==0:
        return ()
    # 'a' is non empty tuple
    if isinstance(a[0], Number):
        # 'a' is a flat list
        return tuple(a)
    else:
        # 'a' must be a nested list with 2 levels (a matrix)
        return tuple(tuple(r) for r in a)
    
    
def convert_to_list(a):
    '''
    Convert the array-like parameter 'a' into a nested list of the same 
    shape as 'a'.

    Parameters
    ----------
    a : flat array or array of arrays

    Returns
    -------
    the conversion of 'a' into a list or a list of lists

    '''
    if isinstance(a, Number):
        return a
    if len(a)==0:
        return []
    # 'a' is non empty tuple
    if isinstance(a[0], Number):
        # 'a' is a flat list
        return list(a)
    else:
        # 'a' must be a nested list with 2 levels (a matrix)
        return [list(r) for r in a]    




class Mine(search.Problem):
    '''
    
    Mine represent an open mine problem defined by a grid of cells 
    of various values. The grid is called 'underground'. It can be
    a 2D or 3D array.
    
    The z direction is pointing down, the x and y directions are surface
    directions.
    
    An instance of a Mine is characterized by 
    - self.underground : the ndarray that contains the values of the grid cells
    - self.dig_tolerance : the maximum depth difference allowed between 
                           adjacent columns 
    
    Other attributes:
        self.len_x, self.len_y, self.len_z : int : underground.shape
        self.cumsum_mine : float array : cumulative sums of the columns of the 
                                         mine
    
    A state has the same dimension as the surface of the mine.
    If the mine is 2D, the state is 1D.
    If the mine is 3D, the state is 2D.
    
    state[loc] is zero if digging has not started at location loc.
    More generally, state[loc] is the z-index of the first cell that has
    not been dug in column loc. This number is also the number of cells that
    have been dugged in the column.
    
    States must be tuple-based.
    
    '''    
    
    def __init__(self, underground, dig_tolerance = 1):
        '''
        Constructor
        
        Initialize the attributes
        self.underground, self.dig_tolerance, self.len_x, self.len_y, self.len_z,
        self.cumsum_mine, and self.initial
        
        The state self.initial is a filled with zeros.

        Parameters
        ----------
        underground : np.array
            2D or 3D. Each element of the array contains 
            the profit value of the corresponding cell.
        dig_tolerance : int
             Mine attribute (see class header comment)
        Returns
        -------
        None.

        '''
        # super().__init__() # call to parent class constructor not needed
        
        self.underground = underground 
        # self.underground  should be considered as a 'read-only' variable!
        self.dig_tolerance = dig_tolerance
        assert underground.ndim in (2,3)
        
        ####################### Inserting code here! #######################    
        
        # Determine if mine is 3D or not
        if self.underground.ndim == 3:
            self.three_dim = True
        else:
            self.three_dim = False
        
        self.len_z = self.underground.shape[-1] # -1 axis is always z
        self.len_x = self.underground.shape[-2] #change# -2 is first for 2d and 2nd for 3d, 3d indexing is (y,x,z) idk y
        
        # 3D mine case
        if self.three_dim:
            self.len_y = self.underground.shape[0]
            self.initial = np.zeros((self.len_x,self.len_y), dtype=int)
        # 2D mine case            
        else:
            self.len_y = 0            
            self.initial = np.zeros(self.len_x, dtype=int)        
            
        self.cumsum_mine = np.cumsum(self.underground, dtype=float, axis=-1)         
                       
        ##### Old code, just in case #####
        # # 2D mine
        # if self.undergound.ndim == 2:
        #     self.len_x = self.underground.shape[0]
        #     self.len_y = 0;
        #     self.len_z = self.underground.shape[1]    
        #     self.cumsum_mine = np.cumsum(self.underground, dtype=float, axis=1) 
        # # 3D mine
        # else:
        #     self.cumsum_mine = np.cumsum(self.underground, dtype=float, axis=2) 
        #     self.len_x = self.underground.shape[1]
        #     self.len_y = self.underground.shape[0]  
        #     self.len_z = self.underground.shape[2]
        ##### Old code #####
        
        ####################### Inserting code here! #######################
        
    def surface_neigbhours(self, loc):
        '''
        Return the list of neighbours of loc

        Parameters
        ----------
        loc : surface coordinates of a cell.
            a singleton (x,) in case of a 2D mine
            a pair (x,y) in case of a 3D mine

        Returns
        -------
        A list of tuples representing the surface coordinates of the
        neighbouring surface cells.

        '''
        L=[]
        assert len(loc) in (1,2)
        if len(loc)==1:
            if loc[0]-1>=0:
                L.append((loc[0]-1,))
            if loc[0]+1<self.len_x:
                L.append((loc[0]+1,))
        else:
            # len(loc) == 2
            for dx,dy in ((-1,-1),(-1,0),(-1,+1),
                          (0,-1),(0,+1),
                          (+1,-1),(+1,0),(+1,+1)):
                if  (0 <= loc[0]+dx < self.len_x) and (0 <= loc[1]+dy < self.len_y):
                    L.append((loc[0]+dx, loc[1]+dy))
        return L
     
    
    def actions(self, state):
        '''
        Return a generator of valid actions in the given state 'state'
        An action is represented as a location. An action is deemed valid if
        it doesn't break the dig_tolerance constraint.

        Parameters
        ----------
        state : 
            represented with nested lists, tuples or a ndarray
            state of the partially dug mine

        Returns
        -------
        a generator of valid actions

        '''        
        state = np.array(state)

        ####################### Inserting code here! #######################
        
        
        
        
        
        
        ####################### Inserting code here! #######################
        
                  
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must a valid actions.
        That is, one of those generated by  self.actions(state)."""
        action = tuple(action)
        new_state = np.array(state) # Make a copy
        new_state[action] += 1
        return convert_to_tuple(new_state)
                
    
    def console_display(self):
        '''
        Display the mine on the console

        Returns
        -------
        None.

        '''
        print('Mine of depth {}'.format(self.len_z))
        if self.underground.ndim == 2:
            # 2D mine
            print('Plane x,z view')
        else:
            # 3D mine
            print('Level by level x,y slices')
        #
        print(self.__str__())
        
    def __str__(self):
        if self.underground.ndim == 2:
            # 2D mine
            return str(self.underground.T)
        else:
            # 3D mine
            # level by level representation
            return '\n'.join('level {}\n'.format(z)
                   +str(self.underground[...,z]) for z in range(self.len_z))
                    
                        
                
            return self.underground[loc[0], loc[1],:]
    
    @staticmethod   
    def plot_state(state):
        if state.ndim==1:
            fig, ax = plt.subplots()
            ax.bar(np.arange(state.shape[0]) ,
                    state
                    )
            ax.set_xlabel('x')
            ax.set_ylabel('z')
        else:
            assert state.ndim==2
            # bar3d(x, y, z, dx, dy, dz,
            # fake data
            _x = np.arange(state.shape[0])
            _y = np.arange(state.shape[1])
            _yy, _xx = np.meshgrid(_y, _x) # cols, rows
            x, y = _xx.ravel(), _yy.ravel()            
            top = state.ravel()
            bottom = np.zeros_like(top)
            width = depth = 1
            fig = plt.figure(figsize=(3,3))
            ax1 = fig.add_subplot(111,projection='3d')
            ax1.bar3d(x, y, bottom, width, depth, top, shade=True)
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ax1.set_zlabel('z')
            ax1.set_title('State')
        #
        plt.show()

    def payoff(self, state):
        '''
        Compute and return the payoff for the given state.
        That is, the sum of the values of all the digged cells.
        
        No loops needed in the implementation!        
        '''
        # convert to np.array in order to use tuple addressing
        # state[loc]   where loc is a tuple
        state = np.array(state)

        ####################### Inserting code here! #######################
        #will fix comments for submission these r just to explain it to you guys

        x_Locs = np.arange(self.len_x)  # array of indexes for all X columns
        z_Locs = state - 1  # dug level -1 as indexes would be a level too deep

        # 3D case
        if self.three_dim:
            y_Locs = np.arange(self.len_y)
            res_arr = self.cumsum_mine[y_Locs, x_Locs, z_Locs]#to index multiple locs you want arrays of all x then y ect not aray of indexes with values all togeter

        #2D case
        else:
            res_arr = self.cumsum_mine[x_Locs, z_Locs] #for every X column index the z level corresponding to dug level in state. now have the cumsum of each loc

        check = z_Locs >= 0  # if the dug level in state was 0 it will now be -1 so we make it false so we can do (payoff for not dug colum)*0=0 to not affect sum
        return np.sum((res_arr * check))  # add up cumsum values for colums actualy dug in






    def is_dangerous(self, state):
        '''
        Return True iff the given state breaches the dig_tolerance constraints.
        
        No loops needed in the implementation!
        '''
        # convert to np.array in order to use numpy operators
        state = np.array(state)         

        ####################### Inserting code here! #######################
        # 3D case
        if self.three_dim:
            xtest = state[:,:-1] - state[:,1:] # x axis
            ytest = state[:-1,:] - state[1:,:] # y axis
            dia1test = state[:-1,:-1] - state[1:,1:] # 1st diag axis
            dia2test = np.rot90(state)[:-1,:-1] - np.rot90(state)[1:,1:] # 2nd diag axis
            
            # Concatenate all tests and check for unacceptable tolerances
            return(np.any(abs(np.concatenate((xtest,ytest,dia1test,dia2test),
                                             axis=None)) > self.dig_tolerance))
        # 2D case
        else:
            # Simply check along the x axis for unacceptable tolerances
            return(np.any(abs(state[:-1] - state[1:]) > self.dig_tolerance))
        
        
        ####################### Inserting code here! #######################   


    
    # ========================  Class Mine  ==================================
    
    
    
def search_dp_dig_plan(mine):
    '''
    Search using Dynamic Programming the most profitable sequence of 
    digging actions from the initial state of the mine.
    
    Return the sequence of actions, the final state and the payoff
    

    Parameters
    ----------
    mine : a Mine instance

    Returns
    -------
    best_payoff, best_action_list, best_final_state

    '''
    raise NotImplementedError


    
    
def search_bb_dig_plan(mine):
    '''
    Compute, using Branch and Bound, the most profitable sequence of 
    digging actions from the initial state of the mine.
        

    Parameters
    ----------
    mine : Mine
        An instance of a Mine problem.

    Returns
    -------
    best_payoff, best_action_list, best_final_state

    '''
    
    
    raise NotImplementedError



def find_action_sequence(s0, s1):
    '''
    Compute a sequence of actions to go from state s0 to state s1.
    There may be several possible sequences.
    
    Preconditions: 
        s0 and s1 are legal states, s0<=s1 and 
    
    Parameters
    ----------
    s0 : tuple based mine state
    s1 : tuple based mine state 

    Returns
    -------
    A sequence of actions to go from state s0 to state s1

    '''    
    # approach: among all columns for which s0 < s1, pick the column loc
    # with the smallest s0[loc]
    raise NotImplementedError
        
     
        
        
        
        
    
    
    