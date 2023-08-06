import warnings
import numpy as np
import pandas as pd
from copy import deepcopy
from tqdm import tqdm, trange
from sklearn.utils import resample
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression, LinearRegression, LassoCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_selection import f_regression, f_classif
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, log_loss
from glmnet import ElasticNet
try:
    from rich import print
except ImportError:
    print('If you would like very pretty printing you can install the `rich` package')


def vec_to_array(a: np.ndarray):
    return a.reshape((len(a), 1))


# noinspection PyPep8Naming
class Blooper(BaseEstimator, RegressorMixin):
    """
    Boostrap Lasso with Partial Ridge Regression
    https://arxiv.org/pdf/1706.02150v1.pdf
    """
    def __init__(
            self,
            n_lams: int = 50,
            eps: float = 1e-3,
            draws: int = 100,
            cv: int = 10,
            domain: str = None,
            best_lam=None,
            ridge_penalty=None,
            fit_intercept=False,
            verbose=False
    ):
        """
        Boostrap Lasso with Partial Ridge Regression
        https://arxiv.org/pdf/1706.02150v1.pdf

        :param n_lams:
        :param eps: The ratio between the max lambda and the min lambda
        :param draws: Number of sample to draw form the posterior distribution
        :param cv:
        :param domain: {None, 'all', 'pos', 'neg'}
        :param best_lam:
        :param ridge_penalty: Only override if you know what you're doing
        :param fit_intercept:
        :param verbose:
        """
        self.n_lams = n_lams
        self.eps = eps
        self.draws = draws
        self.cv = cv
        self.domain = domain
        self.best_lam = best_lam
        self.ridge_penalty = ridge_penalty
        self.fit_intercept = fit_intercept
        self.verbose = verbose

        self.coef_trace_ = None
        self.intercept_trace_ = None
        self.coef_mle_ = None
        self.intercept_mle_ = None

        if domain not in {None, 'all', 'pos', 'neg'}:
            raise ValueError('`domain` must be one of the following None, "all", "pos", "neg"')

    def fit(self, X: np.ndarray, y: np.ndarray):
        # Do any preprocessing needed
        X, y = X.astype(float), y.astype(float)
        if self.ridge_penalty is None:
            self.ridge_penalty = 1 / len(X)

        # This is the paired BLPR algorithm
        self._fit_paired_blpr(X, y)

        return self

    def predict(self, X):
        self._check_is_fitted()
        return X @ self.coef_mle_ + self.intercept_mle_

    def predict_ppc(self, X, n_samples=None):
        self._check_is_fitted()
        if n_samples is None:
            n_samples = range(len(self.coef_trace_))
        else:
            assert 0 < n_samples <= len(self.coef_trace_)
            n_samples = np.random.choice(
                np.arange(len(self.coef_trace_)),
                n_samples,
                replace=False
            )

        y_hats = []
        for i in n_samples:
            y_hats.append(X @ self.coef_trace_[i] + self.intercept_trace_[i])
        y_hats = np.vstack(y_hats)
        return y_hats

    def _check_is_fitted(self):
        if self.coef_mle_ is None:
            from sklearn.exceptions import NotFittedError
            raise NotFittedError

    def _get_glmnet_limits_from_domain(self) -> dict:
        limits = {
            'upper_limits': np.inf,
            'lower_limits': -np.inf
        }
        if self.domain == 'pos':
            limits['lower_limits'] = 0
        if self.domain == 'neg':
            limits['upper_limits'] = 0

        return limits

    @staticmethod
    def _get_glmnet_lambda_path(lam):
        return np.array([lam * 0.98, lam])

    def _fit_paired_blpr(self, x, y):
        warnings.simplefilter('ignore')
        n, p = x.shape

        m_trace, b_trace, i_boot, i_failed_run = [], [], 0, 0
        progressor = tqdm(total=self.draws, desc='Bootstrap Iterations')
        # for b in progressor:
        while i_boot < self.draws:
            # 1. Create bootstrap samples of x -> x_boot & y -> y_boot
            x_boot, y_boot = resample(x, y, replace=True, random_state=i_boot + i_failed_run)

            # 2. Find the best λ
            if self.best_lam is None:
                best_lam_finder = ElasticNet(
                    alpha=1,
                    n_splits=self.cv,
                    n_lambda=self.n_lams,
                    min_lambda_ratio=self.eps,
                    fit_intercept=self.fit_intercept,
                    **self._get_glmnet_limits_from_domain()
                )
                best_lam_finder.fit(x, y)  # TODO (15-Mar-21) add weights later
                self.best_lam = best_lam_finder.lambda_best_[0]
                if self.verbose:
                    print(f'Optimal λ => {self.best_lam:.3f}')

            boot_l1_model = ElasticNet(
                alpha=1,
                n_splits=self.cv,
                lambda_path=self._get_glmnet_lambda_path(self.best_lam),
                fit_intercept=self.fit_intercept,
                **self._get_glmnet_limits_from_domain()
            )
            boot_l1_model.fit(x_boot, y_boot)
            m_boot_l1 = boot_l1_model.coef_

            partial_ridge_selector = np.ones(p)
            partial_ridge_selector[m_boot_l1.nonzero()] = 0

            # 4. Solve m_boot_blpr
            blpr = ElasticNet(
                alpha=0,
                n_splits=self.cv,
                lambda_path=self._get_glmnet_lambda_path(self.ridge_penalty / 2),
                fit_intercept=self.fit_intercept,
                **self._get_glmnet_limits_from_domain()
            )
            try:
                blpr.fit(
                    x_boot, y_boot,
                    relative_penalties=partial_ridge_selector
                )
                m_trace.append(blpr.coef_)
                b_trace.append(blpr.intercept_)
                i_boot += 1
                if self.verbose:
                    progressor.update(i_boot)
            except ValueError:
                i_failed_run += 1
                warnings.simplefilter('default')
                warnings.warn('BLPR failed, retrying')
                warnings.simplefilter('ignore')
                continue

        m_trace = np.vstack(m_trace)
        b_trace = np.array(b_trace)
        self.coef_trace_ = m_trace.copy()
        self.intercept_trace_ = b_trace.copy()
        self.coef_mle_ = self.coef_trace_.mean(axis=0)
        self.intercept_mle_ = b_trace.mean(axis=0)

        warnings.simplefilter('default')
        if self.verbose:
            progressor.close()


# noinspection PyPep8Naming
class BairSupervisedPCA(BaseEstimator, TransformerMixin):
    """
    Supervised Principal Components Analysis
    This is the one as described by 'Prediction by Supervised Principal Components' (Eric Bair, Trevor Hastie et al)
    https://stats.stackexchange.com/a/767/91928
    NOTE -> Use sklearn LinearRegression over statsmodels OLS because it is ~3x faster.
    Example below
    >>> from sklearn.datasets import load_boston, load_breast_cancer
    >>> require_dims = 3
    >>> data, target = load_boston(True)
    >>> bspca = BairSupervisedPCA(n_components=require_dims)
    >>> trans_a = bspca.fit_transform(data, target)
    >>> trans_b = bspca.transform(data)
    >>> trans_a.ndim
    2
    >>> trans_a.shape[1]
    3
    >>> np.isclose(trans_a, trans_b).all()
    True
    >>> data, target = load_breast_cancer(True)
    >>> lspca = BairSupervisedPCA(require_dims)
    >>> trans_a = lspca.fit_transform(data, target)
    >>> trans_b = lspca.transform(data)
    >>> trans_a.ndim
    2
    >>> trans_a.shape[1]
    3
    >>> np.isclose(trans_a, trans_b).all()
    True
    >>> print('Done')
    Done
    """

    def __init__(self, n_components=None, is_regression=True, cv=5,
                 threshold_samples=25, use_pvalues=False, verbose=False):
        self.pca = PCA(n_components=n_components, whiten=True)
        self.conditioner_model_ = LinearRegression() if is_regression else LogisticRegression()
        self.cv, self.n_thres = cv, threshold_samples
        self.n_components = n_components
        self.is_regression, self.use_pvalues = is_regression, use_pvalues
        self.cv_results, self.indices, self.best = 3 * [None]
        self.verbose = verbose

        if use_pvalues:
            warnings.warn('Using p-values could select spurious features as important!')

    def _check_is_fitted(self):
        if self.indices is None or self.best is None:
            raise NotFittedError

    def plot_learning_curve(self, show_graph=False):
        import matplotlib.pyplot as graph
        try:
            from rosey_graph import plot_learning_curve as plc
        except ImportError:
            raise ImportError('You need have rosey-graph installed to call this function')
        self._check_is_fitted()

        plc(self.cv_results['mean'], self.cv_results['std'], self.cv_results['theta'], n=self.cv)
        graph.ylabel('R2 Score' if self.is_regression else 'Log loss')
        graph.xlabel(r'$\theta$')
        if show_graph:
            graph.show()

    def _univariate_regression(self, x, y):
        def model(x_i):
            lm_i = LinearRegression() if self.is_regression else LogisticRegression()
            lm_i.fit(vec_to_array(x_i), y)
            return lm_i.coef_[0]

        iterator = range(x.shape[1])
        if self.verbose and tqdm:
            iterator = tqdm(iterator, desc='Computing Coefs')
        return np.array([model(x[:, i]) for i in iterator])

    def fit(self, X, y):
        # Step 1 -> Compute (univariate) standard regression coefficient for each feature
        if self.use_pvalues:
            _, thetas = f_regression(X, y) if self.is_regression else f_classif(X, y)
            grid_sweep = np.linspace(thetas.min(), 1, self.n_thres)
        else:
            # Compute the regression coef like it says in the paper
            if self.is_regression:
                y_centered = y - np.mean(y)
                thetas = self._univariate_regression(X, y_centered)
            else:
                thetas = self._univariate_regression(X, y)
            # noinspection PyTypeChecker
            grid_sweep = np.percentile(np.abs(thetas), np.linspace(0.01, 1, self.n_thres)[::-1] * 100)

        # Step 2 -> Form a reduced data matrix
        thetas = (thetas if self.use_pvalues else np.abs(thetas)).flatten()
        cv_results = []
        for thres in grid_sweep:
            select = np.squeeze(np.argwhere(thetas <= thres) if self.use_pvalues else np.argwhere(thetas >= thres))
            x_selected = X[:, select]
            try:
                comps = float('inf') if self.n_components is None else self.n_components
                u_selected = PCA(min(x_selected.shape[1], comps), whiten=True).fit_transform(x_selected)
            except (ValueError, IndexError):
                u_selected = x_selected

            kf, scores = KFold(n_splits=self.cv, shuffle=True), []
            for train_ind, val_ind in kf.split(u_selected):
                # Split
                x_train, x_val = u_selected[train_ind], u_selected[val_ind]
                y_train, y_val = y[train_ind], y[val_ind]

                # Fit
                if x_train.ndim == 1:
                    x_train, x_val = vec_to_array(x_train), vec_to_array(x_val)

                if self.is_regression:
                    lm = LinearRegression().fit(x_train, y_train)
                else:
                    lm = LogisticRegression().fit(x_train, y_train)

                # Score
                y_hat = lm.predict(x_val)
                score = mean_squared_error(y_val, y_hat) if self.is_regression else log_loss(y_val, y_hat)

                # Test
                scores.append(score)

            # Score threshold
            scores = np.array(scores)
            cv_results.append((scores.mean(), scores.std()))
            if self.verbose:
                print(f'Theta -> {thres}', cv_results[-1])

        # Get best results
        self.cv_results = pd.DataFrame(cv_results, columns=['mean', 'std'])
        self.cv_results['theta'] = grid_sweep
        self.cv_results = self.cv_results.tail(len(self.cv_results) - 1)

        self.best = self.cv_results.sort_values(by='mean', ascending=False if self.is_regression else True).head(1)
        if self.use_pvalues:
            best_select = np.argwhere(thetas <= self.best['theta'].values)
        else:
            best_select = np.argwhere(thetas >= self.best['theta'].values)
        self.indices = np.squeeze(best_select)

        X = vec_to_array(X[:, self.indices]) if X[:, self.indices].shape[1] == 1 else X[:, self.indices]
        self.pca.fit(X)
        self.conditioner_model_.fit(self.pca.transform(X), y)

        return self

    def transform(self, X, y=None, **fit_params):
        self._check_is_fitted()

        # Step 3 -> Reduce X and then perform PCA
        x_reduced = X[:, self.indices]
        self.n_components = min(x_reduced.shape[1], float('inf') if self.n_components is None else self.n_components)
        return self.pca.transform(x_reduced)

    def fit_transform(self, X, y=None, **fit_params):
        assert y is not None
        if X.ndim == 1:
            raise ValueError('X cannot be a vector')
        elif X.shape[1] == 1:
            raise ValueError('X must have more than 1 feature')

        self.fit(X, y)
        return self.transform(X)

    def precondition(self, X):
        """
        This returns the preconditioned target variable (It predicts y from the input data)
        :param X:
        :return:
        """
        return self.conditioner_model_.predict(self.pca.transform(X[:, self.indices]))


# noinspection PyPep8Naming
class M5TreeRegressor(BaseEstimator, RegressorMixin):
    def __init__(
            self,
            min_samples_leaf: int or str = 'auto',
            linear_estimator=LassoCV(cv=3),
            decision_tree_kwargs=None,
            verbose=False
    ):
        if decision_tree_kwargs is not None:
            assert 'min_samples_leaf' not in decision_tree_kwargs.keys()
            assert 'max_features' not in decision_tree_kwargs.keys()

        self.min_samples_leaf = min_samples_leaf
        self.linear_estimator = linear_estimator
        self.decision_tree_kwargs = decision_tree_kwargs if isinstance(decision_tree_kwargs, dict) else {}
        self.verbose = verbose

        self._tree = None  # type: DecisionTreeRegressor
        self._linear_models = {}  # type: dict

    def fit(self, X: np.ndarray, y: np.ndarray, sample_weight=None):
        n, p = X.shape
        estimated_min_samples_leaf = p*10 if self.min_samples_leaf == 'auto' else self.min_samples_leaf
        if n <= estimated_min_samples_leaf:
            warnings.warn(f'Small dataset! N={n:,} min samples per leaf = {estimated_min_samples_leaf:,}')

        # Fit underlying tree
        if self.verbose:
            print('Fitting Tree...', flush=True)
        self._tree = DecisionTreeRegressor(
            min_samples_leaf=estimated_min_samples_leaf,
            max_features='auto',
            **self.decision_tree_kwargs
        )
        self._tree.fit(X, y, sample_weight)
        sample_leaf_id = self._tree.apply(X)
        unique_leaves = np.unique(sample_leaf_id)

        # Fit linear models
        progressor = tqdm(unique_leaves, desc='Fitting Linear Models...') if self.verbose else unique_leaves
        for leaf_id in progressor:
            selector = sample_leaf_id == leaf_id
            model = deepcopy(self.linear_estimator)
            self._linear_models[leaf_id] = model.fit(X[selector, :], y[selector])

        if self.verbose:
            print('Done!')

    def predict(self, X, verbose=False):
        self._check_is_fitted()

        y_hat = np.zeros(len(X))
        sample_leaf_id = self._tree.apply(X)
        progressor = tqdm(np.unique(sample_leaf_id)) if verbose else np.unique(sample_leaf_id)
        for leaf_id in progressor:
            selector = sample_leaf_id == leaf_id
            y_hat[selector] = self._linear_models[leaf_id].predict(X[selector, :])

        return y_hat

    def score(self, X, y, sample_weight=None):
        from sklearn.metrics import r2_score
        self._check_is_fitted()

        return r2_score(y, self.predict(X))

    def _check_is_fitted(self):
        if self._tree is None:
            raise NotFittedError
