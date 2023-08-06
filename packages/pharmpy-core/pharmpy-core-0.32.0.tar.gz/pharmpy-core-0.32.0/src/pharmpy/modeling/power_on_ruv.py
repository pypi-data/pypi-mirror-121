"""
:meta private:
"""

from pharmpy.modeling import has_proportional_error_model
from pharmpy.modeling.help_functions import _format_input_list
from pharmpy.parameter import Parameter
from pharmpy.symbols import symbol as S


def set_power_on_ruv(model, list_of_eps=None):
    """Applies a power effect to provided epsilons.

    Initial estimates for new thetas are 1 if the error
    model is proportional, otherwise they are 0.1.

    Parameters
    ----------
    model : Model
        Pharmpy model to create block effect on.
    list_of_eps : str, list
        Name/names of epsilons to apply power effect. If None, all epsilons will be used.
        None is default.

    Return
    ------
    Model
        Reference to the same model

    Examples
    --------
    >>> from pharmpy.modeling import *
    >>> model = load_example_model("pheno")
    >>> set_power_on_ruv(model)   # doctest: +ELLIPSIS
    <...>
    >>> model.statements.find_assignment("Y")
    Y := CIPREDI**power1*EPS(1)*W + F

    See also
    --------
    set_iiv_on_ruv

    """
    list_of_eps = _format_input_list(list_of_eps)
    eps = model.random_variables.epsilons
    if list_of_eps is not None:
        eps = eps[list_of_eps]
    pset, sset = model.parameters, model.statements

    if has_proportional_error_model(model):
        theta_init = 1
    else:
        theta_init = 0.1

    for i, e in enumerate(eps):
        theta_name = str(model.create_symbol(stem='power', force_numbering=True))
        theta = Parameter(theta_name, theta_init)
        pset.append(theta)
        sset.subs({e.name: model.individual_prediction_symbol ** S(theta.name) * e.symbol})

    model.parameters = pset
    model.statements = sset

    return model
