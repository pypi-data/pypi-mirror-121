# A Python package for Decision from Experience Behavior Modeling (DEBM)

DEBM is a **playground** for modeling behavior in decision from experience paradigm. 

With DEBM, we ask to
----
(1) Make behavioral modeling science more replicable.
(2) Make modeling more accessible for people with basic programming skills.
(3) Be a central repository for published models.
(4) Speed up the process of comparing, assessing and developing behavioral models.


DEBM contains the basic building blocks of behavioral models, alongside a few built-in models which serve for testing and demonstration.

Contribute
====
Add your own model
----
Follow this tutorial to develop your own mode, or re-write an existing model into the DEBM package.
Currently, only published models, or those in the process of publishing (e.g., submitted papers), will be included in the package.
Send your code to ofiryakobi+debm (at) gmail.com with a reference to a pre-print or the published paper describing the model.

Correct existing models
----
Did you find an error in one of the models, a result that does not replicate, or simply found a more efficient way to write an existing code?
Please email me at ofiryakobi+debm (at) gmail.com

Always stay up to date
----
**Important** - one of the essential goals for this package is to keep coding free of errors and bugs. If code is being corrected, you will not be able to enjoy it until you update your existing package.
To do that, make sure once in a while to update the package by going to command line, and running
`pip install debm -U`

# Tutorial

The basics
====
Using an existing model (whether it was created by you, or one of the built-in models) is easy.

As an example, we will use the sample-of-k model, also known as Naive Sampler (Erev & Roth, 2014).
This model asserts that when making repeated decisions, people use a small portion of their past experience to evaluate the different prospects (i.e., a sample in the size of k).
The sampling process is done with replacement from all previous experience.

As an example, we will replicate the predictions of Erev and Roth (2014), problem 1 & 2 (Table 2).

Installing debm
----
Go to command line (e.g., Start -> run -> cmd. If you use Anaconda: Start -> Anaconda prompt).  
Type `pip install debm`

Setting up
----
Using your favorite Python IDE (I recommend installing Anaconda and using Spyder), we will now import *debm* and define the environment: the prospects and model.
The hash tag symbol is used for commenting, and will be used here to clarify the code.

```# We will use Prospect and Sample_of_K for now, the rest will be used later  
from debm import Prospect, Sample_of_K, resPlot, FitMultiGame, makeGrid, saveEstimation, resPlot
import numpy as np #We will use NumPy as well, with its short alias np
```

We will define the prospects first, both simulating 100 trials choice problems.  
The first is the status quo, and we will name it accordingly:
`StatQuo=Prospect(100,[0]*100,False)`
This line of code creates a Prospect named StatusQuo, with 100 trials (the 1st argument).  
The 2nd argument is an array of 100 zeros (instead of writing [0,0,0,0,0....,0]) - these are the outcomes.  
The 3rd argument passed to Prospect is boolean (True/False), and it is used when we pass a function (see below).  
  
Now we will define a prospect that produce -10 (minus 10) 10% of the time, and +1 (a gain of one point) 90% of the time.  
For that, we will use NumPy's (a popular Python package) function - np.random.choice.  
The syntax is np.random.choice(a, size, replace, p):  
a – the array of possible outcomes; size – how many samples to draw;  
replace – draw with replacement? (True/False). If false – the size should be equal or less than the size of the array a;  
p – an array of probabilities in the size of a. Let’s consider the example below:  
np.random.choice([1,-10],1,True,[0.9,0.1])
The result would be one number, either 1 (in probability 0.9) or -10.  
If we want to output 100 numbers instead of one: np.random.choice([1,-10],1,True,[0.9,0.1]).  
  
When creating a prospect, we can pass a function (and corresponding arguments), as follows:
`B1=Prospect(100,np.random.choice,False,[-10,1],100,True,[0.1,0.9])`

We defined a prospect named B1 with 100 trials, passed the function np.random.choice,  
Passed False to state that the function we are passing generates all trials at once (not one by one),  
Then we passed the arguments for `np.random.choice` as before: [-10,1],100,True,[0.1,0.9].  
  
Now we will define the Sample_of_K model, we will name it sok1 (sample of k, problem 1) for convenience.  
The syntax for Sample_of_K is Sample_of_K(parameters, prospect_list, number_of_simulations).  
Let's consider the code below:
`sok1=Sample_of_K({'Kappa':5},[StatQuo,B1],1000)`
Parameters is a dictionary of parameters. In this specific model we only have Kappa, which we defined as 5 (as in Erev & Roth 2014).  
[StatQuo,B1] - a list of the two prospects we defined.  
1000 - the number of simulations to run each time we generate predictions.  

That's it! we set up a model, and your code should look like that at this point:  
```
from debm import Prospect, Sample_of_K, resPlot, FitMultiGame, makeGrid, saveEstimation ,resPlot
import numpy as np #We will use NumPy as well, with its short alias np

StatQuo=Prospect(100,[0]*100,False)
B1=Prospect(100,np.random.choice,False,[-10,1],100,True,[0.1,0.9])
sok1=Sample_of_K({'Kappa':5},[StatQuo,B1],1000)
```

Now let's make predictions, and save them to a new variable called choices1:  
`choices1=sok1.Predict()`  
choices1 stores the choice rates predicted for each prospect for the 100 trials we defined, based on 1000 simulations.  
You can `print(choices1)` to inspect the results.  
To see the mean over all trials, type `choices1.mean(axis=0)` (axis=0 states that we want the mean over rows [trials] and not the grand mean).  
The results should be approximately 38% and 62% as in Erev and Roth.  

We can easily plot the results:  
`sok1.plot_predicted()`
If you want to aggregate over blocks, you can simply type the number of blocks:  
`sok1.plot_predicted(4)` (just make sure the number of trials is dividable by the number of blocks)  
Regardless to the names you gave each prospect, they will be named in the figure according to their order in the model (A, B, C...Z).  
In our case, StatusQuo was entered first and corresponds to *A*.  


Fitting
----

If we want to estimate the parameters of the model, we need real human data observations.  
Download the following example [https://github.com/ofiryakobi/debm/blob/master/docs/ex1.csv](https://github.com/ofiryakobi/debm/blob/master/docs/ex1.csv) to your computer.  
Make sure you know the path of the file you downloaded (e.g., c:\users\myName\downloads\).  

Add the following line of code to your script, and change the path to the real file path:  
`observed1=np.genfromtxt('c:\\users\\myName\\downloads\\ex1.csv', delimiter=',')`  

**Note**: Python does not like \\ (one backslash) - use two as in the code line above.  

After running this line of code, you will have a variable called *observed1*, containing the aggregated observed choice rates of 86 participants (in this case they are simulated).  
Use `print(observed1)` to inspect the choice rates.  

We will store them in our model:  
`sok1.set_obs_choices(observed1)`  

Now we can even plot them, using a similar syntax to the one we used earlier:  
`sok1.plot_observed()`
or, e.g.:  
`sok1.plot_observed(4)`

We can even plot the fit of the current predicted choices (the ones we generated earlier, with Kappa=5):
`sok1.plot_fit(4)`

You can see that the fit is not great. We can quantify it, using `sok1.loss(loss_function, scope)`.  
loss_function could be MSD (mean squared deviation; identical to MSE) or -LL (negative log-likelihood),  
and the scope should be either *prospectwise* (comparing one value for each prospect), or *bitwise* (comparing each trial of each prospect).  
Calculating the MSD prospectwise:
`sok1.loss('MSD','pw')`  
The current MSD is ~0.0145.

Can we find a better fit?  
Using the built-in OptimizeBF (BF stands for brute-force, trying all possible values as in a grid search).  
`OptimizeBF(pars_dicts, kwargs)`  
We need to pass a list of parameters, each packed in a dictionary as before, as well as arguments to the loss function.  

We can easily create a grid using the helper function *makeGrid*:  
`pspace=makeGrid({'Kappa':range(1,51)})`  
Now the variable pspace (pspace as in parameter-space) contains all possible Kappa values from 1 to 50 (**note** that in Python the upper bound is usually exclusive, so 1,5 means 1,2,3,4), in the right structure.  
To estimate Kappa we can run the following command:  
`res1=sok1.OptimizeBF(pspace,True,'MSD','pw')`

The first argument is pspace - the parameter space and values over the grid we evaluate.  
The second is boolean (True/False) stating if we want to see a progress bar during the process.  
The next two arguments go directly to the *loss* function we used before - telling it the loss function and scope we would like to use for fitting.  
We save the results in a new variable we called *res1*.  

res1 is a dictionary, containing the best set of parameters found, the corresponding minimum loss value, and a list of loss values for each iteration.  
The following command will pring the best fitted Kappa:  
`print(res1['bestp'])`  # We found Kappa=3 was the best representation of the data

We can use the helper function *resPlot* to plot the loss function over iterations (useful mostly for 1 or 2 parameter models):  
`resPlot(res1)`

It is possible to plot the fit (visualizing the observed and predicted choice rates), but first we will need to update our predictions:  
```
sok1.parameters={'Kappa':3} # Set Kappa according to the estimation
sok1.Predict() # Generate new predictions with Kappa=3
```

Now we can plot the fit, e.g. over five blocks of 20 trials:
`sok1.plot_fit(5)`

To save the estimation's results to a csv file, use:  
`saveEstimation(res1,'c:\\your_desired_path\\results.csv')`  


More advanced user can use external packages (e.g. SciPy) for optimization, using the CalcLoss function which accepts parameters and returns the loss.
e.g. `res=minimize(modelname.CalcLoss,[0],('MSE','pw'))`  


Individual differences
----
The example above demonstrated fitting over the aggregated choice rates of 84 participants.  
We can also fit Kappa for each individual, using the same mechanism. However, an extra layer of Python programming is required.  
(note: I plan to add a built-in functionality for individual differences estimation in future release)  

Download the data of three subjects:  
[Subject 1](https://github.com/ofiryakobi/debm/blob/master/docs/sub1.csv)  
[Subject 2](https://github.com/ofiryakobi/debm/blob/master/docs/sub2.csv)  
[Subject 3](https://github.com/ofiryakobi/debm/blob/master/docs/sub3.csv)  

To make the estimation faster (for demonstration only), we will limit the values of Kappa to 1-10.  

```
path='C:\\your\\path\\' # Set the path for the downloaded files, remember double backslashes
pspace=makeGrid({'Kappa':range(1,11)})
individual_kappas=[] # We will store the Kappas we found in this array
for file in ['sub1.csv','sub2.csv','sub3.csv']: # A loop going through the different subject data files
    observed=np.genfromtxt(path+file,delimiter=',') # This NumPy function reads the relevant csv file in each loop iteration, and stores it in the variable observed
    sok1.set_obs_choices(observed) # Store the observed choices in the model
    tmp_res=sok1.OptimizeBF(pspace,True,'MSD','pw')  # Estimate 
    individual_kappas.append(tmp_res['bestp']['Kappa']) # Append the best Kappa from the results variable tmp_res into individual_kappas array
```

individual_kappas is an array which now contains the best Kappas found for subject 1,2,3. The values should be 8, 3, 6.





use cases
create your own model
dependent prospects
individual differences
dynamic prospects

future
multiprocessors
partial feedback
more estimation methods
new models