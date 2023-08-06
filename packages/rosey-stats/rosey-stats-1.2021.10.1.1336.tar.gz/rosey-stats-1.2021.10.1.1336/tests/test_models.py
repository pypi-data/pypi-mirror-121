import numpy as np
from scipy import stats
from sklearn.linear_model import LassoCV
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_boston, load_breast_cancer
from rosey_stats.models import BairSupervisedPCA, Blooper, M5TreeRegressor


def test_bair_supervised_pca():
    require_dims = 3
    data, target = load_boston(True)

    bspca = BairSupervisedPCA(n_components=require_dims)
    trans_a = bspca.fit_transform(data, target)
    trans_b = bspca.transform(data)

    assert trans_a.ndim == 2
    assert trans_a.shape[1] == 3
    assert np.isclose(trans_a, trans_b).all()

    data, target = load_breast_cancer(True)
    lspca = BairSupervisedPCA(require_dims)
    trans_a = lspca.fit_transform(data, target)
    trans_b = lspca.transform(data)

    assert trans_a.ndim == 2
    assert trans_a.shape[1] == 3
    assert np.isclose(trans_a, trans_b).all()


def test_blooper():
    N, P = 300, 30
    m_true = np.zeros(P)
    m_true[:4] = [2, -2, 2, 3]

    noise = 3 * stats.norm().rvs(N)

    data = 3 * stats.norm().rvs((N, P))
    target = data @ m_true + noise

    lasso_cv = LassoCV(cv=10, positive=True).fit(data, target)

    # Check if any fail
    Blooper(best_lam=lasso_cv.alpha_, draws=100).fit(data, target)
    Blooper(best_lam=lasso_cv.alpha_, domain='pos', draws=100).fit(data, target)
    Blooper(best_lam=lasso_cv.alpha_, domain='neg', draws=100).fit(data, target)
    Blooper(draws=100, domain='pos', verbose=True).fit(data, target)
    Blooper(draws=100, domain='neg', verbose=True).fit(data, target)
    Blooper(draws=100, verbose=True).fit(data, target)


def test_m5tree():
    from sklearn.tree import DecisionTreeRegressor
    x, y = load_boston(return_X_y=True)
    cv_kwargs = dict(
        cv=10,
        n_jobs=-1
    )

    m5_scores = cross_val_score(M5TreeRegressor(), x, y, **cv_kwargs)
    dt_scores = cross_val_score(DecisionTreeRegressor(min_samples_leaf=10), x, y, **cv_kwargs)

    assert m5_scores.mean() > dt_scores.mean(), 'M5Tree must outperform Decision Trees'
