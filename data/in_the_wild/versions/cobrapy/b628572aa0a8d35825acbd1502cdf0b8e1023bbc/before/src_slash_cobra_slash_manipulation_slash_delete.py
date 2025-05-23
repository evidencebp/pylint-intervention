"""Provide functions for pruning reactions, metabolites and genes."""
from ast import And, BoolOp, Module, Name, NodeTransformer
from functools import partial
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, Union
from warnings import warn

from cobra.util import get_context


if TYPE_CHECKING:
    from cobra import Gene, Metabolite, Model, Reaction


def prune_unused_metabolites(model: "Model") -> Tuple["Model", List["Metabolite"]]:
    """Remove metabolites not involved in any reactions.

    Parameters
    ----------
    model: cobra.Model
        The model to remove unused metabolites from.

    Returns
    -------
    cobra.Model
        Input model with unused metabolites removed.
    list of cobra.Metabolite
        List of metabolites that were removed.

    """
    output_model = model.copy()
    inactive_metabolites = [
        m for m in output_model.metabolites if len(m.reactions) == 0
    ]
    output_model.remove_metabolites(inactive_metabolites)
    return output_model, inactive_metabolites


def prune_unused_reactions(model: "Model") -> Tuple["Model", List["Reaction"]]:
    """Remove reactions with no assigned metabolites, returns pruned model.

    Parameters
    ----------
    model: cobra.Model
        The model to remove unused reactions from.

    Returns
    -------
    cobra.Model
        Input model with unused reactions removed.
    list of cobra.Reaction
        List of reactions that were removed.

    """
    output_model = model.copy()
    reactions_to_prune = [r for r in output_model.reactions if len(r.metabolites) == 0]
    output_model.remove_reactions(reactions_to_prune)
    return output_model, reactions_to_prune


def undelete_model_genes(model: "Model") -> None:
    """Undo the effects of a call to `delete_model_genes` in place.

    Parameters
    ----------
    model: cobra.Model
        The model which will be modified in place.

    """
    if model._trimmed_genes is not None:
        for x in model._trimmed_genes:
            x.functional = True

    if model._trimmed_reactions is not None:
        for (
            the_reaction,
            (lower_bound, upper_bound),
        ) in model._trimmed_reactions.items():
            the_reaction.lower_bound = lower_bound
            the_reaction.upper_bound = upper_bound

    model._trimmed_genes = []
    model._trimmed_reactions = {}
    model._trimmed = False


def get_compiled_gene_reaction_rules(model: "Model") -> Dict["Reaction", Module]:
    """Generate a dictionary of compiled gene-reaction rules.

    Any gene-reaction rule expression which cannot be compiled or do not
    evaluate after compiling will be excluded. The result can be used in the
    `find_gene_knockout_reactions` function to speed up evaluation of these
    rules.

    Parameters
    ----------
    model: cobra.Model
        The model to get gene-reaction rules for.

    Returns
    -------
    dict of cobra.Reaction, ast.Module
        The dictionary of cobra.Reaction objects as keys and ast.Module
        objects as keys.

    .. deprecated::
        Internal function that has outlived its purpose.

    """
    warn(
        "The function `get_compiled_gene_reaction_rules` has outlived its purpose. "
        "It will be removed soon.",
        DeprecationWarning,
    )
    return {r: r.gpr for r in model.reactions}


def find_gene_knockout_reactions(
    model: "Model",
    gene_list: List["Gene"],
    compiled_gene_reaction_rules: Optional[Dict["Reaction", Module]] = None,
) -> List["Reaction"]:
    """Identify reactions which will be disabled when genes are knocked out.

    Parameters
    ----------
    model: cobra.Model
        The model for which to find gene knock-out reactions.
    gene_list: list of cobra.Gene
        The list of genes to knock-out.
    compiled_gene_reaction_rules: dict of {reaction: compiled_string},
                                  optional
        If provided, this gives pre-compiled gene-reaction rule strings.
        The compiled rule strings can be evaluated much faster. If a rule
        is not provided, the regular expression evaluation will be used.
        Because not all gene-reaction rule strings can be evaluated, this
        dict must exclude any rules which can not be used with eval
        (default None).

    Returns
    -------
    list of cobra.Reaction
       The list of cobra.Reaction objects which will be disabled.

    .. deprecated:: 0.22.1
        Internal function that has outlived its purpose.

    """
    warn(
        "The function `find_gene_knockout_reactions` has outlived its purpose. "
        "It will be removed in the next minor version (0.23.0).",
        DeprecationWarning,
    )
    potential_reactions = set()
    for gene in gene_list:
        if isinstance(gene, str):
            gene = model.genes.get_by_id(gene)
        potential_reactions.update(gene._reaction)
    gene_set = {str(i) for i in gene_list}
    if compiled_gene_reaction_rules is None:
        compiled_gene_reaction_rules = {r: r.gpr for r in potential_reactions}

    return [
        r
        for r in potential_reactions
        if not compiled_gene_reaction_rules[r].eval(gene_set)
    ]


def delete_model_genes(
    model: "Model",
    gene_list: Union[List["Gene"], Set["Gene"], List[str], Set[str]],
    cumulative_deletions: bool = True,
    disable_orphans: bool = False,
) -> None:
    """Temporarily remove the effect of genes in `gene_list`.

    It sets the bounds to "zero" for reactions catalysed by the genes in
    `gene_list` if deleting the genes stops the reactions from proceeding.

    Parameters
    ----------
    model: cobra.Model
        The model whose reaction bounds are to be set.
    gene_list: list of cobra.Gene
        The list of genes to knock-out.
    cumulative_deletions: bool, optional
        If True, then any previous deletions will be maintained in the
        model (default True).
    disable_orphans: bool, optional
        If True, then orphan reactions will be disabled. Currently, this
        is not implemented (default False).

    """
    if disable_orphans:
        raise NotImplementedError("disable_orphans not implemented")
    if not hasattr(model, "_trimmed"):
        model._trimmed = False
        model._trimmed_genes = []
        model._trimmed_reactions = {}  # Store the old bounds in here.
    # older models have this
    if model._trimmed_genes is None:
        model._trimmed_genes = []
    if model._trimmed_reactions is None:
        model._trimmed_reactions = {}
    # Allow a single gene to be fed in as a string instead of a list.
    if not hasattr(gene_list, "__iter__") or hasattr(
        gene_list, "id"
    ):  # cobra.Gene has __iter__
        gene_list = [gene_list]

    if not hasattr(gene_list[0], "id"):
        if gene_list[0] in model.genes:
            tmp_gene_dict = dict([(x.id, x) for x in model.genes])
        else:
            # assume we're dealing with names if no match to an id
            tmp_gene_dict = dict([(x.name, x) for x in model.genes])
        gene_list = [tmp_gene_dict[x] for x in gene_list]

    # Make the genes non-functional
    for x in gene_list:
        x.functional = False

    if cumulative_deletions:
        gene_list.extend(model._trimmed_genes)
    else:
        undelete_model_genes(model)

    for the_reaction in find_gene_knockout_reactions(model, gene_list):
        # Running this on an already deleted reaction will overwrite the
        # stored reaction bounds.
        if the_reaction in model._trimmed_reactions:
            continue
        old_lower_bound = the_reaction.lower_bound
        old_upper_bound = the_reaction.upper_bound
        model._trimmed_reactions[the_reaction] = (
            old_lower_bound,
            old_upper_bound,
        )
        the_reaction.lower_bound = 0.0
        the_reaction.upper_bound = 0.0
        model._trimmed = True

    model._trimmed_genes = list(set(model._trimmed_genes + gene_list))


class _GeneRemover(NodeTransformer):
    """
    Class to represent a gene set remover.

    Parameters
    ----------
    target_genes: list or set of cobra.Gene
        A set of genes to be removed.

    """

    def __init__(self, target_genes: Set["Gene"], **kwargs) -> None:
        """Initialize a new object.

        Other Parameters
        ----------------
        kwargs:
            Further keyword arguments are passed on to the parent class.

        """
        super().__init__(**kwargs)
        self.target_genes = {str(i) for i in target_genes}

    def visit_Name(self, node: "Name") -> Optional["Name"]:
        """Remove a gene.

        Parameters
        ----------
        node: ast.Name
            The gene to remove.

        Returns
        -------
        cobra.Gene or None
            None if gene object is in `target_genes`.

        """
        return None if node.id in self.target_genes else node

    def visit_BoolOp(self, node: "BoolOp") -> Optional[Union["BoolOp", "Name"]]:
        """Rules for boolean operations.

        Parameters
        ----------
        node: ast.Name
            The gene to apply rules to.

        Returns
        -------
        ast.Name or None
            None if size of Or node values is zero after applying rule,
            or size of And node values is lower after applying rule.

        """
        original_n = len(node.values)
        self.generic_visit(node)
        if len(node.values) == 0:
            return None
        # AND with any entities removed
        if len(node.values) < original_n and isinstance(node.op, And):
            return None
        # if one entity in an OR was left, just that entity passed up
        if len(node.values) == 1:
            return node.values[0]
        return node


def remove_genes(
    model: "Model",
    gene_list: Union[List["Gene"], Set["Gene"], List[str], Union[str]],
    remove_reactions: bool = True,
) -> None:
    """Remove genes entirely from the model.

    This will also simplify all gene-reaction rules with the genes
    inactivated.

    Parameters
    ----------
    model: cobra.Model
        The model to remove genes from.
    gene_list: list of cobra.Gene or gene ids
        The list of gene objects to remove.
    remove_reactions: bool, optional
        Whether to remove reactions associated with genes in `gene_list`
        (default True).

    """
    gene_set = {model.genes.get_by_id(str(i)) for i in gene_list}
    gene_id_set = {i.id for i in gene_set}
    remover = _GeneRemover(gene_id_set)
    target_reactions = []
    rxns_to_revisit = set()
    context = get_context(model)
    for rxn in model.reactions:
        if rxn.gene_reaction_rule is None or len(rxn.gene_reaction_rule) == 0:
            continue
        # reactions to remove
        if remove_reactions and not rxn.gpr.eval(gene_id_set):
            target_reactions.append(rxn)
        else:
            # if the reaction is not removed, remove the gene
            # from its gpr
            old_gpr = rxn.gpr.copy()
            remover.visit(rxn.gpr)
            # If the remover completely removed the AST tree from the GPR, it will not
            # have body at all, which is why this isn't if body is None.
            if not hasattr(rxn.gpr, "body"):
                rxn.gpr.body = None
                rxn._genes = set()
            else:
                rxns_to_revisit.add(rxn)
            if context:
                context(partial(setattr, rxn, "gpr", old_gpr))
                context(partial(rxn.update_genes_from_gpr))
    for gene in gene_set:
        model.genes.remove(gene)
        gene._model = None
        if context:
            context(partial(model.genes.add, gene))
            context(partial(setattr, gene, "_model", model))
        # remove reference to the gene in all groups
        associated_groups = model.get_associated_groups(gene)
        for group in associated_groups:
            group.remove_members(gene)
    model.remove_reactions(target_reactions)
    for rxn in rxns_to_revisit:
        rxn.update_genes_from_gpr()
