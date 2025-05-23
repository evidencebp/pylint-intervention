import json
import itertools
from copy import deepcopy
from .serializers import AnalyzedExperimentSerializer, AnalyzedExperimentFilter
from collections import defaultdict

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import *
from django.db.models import Count, Min, Max, Subquery
from django.views.decorators.csrf import csrf_exempt

from rest_framework_datatables.django_filters.backends import DatatablesFilterBackend
from rest_framework import generics

from common.models import ReleaseNotes
from common.phylogenetic_tree import PhylogeneticTreeGenerator
from common.selection import Selection
from ligand.models import *
from protein.models import Protein, ProteinFamily



class LigandBrowser(TemplateView):
    """
    Per target summary of ligands.
    """
    template_name = 'ligand_browser.html'

    def get_context_data(self, **kwargs):

        context = super(LigandBrowser, self).get_context_data(**kwargs)

        ligands = AssayExperiment.objects.values(
            'protein__entry_name',
            'protein__species__common_name',
            'protein__family__name',
            'protein__family__parent__name',
            'protein__family__parent__parent__name',
            'protein__family__parent__parent__parent__name',
            'protein__species__common_name'
        ).annotate(num_ligands=Count('ligand', distinct=True))

        context['ligands'] = ligands

        return context


def LigandDetails(request, ligand_id):
    """
    The details of a ligand record. Lists all the assay experiments for a given ligand.
    """
    ligand_records = AssayExperiment.objects.filter(
        ligand__properities__web_links__index=ligand_id
    ).order_by('protein__entry_name')

    record_count = ligand_records.values(
        'protein',
    ).annotate(num_records=Count('protein__entry_name')
               ).order_by('protein__entry_name')

    ligand_data = []

    for record in record_count:
        per_target_data = ligand_records.filter(protein=record['protein'])
        protein_details = Protein.objects.get(pk=record['protein'])

        """
        A dictionary of dictionaries with a list of values.
        Assay_type
        |
        ->  Standard_type [list of values]
        """
        tmp = defaultdict(lambda: defaultdict(list))
        tmp_count = 0
        for data_line in per_target_data:
            tmp[data_line.assay_type][data_line.standard_type].append(
                data_line.standard_value)
            tmp_count += 1

        # Flattened list of lists of dict values
        values = list(itertools.chain(
            *[itertools.chain(*tmp[x].values()) for x in tmp.keys()]))
        # TEMPORARY workaround for handling string values
        values = [float(item) for item in values if float(item)]

        if len(values) > 0:
            ligand_data.append({
                'protein_name': protein_details.entry_name,
                'receptor_family': protein_details.family.parent.name,
                'ligand_type': protein_details.get_protein_family(),
                'class': protein_details.get_protein_class(),
                'record_count': tmp_count,
                'assay_type': ', '.join(tmp.keys()),
                # Flattened list of lists of dict keys:
                'value_types': ', '.join(itertools.chain(*(list(tmp[x]) for x in tmp.keys()))),
                'low_value': min(values),
                'average_value': sum(values) / len(values),
                'standard_units': ', '.join(list(set([x.standard_units for x in per_target_data])))
            })

    context = {'ligand_data': ligand_data, 'ligand': ligand_id}

    return render(request, 'ligand_details.html', context)


def TargetDetailsCompact(request, **kwargs):
    if 'slug' in kwargs:
        slug = kwargs['slug']
        if slug.count('_') == 0:
            ps = AssayExperiment.objects.filter(
                protein__family__parent__parent__parent__slug=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        elif slug.count('_') == 1 and len(slug) == 7:
            ps = AssayExperiment.objects.filter(
                protein__family__parent__parent__slug=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        elif slug.count('_') == 2:
            ps = AssayExperiment.objects.filter(
                protein__family__parent__slug=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        elif slug.count('_') == 3:
            ps = AssayExperiment.objects.filter(
                protein__family__slug=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        elif slug.count('_') == 1 and len(slug) != 7:
            ps = AssayExperiment.objects.filter(
                protein__entry_name=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')

        if slug.count('_') == 1 and len(slug) == 7:
            f = ProteinFamily.objects.get(slug=slug)
        else:
            f = slug

        context = {
            'target': f
        }
    else:
        simple_selection = request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)
        if selection.targets != []:
            prot_ids = [x.item.id for x in selection.targets]
            ps = AssayExperiment.objects.filter(
                protein__in=prot_ids, ligand__properities__web_links__web_resource__slug='chembl_ligand')
            context = {
                'target': ', '.join([x.item.entry_name for x in selection.targets])
            }

    ps = ps.prefetch_related(
        'protein', 'ligand__properities__web_links__web_resource', 'ligand__properities__vendors__vendor')
    d = {}
    for p in ps:
        if p.ligand not in d:
            d[p.ligand] = {}
        if p.protein not in d[p.ligand]:
            d[p.ligand][p.protein] = []
        d[p.ligand][p.protein].append(p)
    ligand_data = []
    for lig, records in d.items():

        links = lig.properities.web_links.all()
        chembl_id = [x for x in links if x.web_resource.slug ==
                     'chembl_ligand'][0].index

        vendors = lig.properities.vendors.all()
        purchasability = 'No'
        for v in vendors:
            if v.vendor.name not in ['ZINC', 'ChEMBL', 'BindingDB', 'SureChEMBL', 'eMolecules', 'MolPort', 'PubChem']:
                purchasability = 'Yes'

        for record, vals in records.items():
            per_target_data = vals
            protein_details = record

            """
            A dictionary of dictionaries with a list of values.
            Assay_type
            |
            ->  Standard_type [list of values]
            """
            tmp = defaultdict(list)
            tmp_count = 0
            for data_line in per_target_data:
                tmp["Bind" if data_line.assay_type == 'b' else "Funct"].append(
                    data_line.pchembl_value)
                tmp_count += 1

            # TEMPORARY workaround for handling string values
            values = [float(item) for item in itertools.chain(
                *tmp.values()) if float(item)]

            if len(values) > 0:
                ligand_data.append({
                    'ligand_id': chembl_id,
                    'protein_name': protein_details.entry_name,
                    'species': protein_details.species.common_name,
                    'record_count': tmp_count,
                    'assay_type': ', '.join(tmp.keys()),
                    'purchasability': purchasability,
                    # Flattened list of lists of dict keys:
                    'low_value': min(values),
                    'average_value': sum(values) / len(values),
                    'high_value': max(values),
                    'standard_units': ', '.join(list(set([x.standard_units for x in per_target_data]))),
                    'smiles': lig.properities.smiles,
                    'mw': lig.properities.mw,
                    'rotatable_bonds': lig.properities.rotatable_bonds,
                    'hdon': lig.properities.hdon,
                    'hacc': lig.properities.hacc,
                    'logp': lig.properities.logp,
                })
    context['ligand_data'] = ligand_data

    return render(request, 'target_details_compact.html', context)


def TargetDetails(request, **kwargs):

    if 'slug' in kwargs:
        slug = kwargs['slug']
        if slug.count('_') == 0:
            ps = AssayExperiment.objects.filter(
                protein__family__parent__parent__parent__slug=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        elif slug.count('_') == 1 and len(slug) == 7:
            ps = AssayExperiment.objects.filter(
                protein__family__parent__parent__slug=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        elif slug.count('_') == 2:
            ps = AssayExperiment.objects.filter(
                protein__family__parent__slug=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        elif slug.count('_') == 3:
            ps = AssayExperiment.objects.filter(
                protein__family__slug=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        elif slug.count('_') == 1 and len(slug) != 7:
            ps = AssayExperiment.objects.filter(
                protein__entry_name=slug, ligand__properities__web_links__web_resource__slug='chembl_ligand')

        if slug.count('_') == 1 and len(slug) == 7:
            f = ProteinFamily.objects.get(slug=slug)
        else:
            f = slug

        context = {
            'target': f
        }
    else:
        simple_selection = request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)
        if selection.targets != []:
            prot_ids = [x.item.id for x in selection.targets]
            ps = AssayExperiment.objects.filter(
                protein__in=prot_ids, ligand__properities__web_links__web_resource__slug='chembl_ligand')
            context = {
                'target': ', '.join([x.item.entry_name for x in selection.targets])
            }
    ps = ps.values('standard_type',
                   'standard_relation',
                   'standard_value',
                   'assay_description',
                   'assay_type',
                   # 'standard_units',
                   'pchembl_value',
                   'ligand__id',
                   'ligand__properities_id',
                   'ligand__properities__web_links__index',
                   # 'ligand__properities__vendors__vendor__name',
                   'protein__species__common_name',
                   'protein__entry_name',
                   'ligand__properities__mw',
                   'ligand__properities__logp',
                   'ligand__properities__rotatable_bonds',
                   'ligand__properities__smiles',
                   'ligand__properities__hdon',
                   'ligand__properities__hacc', 'protein'
                   ).annotate(num_targets=Count('protein__id', distinct=True))
    for record in ps:
        record['purchasability'] = 'Yes' if len(LigandVendorLink.objects.filter(lp=record['ligand__properities_id']).exclude(
            vendor__name__in=['ZINC', 'ChEMBL', 'BindingDB', 'SureChEMBL', 'eMolecules', 'MolPort', 'PubChem'])) > 0 else 'No'

    context['proteins'] = ps

    return render(request, 'target_details.html', context)


def TargetPurchasabilityDetails(request, **kwargs):

    simple_selection = request.session.get('selection', False)
    selection = Selection()
    if simple_selection:
        selection.importer(simple_selection)
    if selection.targets != []:
        prot_ids = [x.item.id for x in selection.targets]
        ps = AssayExperiment.objects.filter(
            protein__in=prot_ids, ligand__properities__web_links__web_resource__slug='chembl_ligand')
        context = {
            'target': ', '.join([x.item.entry_name for x in selection.targets])
        }

    ps = ps.values('standard_type',
                   'standard_relation',
                   'standard_value',
                   'assay_description',
                   'assay_type',
                   'standard_units',
                   'pchembl_value',
                   'ligand__id',
                   'ligand__properities_id',
                   'ligand__properities__web_links__index',
                   'ligand__properities__vendors__vendor__id',
                   'ligand__properities__vendors__vendor__name',
                   'protein__species__common_name',
                   'protein__entry_name',
                   'ligand__properities__mw',
                   'ligand__properities__logp',
                   'ligand__properities__rotatable_bonds',
                   'ligand__properities__smiles',
                   'ligand__properities__hdon',
                   'ligand__properities__hacc', 'protein'
                   ).annotate(num_targets=Count('protein__id', distinct=True))
    purchasable = []
    for record in ps:
        try:
            if record['ligand__properities__vendors__vendor__name'] in ['ZINC', 'ChEMBL', 'BindingDB', 'SureChEMBL', 'eMolecules', 'MolPort', 'PubChem', 'IUPHAR/BPS Guide to PHARMACOLOGY']:
                continue
            tmp = LigandVendorLink.objects.filter(
                vendor=record['ligand__properities__vendors__vendor__id'], lp=record['ligand__properities_id'])[0]
            record['vendor_id'] = tmp.vendor_external_id
            record['vendor_link'] = tmp.url
            purchasable.append(record)
        except:
            continue

    context['proteins'] = purchasable

    return render(request, 'target_purchasability_details.html', context)


class LigandStatistics(TemplateView):
    """
    Per class statistics of known ligands.
    """

    template_name = 'ligand_statistics.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # assays = AssayExperiment.objects.all().prefetch_related('protein__family__parent__parent__parent', 'protein__family')

        lig_count_dict = {}
        assays_lig = list(AssayExperiment.objects.all().values(
            'protein__family__parent__parent__parent__name').annotate(c=Count('ligand', distinct=True)))
        for a in assays_lig:
            lig_count_dict[a['protein__family__parent__parent__parent__name']] = a['c']
        target_count_dict = {}
        assays_target = list(AssayExperiment.objects.all().values(
            'protein__family__parent__parent__parent__name').annotate(c=Count('protein__family', distinct=True)))
        for a in assays_target:
            target_count_dict[a['protein__family__parent__parent__parent__name']] = a['c']

        prot_count_dict = {}
        proteins_count = list(Protein.objects.all().values(
            'family__parent__parent__parent__name').annotate(c=Count('family', distinct=True)))
        for pf in proteins_count:
            prot_count_dict[pf['family__parent__parent__parent__name']] = pf['c']

        classes = ProteinFamily.objects.filter(
            slug__in=['001', '002', '003', '004', '005', '006', '007'])  # ugly but fast

        ligands = []

        for fam in classes:
            if fam.name in lig_count_dict:
                lig_count = lig_count_dict[fam.name]
                target_count = target_count_dict[fam.name]
            else:
                lig_count = 0
                target_count = 0
            prot_count = prot_count_dict[fam.name]
            ligands.append({
                'name': fam.name.replace('Class',''),
                'num_ligands': lig_count,
                'avg_num_ligands': lig_count / prot_count,
                'target_percentage': target_count / prot_count * 100,
                'target_count': target_count
            })
        lig_count_total = sum([x['num_ligands'] for x in ligands])
        prot_count_total = Protein.objects.filter(
            family__slug__startswith='00').all().distinct('family').count()
        target_count_total = sum([x['target_count'] for x in ligands])
        lig_total = {
            'num_ligands': lig_count_total,
            'avg_num_ligands': lig_count_total / prot_count_total,
            'target_percentage': target_count_total / prot_count_total * 100,
            'target_count': target_count_total
        }
        # Elegant solution but kinda slow (6s querries):
        """
        ligands = AssayExperiment.objects.values(
            'protein__family__parent__parent__parent__name',
            'protein__family__parent__parent__parent',
            ).annotate(num_ligands=Count('ligand', distinct=True))
        for prot_class in ligands:
            class_subset = AssayExperiment.objects.filter(
                id=prot_class['protein__family__parent__parent__parent']).values(
                    'protein').annotate(
                        avg_num_ligands=Avg('ligand', distinct=True),
                        p_count=Count('protein')
                        )
            prot_class['avg_num_ligands']=class_subset[0]['avg_num_ligands']
            prot_class['p_count']=class_subset[0]['p_count']

        """
        context['ligands_total'] = lig_total
        context['ligands_by_class'] = ligands

        context['release_notes'] = ReleaseNotes.objects.all()[0]

        tree = PhylogeneticTreeGenerator()
        class_a_data = tree.get_tree_data(
            ProteinFamily.objects.get(name='Class A (Rhodopsin)'))
        context['class_a_options'] = deepcopy(tree.d3_options)
        context['class_a_options']['anchor'] = 'class_a'
        context['class_a_options']['leaf_offset'] = 50
        context['class_a_options']['label_free'] = []
        # section to remove Orphan from Class A tree and apply to a different tree
        whole_class_a = class_a_data.get_nodes_dict('ligands')
        for item in whole_class_a['children']:
            if item['name'] == 'Orphan':
                orphan_data = OrderedDict([('name', ''), ('value', 3000), ('color', ''), ('children',[item])])
                whole_class_a['children'].remove(item)
                break
        context['class_a'] = json.dumps(whole_class_a)
        class_b1_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class B1 (Secretin)'))
        context['class_b1_options'] = deepcopy(tree.d3_options)
        context['class_b1_options']['anchor'] = 'class_b1'
        context['class_b1_options']['branch_trunc'] = 60
        context['class_b1_options']['label_free'] = [1, ]
        context['class_b1'] = json.dumps(
            class_b1_data.get_nodes_dict('ligands'))
        class_b2_data = tree.get_tree_data(
            ProteinFamily.objects.get(name__startswith='Class B2 (Adhesion)'))
        context['class_b2_options'] = deepcopy(tree.d3_options)
        context['class_b2_options']['anchor'] = 'class_b2'
        context['class_b2_options']['label_free'] = [1, ]
        context['class_b2'] = json.dumps(
            class_b2_data.get_nodes_dict('ligands'))
        class_c_data = tree.get_tree_data(
            ProteinFamily.objects.get(name__startswith='Class C (Glutamate)'))
        context['class_c_options'] = deepcopy(tree.d3_options)
        context['class_c_options']['anchor'] = 'class_c'
        context['class_c_options']['branch_trunc'] = 50
        context['class_c_options']['label_free'] = [1, ]
        context['class_c'] = json.dumps(class_c_data.get_nodes_dict('ligands'))
        class_f_data = tree.get_tree_data(
            ProteinFamily.objects.get(name__startswith='Class F (Frizzled)'))
        context['class_f_options'] = deepcopy(tree.d3_options)
        context['class_f_options']['anchor'] = 'class_f'
        context['class_f_options']['label_free'] = [1, ]
        context['class_f'] = json.dumps(class_f_data.get_nodes_dict('ligands'))
        class_t2_data = tree.get_tree_data(
            ProteinFamily.objects.get(name__startswith='Class T (Taste 2)'))
        context['class_t2_options'] = deepcopy(tree.d3_options)
        context['class_t2_options']['anchor'] = 'class_t2'
        context['class_t2_options']['label_free'] = [1,]
        context['class_t2'] = json.dumps(class_t2_data.get_nodes_dict('ligands'))
        # definition of the class a orphan tree
        context['orphan_options'] = deepcopy(tree.d3_options)
        context['orphan_options']['anchor'] = 'orphan'
        context['orphan_options']['label_free'] = [1,]
        context['orphan'] = json.dumps(orphan_data)

        whole_receptors = Protein.objects.prefetch_related("family", "family__parent__parent__parent")
        whole_rec_dict = {}
        for rec in whole_receptors:
            rec_uniprot = rec.entry_short()
            rec_iuphar = rec.family.name.replace("receptor", '').replace("<i>","").replace("</i>","").strip()
            whole_rec_dict[rec_uniprot] = [rec_iuphar]
        context["whole_receptors"] = json.dumps(whole_rec_dict)
        context["render"] = "not_bias"
        return context


class LigandBiasStatistics(TemplateView):
    """
    Per class statistics of known ligands.
    """

    template_name = 'ligand_statistics.html'

    def get_context_data (self, **kwargs):

        context = super().get_context_data(**kwargs)
        # assays = AnalyzedExperiment.objects.all().prefetch_related('receptor__family__parent__parent__parent', 'receptor__family')

        lig_count_dict = {}
        assays_lig = list(AnalyzedExperiment.objects.all().values('receptor__family__parent__parent__parent__name').annotate(c=Count('ligand_id',distinct=True)))
        for a in assays_lig:
            lig_count_dict[a['receptor__family__parent__parent__parent__name']] = a['c']
        target_count_dict = {}
        assays_target = list(AnalyzedExperiment.objects.all().values('receptor__family__parent__parent__parent__name').annotate(c=Count('receptor__family',distinct=True)))
        for a in assays_target:
            target_count_dict[a['receptor__family__parent__parent__parent__name']] = a['c']

        prot_count_dict = {}
        proteins_count = list(Protein.objects.all().values('family__parent__parent__parent__name').annotate(c=Count('family',distinct=True)))
        for pf in proteins_count:
            prot_count_dict[pf['family__parent__parent__parent__name']] = pf['c']

        classes = ProteinFamily.objects.filter(slug__in=['001', '002', '003', '004', '005', '006', '007']) #ugly but fast
        proteins = Protein.objects.all().prefetch_related('family__parent__parent__parent')
        ligands = []

        for fam in classes:
            if fam.name in lig_count_dict:
                lig_count = lig_count_dict[fam.name]
                target_count = target_count_dict[fam.name]
            else:
                lig_count = 0
                target_count = 0
            prot_count = prot_count_dict[fam.name]
            ligands.append({
                'name': fam.name.replace('Class',''),
                'num_ligands': lig_count,
                'avg_num_ligands': lig_count/prot_count,
                'target_percentage': target_count/prot_count*100,
                'target_count': target_count
                })
        lig_count_total = sum([x['num_ligands'] for x in ligands])
        prot_count_total = Protein.objects.filter(family__slug__startswith='00').all().distinct('family').count()
        target_count_total = sum([x['target_count'] for x in ligands])
        lig_total = {
            'num_ligands': lig_count_total,
            'avg_num_ligands': lig_count_total/prot_count_total,
            'target_percentage': target_count_total/prot_count_total*100,
            'target_count': target_count_total
            }
        #Elegant solution but kinda slow (6s querries):
        """
        ligands = AnalyzedExperiment.objects.values(
            'receptor__family__parent__parent__parent__name',
            'receptor__family__parent__parent__parent',
            ).annotate(num_ligands=Count('ligand', distinct=True))
        for prot_class in ligands:
            class_subset = AnalyzedExperiment.objects.filter(
                id=prot_class['receptor__family__parent__parent__parent']).values(
                    'receptor').annotate(
                        avg_num_ligands=Avg('ligand', distinct=True),
                        p_count=Count('receptor')
                        )
            prot_class['avg_num_ligands']=class_subset[0]['avg_num_ligands']
            prot_class['p_count']=class_subset[0]['p_count']

        """
        context['ligands_total'] = lig_total
        context['ligands_by_class'] = ligands

        context['release_notes'] = ReleaseNotes.objects.all()[0]

        tree = PhylogeneticTreeGenerator()
        class_a_data = tree.get_tree_data(ProteinFamily.objects.get(name='Class A (Rhodopsin)'))
        context['class_a_options'] = deepcopy(tree.d3_options)
        context['class_a_options']['anchor'] = 'class_a'
        context['class_a_options']['leaf_offset'] = 50
        context['class_a_options']['label_free'] = []
        # section to remove Orphan from Class A tree and apply to a different tree
        whole_class_a = class_a_data.get_nodes_dict('ligand_bias')
        for item in whole_class_a['children']:
            if item['name'] == 'Orphan':
                orphan_data = OrderedDict([('name', ''), ('value', 3000), ('color', ''), ('children',[item])])
                whole_class_a['children'].remove(item)
                break
        context['class_a'] = json.dumps(whole_class_a)
        class_b1_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class B1 (Secretin)'))
        context['class_b1_options'] = deepcopy(tree.d3_options)
        context['class_b1_options']['anchor'] = 'class_b1'
        context['class_b1_options']['branch_trunc'] = 60
        context['class_b1_options']['label_free'] = [1,]
        context['class_b1'] = json.dumps(class_b1_data.get_nodes_dict('ligand_bias'))
        class_b2_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class B2 (Adhesion)'))
        context['class_b2_options'] = deepcopy(tree.d3_options)
        context['class_b2_options']['anchor'] = 'class_b2'
        context['class_b2_options']['label_free'] = [1,]
        context['class_b2'] = json.dumps(class_b2_data.get_nodes_dict('ligand_bias'))
        class_c_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class C (Glutamate)'))
        context['class_c_options'] = deepcopy(tree.d3_options)
        context['class_c_options']['anchor'] = 'class_c'
        context['class_c_options']['branch_trunc'] = 50
        context['class_c_options']['label_free'] = [1,]
        context['class_c'] = json.dumps(class_c_data.get_nodes_dict('ligand_bias'))
        class_f_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class F (Frizzled)'))
        context['class_f_options'] = deepcopy(tree.d3_options)
        context['class_f_options']['anchor'] = 'class_f'
        context['class_f_options']['label_free'] = [1,]
        context['class_f'] = json.dumps(class_f_data.get_nodes_dict('ligand_bias'))
        class_t2_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class T (Taste 2)'))
        context['class_t2_options'] = deepcopy(tree.d3_options)
        context['class_t2_options']['anchor'] = 'class_t2'
        context['class_t2_options']['label_free'] = [1,]
        context['class_t2'] = json.dumps(class_t2_data.get_nodes_dict('ligand_bias'))
        # definition of the class a orphan tree
        context['orphan_options'] = deepcopy(tree.d3_options)
        context['orphan_options']['anchor'] = 'orphan'
        context['orphan_options']['label_free'] = [1,]
        context['orphan'] = json.dumps(orphan_data)

        whole_receptors = Protein.objects.prefetch_related("family", "family__parent__parent__parent").filter(sequence_type__slug="wt", family__slug__startswith="00")
        whole_rec_dict = {}
        for rec in whole_receptors:
            rec_uniprot = rec.entry_short()
            rec_iuphar = rec.family.name.replace("receptor", '').replace("<i>","").replace("</i>","").strip()
            whole_rec_dict[rec_uniprot] = [rec_iuphar]
        context["whole_receptors"] = json.dumps(whole_rec_dict)
        context["render"] = "bias"
        return context

class ExperimentEntryView(DetailView):
    context_object_name = 'experiment'
    model = AnalyzedExperiment
    template_name = 'biased_experiment_data.html'

# Biased pathways part


class PathwayExperimentEntryView(DetailView):
    context_object_name = 'experiment'
    model = BiasedPathways
    template_name = 'biased_pathways_data.html'


@csrf_exempt
def test_link(request):
    request.session['ids'] = ''
    # try:
    request.session['ids']
    if request.POST.get('action') == 'post':
        request.session.modified = True
        data = request.POST.get('ids')
        data = filter(lambda char: char not in " \"?.!/;:[]", data)
        datum = "".join(data)
        request.session['ids'] = datum
        request.session.set_expiry(15)

    return HttpResponse(request)


class BiasVendorBrowser(TemplateView):

    template_name = 'biased_ligand_vendor.html'

    def get_context_data(self, **kwargs):
        # try:
        context = dict()
        datum = self.request.session.get('ids')

        self.request.session.modified = True
        rd = list()
        for i in datum.split(','):
            ligand = Ligand.objects.filter(id=i)
            ligand = ligand.get()
            links = LigandVendorLink.objects.filter(
                lp=ligand.properities_id).prefetch_related('lp', 'vendor')
            for x in links:
                if x.vendor.name not in ['ZINC', 'ChEMBL', 'BindingDB', 'SureChEMBL', 'eMolecules', 'MolPort', 'PubChem']:
                    temp = dict()
                    vendor = LigandVendors.objects.filter(id=x.vendor_id)
                    vendor = vendor.get()
                    temp['ligand'] = ligand
                    temp['url'] = x.url
                    temp['vendor_id'] = x.vendor_external_id
                    temp['vendor'] = vendor

                    rd.append(temp)
            context['data'] = rd
        del self.request.session['ids']
        return context
        # except:
        #     raise

# pylint: disable=F405
class BiasAPI(generics.ListAPIView):
    serializer_class = AnalyzedExperimentSerializer
    filter_backends = (DatatablesFilterBackend,)
    filterset_class = AnalyzedExperimentFilter

    @staticmethod
    def get_queryset():
        assay_qs = AnalyzedAssay.objects.filter(
            order_no__lte=5,
            assay_description__isnull=True,
            experiment=OuterRef('pk'),
        ).order_by('order_no')

        queryset = AnalyzedExperiment.objects.filter(
            source='different_family',
        ).prefetch_related(
            'analyzed_data', 'ligand', 'ligand__reference_ligand', 'reference_ligand',
            'endogenous_ligand', 'ligand__properities', 'receptor', 'receptor', 'receptor__family',
            'receptor__family__parent', 'receptor__family__parent__parent__parent',
            'receptor__family__parent__parent', 'receptor__family', 'receptor__species',
            'publication', 'publication__web_link', 'publication__web_link__web_resource',
            'publication__journal', 'ligand__ref_ligand_bias_analyzed',
            'analyzed_data__emax_ligand_reference'
        ).annotate(
            # pathways
            pathways_p1=Subquery(assay_qs.values('family')[:1]),
            pathways_p2=Subquery(assay_qs.values('family')[1:2]),
            pathways_p3=Subquery(assay_qs.values('family')[2:3]),
            pathways_p4=Subquery(assay_qs.values('family')[3:4]),
            pathways_p5=Subquery(assay_qs.values('family')[4:5]),

            # t_factor
            opmodel_p2_p1=Subquery(assay_qs.values('t_factor')[1:2]),
            opmodel_p3_p1=Subquery(assay_qs.values('t_factor')[2:3]),
            opmodel_p4_p1=Subquery(assay_qs.values('t_factor')[3:4]),
            opmodel_p5_p1=Subquery(assay_qs.values('t_factor')[4:5]),

            # log bias factor
            lbf_p2_p1=Subquery(assay_qs.values('log_bias_factor')[1:2]),
            lbf_p3_p1=Subquery(assay_qs.values('log_bias_factor')[2:3]),
            lbf_p4_p1=Subquery(assay_qs.values('log_bias_factor')[3:4]),
            lbf_p5_p1=Subquery(assay_qs.values('log_bias_factor')[4:5]),

            # Potency ratio
            potency_p2_p1=Subquery(assay_qs.values('potency')[1:2]),
            potency_p3_p1=Subquery(assay_qs.values('potency')[2:3]),
            potency_p4_p1=Subquery(assay_qs.values('potency')[3:4]),
            potency_p5_p1=Subquery(assay_qs.values('potency')[4:5]),

            # Potency
            activity_p1=Subquery(assay_qs.values(
                'quantitive_activity_initial')[:1]),
            activity_p2=Subquery(assay_qs.values(
                'quantitive_activity_initial')[1:2]),
            activity_p3=Subquery(assay_qs.values(
                'quantitive_activity_initial')[2:3]),
            activity_p4=Subquery(assay_qs.values(
                'quantitive_activity_initial')[3:4]),
            activity_p5=Subquery(assay_qs.values(
                'quantitive_activity_initial')[4:5]),

            # quality_activity
            quality_activity_p1=Subquery(assay_qs.values('qualitative_activity')[:1]),
            quality_activity_p2=Subquery(assay_qs.values('qualitative_activity')[1:2]),
            quality_activity_p3=Subquery(assay_qs.values('qualitative_activity')[2:3]),
            quality_activity_p4=Subquery(assay_qs.values('qualitative_activity')[3:4]),
            quality_activity_p5=Subquery(assay_qs.values('qualitative_activity')[4:5]),
            # quality_activity
            standard_type_p1=Subquery(assay_qs.values('quantitive_measure_type')[:1]),
            standard_type_p2=Subquery(assay_qs.values('quantitive_measure_type')[1:2]),
            standard_type_p3=Subquery(assay_qs.values('quantitive_measure_type')[2:3]),
            standard_type_p4=Subquery(assay_qs.values('quantitive_measure_type')[3:4]),
            standard_type_p5=Subquery(assay_qs.values('quantitive_measure_type')[4:5]),

            # E Max
            emax_p1=Subquery(assay_qs.values('quantitive_efficacy')[:1]),
            emax_p2=Subquery(assay_qs.values('quantitive_efficacy')[1:2]),
            emax_p3=Subquery(assay_qs.values('quantitive_efficacy')[2:3]),
            emax_p4=Subquery(assay_qs.values('quantitive_efficacy')[3:4]),
            emax_p5=Subquery(assay_qs.values('quantitive_efficacy')[4:5]),

            # T factor
            tfactor_p1=Subquery(assay_qs.values('t_value')[:1]),
            tfactor_p2=Subquery(assay_qs.values('t_value')[1:2]),
            tfactor_p3=Subquery(assay_qs.values('t_value')[2:3]),
            tfactor_p4=Subquery(assay_qs.values('t_value')[3:4]),
            tfactor_p5=Subquery(assay_qs.values('t_value')[4:5]),

            # Assay
            assay_p1=Subquery(assay_qs.values('assay_type')[:1]),
            assay_p2=Subquery(assay_qs.values('assay_type')[1:2]),
            assay_p3=Subquery(assay_qs.values('assay_type')[2:3]),
            assay_p4=Subquery(assay_qs.values('assay_type')[3:4]),
            assay_p5=Subquery(assay_qs.values('assay_type')[4:5]),

            # Cell Line
            cell_p1=Subquery(assay_qs.values('cell_line')[:1]),
            cell_p2=Subquery(assay_qs.values('cell_line')[1:2]),
            cell_p3=Subquery(assay_qs.values('cell_line')[2:3]),
            cell_p4=Subquery(assay_qs.values('cell_line')[3:4]),
            cell_p5=Subquery(assay_qs.values('cell_line')[4:5]),

            # Time
            time_p1=Subquery(assay_qs.values('assay_time_resolved')[:1]),
            time_p2=Subquery(assay_qs.values('assay_time_resolved')[1:2]),
            time_p3=Subquery(assay_qs.values('assay_time_resolved')[2:3]),
            time_p4=Subquery(assay_qs.values('assay_time_resolved')[3:4]),
            time_p5=Subquery(assay_qs.values('assay_time_resolved')[4:5]),
        )

        return queryset

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)

        base_queryset = self.get_queryset()
        queryset = self.filter_queryset(base_queryset)

        response.data['filterOptions'] = {
            'class': [
                {'value': receptor_id, 'label': receptor_name.replace('Class', '').strip()}
                for receptor_id, receptor_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor__family__parent__parent__parent_id',
                    'receptor__family__parent__parent__parent__name',
                ).order_by('receptor__family__parent__parent__parent_id').distinct()
            ],
            'receptor': [
                {'value': receptor_id, 'label': receptor_name.replace('Class', '').strip()}
                for receptor_id, receptor_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor__family__parent_id', 'receptor__family__parent__name',
                ).order_by('receptor__family__parent_id').distinct()
            ],
            'uniprot': [
                {'value': receptor_id, 'label': receptor_name.split('_')[0].upper()}
                for receptor_id, receptor_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor_id', 'receptor__entry_name',
                ).order_by('receptor_id').distinct()
            ],
            'iuphar': [
                {
                    'value': receptor_id,
                    'label': receptor_name.split(' ', 1)[0].split('-adrenoceptor', 1)[0].strip()
                }
                for receptor_id, receptor_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor_id', 'receptor__name',
                ).order_by('receptor_id').distinct()
            ],
            'species': [
                {'value': specie_id, 'label': common_name}
                for specie_id, common_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor__species_id', 'receptor__species__common_name',
                ).order_by('receptor__species_id').distinct()
            ],
            'endogenous_ligand': [
                {'value': endogenous_ligand_id, 'label': endogenous_ligand_name}
                for endogenous_ligand_id, endogenous_ligand_name in queryset.exclude(
                    endogenous_ligand__isnull=True,
                ).values_list(
                    'endogenous_ligand_id', 'endogenous_ligand__name',
                ).order_by('endogenous_ligand_id').distinct()
            ],
            'reference_ligand': [
                {'value': reference_ligand_id, 'label': reference_ligand_name}
                for reference_ligand_id, reference_ligand_name in queryset.exclude(
                    reference_ligand__isnull=True
                ).values_list(
                    'reference_ligand_id', 'reference_ligand__name',
                ).order_by('reference_ligand_id').distinct()
            ],
            'ligand': [
                {'value': ligand_id, 'label': ligand_name}
                for ligand_id, ligand_name in queryset.exclude(
                    ligand__isnull=True
                ).values_list(
                    'ligand_id', 'ligand__name',
                ).order_by('ligand_id').distinct()
            ],
            'primary': [
                {'value': primary.replace(' ', '_'), 'label': primary.replace(' family,', '')}
                for primary in queryset.exclude(
                    models.Q(primary__isnull=True) | models.Q(primary='')
                ).values_list(
                    'primary', flat=True
                ).order_by('primary').distinct()
            ],
            'secondary': [
                {'value': secondary.replace(' ', '_'), 'label': secondary.replace(' family,', '')}
                for secondary in queryset.exclude(
                    models.Q(secondary__isnull=True) | models.Q(secondary='')
                ).values_list(
                    'secondary', flat=True
                ).order_by('secondary').distinct()
            ],
            'pathways_p1': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p1__isnull=True) | models.Q(pathways_p1="")
                ).values_list(
                    'pathways_p1', flat=True
                ).order_by('pathways_p1').distinct()
            ],
            'pathways_p2': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p2__isnull=True) | models.Q(pathways_p2="")
                ).values_list(
                    'pathways_p2', flat=True
                ).order_by('pathways_p2').distinct()
            ],
            'pathways_p3': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p3__isnull=True) | models.Q(pathways_p3="")
                ).values_list(
                    'pathways_p3', flat=True
                ).order_by('pathways_p3').distinct()
            ],
            'pathways_p4': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p4__isnull=True) | models.Q(pathways_p4="")
                ).values_list(
                    'pathways_p4', flat=True
                ).order_by('pathways_p4').distinct()
            ],
            'pathways_p5': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p5__isnull=True) | models.Q(
                        pathways_p5="")
                ).values_list(
                    'pathways_p5', flat=True
                ).order_by('pathways_p5').distinct()
            ],
            'assay_p1': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p1__isnull=True) | models.Q(assay_p1="")
                ).values_list(
                    'assay_p1', flat=True
                ).order_by('assay_p1').distinct()
            ],
            'assay_p2': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p2__isnull=True) | models.Q(assay_p2="")
                ).values_list(
                    'assay_p2', flat=True
                ).order_by('assay_p2').distinct()
            ],
            'assay_p3': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p3__isnull=True) | models.Q(assay_p3="")
                ).values_list(
                    'assay_p3', flat=True
                ).order_by('assay_p3').distinct()
            ],
            'assay_p4': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p4__isnull=True) | models.Q(assay_p4="")
                ).values_list(
                    'assay_p4', flat=True
                ).order_by('assay_p4').distinct()
            ],
            'assay_p5': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p5__isnull=True) | models.Q(assay_p5="")
                ).values_list(
                    'assay_p5', flat=True
                ).order_by('assay_p5').distinct()
            ],
            'cell_p1': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p1__isnull=True) | models.Q(cell_p1="")
                ).values_list(
                    'cell_p1', flat=True
                ).order_by('cell_p1').distinct()
            ],
            'cell_p2': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p2__isnull=True) | models.Q(cell_p2="")
                ).values_list(
                    'cell_p2', flat=True
                ).order_by('cell_p2').distinct()
            ],
            'cell_p3': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p3__isnull=True) | models.Q(cell_p3="")
                ).values_list(
                    'cell_p3', flat=True
                ).order_by('cell_p3').distinct()
            ],
            'cell_p4': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p4__isnull=True) | models.Q(cell_p4="")
                ).values_list(
                    'cell_p4', flat=True
                ).order_by('cell_p4').distinct()
            ],
            'cell_p5': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p5__isnull=True) | models.Q(cell_p5="")
                ).values_list(
                    'cell_p5', flat=True
                ).order_by('cell_p5').distinct()
            ],
            'time_p1': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p1__isnull=True) | models.Q(time_p1="")
                ).values_list(
                    'time_p1', flat=True
                ).order_by('time_p1').distinct()
            ],
            'time_p2': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p2__isnull=True) | models.Q(time_p2="")
                ).values_list(
                    'time_p2', flat=True
                ).order_by('time_p2').distinct()
            ],
            'time_p3': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p3__isnull=True) | models.Q(time_p3="")
                ).values_list(
                    'time_p3', flat=True
                ).order_by('time_p3').distinct()
            ],
            'time_p4': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p4__isnull=True) | models.Q(time_p4="")
                ).values_list(
                    'time_p4', flat=True
                ).order_by('time_p4').distinct()
            ],
            'time_p5': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p5__isnull=True) | models.Q(time_p5="")
                ).values_list(
                    'time_p5', flat=True
                ).order_by('time_p5').distinct()
            ],
            'authors': [
                {'value': authors, 'label': authors}
                for authors in queryset.exclude(
                    publication__authors__isnull=True
                ).values_list(
                    'publication__authors', flat=True
                ).order_by('publication__authors').distinct()
            ],
            'doi_reference': [
                {'value': web_link_id, 'label': web_link_index}
                for web_link_id, web_link_index in queryset.exclude(
                    publication__authors__isnull=True
                ).values_list(
                    'publication__web_link_id', 'publication__web_link__index',
                ).order_by('publication__web_link_id').distinct()
            ],
        }
        return response

class GBiasAPI(generics.ListAPIView):
    serializer_class = AnalyzedExperimentSerializer
    filter_backends = (DatatablesFilterBackend,)
    filterset_class = AnalyzedExperimentFilter

    def get_queryset(self):
        assay_qs = AnalyzedAssay.objects.filter(
            order_no__lte=5,
            assay_description__isnull=True,
            experiment=OuterRef('pk'),
        ).order_by('order_no')

        queryset = AnalyzedExperiment.objects.filter(
            source='same_family',
        ).prefetch_related(
            'analyzed_data', 'ligand', 'ligand__reference_ligand', 'reference_ligand',
            'endogenous_ligand', 'ligand__properities', 'receptor', 'receptor', 'receptor__family',
            'receptor__family__parent', 'receptor__family__parent__parent__parent',
            'receptor__family__parent__parent', 'receptor__family', 'receptor__species',
            'publication', 'publication__web_link', 'publication__web_link__web_resource',
            'publication__journal', 'ligand__ref_ligand_bias_analyzed',
            'analyzed_data__emax_ligand_reference'
            ).annotate(
                # pathways
                pathways_p1=Subquery(assay_qs.values('signalling_protein')[:1]),
                pathways_p2=Subquery(assay_qs.values('signalling_protein')[1:2]),
                pathways_p3=Subquery(assay_qs.values('signalling_protein')[2:3]),
                pathways_p4=Subquery(assay_qs.values('signalling_protein')[3:4]),
                pathways_p5=Subquery(assay_qs.values('signalling_protein')[4:5]),

                # t_factor
                opmodel_p2_p1=Subquery(assay_qs.values('t_factor')[1:2]),
                opmodel_p3_p1=Subquery(assay_qs.values('t_factor')[2:3]),
                opmodel_p4_p1=Subquery(assay_qs.values('t_factor')[3:4]),
                opmodel_p5_p1=Subquery(assay_qs.values('t_factor')[4:5]),

                # log bias factor
                lbf_p2_p1=Subquery(assay_qs.values('log_bias_factor')[1:2]),
                lbf_p3_p1=Subquery(assay_qs.values('log_bias_factor')[2:3]),
                lbf_p4_p1=Subquery(assay_qs.values('log_bias_factor')[3:4]),
                lbf_p5_p1=Subquery(assay_qs.values('log_bias_factor')[4:5]),

                # Potency ratio
                potency_p2_p1=Subquery(assay_qs.values('potency')[1:2]),
                potency_p3_p1=Subquery(assay_qs.values('potency')[2:3]),
                potency_p4_p1=Subquery(assay_qs.values('potency')[3:4]),
                potency_p5_p1=Subquery(assay_qs.values('potency')[4:5]),

                # Potency
                activity_p1=Subquery(assay_qs.values(
                    'quantitive_activity_initial')[:1]),
                activity_p2=Subquery(assay_qs.values(
                    'quantitive_activity_initial')[1:2]),
                activity_p3=Subquery(assay_qs.values(
                    'quantitive_activity_initial')[2:3]),
                activity_p4=Subquery(assay_qs.values(
                    'quantitive_activity_initial')[3:4]),
                activity_p5=Subquery(assay_qs.values(
                    'quantitive_activity_initial')[4:5]),

                # quality_activity
                quality_activity_p1=Subquery(assay_qs.values('qualitative_activity')[:1]),
                quality_activity_p2=Subquery(assay_qs.values('qualitative_activity')[1:2]),
                quality_activity_p3=Subquery(assay_qs.values('qualitative_activity')[2:3]),
                quality_activity_p4=Subquery(assay_qs.values('qualitative_activity')[3:4]),
                quality_activity_p5=Subquery(assay_qs.values('qualitative_activity')[4:5]),
                # quality_activity
                standard_type_p1=Subquery(assay_qs.values('quantitive_measure_type')[:1]),
                standard_type_p2=Subquery(assay_qs.values('quantitive_measure_type')[1:2]),
                standard_type_p3=Subquery(assay_qs.values('quantitive_measure_type')[2:3]),
                standard_type_p4=Subquery(assay_qs.values('quantitive_measure_type')[3:4]),
                standard_type_p5=Subquery(assay_qs.values('quantitive_measure_type')[4:5]),

                # E Max
                emax_p1=Subquery(assay_qs.values('quantitive_efficacy')[:1]),
                emax_p2=Subquery(assay_qs.values('quantitive_efficacy')[1:2]),
                emax_p3=Subquery(assay_qs.values('quantitive_efficacy')[2:3]),
                emax_p4=Subquery(assay_qs.values('quantitive_efficacy')[3:4]),
                emax_p5=Subquery(assay_qs.values('quantitive_efficacy')[4:5]),

                # T factor
                tfactor_p1=Subquery(assay_qs.values('t_value')[:1]),
                tfactor_p2=Subquery(assay_qs.values('t_value')[1:2]),
                tfactor_p3=Subquery(assay_qs.values('t_value')[2:3]),
                tfactor_p4=Subquery(assay_qs.values('t_value')[3:4]),
                tfactor_p5=Subquery(assay_qs.values('t_value')[4:5]),

                # Assay
                assay_p1=Subquery(assay_qs.values('assay_type')[:1]),
                assay_p2=Subquery(assay_qs.values('assay_type')[1:2]),
                assay_p3=Subquery(assay_qs.values('assay_type')[2:3]),
                assay_p4=Subquery(assay_qs.values('assay_type')[3:4]),
                assay_p5=Subquery(assay_qs.values('assay_type')[4:5]),

                # Cell Line
                cell_p1=Subquery(assay_qs.values('cell_line')[:1]),
                cell_p2=Subquery(assay_qs.values('cell_line')[1:2]),
                cell_p3=Subquery(assay_qs.values('cell_line')[2:3]),
                cell_p4=Subquery(assay_qs.values('cell_line')[3:4]),
                cell_p5=Subquery(assay_qs.values('cell_line')[4:5]),

                # Time
                time_p1=Subquery(assay_qs.values('assay_time_resolved')[:1]),
                time_p2=Subquery(assay_qs.values('assay_time_resolved')[1:2]),
                time_p3=Subquery(assay_qs.values('assay_time_resolved')[2:3]),
                time_p4=Subquery(assay_qs.values('assay_time_resolved')[3:4]),
                time_p5=Subquery(assay_qs.values('assay_time_resolved')[4:5]),
            )

        return queryset

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)

        base_queryset = self.get_queryset()
        queryset = self.filter_queryset(base_queryset)

        response.data['filterOptions'] = {
            'class': [
                {'value': receptor_id, 'label': receptor_name.replace('Class', '').strip()}
                for receptor_id, receptor_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor__family__parent__parent__parent_id',
                    'receptor__family__parent__parent__parent__name',
                ).order_by('receptor__family__parent__parent__parent_id').distinct()
            ],
            'receptor': [
                {'value': receptor_id, 'label': receptor_name.replace('Class', '').strip()}
                for receptor_id, receptor_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor__family__parent_id', 'receptor__family__parent__name',
                ).order_by('receptor__family__parent_id').distinct()
            ],
            'uniprot': [
                {'value': receptor_id, 'label': receptor_name.split('_')[0].upper()}
                for receptor_id, receptor_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor_id', 'receptor__entry_name',
                ).order_by('receptor_id').distinct()
            ],
            'iuphar': [
                {
                    'value': receptor_id,
                    'label': receptor_name.split(' ', 1)[0].split('-adrenoceptor', 1)[0].strip()
                }
                for receptor_id, receptor_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor_id', 'receptor__name',
                ).order_by('receptor_id').distinct()
            ],
            'species': [
                {'value': specie_id, 'label': common_name}
                for specie_id, common_name in queryset.exclude(
                    receptor__isnull=True
                ).values_list(
                    'receptor__species_id', 'receptor__species__common_name',
                ).order_by('receptor__species_id').distinct()
            ],
            'endogenous_ligand': [
                {'value': endogenous_ligand_id, 'label': endogenous_ligand_name}
                for endogenous_ligand_id, endogenous_ligand_name in queryset.exclude(
                    endogenous_ligand__isnull=True,
                ).values_list(
                    'endogenous_ligand_id', 'endogenous_ligand__name',
                ).order_by('endogenous_ligand_id').distinct()
            ],
            'reference_ligand': [
                {'value': reference_ligand_id, 'label': reference_ligand_name}
                for reference_ligand_id, reference_ligand_name in queryset.exclude(
                    reference_ligand__isnull=True
                ).values_list(
                    'reference_ligand_id', 'reference_ligand__name',
                ).order_by('reference_ligand_id').distinct()
            ],
            'ligand': [
                {'value': ligand_id, 'label': ligand_name}
                for ligand_id, ligand_name in queryset.exclude(
                    ligand__isnull=True
                ).values_list(
                    'ligand_id', 'ligand__name',
                ).order_by('ligand_id').distinct()
            ],
            'primary': [
                {'value': primary.replace(' ', '_'), 'label': primary.replace(' family,', '')}
                for primary in queryset.exclude(
                    models.Q(primary__isnull=True) | models.Q(primary='')
                ).values_list(
                    'primary', flat=True
                ).order_by('primary').distinct()
            ],
            'secondary': [
                {'value': secondary.replace(' ', '_'), 'label': secondary.replace(' family,', '')}
                for secondary in queryset.exclude(
                    models.Q(secondary__isnull=True) | models.Q(secondary='')
                ).values_list(
                    'secondary', flat=True
                ).order_by('secondary').distinct()
            ],
            'pathways_p1': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p1__isnull=True) | models.Q(pathways_p1="")
                ).values_list(
                    'pathways_p1', flat=True
                ).order_by('pathways_p1').distinct()
            ],
            'pathways_p2': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p2__isnull=True) | models.Q(pathways_p2="")
                ).values_list(
                    'pathways_p2', flat=True
                ).order_by('pathways_p2').distinct()
            ],
            'pathways_p3': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p3__isnull=True) | models.Q(pathways_p3="")
                ).values_list(
                    'pathways_p3', flat=True
                ).order_by('pathways_p3').distinct()
            ],
            'pathways_p4': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p4__isnull=True) | models.Q(pathways_p4="")
                ).values_list(
                    'pathways_p4', flat=True
                ).order_by('pathways_p4').distinct()
            ],
            'pathways_p5': [
                {'value': pathways, 'label': pathways}
                for pathways in queryset.exclude(
                    models.Q(pathways_p5__isnull=True) | models.Q(
                        pathways_p5="")
                ).values_list(
                    'pathways_p5', flat=True
                ).order_by('pathways_p5').distinct()
            ],
            'assay_p1': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p1__isnull=True) | models.Q(assay_p1="")
                ).values_list(
                    'assay_p1', flat=True
                ).order_by('assay_p1').distinct()
            ],
            'assay_p2': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p2__isnull=True) | models.Q(assay_p2="")
                ).values_list(
                    'assay_p2', flat=True
                ).order_by('assay_p2').distinct()
            ],
            'assay_p3': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p3__isnull=True) | models.Q(assay_p3="")
                ).values_list(
                    'assay_p3', flat=True
                ).order_by('assay_p3').distinct()
            ],
            'assay_p4': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p4__isnull=True) | models.Q(assay_p4="")
                ).values_list(
                    'assay_p4', flat=True
                ).order_by('assay_p4').distinct()
            ],
            'assay_p5': [
                {'value': assay, 'label': assay}
                for assay in queryset.exclude(
                    models.Q(assay_p5__isnull=True) | models.Q(assay_p5="")
                ).values_list(
                    'assay_p5', flat=True
                ).order_by('assay_p5').distinct()
            ],
            'cell_p1': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p1__isnull=True) | models.Q(cell_p1="")
                ).values_list(
                    'cell_p1', flat=True
                ).order_by('cell_p1').distinct()
            ],
            'cell_p2': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p2__isnull=True) | models.Q(cell_p2="")
                ).values_list(
                    'cell_p2', flat=True
                ).order_by('cell_p2').distinct()
            ],
            'cell_p3': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p3__isnull=True) | models.Q(cell_p3="")
                ).values_list(
                    'cell_p3', flat=True
                ).order_by('cell_p3').distinct()
            ],
            'cell_p4': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p4__isnull=True) | models.Q(cell_p4="")
                ).values_list(
                    'cell_p4', flat=True
                ).order_by('cell_p4').distinct()
            ],
            'cell_p5': [
                {'value': cell, 'label': cell}
                for cell in queryset.exclude(
                    models.Q(cell_p5__isnull=True) | models.Q(cell_p5="")
                ).values_list(
                    'cell_p5', flat=True
                ).order_by('cell_p5').distinct()
            ],
            'time_p1': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p1__isnull=True) | models.Q(time_p1="")
                ).values_list(
                    'time_p1', flat=True
                ).order_by('time_p1').distinct()
            ],
            'time_p2': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p2__isnull=True) | models.Q(time_p2="")
                ).values_list(
                    'time_p2', flat=True
                ).order_by('time_p2').distinct()
            ],
            'time_p3': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p3__isnull=True) | models.Q(time_p3="")
                ).values_list(
                    'time_p3', flat=True
                ).order_by('time_p3').distinct()
            ],
            'time_p4': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p4__isnull=True) | models.Q(time_p4="")
                ).values_list(
                    'time_p4', flat=True
                ).order_by('time_p4').distinct()
            ],
            'time_p5': [
                {'value': time, 'label': time}
                for time in queryset.exclude(
                    models.Q(time_p5__isnull=True) | models.Q(time_p5="")
                ).values_list(
                    'time_p5', flat=True
                ).order_by('time_p5').distinct()
            ],
            'authors': [
                {'value': authors, 'label': authors}
                for authors in queryset.exclude(
                    publication__authors__isnull=True
                ).values_list(
                    'publication__authors', flat=True
                ).order_by('publication__authors').distinct()
            ],
            'doi_reference': [
                {'value': web_link_id, 'label': web_link_index}
                for web_link_id, web_link_index in queryset.exclude(
                    publication__authors__isnull=True
                ).values_list(
                    'publication__web_link_id', 'publication__web_link__index',
                ).order_by('publication__web_link_id').distinct()
            ],
        }
        return response

class BiasBrowserChembl(TemplateView):
    template_name = 'bias_browser_chembl.html'
    # @cache_page(50000)

    def get_context_data(self, *args, **kwargs):
        content = AnalyzedExperiment.objects.filter(source='chembl_data').prefetch_related(
            'analyzed_data', 'ligand', 'ligand__reference_ligand', 'reference_ligand',
            'endogenous_ligand', 'ligand__properities', 'receptor', 'receptor__family',
            'receptor__family__parent', 'receptor__family__parent__parent__parent',
            'receptor__family__parent__parent', 'receptor__species',
            'publication', 'publication__web_link', 'publication__web_link__web_resource',
            'publication__journal', 'ligand__ref_ligand_bias_analyzed',
            'analyzed_data__emax_ligand_reference')
        context = dict()
        prepare_data = self.process_data(content)
        keys = [k for k, v in prepare_data.items() if len(v['biasdata']) < 2]
        for x in keys:
            del prepare_data[x]

        self.multply_assay(prepare_data)
        context.update({'data': prepare_data})
        return context

    def process_data(self, content):
        '''
        Merge BiasedExperiment with its children
        and pass it back to loop through dublicates
        '''
        rd = dict()
        increment = 0

        for instance in content:
            fin_obj = {}
            fin_obj['main'] = instance
            temp = dict()
            doubles = []
            # TODO: mutation residue
            temp['experiment_id'] = instance.id
            temp['ligand'] = instance.ligand
            temp['source'] = instance.source
            temp['chembl'] = instance.chembl
            temp['endogenous_ligand'] = instance.endogenous_ligand
            temp['vendor_quantity'] = instance.vendor_quantity
            temp['primary'] = instance.primary
            temp['secondary'] = instance.secondary

            if instance.receptor:
                temp['receptor'] = instance.receptor
            else:
                temp['receptor'] = 'Error appeared'
            temp['biasdata'] = list()
            increment_assay = 0
            for entry in instance.analyzed_data.all():
                if entry.order_no < 5:
                    temp_dict = dict()
                    temp_dict['family'] = entry.family
                    temp_dict['assay'] = entry.assay_type
                    temp_dict['assay_description'] = entry.assay_description
                    temp_dict['show_family'] = entry.signalling_protein
                    temp_dict['signalling_protein'] = entry.signalling_protein
                    temp_dict['quantitive_measure_type'] = entry.quantitive_measure_type
                    temp_dict['quantitive_activity'] = entry.quantitive_activity
                    temp_dict['quantitive_activity_initial'] = entry.quantitive_activity_initial
                    temp_dict['quantitive_unit'] = entry.quantitive_unit
                    temp_dict['qualitative_activity'] = entry.qualitative_activity
                    temp_dict['order_no'] = int(entry.order_no)

                    if entry.potency != None and entry.potency != 'None':
                        temp_dict['potency'] = entry.potency
                    else:
                        temp_dict['potency'] = ''

                    temp['biasdata'].append(temp_dict)
                    doubles.append(temp_dict)
                    increment_assay += 1
                else:
                    continue
            rd[increment] = temp
            increment += 1
        return rd

    def multply_assay(self, data):
        for i in data.items():
            lenght = len(i[1]['biasdata'])
            for key in range(lenght, 5):
                temp_dict = dict()
                temp_dict['pathway'] = ''
                temp_dict['order_no'] = lenght
                i[1]['biasdata'].append(temp_dict)
                lenght += 1
            test = sorted(i[1]['biasdata'], key=lambda x: x['order_no'],
                          reverse=True)
            i[1]['biasdata'] = test[:5]

    '''
    End  of Bias Browser
    '''


class BiasPathways(TemplateView):

    template_name = 'bias_browser_pathways.html'
    # @cache_page(50000)

    def get_context_data(self, *args, **kwargs):
        content = BiasedPathways.objects.all().prefetch_related(
            'biased_pathway', 'ligand', 'receptor', 'receptor', 'receptor__family',
            'receptor__family__parent', 'receptor__family__parent__parent__parent',
            'receptor__family__parent__parent', 'receptor__species',
            'publication', 'publication__web_link', 'publication__web_link__web_resource',
            'publication__journal')
        context = dict()
        prepare_data = self.process_data(content)
        context.update({'data': prepare_data})

        return context

    def process_data(self, content):
        '''
        Merge BiasedExperiment with its children
        and pass it back to loop through dublicates
        '''
        rd = dict()
        increment = 0

        for instance in content:
            fin_obj = {}
            fin_obj['main'] = instance
            temp = dict()
            doubles = []
            # TODO: mutation residue
            temp['experiment_id'] = instance.id
            temp['publication'] = instance.publication
            temp['ligand'] = instance.ligand
            temp['rece'] = instance.chembl
            temp['chembl'] = instance.chembl
            temp['relevance'] = instance.relevance
            temp['signalling_protein'] = instance.signalling_protein

            if instance.receptor:
                temp['receptor'] = instance.receptor
                temp['uniprot'] = instance.receptor.entry_short
                temp['IUPHAR'] = instance.receptor.name.split(' ', 1)[
                    0].strip()
            else:
                temp['receptor'] = 'Error appeared'
            # at the moment, there is only 1 pathways for every biased_pathway
            # change if more pathways added (logic changed)
            for entry in instance.biased_pathway.all():
                temp['pathway_outcome_high'] = entry.pathway_outcome_high
                temp['pathway_outcome_summary'] = entry.pathway_outcome_summary
                temp['pathway_outcome_detail'] = entry.pathway_outcome_detail
                temp['experiment_pathway_distinction'] = entry.experiment_pathway_distinction
                temp['experiment_system'] = entry.experiment_system
                temp['experiment_outcome_method'] = entry.experiment_outcome_method

            rd[increment] = temp
            increment += 1

        return rd

    '''
    End  of Bias Browser
    '''
