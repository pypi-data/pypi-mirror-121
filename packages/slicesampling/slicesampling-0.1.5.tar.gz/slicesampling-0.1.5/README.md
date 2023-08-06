# slicesampler

Set of Markov chain Monte Carlo (MCMC) sampling methods based on slice sampling

## Available methods

The package includes the following methods:
1. Univariate slice sampler, as described in [1]
2. Multivariate slice sampler based on univariate updates along eigenvectors, as described in [2]
3. Multivariate slice sampler based on combination of hit-and-run and univariate slice sampler, named hybrid slice sampler in [3]

## Examples

Examples are included in the git repo at https://code.ornl.gov/2kv/slicesampling
1. example1_univariate.py illustrates how to use the package for univariate slice sampling
2. example2_bivariate.py illustrates how to use the package for multivariate slice sampling

## References
[1] Neal, Radford M. (2003). Slice sampling. The Annals of Statistics, 31(3), 705 - 767. URL: https://doi.org/10.1214/aos/1056562461

[2] Thompson, Madeleine (2011). Slice Sampling with Multivariate Steps. PhD Thesis. URL: https://hdl.handle.net/1807/31955

[3] Rudolf, Daniel; Ullrich, Mario (2018). Comparison of hit-and-run, slice_sampler sampler and random walk metropolis. Journal of Applied Probability, 55(4), 1186-1202. URL: https://doi.org/10.1017/jpr.2018.78
