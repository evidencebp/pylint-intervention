from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count, Q, Prefetch, TextField, Avg
from django.db.models.functions import Concat
from django import forms

from django.shortcuts import redirect

from common.phylogenetic_tree import PhylogeneticTreeGenerator
from protein.models import ProteinSegment
from structure.models import Structure, StructureModel, StructureComplexModel, StructureExtraProteins, StructureVectors, StructureModelRMSD, StructureModelpLDDT, StructureAFScores
from structure.functions import CASelector, SelectionParser, GenericNumbersSelector, SubstructureSelector, ModelRotamer
from structure.assign_generic_numbers_gpcr import GenericNumbering, GenericNumberingFromDB
from structure.structural_superposition import ProteinSuperpose,FragmentSuperpose
from structure.forms import *
from signprot.models import SignprotComplex, SignprotStructure, SignprotStructureExtraProteins
from interaction.models import ResidueFragmentInteraction,StructureLigandInteraction
from protein.models import Protein, ProteinFamily, ProteinCouplings
from construct.models import Construct
from construct.functions import convert_ordered_to_disordered_annotation,add_construct
from common.views import AbsSegmentSelection,AbsReferenceSelection
from common.selection import Selection, SelectionItem
from common.extensions import MultiFileField
from common.models import ReleaseNotes
from common.alignment import Alignment, GProteinAlignment
from residue.models import Residue
from contactnetwork.models import Interaction

import io
import numpy as np
from scipy.optimize import linear_sum_assignment
from Bio.PDB.vectors import Vector, rotmat

Alignment = getattr(__import__('common.alignment_' + settings.SITE_NAME, fromlist=['Alignment']), 'Alignment')

import inspect
import os
import time
import zipfile
import json

from copy import deepcopy
from io import StringIO, BytesIO
from collections import OrderedDict, defaultdict
from Bio.PDB import PDBIO, PDBParser, Select

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

class_dict = {'001':'A','002':'B1','003':'B2','004':'C','005':'D1','006':'F','007':'T','008':'O'}

class StructureBrowser(TemplateView):
    """
    Fetching Structure data for browser
    """
    template_name = "structure_browser.html"

    def get_context_data (self, **kwargs):

        context = super(StructureBrowser, self).get_context_data(**kwargs)
        try:
            structures = Structure.objects.all().exclude(structure_type__slug__startswith='af-').select_related(
                "state",
                "structure_type",
                "pdb_code__web_resource",
                "protein_conformation__protein__species",
                "protein_conformation__protein__source",
                "protein_conformation__protein__family__parent__parent__parent",
                "publication__web_link__web_resource").prefetch_related(
                "stabilizing_agents", "construct__crystallization__crystal_method",
                "protein_conformation__protein__parent__endogenous_gtp_set__ligand__ligand_type",
                "protein_conformation__site_protein_conformation__site","structure_type",
                Prefetch("ligands", queryset=StructureLigandInteraction.objects.filter(
                annotated=True).exclude(structure__structure_type__slug__startswith='af-').prefetch_related('ligand__ligand_type', 'ligand_role','ligand__ids__web_resource')),
                Prefetch("extra_proteins", queryset=StructureExtraProteins.objects.all().prefetch_related(
                    'protein_conformation','wt_protein')),
                Prefetch("signprotcomplex_set", queryset=SignprotComplex.objects.all().prefetch_related('protein')))
        except Structure.DoesNotExist as e:
            pass

        residue_counts = Residue.objects.values("protein_conformation").filter(protein_segment__isnull=False).order_by("protein_conformation").annotate(Count=Count("protein_conformation"))
        structure_residues = {}
        for pair in residue_counts:
            if pair['protein_conformation'] not in structure_residues.keys():
                structure_residues[pair['protein_conformation']] =  pair['Count']

        structs_and_coverage = []
        for s in structures:
            # structure_residues = Residue.objects.filter(protein_conformation=s.protein_conformation, protein_segment__isnull=False)
            residue_num = structure_residues[s.protein_conformation.id]
            # coverage = round((len(structure_residues) / len(s.protein_conformation.protein.parent.sequence))*100)
            coverage = round((residue_num / len(s.protein_conformation.protein.parent.sequence))*100)
            structs_and_coverage.append([s, coverage])
        context['structures'] = structs_and_coverage

        return context


class EffectorStructureBrowser(TemplateView):
    """
    Fetching Structure data for browser
    """
    template_name = "g_protein_structure_browser.html"
    effector = 'gprot'

    def get_context_data (self, **kwargs):
        # Fetch g prot - receptor compleces
        if self.effector == 'gprot':
            slug_start = '100'
        elif self.effector == 'arrestin':
            slug_start = '200'

        context = super(EffectorStructureBrowser, self).get_context_data(**kwargs)
        complexstructs = SignprotComplex.objects.filter(protein__family__slug__startswith=slug_start).exclude(structure__structure_type__slug__startswith='af-')
        try:
            context['structures'] = Structure.objects.filter(id__in=complexstructs.values_list('structure', flat=True)).select_related(
                "state",
                "structure_type",
                "pdb_code__web_resource",
                "protein_conformation__protein__species",
                "protein_conformation__protein__source",
                "protein_conformation__protein__family__parent__parent__parent",
                "publication__web_link__web_resource").prefetch_related(
                "stabilizing_agents", "construct__crystallization__crystal_method", "structure_type",
                "protein_conformation__protein__parent__endogenous_gtp_set__ligand__ligand_type",
                "protein_conformation__site_protein_conformation__site",
                Prefetch("ligands", queryset=StructureLigandInteraction.objects.filter(
                annotated=True).exclude(structure__structure_type__slug__startswith='af-').prefetch_related('ligand__ligand_type', 'ligand_role','ligand__ids__web_resource')),
                Prefetch("extra_proteins", queryset=StructureExtraProteins.objects.all().prefetch_related(
                    'protein_conformation','wt_protein', 'wt_protein__species', 'wt_protein__family', 'wt_protein__family__parent')),
                Prefetch("signprot_complex", queryset=SignprotComplex.objects.all().prefetch_related(
                'protein', 'protein__family', 'protein__family__parent', 'protein__species')))
        except Structure.DoesNotExist as e:
            pass
        # Fetch non-complex g prot structures and filter for overlaps preferring SignprotComplex
        ncstructs = SignprotStructure.objects.filter(protein__family__slug__startswith=slug_start).select_related(
                "protein__family",
                "protein__species",
                "structure_type",
                "pdb_code__web_resource",
                "publication__web_link__web_resource").prefetch_related(
                "protein", "stabilizing_agents", "structure_type", "protein__species", "protein__family", "protein__family__parent",
                Prefetch("extra_proteins", queryset=SignprotStructureExtraProteins.objects.all().prefetch_related(
                'protein_conformation','wt_protein', 'wt_protein__species', 'wt_protein__family', 'wt_protein__family__parent')))
        pdbs = []
        filtered_ncstructs = []
        for i in context['structures']:
            if i.pdb_code.index not in pdbs:
                pdbs.append(i.pdb_code.index)
        for i in ncstructs:
            if i.pdb_code.index not in pdbs:
                pdbs.append(i.pdb_code.index)
                filtered_ncstructs.append(i)
        context['structures'] = list(context['structures'])+list(filtered_ncstructs)
        context['effector'] = self.effector
        return context


class ServeHomologyModels(TemplateView):

    template_name = "homology_models.html"
    def get_context_data(self, **kwargs):
        context = super(ServeHomologyModels, self).get_context_data(**kwargs)
        try:
            context['structure_model'] = StructureModel.objects.all().prefetch_related(
                "protein__family",
                "state",
                "protein__family__parent__parent__parent",
                "protein__species",
                "main_template__protein_conformation__protein__parent__family",
                "main_template__pdb_code")
        except StructureModel.DoesNotExist as e:
            pass

        return context


class ServeComplexModels(TemplateView):

    template_name = "complex_models.html"
    def get_context_data(self, **kwargs):
        context = super(ServeComplexModels, self).get_context_data(**kwargs)
        # try:
        #     context['structure_complex_model'] = StructureComplexModel.objects.all().prefetch_related(
        #         "receptor_protein",
        #         "receptor_protein__family",
        #         "receptor_protein__family__parent__parent__parent",
        #         "receptor_protein__species",
        #         "sign_protein",
        #         "sign_protein__family",
        #         "sign_protein__family__parent__parent__parent",
        #         "main_template__protein_conformation__protein__parent__family",
        #         "main_template__pdb_code",
        #         "main_template__signprot_complex")
        # except StructureComplexModel.DoesNotExist as e:
        #     pass
        ##### DATA
        # model.structure_type.slug
        # model.pdb_code.index
        #
        # model.protein_conformation.protein.accession
        # model.protein_conformation.protein.parent.accession
        # model.protein_conformation.protein.parent.entry_short
        # model.protein_conformation.protein.entry_short
        # model.protein_conformation.protein.entry_name
        # model.protein_conformation.protein.short
        # model.protein_conformation.protein.family.name
        # model.protein_conformation.protein.family.parent.short
        # model.protein_conformation.protein.family.parent.parent.parent.short
        # model.protein_conformation.protein.species.common_name
        #
        # model.publication_date
        # model.signprot_complex.protein.name
        # model.signprot_complex.protein.family.name
        # model.signprot_complex.protein.entry_name
        try:
            complex_models = list(Structure.objects.filter(structure_type__slug='af-signprot').prefetch_related(
                "protein_conformation__protein",
                "protein_conformation__protein__parent",
                "protein_conformation__protein__family",
                "protein_conformation__protein__family__parent",
                "protein_conformation__protein__family__parent__parent__parent",
                "protein_conformation__protein__species",
                "signprot_complex__protein",
                "signprot_complex__protein__famliy",
                "signprot_complex__protein__family__parent").values("structure_type__slug",
                                                                    "pdb_code__index",
                                                                    "protein_conformation__protein__accession",
                                                                    "protein_conformation__protein__parent__accession",
                                                                    "protein_conformation__protein__parent__name",
                                                                    "protein_conformation__protein__entry_name",
                                                                    "protein_conformation__protein",
                                                                    "protein_conformation__protein__name",
                                                                    "protein_conformation__protein__family__name",
                                                                    "protein_conformation__protein__family__parent__name",
                                                                    "protein_conformation__protein__family__parent__parent__parent__name",
                                                                    "protein_conformation__protein__species__common_name",
                                                                    "publication_date",
                                                                    "signprot_complex__protein__name",
                                                                    "signprot_complex__protein__family",
                                                                    "signprot_complex__protein__family__name",
                                                                    "signprot_complex__protein__family__parent__name",
                                                                    "signprot_complex__protein__entry_name"))

            sep = StructureExtraProteins.objects.filter(structure__structure_type__slug='af-signprot').prefetch_related("structure__pdb_code").values("structure__pdb_code__index").annotate(sepcount=Count("structure__pdb_code__index")).order_by()
            sep_dict = {}
            for s in sep:
                sep_dict[s["structure__pdb_code__index"]] = s["sepcount"]
            couplings_data = list(ProteinCouplings.objects.all().prefetch_related("g_protein", "protein").values("transduction",
                                                                                                                 "g_protein__name",
                                                                                                                 "g_protein_subunit__entry_name",
                                                                                                                 "g_protein_subunit__name",
                                                                                                                 "protein__name",
                                                                                                                 "source",
                                                                                                                 "logmaxec50",
                                                                                                                 "protein__entry_name"))

            for i, cm in enumerate(complex_models):
                ### Heterotrimer
                if sep_dict[cm["pdb_code__index"]]==3:
                    heterotrimer = "Yes"
                else:
                    heterotrimer = "No"
                cm["heterotrimer"] =  heterotrimer
                ### Coupling
                cm["GuideToPharma"] = "-"
                cm["Inoue"] = "-"
                cm["Roth"] = "-"
                cm["Bouvier"] = "-"
                # cm["transduction"] = "-"
                for coupling in couplings_data:
                    if coupling["source"] == 'GuideToPharma':
                        if (cm["protein_conformation__protein__entry_name"] == coupling["protein__entry_name"]) and (cm["signprot_complex__protein__family__parent__name"] == coupling["g_protein__name"]):
                            # cm["transduction"] = coupling["transduction"]
                            cm["GuideToPharma"] = coupling["transduction"]
                    else:
                        if (cm["protein_conformation__protein__entry_name"] == coupling["protein__entry_name"]) and (cm["signprot_complex__protein__name"] == coupling["g_protein_subunit__name"]):
                            # cm["transduction"] = coupling["transduction"]
                            if coupling["source"] == 'Inoue':
                                cm["Inoue"] = coupling["logmaxec50"]
                            elif coupling["source"] == 'Bouvier':
                                cm["Bouvier"] = coupling["logmaxec50"]
                            elif coupling["source"] == 'Roth':
                                cm["Roth"] = coupling["logmaxec50"]

            context['structure_complex_model'] = complex_models

        except StructureComplexModel.DoesNotExist as e:
            pass

        return context


class ServeModelStatistics(TemplateView):

    template_name = "model_statistics.html"
    def get_context_data(self, **kwargs):
        context = super(ServeModelStatistics, self).get_context_data(**kwargs)
        smr = StructureModelRMSD.objects.all()
        try:
            context['structure_model_rmsds'] = smr.prefetch_related(
                "target_structure__protein_conformation__protein__parent",
                "target_structure__protein_conformation__protein__parent__family")
        except StructureModelRMSD.DoesNotExist as e:
            print(e)

        return context


def RedirectBrowser(request):
    response = redirect("/structure/")
    return response

def HomologyModelDetails(request, modelname, state):
    """
    Show homology models details
    """
    modelname = modelname

    color_palette = ["orange","cyan","yellow","lime","fuchsia","green","teal","olive","thistle","grey","chocolate","blue","red","pink","maroon"]
    model_plddt = StructureModelpLDDT.objects.filter(structure_model__protein__entry_name=modelname, structure_model__state__slug=state).prefetch_related('residue','residue__protein_conformation__protein')
    residues_plddt = {}
    for item in model_plddt:
        if item.residue.protein_conformation.protein not in residues_plddt:
            residues_plddt[item.residue.protein_conformation.protein] = {}
        residues_plddt[item.residue.protein_conformation.protein][item.residue.id] = [item.residue, item.pLDDT]

    model = StructureModel.objects.get(protein__entry_name=modelname, state__slug=state)
    version = model.version
    ### Keep old coloring for refined structures
    if model.protein.accession==None:
        model_main_template = model.main_template
        if model.protein.accession:
            residues = Residue.objects.filter(protein_conformation__protein=model.protein)
            a = Alignment()
            a.load_reference_protein(model.protein)
            a.load_proteins([model.main_template.protein_conformation.protein.parent])
            segs = ProteinSegment.objects.filter(id__in=residues.order_by("protein_segment__slug").distinct("protein_segment__slug").values_list("protein_segment", flat=True))
            a.load_segments(segs)
            a.build_alignment()
            a.calculate_similarity()
            main_template_seqsim = a.proteins[1].similarity
        else:
            residues = Residue.objects.filter(protein_conformation__protein=model.protein.parent)
            main_template_seqsim = 100
        rotamers = parse_model_statsfile(model.stats_text.stats_text, residues)

        bb_temps, backbone_templates, r_temps, rotamer_templates, segments_out, bb_main, bb_alt, bb_none, sc_main, sc_alt, sc_none, template_list, colors = format_model_details(rotamers, model_main_template, color_palette)
        return render(request,'homology_models_details.html',{'model': model,
                                                              'modelname': modelname,
                                                              'rotamers': rotamers,
                                                              'backbone_templates': bb_temps,
                                                              'backbone_templates_number': len(backbone_templates),
                                                              'rotamer_templates': r_temps,
                                                              'rotamer_templates_number': len(rotamer_templates),
                                                              'color_residues': json.dumps(segments_out),
                                                              'bb_main': round(bb_main/len(rotamers)*100, 1),
                                                              'bb_alt': round(bb_alt/len(rotamers)*100, 1),
                                                              'bb_none': round(bb_none/len(rotamers)*100, 1),
                                                              'sc_main': round(sc_main/len(rotamers)*100, 1),
                                                              'sc_alt': round(sc_alt/len(rotamers)*100, 1),
                                                              'sc_none': round(sc_none/len(rotamers)*100, 1),
                                                              'main_template_seqsim': main_template_seqsim,
                                                              'template_list': template_list,
                                                              'model_main_template': model_main_template,
                                                              'state': state,
                                                              'version': version
                                                              })
    ### AF models
    else:
        segments_out = af_model_coloring(residues_plddt, ['A'])
        return render(request,'homology_models_details.html',{'model': model,
                                                              'modelname': modelname,
                                                              'color_residues': json.dumps(segments_out),
                                                              'state': state,
                                                              'version': version
                                                              })

def af_model_coloring(residues_plddt, chains=[]):
    segments, segments_formatted_chains, segment_colors = {},{},{}
    hex_colors = colour_af_plddt()
    for chain_i, (prot, pos) in enumerate(residues_plddt.items()):
        segments_formatted = {}
        c = chains[chain_i]
        segment_colors[c] = {}
        for r, val in pos.items():
            color = from_score_to_color(val[1], hex_colors)
            if color in segment_colors[c].keys():
                segment_colors[c][color].append(val[0].sequence_number)
            else:
                segment_colors[c][color] = [val[0].sequence_number]
            if prot.entry_name=='gbb1_human':
                seg = 'beta'
            elif prot.entry_name=='gbg2_human':
                seg = 'gamma'
            else:
                seg = val[0].protein_segment.slug
            if seg not in segments:
                segments[seg] = [val[0].sequence_number]
            else:
                segments[seg].append(val[0].sequence_number)

        for s, nums in segment_colors[c].items():
            for i, num in enumerate(nums):
                if i==0:
                    segments_formatted[s] = [[num]]
                elif nums[i-1]!=num-1:
                    if segments_formatted[s][-1][0]==nums[i-1]:
                        segments_formatted[s][-1] = '{}'.format(segments_formatted[s][-1][0])
                    else:
                        segments_formatted[s][-1] = '{}-{}'.format(segments_formatted[s][-1][0], nums[i-1])
                    segments_formatted[s].append([num])
                    if i+1==len(segment_colors[c][s]):
                        segments_formatted[s][-1] = '{}'.format(segments_formatted[s][-1][0])
                elif i+1==len(segment_colors[c][s]):
                    segments_formatted[s][-1] = '{}-{}'.format(segments_formatted[s][-1][0], nums[i-1]+1)
            if len(nums)==1:
                segments_formatted[s] = ['{}'.format(segments_formatted[s][0][0])]
    
        for s, nums in segments_formatted.items():
            if len(nums)>1:
                text = ':{} and ('.format(chains[chain_i])
                for n in nums:
                    text+='{} or '.format(n)
                    segments_formatted[s] = text[:-4]
                text+=')'
            else:
                segments_formatted[s] = ':{} and ({})'.format(chains[chain_i], segments_formatted[s][0])
        segments_formatted_chains[chains[chain_i]] = segments_formatted
    segments_out = []

    for chain, segments_formatted in segments_formatted_chains.items():
        for i,j in segments_formatted.items():
            segments_out.append([i,j])

    return segments_out

def colour_af_plddt():
    ''' Generates full gradient from 0 to 100 for plddt score '''
    blue_hex = RGB_to_hex([0,76,202])
    lightblue_hex = RGB_to_hex([73, 196, 238])
    yellow_hex = RGB_to_hex([255, 213, 57])
    orange_hex = RGB_to_hex([255, 113, 67])
    red_hex = RGB_to_hex([255, 0, 0])

    bad_confidence_gradient = linear_gradient(red_hex, orange_hex, 50)
    low_confidence_gradient = linear_gradient(orange_hex, yellow_hex, 20)
    expected_confidence_gradient= linear_gradient(yellow_hex, lightblue_hex, 20)
    high_confidence_gradient= linear_gradient(lightblue_hex, blue_hex, 10)

    full_gradient_hex = bad_confidence_gradient['hex'] + low_confidence_gradient['hex'] + expected_confidence_gradient['hex'] + high_confidence_gradient['hex']

    return full_gradient_hex

def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  return {"hex":[RGB_to_hex(RGB) for RGB in gradient]}


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)

def from_score_to_color(residue, gradient):
    residue = int(round(residue, 0))
    color = gradient[residue]
    return color

def RefinedModelDetails(request, pdbname):
    if len(pdbname) == 4:
        try:
            structure = Structure.objects.get(pdb_code__index=pdbname.upper())
            if structure.refined:
                complex_mod_details = SignprotComplex.objects.filter(structure=structure, beta_protein__isnull=False, gamma_protein__isnull=False) # Temp fix for G protein fragment coupled structures
                if len(complex_mod_details) > 0:
                    complex_mod = complex_mod_details.first()
                    return ComplexModelDetails(request, pdbname.lower(), True)
                else:
                    return HomologyModelDetails(request, pdbname.lower(), structure.state.slug)

            else:
                error = f"This structure ({pdbname}) does not have a refined model"
        except Structure.DoesNotExist:
            error = f"The structure {pdbname} does not exist in the GPCRdb"
    else:
        error = f"An incorrect PDB entry ({pdbname}) was specified"

    return HttpResponse(error)

def remove_duplicate_dicts(dict_list):
    unique_dicts = []
    seen = set()

    for d in dict_list:
        # Convert the dictionary to a string to make it hashable
        dict_str = json.dumps(d, sort_keys=True)

        # If the string is not in the set, add it back to the list and mark it as seen
        if dict_str not in seen:
            seen.add(dict_str)
            unique_dicts.append(d)

    return unique_dicts

def find_dict_index(dict_list, target_dict):
    for i, d in enumerate(dict_list):
        if d == target_dict:
            return i
    return -1  # return -1 if the dictionary is not found

def minimize_distance(connections):
    outer_to_new_outer = {} # maps old outer index to new outer index
    inner_to_outer = defaultdict(list) # aggregate all outer indexes for each inner index

    # Invert the mapping for easier manipulation
    for inner, outers in connections.items():
        for outer in outers:
            inner_to_outer[inner].append(outer)

    available_outer_indexes = set()
    for outers in inner_to_outer.values():
        available_outer_indexes.update(outers)

    next_available_outer = 0  # Initialize new outer index

    # Loop through sorted inner indexes
    for inner in sorted(inner_to_outer.keys()):
        # Sort the outer indexes by their current value
        for outer in sorted(inner_to_outer[inner]):
            if outer not in outer_to_new_outer: # Assign new index if not assigned before
                outer_to_new_outer[outer] = next_available_outer
                next_available_outer += 1

    return outer_to_new_outer

def sort_and_update(push_gpcr, gpcr, push_gprot, gprot, interactions):
  for key in push_gpcr:
      gpcr[key]['interactions'] = ', '.join(push_gpcr[key])
  for key in push_gprot:
      gprot[key]['interactions'] = ', '.join(push_gprot[key])

  matching_dict = {}
  for record in interactions:
      if record['innerIndex'] not in matching_dict.keys():
          matching_dict[record['innerIndex']] = []
      if record['outerIndex'] not in matching_dict[record['innerIndex']]:
          matching_dict[record['innerIndex']].append(record['outerIndex'])

  conversion = minimize_distance(matching_dict)

  # Create new_dict_b by reordering dict_b based on index_mapping
  new_dict_b = [None] * len(gpcr)
  for original, new in conversion.items():
      new_dict_b[new] = gpcr[original]

  # Remove None values if any (in case dict_b has more elements than mapping_dict)
  gpcr = [item for item in new_dict_b if item is not None]
  for record in interactions:
      record['outerIndex'] = conversion[record['outerIndex']]

  return gpcr, gprot

def ComplexModelDetails(request, header, refined=False):
    """
    Show complex homology models details
    """
    color_palette = ["orange","cyan","yellow","lime","fuchsia","limegreen","teal","olive","thistle","grey","chocolate","blue","red","pink","palegoldenrod","steelblue","tan","lightcoral","skyblue","papayawhip"]
    if refined:
        main_template = Structure.objects.get(pdb_code__index=header.upper())
        header = header.upper()+'_refined'
    model = Structure.objects.get(pdb_code__index=header)

    if not refined:
        scores = StructureAFScores.objects.get(structure=model)
        #Need to build the plDDT colors
        model_plddt = StructureModelpLDDT.objects.filter(structure=model).order_by('residue__protein_conformation__protein__id').prefetch_related('residue','residue__protein_conformation__protein','residue__protein_segment')
        avg_plddt = model_plddt.aggregate(Avg('pLDDT'))
        residues_plddt = {}
        for item in model_plddt:
            if item.residue.protein_conformation.protein not in residues_plddt:
                residues_plddt[item.residue.protein_conformation.protein] = {}
            residues_plddt[item.residue.protein_conformation.protein][item.residue.id] = [item.residue, item.pLDDT]

    ### Gathering interaction info and structuring JS data
    interactions = Interaction.objects.filter(interacting_pair__referenced_structure=model).prefetch_related('interacting_pair__res1', 'interacting_pair__res2',
                                                                                                             'interacting_pair__res1__display_generic_number', 'interacting_pair__res2__display_generic_number',
                                                                                                             'interacting_pair__res1__protein_segment', 'interacting_pair__res2__protein_segment')

    gpcr_aminoacids = []
    gprot_aminoacids = []
    protein_interactions = []
    protein_interactions_strict = []
    conversion = {'aromatic': 'Aromatic',
                  'hydrophobic': 'Hydrophobic',
                  'ionic': 'Ionic',
                  'polar': 'Polar',
                  'van-der-waals': 'Van der waals'}

    for pair in interactions:
        try:
            gn1 = pair.interacting_pair.res1.display_generic_number.label
        except AttributeError:
            gn1 = '-'

        try:
            gn2 = pair.interacting_pair.res2.display_generic_number.label
        except AttributeError:
            gn2 = '-'

        gpcr = {'aminoAcid': pair.interacting_pair.res1.amino_acid,
                'segment': pair.interacting_pair.res1.protein_segment.slug,
                'generic_number': gn1,
                'sequence_number': pair.interacting_pair.res1.sequence_number,
                'interaction_level': pair.interaction_level
                }
        gprot = {'aminoAcid': pair.interacting_pair.res2.amino_acid,
                'segment': pair.interacting_pair.res2.protein_segment.slug,
                'generic_number': gn2,
                'sequence_number': pair.interacting_pair.res2.sequence_number,
                'interaction_level': pair.interaction_level
                }

        gpcr_aminoacids.append(gpcr)
        gprot_aminoacids.append(gprot)

    gpcr_aminoacids_strict = [record for record in gpcr_aminoacids if record['interaction_level'] == 1]
    gprot_aminoacids_strict = [record for record in gprot_aminoacids if record['interaction_level'] == 1]

    gpcr_aminoacids = [{key: value for key, value in d.items() if key != 'interaction_level'} for d in gpcr_aminoacids]
    gprot_aminoacids = [{key: value for key, value in d.items() if key != 'interaction_level'} for d in gprot_aminoacids]
    gpcr_aminoacids_strict = [{key: value for key, value in d.items() if key != 'interaction_level'} for d in gpcr_aminoacids_strict]
    gprot_aminoacids_strict = [{key: value for key, value in d.items() if key != 'interaction_level'} for d in gprot_aminoacids_strict]

    gpcr_aminoacids_strict = remove_duplicate_dicts(gpcr_aminoacids_strict)
    gprot_aminoacids_strict = remove_duplicate_dicts(gprot_aminoacids_strict)
    gpcr_aminoacids = remove_duplicate_dicts(gpcr_aminoacids)
    gprot_aminoacids = remove_duplicate_dicts(gprot_aminoacids)

    segments_order = ['TM1','ICL1', 'TM2', 'ICL2', 'TM3', 'ICL3', 'TM4', 'TM5', 'TM6', 'TM7', 'ICL4', 'H8', 'C-term']
    gprot_segments = ['G.HN','G.hns1','G.S1','G.s1h1','G.H1','G.h1ha','H.HA','H.hahb','H.HB','H.hbhc','H.HC','H.hchd','H.HD','H.hdhe','H.HE','H.hehf','H.HF','G.hfs2','G.S2','G.s2s3','G.S3','G.s3h2','G.H2','G.h2s4','G.S4','G.s4h3','G.H3','G.h3s5','G.S5','G.s5hg','G.HG','G.hgh4','G.H4','G.h4s6','G.S6','G.s6h5','G.H5']
    # Create a dictionary that maps segments to their positions in the custom order
    order_gpcr = {segment: index for index, segment in enumerate(segments_order)}
    order_gprot = {segment: index for index, segment in enumerate(gprot_segments)}

    # Sort the list of dictionaries based on the custom order
    # gpcr_aminoacids = sorted(gpcr_aminoacids, key=lambda x: order_gpcr.get(x['segment'], float('inf')))
    # gprot_aminoacids = sorted(gprot_aminoacids, key=lambda x: x['generic_number'])
    gprot_aminoacids = sorted(gprot_aminoacids, key=lambda x: (order_gprot.get(x['segment'], 9999), int(x['generic_number'].split('.')[-1])))
    gprot_aminoacids_strict = sorted(gprot_aminoacids_strict, key=lambda x: (order_gprot.get(x['segment'], 9999), int(x['generic_number'].split('.')[-1])))

    to_push_gpcr = {}
    to_push_gprot = {}
    to_push_gpcr_strict = {}
    to_push_gprot_strict = {}
    for pair in interactions:
        if pair.atomname_residue1 in ['C', 'CA', 'N', 'O']:
            chain_res1 = 'Main'
        else:
            chain_res1 = 'Side'
        if pair.atomname_residue2 in ['C', 'CA', 'N', 'O']:
            chain_res2 = 'Main'
        else:
            chain_res2 = 'Side'
        try:
            gn1 = pair.interacting_pair.res1.display_generic_number.label
        except AttributeError:
            gn1 = '-'
        try:
            gn2 = pair.interacting_pair.res2.display_generic_number.label
        except AttributeError:
            gn2 = '-'
        gpcr = {'aminoAcid': pair.interacting_pair.res1.amino_acid,
                'segment': pair.interacting_pair.res1.protein_segment.slug,
                'generic_number': gn1,
                'sequence_number': pair.interacting_pair.res1.sequence_number
                }
        gprot = {'aminoAcid': pair.interacting_pair.res2.amino_acid,
                'segment': pair.interacting_pair.res2.protein_segment.slug,
                'generic_number': gn2,
                'sequence_number': pair.interacting_pair.res2.sequence_number
                }

        gpcr_index = find_dict_index(gpcr_aminoacids, gpcr)
        gprot_index = find_dict_index(gprot_aminoacids, gprot)
        protein_interactions.append({'innerIndex': gprot_index, 'outerIndex': gpcr_index, 'type': conversion[pair.interaction_type], 'innerChain': chain_res2, 'outerChain': chain_res1, 'interaction_level': pair.interaction_level})

        if gpcr_index not in to_push_gpcr.keys():
            to_push_gpcr[gpcr_index] = []
        if gprot_index not in to_push_gprot.keys():
            to_push_gprot[gprot_index] = []

        if (conversion[pair.interaction_type]) not in to_push_gpcr[gpcr_index]:
            to_push_gpcr[gpcr_index].append(conversion[pair.interaction_type])
        if (conversion[pair.interaction_type]) not in to_push_gprot[gprot_index]:
            to_push_gprot[gprot_index].append(conversion[pair.interaction_type])

        if pair.interaction_level == 1:
            gpcr_index_strict = find_dict_index(gpcr_aminoacids_strict, gpcr)
            gprot_index_strict = find_dict_index(gprot_aminoacids_strict, gprot)
            protein_interactions_strict.append({'innerIndex': gprot_index_strict, 'outerIndex': gpcr_index_strict, 'type': conversion[pair.interaction_type], 'innerChain': chain_res2, 'outerChain': chain_res1, 'interaction_level': pair.interaction_level})
            ### Copy logic for the strict ones
            if gpcr_index_strict not in to_push_gpcr_strict.keys():
                to_push_gpcr_strict[gpcr_index_strict] = []
            if gprot_index_strict not in to_push_gprot_strict.keys():
                to_push_gprot_strict[gprot_index_strict] = []

            if (conversion[pair.interaction_type]) not in to_push_gpcr_strict[gpcr_index_strict]:
                to_push_gpcr_strict[gpcr_index_strict].append(conversion[pair.interaction_type])
            if (conversion[pair.interaction_type]) not in to_push_gprot_strict[gprot_index_strict]:
                to_push_gprot_strict[gprot_index_strict].append(conversion[pair.interaction_type])

    protein_interactions = remove_duplicate_dicts(protein_interactions)
    protein_interactions_strict = remove_duplicate_dicts(protein_interactions_strict)

    gpcr_aminoacids, gprot_aminoacids = sort_and_update(to_push_gpcr, gpcr_aminoacids, to_push_gprot, gprot_aminoacids, protein_interactions)
    gpcr_aminoacids_strict, gprot_aminoacids_strict = sort_and_update(to_push_gpcr_strict, gpcr_aminoacids_strict, to_push_gprot_strict, gprot_aminoacids_strict, protein_interactions_strict)

    ### Keep old coloring for refined structures
    if model.structure_type.slug.startswith('af-signprot-refined'):
        # if model.protein_conformation.protein.accession:
        # parent_struct = Structure.objects.get(model.pdb_code.index.split('_')[0])
        # receptor_residues = Residue.objects.filter(protein_conformation__protein=model.protein_conformation.protein)
        # signprot_residues = Residue.objects.filter(protein_conformation__protein=model.signprot_complex.protein)
        # a = Alignment()
        # a.load_reference_protein(parent_struct.protein_conformation.protein)
        # a.load_proteins([model.protein_conformation.protein])
        # segs = ProteinSegment.objects.filter(id__in=receptor_residues.order_by("protein_segment__slug").distinct("protein_segment__slug").values_list("protein_segment", flat=True))
        # a.load_segments(segs)
        # a.build_alignment()
        # a.calculate_similarity()
        # main_template_seqsim = a.proteins[1].similarity
        # else:
        receptor_residues = Residue.objects.filter(protein_conformation__protein=model.protein_conformation.protein).prefetch_related('protein_conformation__protein', 'protein_conformation__protein__parent', 'display_generic_number', 'protein_segment')
        signprot_residues = Residue.objects.filter(protein_conformation__protein=model.signprot_complex.protein).prefetch_related('protein_conformation__protein', 'protein_conformation__protein__parent', 'display_generic_number', 'protein_segment')
        main_template_seqsim = 100
        receptor_rotamers, signprot_rotamers = parse_model_statsfile(model.stats_text.stats_text, receptor_residues, signprot_residues)

        loop_segments = ProteinSegment.objects.filter(category='loop', proteinfamily='Alpha')

        bb_temps, backbone_templates, r_temps, rotamer_templates, segments_out, bb_main, bb_alt, bb_none, sc_main, sc_alt, sc_none, template_list, colors = format_model_details(receptor_rotamers, model, color_palette, chain='R')
        signprot_color_palette = [i for i in color_palette if i not in list(colors.values())]
        bb_temps2, backbone_templates2, r_temps2, rotamer_templates2, segments_out2, bb_main2, bb_alt2, bb_none2, sc_main2, sc_alt2, sc_none2, template_list2, colors2 = format_model_details(signprot_rotamers, model, signprot_color_palette, chain='A', used_colors=colors)

        for n in bb_temps2.values():
            for s in n:
                if s.protein_conformation.protein.parent not in bb_temps:
                    bb_temps[s.protein_conformation.protein.parent] = [s]
                else:
                    if s not in bb_temps[s.protein_conformation.protein.parent]:
                        bb_temps[s.protein_conformation.protein.parent].append(s)
                        break

        return render(request,'complex_models_details.html',{'model': model, 'receptor_rotamers': receptor_rotamers, 'signprot_rotamers': signprot_rotamers, 'backbone_templates': bb_temps, 'backbone_templates_number': len(backbone_templates),
                                                             'rotamer_templates': r_temps, 'rotamer_templates_number': len(rotamer_templates), 'color_residues': json.dumps(segments_out), 
                                                             'bb_alt_perc': round(bb_alt/len(receptor_rotamers)*100, 1), 'bb_none_perc': round(bb_none/len(receptor_rotamers)*100, 1), 
                                                             'sc_alt_perc': round(sc_alt/len(receptor_rotamers)*100, 1), 'sc_none_perc': round(sc_none/len(receptor_rotamers)*100, 1), 
                                                             'bb_alt': bb_alt, 'bb_none': bb_none, 
                                                             'sc_alt': sc_alt, 'sc_none': sc_none,
                                                             'bb_alt_perc2': round(bb_alt2/len(signprot_rotamers)*100, 1), 'bb_none_perc2': round(bb_none2/len(signprot_rotamers)*100, 1), 
                                                             'sc_alt_perc2': round(sc_alt2/len(signprot_rotamers)*100, 1), 'sc_none_perc2': round(sc_none2/len(signprot_rotamers)*100, 1), 
                                                             'bb_alt2': bb_alt2, 'bb_none2': bb_none2, 
                                                             'sc_alt2': sc_alt2, 'sc_none2': sc_none2,
                                                             'template_list': template_list, 'model_main_template': main_template, 'state': None,
                                                             'signprot_color_residues': json.dumps(segments_out2), 'loop_segments': loop_segments, 'pdbname': header, 'scores': StructureAFScores(),
                                                             'refined': json.dumps(True), 'outer': json.dumps(gpcr_aminoacids), 'inner': json.dumps(gprot_aminoacids), 'structure_type': model.structure_type,
                                                             'interactions': json.dumps(protein_interactions), 'outer_strict': json.dumps(gpcr_aminoacids_strict),'inner_strict': json.dumps(gprot_aminoacids_strict),
                                                             'interactions_strict': json.dumps(protein_interactions_strict),'residues': len(protein_interactions)})

    else:
        chains = ['A','B']
        if model.signprot_complex.beta_chain:
            chains.append('C')
        if model.signprot_complex.gamma_chain:
            chains.append('D')
        segments_out = af_model_coloring(residues_plddt, chains)
        return render(request,'complex_models_details.html',{'model': model,
                                                             'color_residues': json.dumps(segments_out),
                                                             'pdbname': header,
                                                             'scores': scores,
                                                             'refined': json.dumps(False),
                                                             'outer': json.dumps(gpcr_aminoacids),
                                                             'inner': json.dumps(gprot_aminoacids),
                                                             'interactions': json.dumps(protein_interactions),
                                                             'outer_strict': json.dumps(gpcr_aminoacids_strict),
                                                             'inner_strict': json.dumps(gprot_aminoacids_strict),
                                                             'interactions_strict': json.dumps(protein_interactions_strict),
                                                             'residues': len(protein_interactions),
                                                             'structure_type': model.structure_type,
                                                             'plddt_avg': avg_plddt['pLDDT__avg']
                                                             })


# def ComplexModelDetails(request, modelname, signprot):
#     """
#     Show complex homology models details
#     """
#     color_palette = ["orange","cyan","yellow","lime","fuchsia","limegreen","teal","olive","thistle","grey","chocolate","blue","red","pink","palegoldenrod","steelblue","tan","lightcoral","skyblue","papayawhip"]
#
#     model = StructureComplexModel.objects.get(receptor_protein__entry_name=modelname, sign_protein__entry_name=signprot)
#     main_template = model.main_template
#     if model.receptor_protein.accession:
#         receptor_residues = Residue.objects.filter(protein_conformation__protein=model.receptor_protein)
#         signprot_residues = Residue.objects.filter(protein_conformation__protein=model.sign_protein)
#         a = Alignment()
#         a.load_reference_protein(model.receptor_protein)
#         a.load_proteins([model.main_template.protein_conformation.protein.parent])
#         segs = ProteinSegment.objects.filter(id__in=receptor_residues.order_by("protein_segment__slug").distinct("protein_segment__slug").values_list("protein_segment", flat=True))
#         a.load_segments(segs)
#         a.build_alignment()
#         a.calculate_similarity()
#         main_template_seqsim = a.proteins[1].similarity
#     else:
#         receptor_residues = Residue.objects.filter(protein_conformation__protein=model.receptor_protein.parent)
#         signprot_residues = Residue.objects.filter(protein_conformation__protein=model.sign_protein)
#         main_template_seqsim = 100
#     receptor_rotamers, signprot_rotamers = parse_model_statsfile(model.stats_text.stats_text, receptor_residues, signprot_residues)
#
#     loop_segments = ProteinSegment.objects.filter(category='loop', proteinfamily='Alpha')
#
#
#     signprot_template = SignprotComplex.objects.get(structure=main_template).protein
#     bb_temps, backbone_templates, r_temps, rotamer_templates, segments_out, bb_main, bb_alt, bb_none, sc_main, sc_alt, sc_none, template_list, colors = format_model_details(receptor_rotamers, main_template, color_palette, chain='R')
#     signprot_color_palette = [i for i in color_palette if i not in list(colors.values())]
#
#     bb_temps2, backbone_templates2, r_temps2, rotamer_templates2, segments_out2, bb_main2, bb_alt2, bb_none2, sc_main2, sc_alt2, sc_none2, template_list2, colors2 = format_model_details(signprot_rotamers, main_template, signprot_color_palette, chain='A', used_colors=colors)
#
#     gp = GProteinAlignment()
#     gp.run_alignment(model.sign_protein, signprot_template, calculate_similarity=True)
#
#     for n in bb_temps2.values():
#         for s in n:
#             if s.protein_conformation.protein.parent not in bb_temps:
#                 bb_temps[s.protein_conformation.protein.parent] = [s]
#             else:
#                 if s not in bb_temps[s.protein_conformation.protein.parent]:
#                     bb_temps[s.protein_conformation.protein.parent].append(s)
#                     break
#
#     return render(request,'complex_models_details.html',{'model': model, 'modelname': modelname, 'signprot': signprot, 'signprot_template': signprot_template, 'receptor_rotamers': receptor_rotamers, 'signprot_rotamers': signprot_rotamers, 'backbone_templates': bb_temps, 'backbone_templates_number': len(backbone_templates),
#                                                          'rotamer_templates': r_temps, 'rotamer_templates_number': len(rotamer_templates), 'color_residues': json.dumps(segments_out), 'bb_main': round(bb_main/len(receptor_rotamers)*100, 1),
#                                                          'bb_alt': round(bb_alt/len(receptor_rotamers)*100, 1), 'bb_none': round(bb_none/len(receptor_rotamers)*100, 1), 'sc_main': round(sc_main/len(receptor_rotamers)*100, 1),
#                                                          'sc_alt': round(sc_alt/len(receptor_rotamers)*100, 1), 'sc_none': round(sc_none/len(receptor_rotamers)*100, 1), 'main_template_seqsim': main_template_seqsim,
#                                                          'template_list': template_list, 'model_main_template': main_template, 'state': None, 'signprot_sim': int(gp.proteins[1].similarity),
#                                                          'signprot_color_residues': json.dumps(segments_out2), 'loop_segments': loop_segments, 'pdbname': model.main_template.protein_conformation.protein.entry_name})#, 'delta_distance': delta_distance})

def parse_model_statsfile(statstext, receptor_residues, signprot_residues=None):
    receptor_rotamers = []
    receptor_residues_dict = {r.sequence_number:r for r in receptor_residues}
    if signprot_residues:
        signprot_residues_dict = {r.sequence_number:r for r in signprot_residues}
        signprot_rotamers = []
        alpha_segments = ProteinSegment.objects.filter(proteinfamily='Alpha').values_list('slug', flat=True)
    structure_dict = {}

    for line in statstext.split('\n')[1:-1]:
        mr = ModelRotamer()
        split_line = line.split(',')
        del split_line[2]
        if (len(split_line) == 4):
            segment, seqnum, backbone_pdb, rotamer_pdb = split_line
        else:
            del split_line[2]
            segment, seqnum, backbone_pdb, rotamer_pdb = split_line

        if backbone_pdb not in structure_dict:
            if backbone_pdb=='None':
                backbone_struct = None
            else:
                backbone_struct = Structure.objects.get(pdb_code__index=backbone_pdb)
                structure_dict[backbone_pdb] = backbone_struct
        else:
            backbone_struct = structure_dict[backbone_pdb]
        if rotamer_pdb not in structure_dict:
            if rotamer_pdb=='None':
                rotamer_struct = None
            else:
                rotamer_struct = Structure.objects.get(pdb_code__index=rotamer_pdb)
                structure_dict[rotamer_pdb] = rotamer_struct
        else:
            rotamer_struct = structure_dict[rotamer_pdb]
        mr.backbone_template = backbone_struct
        mr.rotamer_template = rotamer_struct
        # Statsfile is for a complex model
        if signprot_residues and segment in alpha_segments:
            mr.residue = signprot_residues_dict[int(seqnum)]#signprot_residues.get(protein_segment__slug=segment, sequence_number=int(seqnum))
            signprot_rotamers.append(mr)
        elif segment in ['Beta','Gamma']:
            continue
        else:
            mr.residue = receptor_residues_dict[int(seqnum)]
            receptor_rotamers.append(mr)
    if signprot_residues:
        return receptor_rotamers, signprot_rotamers
    else:
        return receptor_rotamers

def format_model_details(rotamers, model_main_template, color_palette, chain=None, used_colors=None):
    backbone_templates, rotamer_templates = [],[]
    segments, segments_formatted, segments_out = {},{},{}
    bb_temps, r_temps = OrderedDict(), OrderedDict()
    bb_main, bb_alt, bb_none = 0,0,0
    sc_main, sc_alt, sc_none = 0,0,0

    for r in rotamers:
        if r.backbone_template not in backbone_templates and r.backbone_template!=None:
            backbone_templates.append(r.backbone_template)
            if r.backbone_template.protein_conformation.protein.parent not in bb_temps:
                bb_temps[r.backbone_template.protein_conformation.protein.parent] = [r.backbone_template]
            else:
                bb_temps[r.backbone_template.protein_conformation.protein.parent].append(r.backbone_template)
        if r.rotamer_template not in rotamer_templates and r.rotamer_template!=None:
            rotamer_templates.append(r.rotamer_template)
            if r.rotamer_template.protein_conformation.protein.parent not in r_temps:
                r_temps[r.rotamer_template.protein_conformation.protein.parent] = [r.rotamer_template]
            else:
                r_temps[r.rotamer_template.protein_conformation.protein.parent].append(r.rotamer_template)
        if r.backbone_template not in segments:
            segments[r.backbone_template] = [r.residue.sequence_number]
        else:
            segments[r.backbone_template].append(r.residue.sequence_number)
        if r.backbone_template==model_main_template:
            bb_main+=1
        elif r.backbone_template!=None:
            bb_alt+=1
        elif r.backbone_template==None:
            bb_none+=1
        if r.rotamer_template==model_main_template:
            sc_main+=1
        elif r.rotamer_template!=None:
            sc_alt+=1
        elif r.rotamer_template==None:
            sc_none+=1
    for s, nums in segments.items():
        for i, num in enumerate(nums):
            if i==0:
                segments_formatted[s] = [[num]]
            elif nums[i-1]!=num-1:
                if segments_formatted[s][-1][0]==nums[i-1]:
                    segments_formatted[s][-1] = '{}-{}'.format(segments_formatted[s][-1][0], nums[i-1])
                else:
                    segments_formatted[s][-1] = '{}-{}'.format(segments_formatted[s][-1][0], nums[i-1])
                segments_formatted[s].append([num])
                if i+1==len(segments[s]):
                    segments_formatted[s][-1] = '{}-{}'.format(segments_formatted[s][-1][0], segments_formatted[s][-1][0])
            elif i+1==len(segments[s]):
                segments_formatted[s][-1] = '{}-{}'.format(segments_formatted[s][-1][0], nums[i-1]+1)
        if len(nums)==1:
            segments_formatted[s] = ['{}-{}'.format(segments_formatted[s][0][0], segments_formatted[s][0][0])]

    colors = OrderedDict([(model_main_template,"darkorchid"), (None,"white")])
    i = 0
    for s, nums in segments_formatted.items():
        if len(nums)>1:
            if chain:
                text = ':{} and ('.format(chain)
            else:
                text = ''
            for n in nums:
                text+='{} or '.format(n)
            if chain:
                segments_formatted[s] = text[:-4]+')'
            else:
                segments_formatted[s] = text[:-4]
        else:
            if chain:
                segments_formatted[s] = ':{} and ({})'.format(chain, segments_formatted[s][0])
            else:
                segments_formatted[s] = segments_formatted[s][0]
        if s==model_main_template:
            pass
        elif s==None:
            segments_out["white"] = segments_formatted[s]
        else:
            if used_colors:
                if s in used_colors:
                    segments_out[used_colors[s]] = segments_formatted[s]
                    colors[s] = used_colors[s]
                else:
                    segments_out[color_palette[i]] = segments_formatted[s]
                    colors[s] = color_palette[i]
            else:
                segments_out[color_palette[i]] = segments_formatted[s]
                colors[s] = color_palette[i]
        i+=1
    template_list = []
    for b, temps in bb_temps.items():
        for i, t in enumerate(temps):
            t.color = colors[t]
            bb_temps[b][i] = t
            template_list.append(t.pdb_code.index)

    segments_out = [[i,j] for i,j in segments_out.items()]

    return bb_temps, backbone_templates, r_temps, rotamer_templates, segments_out, bb_main, bb_alt, bb_none, sc_main, sc_alt, sc_none, template_list, colors

def ServeHomModDiagram(request, modelname, state):
    model=StructureModel.objects.filter(protein__entry_name=modelname, state__slug=state)
    if model.exists():
        model=model.get()
    else:
         quit() #quit!

    if model.pdb_data is None:
        quit()

    response = HttpResponse(model.pdb_data.pdb, content_type='text/plain')
    return response

# def ServeComplexModDiagram(request, modelname, signprot):
    # model=StructureComplexModel.objects.filter(receptor_protein__entry_name=modelname, sign_protein__entry_name=signprot)
def ServeComplexModDiagram(request, modelname):
    model=Structure.objects.filter(pdb_code__index=modelname)
    if model.exists():
        model=model.get()
    else:
         quit() #quit!

    if model.pdb_data is None:
        quit()

    response = HttpResponse(model.pdb_data.pdb, content_type='text/plain')
    return response

def StructureDetails(request, pdbname):
    """
    Show structure details
    """
    pdbname = pdbname.upper()
    structures = ResidueFragmentInteraction.objects.values('structure_ligand_pair__ligand__name','structure_ligand_pair__pdb_reference','structure_ligand_pair__annotated').filter(structure_ligand_pair__structure__pdb_code__index=pdbname, structure_ligand_pair__annotated=True).annotate(numRes = Count('pk', distinct = True)).order_by('-numRes')
    resn_list = ''

    main_ligand = 'None'
    for structure in structures:
        if structure['structure_ligand_pair__annotated']:
            resn_list += ",\""+structure['structure_ligand_pair__pdb_reference']+"\""
            main_ligand = structure['structure_ligand_pair__pdb_reference']

    crystal = Structure.objects.get(pdb_code__index=pdbname)
    ligands = StructureLigandInteraction.objects.filter(structure=crystal, annotated=True)
    if pdbname.startswith('AFM'):
        p = Protein.objects.get(id=crystal.protein_conformation.protein.id)
    else:
        p = Protein.objects.get(protein=crystal.protein_conformation.protein)
    residues = ResidueFragmentInteraction.objects.filter(structure_ligand_pair__structure__pdb_code__index=pdbname, structure_ligand_pair__annotated=True).order_by('rotamer__residue__sequence_number')

    # positioning data
    sv = StructureVectors.objects.filter(structure=crystal)
    translation = center_axis = ""
    if sv.exists():
        sv = sv.get()
        translation = sv.translation
        center_axis = sv.center_axis

    # Check if the structure is in complex with a signaling protein
    signaling_complex = SignprotComplex.objects.filter(structure=crystal).count() > 0

    # GN list
    only_gns = list(crystal.protein_conformation.residue_set.exclude(generic_number=None).values_list('protein_segment__slug','sequence_number','generic_number__label','display_generic_number__label').all())
    gn_list = [x[1] for x in only_gns]
    filter_tm1 = [x[1] for x in only_gns if x[2] == "1x46"]
    ref_tm1 = ""
    if len(filter_tm1) > 0:
        ref_tm1 = filter_tm1[0]

    return render(request,'structure_details.html',{'pdbname': pdbname, 'structures': structures, 'crystal': crystal, 'protein':p, 'residues':residues, 'annotated_resn': resn_list, 'main_ligand': main_ligand, 'ligands': ligands, 'translation': translation, 'center_axis': center_axis, 'gn_list': gn_list, 'ref_tm1': ref_tm1, 'signaling_complex': signaling_complex})

def ServePdbDiagram(request, pdbname):
    structure=Structure.objects.filter(pdb_code__index=pdbname.upper())
    if structure.exists():
        structure=structure.get()
    else:
         quit() #quit!

    if structure.pdb_data is None:
        quit()

    response = HttpResponse(structure.pdb_data.pdb, content_type='text/plain')
    return response


def ServeUprightPdbDiagram(request, pdbname):
    structure = Structure.objects.filter(pdb_code__index=pdbname.upper())
    if structure.exists():
        structure = structure.get()
    else:
         quit() #quit!

    if structure.pdb_data is None:
        quit()

    sv = StructureVectors.objects.filter(structure=structure)
    struct = translation = center_axis = ""
    if sv.exists():
        sv = sv.get()
        translation = json.loads(sv.translation)
        center_axis = json.loads(sv.center_axis)

    # Load structure
    parser = PDBParser(QUIET=True)
    with io.StringIO(structure.pdb_data.pdb) as f:
        struct = parser.get_structure(structure.pdb_code.index, f)

    # Neutral references
    translation_neutral = np.array((0, 0, 0), 'f')
    qn_neutral = rotmat(Vector(0, 1, 0), Vector(0, 1, 0))

    # Calculate translation
    translation_matrix = np.array((translation[0], translation[1], translation[2]), 'f')

    # Calculate rotation
    v1 = Vector(0, 1, 0)
    v2 = Vector(center_axis[0], center_axis[1], center_axis[2])
    v3 = Vector(-1, 0, 0)
    qn_upright = rotmat(v1, v2)

    # Calculate rotation around axis (TM1 placement)
    ref_tm1 = Residue.objects.filter(protein_conformation=structure.protein_conformation, generic_number_id__label="1x46")
    if ref_tm1.count() > 0:
        ref_tm1 = ref_tm1.first().sequence_number
        tm1_coord = struct[0][structure.preferred_chain][ref_tm1]["CA"].get_vector()
        ref_vector = Vector(tm1_coord[0], 0, tm1_coord[2]) #height position doesn't matter
        ref_vector = ref_vector.normalized()
        qn_axis = rotmat(ref_vector, v3)


    # Apply transformations
    for atom in struct.get_atoms():
        # First apply translation before rotation
        atom.transform(qn_neutral, translation_matrix)
        # Second rotate - calculate rotation and apply
        atom.transform(qn_upright, translation_neutral)
        # Finally, rotate around axis to place helices correctly
        atom.transform(qn_axis, translation_neutral)

    # Save PDB transformed structure
    out_stream = StringIO()
    pdb_out = PDBIO()
    pdb_out.set_structure(struct)
    pdb_out.save(out_stream)

    # Send as response
    return HttpResponse(out_stream.getvalue(), content_type='chemical/x-pdb')

def ServePdbLigandDiagram(request,pdbname,ligand):
    pair = StructureLigandInteraction.objects.filter(structure__pdb_code__index=pdbname).filter(Q(ligand__inchikey=ligand) | Q(ligand__name=ligand)).exclude(pdb_file__isnull=True).get()
    response = HttpResponse(pair.pdb_file.pdb, content_type='text/plain')
    return response

def ServeCleanPdbDiagram(request, pdbname, ligname):
	structure = Structure.objects.filter(pdb_code__index=pdbname.upper())
	if structure.exists():
		structure = structure.get()
		if structure.pdb_data is None:
			quit()
	else:
		 quit()

	# Obtain and save cleaned PDB
	parser = PDBParser(QUIET = True)
	filtered_pdb = StringIO(structure.get_cleaned_pdb(ligands_to_keep=ligname.upper()))
	pdb_out = PDBIO()
	pdb_out.set_structure(parser.get_structure(structure.pdb_code.index, filtered_pdb))

	# Send as response
	out_stream = StringIO()
	pdb_out.save(out_stream, select = NotDisordered())
	return HttpResponse(out_stream.getvalue(), content_type = 'chemical/x-pdb')

class NotDisordered(Select):
    def accept_atom(self, atom):
        if not atom.is_disordered() or atom.get_altloc() == 'A':
            atom.set_altloc(' ')
            return True
        else:
            return False

    def accept_residue(self, residue):
        if residue.is_disordered():
            residue.disordered = 0
            for atom in residue.get_list():
                atom.disordered_flag = 0
        return True

class StructureStatistics(TemplateView):
    """
    So not ready that EA wanted to publish it.
    """
    template_name = 'structure_statistics.html'
    origin = 'structure'

    def get_context_data (self, **kwargs):
        context = super().get_context_data(**kwargs)
        families = ProteinFamily.objects.all()
        lookup = {}
        for f in families:
            lookup[f.slug] = f.name

        #GENERIC
        all_structs = Structure.objects.all().exclude(structure_type__slug__startswith='af-').prefetch_related('protein_conformation__protein__family')
        all_complexes = all_structs.exclude(ligands=None)
        unique_structs = Structure.objects.exclude(structure_type__slug__startswith='af-').order_by('protein_conformation__protein__family__name', 'state',
            'publication_date', 'resolution').distinct('protein_conformation__protein__family__name').prefetch_related('protein_conformation__protein__family')
        unique_complexes = StructureLigandInteraction.objects.filter(annotated=True).exclude(structure__structure_type__slug__startswith='af-').distinct('ligand', 'structure__protein_conformation__protein__family').prefetch_related('structure', 'structure__protein_conformation', 'structure__protein_conformation__protein', 'structure__protein_conformation__protein__family')
        all_active = all_structs.filter(protein_conformation__state__slug = 'active')
        years = self.get_years_range(list(set([x.publication_date.year for x in all_structs])))
        unique_active = unique_structs.filter(protein_conformation__state__slug = 'active')
        #Stats
        # struct_count = Structure.objects.all().annotate(Count('id'))
        struct_lig_count = Structure.objects.exclude(ligands=None).exclude(structure_type__slug__startswith='af-')
        context['all_structures'] = len(all_structs)
        context['all_structures_by_class'] = self.count_by_class(all_structs, lookup)
        context['all_complexes'] = len(all_complexes)
        context['all_complexes_by_class'] = self.count_by_class(all_complexes, lookup)
        context['all_active'] = len(all_active)
        context['all_active_by_class'] = self.count_by_class(all_active, lookup)
        context['unique_structures'] = len(unique_structs)
        context['unique_structures_by_class'] = self.count_by_class(unique_structs, lookup)
        context['unique_complexes'] = len(unique_complexes)
        context['unique_complexes_by_class'] = self.count_by_class([x.structure for x in unique_complexes], lookup)
        context['unique_active'] = len(unique_active)
        context['unique_active_by_class'] = self.count_by_class(unique_active, lookup)
        context['release_notes'] = ReleaseNotes.objects.all()[0]
        context['latest_structure'] = Structure.objects.exclude(structure_type__slug__startswith='af-').latest('publication_date').publication_date
        context['chartdata'] = self.get_per_family_cumulative_data_series(years, unique_structs, lookup)
        context['chartdata_y'] = self.get_per_family_data_series(years, unique_structs, lookup)
        context['chartdata_all'] = self.get_per_family_cumulative_data_series(years, all_structs, lookup)
        context['chartdata_reso'] = self.get_resolution_coverage_data_series(all_structs)
        context['chartdata_class'] = self.get_per_class_cumulative_data_series(years, unique_structs, lookup)
        context['chartdata_class_y'] = self.get_per_class_data_series(years, unique_structs, lookup)
        context['chartdata_class_all'] = self.get_per_class_cumulative_data_series(years, all_structs, lookup)

        # GPROT Complex information
        all_gprots = StructureExtraProteins.objects.filter(category='G alpha').exclude(structure__structure_type__slug__startswith='af-').prefetch_related("wt_protein","wt_protein__family", "wt_protein__family__parent", "structure__protein_conformation__protein__family")
        # all_gprots = all_structs.filter(id__in=SignprotComplex.objects.filter(protein__family__slug__startswith='100').values_list("structure__id", flat=True))

        ###### these are query sets for G-Prot Structure Statistics
        if self.origin != 'arrestin':
            all_g_A_complexes = all_gprots.filter(structure__protein_conformation__protein__family__slug__startswith='001')
            all_g_B1_complexes = all_gprots.filter(structure__protein_conformation__protein__family__slug__startswith='002')
            all_g_B2_complexes = all_gprots.filter(structure__protein_conformation__protein__family__slug__startswith='003')
            all_g_C_complexes = all_gprots.filter(structure__protein_conformation__protein__family__slug__startswith='004')
            all_g_D1_complexes = all_gprots.filter(structure__protein_conformation__protein__family__slug__startswith='005')
            all_g_F_complexes = all_gprots.filter(structure__protein_conformation__protein__family__slug__startswith='006')
            all_g_T2_complexes = all_gprots.filter(structure__protein_conformation__protein__family__slug__startswith='007')
            # unique_gprots = unique_structs.filter(id__in=SignprotComplex.objects.filter(protein__family__slug__startswith='100').values_list("structure__id", flat=True))
            # unique_gprots = unique_structs.filter(id__in=StructureExtraProteins.objects.filter(category='G alpha').values_list("structure__id", flat=True))
            unique_gprots = StructureExtraProteins.objects.filter(category='G alpha').exclude(structure__structure_type__slug__startswith='af-').prefetch_related("wt_protein", "wt_protein__family", "wt_protein__family__parent", "structure__protein_conformation__protein__family").distinct('structure__protein_conformation__protein__family__name')
            unique_g_A_complexes = all_g_A_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_g_B1_complexes = all_g_B1_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_g_B2_complexes = all_g_B2_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_g_C_complexes = all_g_C_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_g_D1_complexes = all_g_D1_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_g_F_complexes = all_g_F_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_g_T2_complexes = all_g_T2_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            context['all_gprots'] = len(all_gprots)
            context['all_gprots_by_class'] = self.count_by_class(all_gprots, lookup, extra=True)
            context['all_gprots_by_gclass'] = self.count_by_effector_class(all_gprots, lookup)
            context['gA_complexes'] = zip(list(self.count_by_effector_class(all_g_A_complexes, lookup).items()), list(self.count_by_effector_class(unique_g_A_complexes, lookup).items()))
            context['all_g_A_complexes'] = len(all_g_A_complexes)
            context['unique_g_A_complexes'] = len(unique_g_A_complexes)
            context['gB1_complexes'] = zip(list(self.count_by_effector_class(all_g_B1_complexes, lookup).items()), list(self.count_by_effector_class(unique_g_B1_complexes, lookup).items()))
            context['all_g_B1_complexes'] = len(all_g_B1_complexes)
            context['unique_g_B1_complexes'] = len(unique_g_B1_complexes)
            context['gB2_complexes'] = zip(list(self.count_by_effector_class(all_g_B2_complexes, lookup).items()), list(self.count_by_effector_class(unique_g_B2_complexes, lookup).items()))
            context['all_g_B2_complexes'] = len(all_g_B2_complexes)
            context['unique_g_B2_complexes'] = len(unique_g_B2_complexes)
            context['gC_complexes'] = zip(list(self.count_by_effector_class(all_g_C_complexes, lookup).items()), list(self.count_by_effector_class(unique_g_C_complexes, lookup).items()))
            context['all_g_C_complexes'] = len(all_g_C_complexes)
            context['unique_g_C_complexes'] = len(unique_g_C_complexes)
            context['gD1_complexes'] = zip(list(self.count_by_effector_class(all_g_D1_complexes, lookup).items()), list(self.count_by_effector_class(unique_g_D1_complexes, lookup).items()))
            context['all_g_D1_complexes'] = len(all_g_D1_complexes)
            context['unique_g_D1_complexes'] = len(unique_g_D1_complexes)
            context['gF_complexes'] = zip(list(self.count_by_effector_class(all_g_F_complexes, lookup).items()), list(self.count_by_effector_class(unique_g_F_complexes, lookup).items()))
            context['all_g_F_complexes'] = len(all_g_F_complexes)
            context['unique_g_F_complexes'] = len(unique_g_F_complexes)
            context['gT2_complexes'] = zip(list(self.count_by_effector_class(all_g_T2_complexes, lookup).items()), list(self.count_by_effector_class(unique_g_T2_complexes, lookup).items()))
            context['all_g_T2_complexes'] = len(all_g_T2_complexes)
            context['unique_g_T2_complexes'] = len(unique_g_T2_complexes)
            context['unique_gprots'] = len(unique_gprots)
            context['unique_gprots_by_gclass'] = self.count_by_effector_class(unique_gprots, lookup)
            context['unique_gprots_by_class'] = self.count_by_class(unique_gprots, lookup, extra=True)

            #GPROT
            if self.origin == 'gprot':
                noncomplex_gprots = SignprotStructure.objects.filter(protein__family__slug__startswith='100').exclude(structure_type__slug__startswith='af-').prefetch_related("protein")
                context['noncomplex_gprots_by_gclass'] = self.count_by_effector_class(noncomplex_gprots, lookup, nc=True)
                context['noncomplex_gprots'] = len(noncomplex_gprots)
                circle_data = all_gprots.values_list(
                              "wt_protein__family__parent__name", "structure__protein_conformation__protein__parent__entry_name", "structure__pdb_code_id__index").order_by(
                              "wt_protein__family__parent__name", "structure__protein_conformation__protein__parent__entry_name", "structure__pdb_code_id__index").distinct(
                              "wt_protein__family__parent__name", "structure__protein_conformation__protein__parent__entry_name", "structure__pdb_code_id__index")
                context['total_gprots_by_gclass'] = []
                for key in context['all_gprots_by_gclass']:
                    context['total_gprots_by_gclass'].append(context['all_gprots_by_gclass'][key] + context['noncomplex_gprots_by_gclass'][key])
                context['total_gprots'] = sum(context['total_gprots_by_gclass'])
            else:
                circle_data = all_structs.values_list(
                              "state_id__slug", "protein_conformation__protein__parent__entry_name", "pdb_code_id__index").order_by(
                              "state_id__slug", "protein_conformation__protein__parent__entry_name", "pdb_code_id__index").distinct(
                              "state_id__slug", "protein_conformation__protein__parent__entry_name", "pdb_code_id__index")

        #ARRESTIN
        else:
            all_arrestins = StructureExtraProteins.objects.filter(category='Arrestin').exclude(structure__structure_type__slug__startswith='af-').prefetch_related("wt_protein","wt_protein__family", "wt_protein__family__parent", "structure__protein_conformation__protein__family")
            noncomplex_arrestins = SignprotStructure.objects.filter(protein__family__slug__startswith='200').exclude(structure_type__slug__startswith='af-').prefetch_related("protein")
            ###### these are query sets for Arrestin Structure Statistics
            all_arr_A_complexes = all_arrestins.filter(structure__protein_conformation__protein__family__slug__startswith='001')
            all_arr_B1_complexes = all_arrestins.filter(structure__protein_conformation__protein__family__slug__startswith='002')
            all_arr_B2_complexes = all_arrestins.filter(structure__protein_conformation__protein__family__slug__startswith='003')
            all_arr_C_complexes = all_arrestins.filter(structure__protein_conformation__protein__family__slug__startswith='004')
            all_arr_D1_complexes = all_arrestins.filter(structure__protein_conformation__protein__family__slug__startswith='005')
            all_arr_F_complexes = all_arrestins.filter(structure__protein_conformation__protein__family__slug__startswith='006')
            all_arr_T2_complexes = all_arrestins.filter(structure__protein_conformation__protein__family__slug__startswith='007')
            # unique_arrestins = unique_structs.filter(id__in=StructureExtraProteins.objects.filter(category='Arrestin').values_list("structure__id", flat=True))
            unique_arrestins = StructureExtraProteins.objects.filter(category='Arrestin').exclude(structure__structure_type__slug__startswith='af-').prefetch_related("wt_protein", "structure__protein_conformation__protein__family").distinct('structure__protein_conformation__protein__family__name')
            unique_arr_A_complexes = all_arr_A_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_arr_B1_complexes = all_arr_B1_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_arr_B2_complexes = all_arr_B2_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_arr_C_complexes = all_arr_C_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_arr_D1_complexes = all_arr_D1_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_arr_F_complexes = all_arr_F_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            unique_arr_T2_complexes = all_arr_T2_complexes.annotate(distinct_name=Concat('wt_protein__family__name', 'structure__protein_conformation__protein__family__name', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
            context['all_arrestins'] = len(all_arrestins)
            context['all_arrestins_by_class'] = self.count_by_class(all_arrestins, lookup, extra=True)
            context['all_arrestins_by_gclass'] = self.count_by_effector_class(all_arrestins, lookup, effector='arrestin')
            context['noncomplex_arrestins_by_gclass'] = self.count_by_effector_class(noncomplex_arrestins, lookup, effector='arrestin', nc=True)
            context['noncomplex_arrestins'] = len(noncomplex_arrestins)
            context['arrA_complexes'] = zip(list(self.count_by_effector_class(all_arr_A_complexes, lookup, effector='arrestin').items()), list(self.count_by_effector_class(unique_arr_A_complexes, lookup, effector='arrestin').items()))
            context['all_arr_A_complexes'] = len(all_arr_A_complexes)
            context['unique_arr_A_complexes'] = len(unique_arr_A_complexes)
            context['arrB1_complexes'] = zip(list(self.count_by_effector_class(all_arr_B1_complexes, lookup, effector='arrestin').items()), list(self.count_by_effector_class(unique_arr_B1_complexes, lookup, effector='arrestin').items()))
            context['all_arr_B1_complexes'] = len(all_arr_B1_complexes)
            context['unique_arr_B1_complexes'] = len(unique_arr_B1_complexes)
            context['arrB2_complexes'] = zip(list(self.count_by_effector_class(all_arr_B2_complexes, lookup, effector='arrestin').items()), list(self.count_by_effector_class(unique_arr_B2_complexes, lookup, effector='arrestin').items()))
            context['all_arr_B2_complexes'] = len(all_arr_B2_complexes)
            context['unique_arr_B2_complexes'] = len(unique_arr_B2_complexes)
            context['arrC_complexes'] = zip(list(self.count_by_effector_class(all_arr_C_complexes, lookup, effector='arrestin').items()), list(self.count_by_effector_class(unique_arr_C_complexes, lookup, effector='arrestin').items()))
            context['all_arr_C_complexes'] = len(all_arr_C_complexes)
            context['unique_arr_C_complexes'] = len(unique_arr_C_complexes)
            context['arrD1_complexes'] = zip(list(self.count_by_effector_class(all_arr_D1_complexes, lookup, effector='arrestin').items()), list(self.count_by_effector_class(unique_arr_D1_complexes, lookup, effector='arrestin').items()))
            context['all_arr_D1_complexes'] = len(all_arr_D1_complexes)
            context['unique_arr_D1_complexes'] = len(unique_arr_D1_complexes)
            context['arrF_complexes'] = zip(list(self.count_by_effector_class(all_arr_F_complexes, lookup, effector='arrestin').items()), list(self.count_by_effector_class(unique_arr_F_complexes, lookup, effector='arrestin').items()))
            context['all_arr_F_complexes'] = len(all_arr_F_complexes)
            context['unique_arr_F_complexes'] = len(unique_arr_F_complexes)
            context['arrT2_complexes'] = zip(list(self.count_by_effector_class(all_arr_T2_complexes, lookup, effector='arrestin').items()), list(self.count_by_effector_class(unique_arr_T2_complexes, lookup, effector='arrestin').items()))
            context['all_arr_T2_complexes'] = len(all_arr_T2_complexes)
            context['unique_arr_T2_complexes'] = len(unique_arr_T2_complexes)
            context['unique_arrestins'] = len(unique_arrestins)
            context['unique_arrestins_by_gclass'] = self.count_by_effector_class(unique_arrestins, lookup, effector='arrestin')
            context['unique_arrestins_by_class'] = self.count_by_class(unique_arrestins, lookup, extra=True)
            circle_data = all_arrestins.values_list(
                          "wt_protein__family__name", "structure__protein_conformation__protein__parent__entry_name", "structure__pdb_code_id__index").order_by(
                          "wt_protein__family__name", "structure__protein_conformation__protein__parent__entry_name", "structure__pdb_code_id__index").distinct(
                          "wt_protein__family__name", "structure__protein_conformation__protein__parent__entry_name", "structure__pdb_code_id__index")
            context['total_arrestins_by_gclass'] = []
            for key in context['all_arrestins_by_gclass']:
                context['total_arrestins_by_gclass'].append(context['all_arrestins_by_gclass'][key] + context['noncomplex_arrestins_by_gclass'][key])
            context['total_arrestins'] = sum(context['total_arrestins_by_gclass'])

        #context['coverage'] = self.get_diagram_coverage()
        #{
        #    'depth': 3,
        #    'anchor': '#crystals'}
        # relabeling table columns for sake of consistency
        for key in list(context['unique_structures_by_class'].keys()):
            context['unique_structures_by_class'][key.replace('Class','')] = context['unique_structures_by_class'].pop(key)
        for key in list(context['all_structures_by_class'].keys()):
            context['all_structures_by_class'][key.replace('Class','')] = context['all_structures_by_class'].pop(key)

        tree = PhylogeneticTreeGenerator()
        class_a_data = tree.get_tree_data(ProteinFamily.objects.get(name='Class A (Rhodopsin)'))
        context['class_a_options'] = deepcopy(tree.d3_options)
        context['class_a_options']['anchor'] = 'class_a'
        context['class_a_options']['leaf_offset'] = 50
        context['class_a_options']['label_free'] = []
        # section to remove Orphan from Class A tree and apply to a different tree
        whole_class_a = class_a_data.get_nodes_dict(None)
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
        context['class_b1'] = json.dumps(class_b1_data.get_nodes_dict('crystals'))
        class_b2_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class B2 (Adhesion)'))
        context['class_b2_options'] = deepcopy(tree.d3_options)
        context['class_b2_options']['anchor'] = 'class_b2'
        context['class_b2_options']['label_free'] = [1,]
        context['class_b2'] = json.dumps(class_b2_data.get_nodes_dict('crystals'))
        class_c_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class C (Glutamate)'))
        context['class_c_options'] = deepcopy(tree.d3_options)
        context['class_c_options']['anchor'] = 'class_c'
        context['class_c_options']['branch_trunc'] = 50
        context['class_c_options']['label_free'] = [1,]
        context['class_c'] = json.dumps(class_c_data.get_nodes_dict('crystals'))
        class_f_data = tree.get_tree_data(ProteinFamily.objects.get(name__startswith='Class F (Frizzled)'))
        context['class_f_options'] = deepcopy(tree.d3_options)
        context['class_f_options']['anchor'] = 'class_f'
        context['class_f_options']['label_free'] = [1,]
        #json.dump(class_f_data.get_nodes_dict('crystalized'), open('tree_test.json', 'w'), indent=4)
        context['class_f'] = json.dumps(class_f_data.get_nodes_dict('crystals'))
        class_t2_data = tree.get_tree_data(ProteinFamily.objects.get(name='Class T (Taste 2)'))
        context['class_t2_options'] = deepcopy(tree.d3_options)
        context['class_t2_options']['anchor'] = 'class_t2'
        context['class_t2_options']['label_free'] = [1,]
        context['class_t2'] = json.dumps(class_t2_data.get_nodes_dict('crystals'))
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
            if (rec_iuphar[0].isupper()) or (rec_iuphar[0].isdigit()):
                whole_rec_dict[rec_uniprot] = [rec_iuphar]
            else:
                whole_rec_dict[rec_uniprot] = [rec_iuphar.capitalize()]

        context["whole_receptors"] = json.dumps(whole_rec_dict)
        context["page"] = self.origin

        save_mapping = {}
        circles = {}

        for data in circle_data:
            # Ugly workaround for mapping non-human receptors to human
            if data[1].split('_')[1] != 'human':
                if data[1] not in save_mapping:
                    tmp = Protein.objects.get(entry_name=data[1])
                    reference = Protein.objects.filter(sequence_type__slug="wt", species__common_name="Human", family=tmp.family)
                    if reference.count():
                        save_mapping[data[1]] = reference.first().entry_name.split('_')[0].upper()

            key = 0
            if data[1].split('_')[1] == 'human':
                key = data[1].split('_')[0].upper()
            elif data[1] in save_mapping:
                key = save_mapping[data[1]]
            if key:
                if key not in circles.keys():
                    circles[key] = {}
                    circles[key][data[0]] = 1
                elif data[0] not in circles[key].keys():
                    circles[key][data[0]] = 1
                else:
                    circles[key][data[0]] += 1

        context["circles_data"] = json.dumps(circles)

        return context

    def get_families_dict(self, queryset, lookup):

        families = []
        for s in queryset:
            fid = s.protein_conformation.protein.family.slug.split("_")
            fname = lookup[fid[0]+"_"+fid[1]]
            cname = lookup[fid[0]]
            if fname not in families:
                families.append(fname)
        return families

    @staticmethod
    def count_by_class(queryset, lookup, extra=False):

        #Ugly walkaround
        classes = [lookup[x] for x in reversed(['001', '002', '003', '004', '005', '006', '007'])]
        records = []
        if extra == False:
            for s in queryset:
                fid = s.protein_conformation.protein.family.slug.split("_")
                cname = lookup[fid[0]]
                records.append(cname)
        else:
            for s in queryset:
                fid = s.structure.protein_conformation.protein.family.slug.split("_")
                cname = lookup[fid[0]]
                records.append(cname)

        tmp = OrderedDict()
        for x in sorted(classes):
            tmp[x] = records.count(x)

        return tmp

    @staticmethod
    def count_by_effector_class(queryset, lookup, nc=False, effector='gprot'):

        #Ugly walkaround
        if effector == 'gprot':
            classes = [lookup[x] for x in ['100_001_001', '100_001_002', '100_001_003', '100_001_004', '100_001_005']]
            translate = {'Gs':'G<sub>s</sub>', 'Gi/o':'G<sub>i/o</sub>', 'Gq/11':'G<sub>q/11</sub>', 'G12/13':'G<sub>12/13</sub>', 'GPa1 family':'GPa1'}
        elif effector == 'arrestin':
            classes = [lookup[x] for x in ['200_000_001_001', '200_000_001_002','200_000_002_001', '200_000_002_002']]
            translate = {'ARRB1':'&beta;-Arrestin<sub>1</sub>', 'ARRB2':'&beta;-Arrestin<sub>2</sub>', 'ARRC':'Arrestin-C', 'ARRS':'S-arrestin'}
        records = []
        if nc == False:
            if effector == "gprot":
                for s in queryset:
                    fid = s.wt_protein.family.parent.slug
                    cname = lookup[fid]
                    records.append(translate[cname])
            else:
                for s in queryset:
                    fid = s.wt_protein.family.slug
                    cname = lookup[fid]
                    records.append(translate[cname])
        else:
            for s in queryset:
                if effector == 'gprot':
                    fid = s.protein.family.parent.slug
                elif effector == 'arrestin':
                    fid = s.protein.family.slug
                cname = lookup[fid]
                records.append(translate[cname])

        tmp = OrderedDict()
        for x in classes:
            tmp[translate[x]] = records.count(translate[x])

        return tmp

    def get_years_range(self, years_list):

        min_y = min(years_list)
        max_y = max(years_list)
        return range(min_y, max_y+1)

    def get_per_class_data_series(self, years, structures, lookup):
        """
        Prepare data for multiBarGraph of unique crystallized receptors grouped by class. Returns data series for django-nvd3 wrapper.
        """
        classes = [lookup[x] for x in ['001', '002', '003', '004', '005', '006', '007']]
        series = []
        data = {}
        for year in years:
            for prot_class in classes:
                if prot_class not in data.keys():
                    data[prot_class] = []
                count = 0
                for structure in structures:
                    fid = structure.protein_conformation.protein.family.slug.split("_")
                    # if structure.protein_conformation.protein.get_protein_family() == family and structure.publication_date.year == year:
                    if lookup[fid[0]] == prot_class and structure.publication_date.year == year:
                        count += 1
                data[prot_class].append(count)
        for prot_class in classes:
            series.append({"values":
                [OrderedDict({
                    'x': years[i],
                    'y': j
                    }) for i, j in enumerate(data[prot_class])],
                "key": prot_class,
                "yAxis": "1"})
        return json.dumps(series)

    def get_per_family_data_series(self, years, structures, lookup):
        """
        Prepare data for multiBarGraph of unique crystallized receptors. Returns data series for django-nvd3 wrapper.
        """
        families = self.get_families_dict(structures, lookup)
        series = []
        data = {}
        for year in years:
            for family in families:
                if family not in data.keys():
                    data[family] = []
                count = 0
                for structure in structures:
                    fid = structure.protein_conformation.protein.family.slug.split("_")
                    # if structure.protein_conformation.protein.get_protein_family() == family and structure.publication_date.year == year:
                    if lookup[fid[0]+"_"+fid[1]] == family and structure.publication_date.year == year:
                        count += 1
                data[family].append(count)
        for family in families:
            series.append({"values":
                [OrderedDict({
                    'x': years[i],
                    'y': j
                    }) for i, j in enumerate(data[family])],
                "key": family,
                "yAxis": "1"})
        return json.dumps(series)

    def get_per_class_cumulative_data_series(self, years, structures, lookup):
        """
        Prepare data for multiBarGraph of unique crystallized receptors. Returns data series for django-nvd3 wrapper.
        """
        classes =  [lookup[x] for x in ['001', '002', '003', '004', '005', '006', '007']]
        series = []
        data = {}
        for year in years:
            for prot_class in classes:
                if prot_class not in data.keys():
                    data[prot_class] = []
                count = 0
                for structure in structures:
                    fid = structure.protein_conformation.protein.family.slug.split("_")
                    # if structure.protein_conformation.protein.get_protein_family() == family and structure.publication_date.year == year:
                    if lookup[fid[0]] == prot_class and structure.publication_date.year == year:
                        count += 1
                if len(data[prot_class]) > 0:
                    data[prot_class].append(count + data[prot_class][-1])
                else:
                    data[prot_class].append(count)
        for prot_class in classes:
            series.append({"values":
                [OrderedDict({
                    'x': years[i],
                    'y': j
                    }) for i, j in enumerate(data[prot_class])],
                "key": prot_class,
                "yAxis": "1"})
        return json.dumps(series)


    def get_per_family_cumulative_data_series(self, years, structures, lookup):
        """
        Prepare data for multiBarGraph of unique crystallized receptors. Returns data series for django-nvd3 wrapper.
        """
        families = self.get_families_dict(structures, lookup)
        series = []
        data = {}
        for year in years:
            for family in families:
                if family not in data.keys():
                    data[family] = []
                count = 0
                for structure in structures:
                    fid = structure.protein_conformation.protein.family.slug.split("_")
                    # if structure.protein_conformation.protein.get_protein_family() == family and structure.publication_date.year == year:
                    if lookup[fid[0]+"_"+fid[1]] == family and structure.publication_date.year == year:
                        count += 1
                if len(data[family]) > 0:
                    data[family].append(count + data[family][-1])
                else:
                    data[family].append(count)
        for family in families:
            series.append({"values":
                [{
                    'x': years[i],
                    'y': j
                    } for i, j in enumerate(data[family])],
                "key": family,
                "yAxis": "1"})
        return json.dumps(series)


    def get_resolution_coverage_data_series(self, structures):
        """
        Prepare data for multiBarGraph of resolution coverage of available crystal structures.
        """
        #Resolutions boundaries
        reso_min = float(min([round(x.resolution, 1) for x in structures]))
        reso_max = float(max([round(x.resolution, 1) for x in structures]))
        step = (reso_max - reso_min)/10

        brackets = [reso_min + step*x for x in range(10)] + [reso_max]

        reso_count = []
        bracket_labels = []
        for idx, bracket in enumerate(brackets):
            if idx == 0:
                reso_count.append(len([x for x in structures if x.resolution <= bracket]))
                bracket_labels.append('< {:.1f}'.format(bracket))
            else:
                reso_count.append(len([x for x in structures if bracket-step < x.resolution <= bracket]))
                bracket_labels.append('{:.1f}-{:.1f}'.format(brackets[idx-1],bracket))

        return json.dumps([{"values": [{
                    'x': bracket_labels[i],
                    'y': j
                    } for i, j in enumerate(reso_count)],
                "key": 'Resolution coverage',
                "yAxis": "1"}])

    def get_diagram_coverage(self):
        """
        Prepare data for coverage diagram.
        """

        families = ProteinFamily.objects.all()
        lookup = {}
        for f in families:
            lookup[f.slug] = f.name.replace("receptors","")

        class_proteins = Protein.objects.filter(family__slug__startswith="00", source__name='SWISSPROT').prefetch_related('family').order_by('family__slug')

        coverage = OrderedDict()

        temp = OrderedDict([
                            ('name',''),
                            ('interactions', 0),
                            ('receptor_i', 0) ,
                            ('mutations' , 0),
                            ('receptor_m', 0),
                            ('mutations_an' , 0),
                            ('receptor_m_an', 0),
                            ('receptor_t',0),
                            ('children', OrderedDict()) ,
                            ('fraction_i',0),
                            ('fraction_m',0),
                            ('fraction_m_an',0)
                            ])

        for p in class_proteins:
            fid = p.family.slug.split("_")
            if fid[0] not in coverage:
                coverage[fid[0]] = deepcopy(temp)
                coverage[fid[0]]['name'] = lookup[fid[0]]
            if fid[1] not in coverage[fid[0]]['children']:
                coverage[fid[0]]['children'][fid[1]] = deepcopy(temp)
                coverage[fid[0]]['children'][fid[1]]['name'] = lookup[fid[0]+"_"+fid[1]]
            if fid[2] not in coverage[fid[0]]['children'][fid[1]]['children']:
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]] = deepcopy(temp)
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['name'] = lookup[fid[0]+"_"+fid[1]+"_"+fid[2]][:28]
            if fid[3] not in coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children']:
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]] = deepcopy(temp)
                coverage[fid[0]]['receptor_t'] += 1
                coverage[fid[0]]['children'][fid[1]]['receptor_t'] += 1
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['receptor_t'] += 1
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]]['name'] = p.entry_name.split("_")[0] #[:10]
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]]['receptor_t'] = 1


        class_interactions = ResidueFragmentInteraction.objects.filter(structure_ligand_pair__annotated=True).prefetch_related(
            'rotamer__residue__display_generic_number','interaction_type',
            'structure_ligand_pair__structure__protein_conformation__protein__parent__family',
            'structure_ligand_pair__ligand',
            )


        score_copy = {'score': {'a':0,'i':0,'i_weight':0,'m':0,'m_weight':0,'s':0,'s_weight':0} , 'interaction' : {},'mutation': {}}

        # Replace above as fractions etc is not required and it was missing xtals that didnt have interactions.
        unique_structs = list(Structure.objects.exclude(structure_type__slug__startswith='af-').order_by('protein_conformation__protein__parent', 'state',
            'publication_date', 'resolution').distinct('protein_conformation__protein__parent').prefetch_related('protein_conformation__protein__family'))

        for s in unique_structs:
            fid = s.protein_conformation.protein.family.slug.split("_")
            coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]]['receptor_i'] = 1
            coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]]['interactions'] += 1

        CSS_COLOR_NAMES = ["SteelBlue","SlateBlue","LightCoral","Orange","LightGreen","LightGray","PeachPuff","PaleGoldenRod"]

        tree = OrderedDict({'name':'GPCRs','children':[]})
        i = 0
        n = 0
        for c_v in coverage.values():
            c_v['name'] = c_v['name'].split("(")[0]
            if c_v['name'].strip() == 'Other GPCRs':
                continue
            children = []
            for lt_v in c_v['children'].values():
                if lt_v['name'].strip() == 'Orphan' and c_v['name'].strip()=="Class A":
                    continue
                children_rf = []
                for rf_v in lt_v['children'].values():
                    rf_v['name'] = rf_v['name'].split("<")[0]
                    if rf_v['name'].strip() == 'Class T (Taste 2)':
                        continue
                    children_r = []
                    for r_v in rf_v['children'].values():
                        r_v['color'] = CSS_COLOR_NAMES[i]
                        r_v['sort'] = n
                        children_r.append(r_v)
                        n += 1
                    rf_v['children'] = children_r
                    rf_v['sort'] = n
                    rf_v['color'] = CSS_COLOR_NAMES[i]
                    children_rf.append(rf_v)
                lt_v['children'] = children_rf
                lt_v['sort'] = n
                lt_v['color'] = CSS_COLOR_NAMES[i]
                children.append(lt_v)
            c_v['children'] = children
            c_v['sort'] = n
            c_v['color'] = CSS_COLOR_NAMES[i]
            tree['children'].append(c_v)
            i += 1

        return json.dumps(tree)

    @staticmethod
    def get_diagram_crystals():
        """
        Prepare data for coverage diagram.
        """

        crystal_proteins = [x.protein_conformation.protein.parent for x in Structure.objects.exclude(structure_type__slug__startswith='af-').order_by('protein_conformation__protein__parent', 'state',
            'publication_date', 'resolution').distinct('protein_conformation__protein__parent').prefetch_related('protein_conformation__protein__parent__family')]

        families = []
        for cryst_prot in crystal_proteins:
            families.append(cryst_prot.family)
            tmp = cryst_prot.family
            while tmp.parent is not None:
                tmp = tmp.parent
                families.append(tmp)
        lookup = {}
        for f in families:
            lookup[f.slug] = f.name.replace("receptors","")

        coverage = OrderedDict()
        temp = OrderedDict([
                            ('name',''),
                            ('interactions', 0),
                            ('receptor_i', 0) ,
                            ('mutations' , 0),
                            ('receptor_m', 0),
                            ('mutations_an' , 0),
                            ('receptor_m_an', 0),
                            ('receptor_t',0),
                            ('children', OrderedDict()) ,
                            ('fraction_i',0),
                            ('fraction_m',0),
                            ('fraction_m_an',0)
                            ])

        for p in crystal_proteins:
            fid = p.family.slug.split("_")
            if fid[0] not in coverage:
                coverage[fid[0]] = deepcopy(temp)
                coverage[fid[0]]['name'] = lookup[fid[0]]
            if fid[1] not in coverage[fid[0]]['children']:
                coverage[fid[0]]['children'][fid[1]] = deepcopy(temp)
                coverage[fid[0]]['children'][fid[1]]['name'] = lookup[fid[0]+"_"+fid[1]]
            if fid[2] not in coverage[fid[0]]['children'][fid[1]]['children']:
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]] = deepcopy(temp)
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['name'] = lookup[fid[0]+"_"+fid[1]+"_"+fid[2]][:28]
            if fid[3] not in coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children']:
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]] = deepcopy(temp)
                coverage[fid[0]]['receptor_t'] += 1
                coverage[fid[0]]['children'][fid[1]]['receptor_t'] += 1
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['receptor_t'] += 1
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]]['name'] = p.entry_name.split("_")[0] #[:10]
                coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]]['receptor_t'] = 1


        class_interactions = ResidueFragmentInteraction.objects.filter(structure_ligand_pair__annotated=True).prefetch_related(
            'rotamer__residue__display_generic_number','interaction_type',
            'structure_ligand_pair__structure__protein_conformation__protein__parent__family',
            'structure_ligand_pair__ligand',
            )

        score_copy = {'score': {'a':0,'i':0,'i_weight':0,'m':0,'m_weight':0,'s':0,'s_weight':0} , 'interaction' : {},'mutation': {}}

        # Replace above as fractions etc is not required and it was missing xtals that didnt have interactions.
        unique_structs = list(Structure.objects.exclude(structure_type__slug__startswith='af-').order_by('protein_conformation__protein__family__name', 'state',
            'publication_date', 'resolution').distinct('protein_conformation__protein__family__name').prefetch_related('protein_conformation__protein__family'))

        for s in unique_structs:
            fid = s.protein_conformation.protein.family.slug.split("_")
            coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]]['receptor_i'] = 1
            coverage[fid[0]]['children'][fid[1]]['children'][fid[2]]['children'][fid[3]]['interactions'] += 1

        CSS_COLOR_NAMES = ["SteelBlue","SlateBlue","LightCoral","Orange","LightGreen","LightGray","PeachPuff","PaleGoldenRod"]

        tree = OrderedDict({'name':'GPCRs','children':[]})
        i = 0
        n = 0
        for c,c_v in coverage.items():
            c_v['name'] = c_v['name'].split("(")[0]
            if c_v['name'].strip() == 'Other GPCRs':
                continue
            children = []
            for lt,lt_v in c_v['children'].items():
                if lt_v['name'].strip() == 'Orphan' and c_v['name'].strip()=="Class A":
                    continue
                children_rf = []
                for rf,rf_v in lt_v['children'].items():
                    rf_v['name'] = rf_v['name'].split("<")[0]
                    if rf_v['name'].strip() == 'Class T (Taste 2)':
                        continue
                    children_r = []
                    for r,r_v in rf_v['children'].items():
                        r_v['color'] = CSS_COLOR_NAMES[i]
                        r_v['sort'] = n
                        children_r.append(r_v)
                        n += 1
                    rf_v['children'] = children_r
                    rf_v['sort'] = n
                    rf_v['color'] = CSS_COLOR_NAMES[i]
                    children_rf.append(rf_v)
                lt_v['children'] = children_rf
                lt_v['sort'] = n
                lt_v['color'] = CSS_COLOR_NAMES[i]
                children.append(lt_v)
            c_v['children'] = children
            c_v['sort'] = n
            c_v['color'] = CSS_COLOR_NAMES[i]
            tree['children'].append(c_v)
            i += 1

        return json.dumps(tree)


class GenericNumberingIndex(TemplateView):
    """
    Starting page of generic numbering assignment workflow.
    """
    template_name = 'common_structural_tools.html'

    #Left panel
    step = 1
    number_of_steps = 2
    documentation_url = settings.DOCUMENTATION_URL
    docs = 'structures.html#pdb-file-residue-numbering'
    title = "UPLOAD A PDB FILE"
    description = """
    Upload a pdb file to be annotated with generic numbers from GPCRdb.

    The numbers can be visualized in molecular viewers such as PyMOL, with scripts available with the output files.

    Once you have selected all your targets, click the green button.
    """

    #Input file form data
    header = "Select a file to upload:"
    upload_form_data = {
        "pdb_file": forms.FileField(),
        }
    form_code = forms.Form()
    form_code.fields = upload_form_data
    form_id = 'gn_pdb_file'
    url = '/structure/generic_numbering_results'
    mid_section = "upload_file_form.html"
    form_height = 200
    #Buttons
    buttons = {
        'continue' : {
            'label' : 'Assign generic numbers',
            'color' : 'success',
            },
        }


    def get_context_data (self, **kwargs):

        context = super(GenericNumberingIndex, self).get_context_data(**kwargs)
        # get attributes of this class and add them to the context
        context['form_code'] = str(self.form_code)
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]

        return context


#Class rendering results from generic numbers assignment
class GenericNumberingResults(TemplateView):

    template_name = 'common_structural_tools.html'

    #Left panel
    step = 1
    number_of_steps = 2
    title = "SELECT SUBSTRUCTURE"
    description = 'Download the desired substructures.'
    #Mid section
    mid_section = 'gn_results.html'
    #Buttons - none


    def post (self, request, *args, **kwargs):

        generic_numbering = GenericNumbering(StringIO(request.FILES['pdb_file'].file.read().decode('UTF-8',"ignore")))
        out_struct = generic_numbering.assign_generic_numbers()
        out_stream = StringIO()
        io = PDBIO()
        io.set_structure(out_struct)
        io.save(out_stream)
        if len(out_stream.getvalue()) > 0:
            request.session['gn_outfile'] = out_stream
            request.session['gn_outfname'] = request.FILES['pdb_file'].name
            self.success = True
        else:
            self.input_file = request.FILES['pdb_file'].name
            self.success = False

        context = super(GenericNumberingResults, self).get_context_data(**kwargs)
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]

        return render(request, self.template_name, context)



class GenericNumberingSelection(AbsSegmentSelection):
    """
    Segment selection for download of annotated substructure.
    """

    step = 2
    number_of_steps = 2

    docs = 'structures.html#pdb-file-residue-numbering'

    #Mid section
    #mid_section = 'segment_selection.html'

    #Right panel
    segment_list = True
    buttons = {
        'continue': {
            'label': 'Download substructure',
            'url': '/structure/generic_numbering_results/substr',
            'color': 'success',
        },
    }
    # OrderedDict to preserve the order of the boxes
    selection_boxes = OrderedDict([('reference', False),
        ('targets', False),
        ('segments', True),])


    def get_context_data(self, **kwargs):

        context = super(GenericNumberingSelection, self).get_context_data(**kwargs)

        simple_selection = self.request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)

        context['selection'] = {}
        context['selection']['site_residue_groups'] = selection.site_residue_groups
        context['selection']['active_site_residue_group'] = selection.active_site_residue_group
        for selection_box, include in self.selection_boxes.items():
            if include:
                context['selection'][selection_box] = selection.dict(selection_box)['selection'][selection_box]

        # get attributes of this class and add them to the context
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]
        return context


class GenericNumberingDownload(View):
    """
    Serve the (sub)structure depending on user's choice.
    """
    def get(self, request, *args, **kwargs):

        if self.kwargs['substructure'] == 'custom':
            return HttpResponseRedirect('/structure/generic_numbering_selection')

        simple_selection = self.request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)
        out_stream = StringIO()
        io = PDBIO()
        request.session['gn_outfile'].seek(0)
        gn_struct = PDBParser(PERMISSIVE=True, QUIET=True).get_structure(request.session['gn_outfname'], request.session['gn_outfile'])[0]

        if self.kwargs['substructure'] == 'full':
            io.set_structure(gn_struct)
            io.save(out_stream)

        if self.kwargs['substructure'] == 'substr':
            io.set_structure(gn_struct)
            io.save(out_stream, GenericNumbersSelector(parsed_selection=SelectionParser(selection)))

        root, ext = os.path.splitext(request.session['gn_outfname'])
        response = HttpResponse(content_type="chemical/x-pdb")
        response['Content-Disposition'] = 'attachment; filename="{}_GPCRDB.pdb"'.format(root)
        response.write(out_stream.getvalue())

        return response


#==============================================================================

#========================Superposition of structures===========================
#Class for starting page of superposition workflow
class SuperpositionWorkflowIndex(TemplateView):

    template_name = "common_structural_tools.html"

    #Left panel
    step = 1
    number_of_steps = 3
    documentation_url = settings.DOCUMENTATION_URL
    docs = 'structures.html#structure-superposition'
    title = "UPLOAD YOUR FILES"
    description = """
    Upload a pdb file for reference structure, and one or more files that will be superposed. You can also select the structures from crystal structure browser.

    Once you have uploaded/selected all your targets, click the green button.
    """

    header = "Upload or select your structures:"
    #
    upload_form_data = OrderedDict([
        ('ref_file', forms.FileField(label="Reference structure")),
        ('alt_files', MultiFileField(label="Structure(s) to superpose", max_num=10, min_num=1)),
        #('exclusive', forms.BooleanField(label='Download only superposed subset of atoms', widget=forms.CheckboxInput())),
        ])
    form_code = forms.Form()
    form_code.fields = upload_form_data
    form_id = 'superpose_files'
    url = '/structure/superposition_workflow_selection'
    mid_section = 'superposition_workflow_upload_file_form.html'

    #Buttons
    buttons = {
        'continue' : {
            'label' : 'Select segments',
            'color' : 'success',
            }
        }

    # OrderedDict to preserve the order of the boxes
    selection_boxes = OrderedDict([('reference', True),
        ('targets', True),
        ('segments', False)])

    def get_context_data (self, **kwargs):
        context = super(SuperpositionWorkflowIndex, self).get_context_data(**kwargs)

        # get selection from session and add to context
        # get simple selection from session
        simple_selection = self.request.session.get('selection', False)
        # print(simple_selection)
        # create full selection and import simple selection (if it exists)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)
        # print(self.kwargs.keys())
        #Clearing selections for fresh run
        if 'clear' in self.kwargs.keys():
            selection.clear('reference')
            selection.clear('targets')
            selection.clear('segments')
            if 'alt_files' in self.request.session.keys():
                del self.request.session['alt_files']
            if 'ref_file' in self.request.session.keys():
                del self.request.session['ref_file']
        context['selection'] = {}
        for selection_box, include in self.selection_boxes.items():
            if include:
                context['selection'][selection_box] = selection.dict(selection_box)['selection'][selection_box]

        # get attributes of this class and add them to the context
        context['form_code'] = str(self.form_code)
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]
        # print(context)
        return context



#Class rendering selection box for sequence segments
class SuperpositionWorkflowSelection(AbsSegmentSelection):

    #Left panel
    step = 2
    number_of_steps = 3

    docs = 'structures.html#structure-superposition'

    #Mid section
    #mid_section = 'segment_selection.html'

    #Right panel
    segment_list = True
    buttons = {
        'continue': {
            'label': 'Superpose proteins',
            'url': '/structure/superposition_workflow_results',
            'color': 'success',
        },
    }
    # OrderedDict to preserve the order of the boxes
    selection_boxes = OrderedDict([('reference', False),
        ('targets', False),
        ('segments', True),])


    def post (self, request, *args, **kwargs):

        # create full selection and import simple selection (if it exists)
        simple_selection = request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)

        if 'ref_file' in request.FILES:
            request.session['ref_file'] = request.FILES['ref_file']
        if 'alt_files' in request.FILES:
            request.session['alt_files'] = request.FILES.getlist('alt_files')

        context = super(SuperpositionWorkflowSelection, self).get_context_data(**kwargs)
        context['selection'] = {}
        for selection_box, include in self.selection_boxes.items():
            if include:
                context['selection'][selection_box] = selection.dict(selection_box)['selection'][selection_box]


        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):

        self.buttons = {
            'continue': {
                'label': 'Download substructures',
                'url': '/structure/superposition_workflow_results/custom',
                'color': 'success',
            },
        }
        context = super(SuperpositionWorkflowSelection, self).get_context_data(**kwargs)

        simple_selection = self.request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)

        context['selection'] = {}
        context['selection']['site_residue_groups'] = selection.site_residue_groups
        context['selection']['active_site_residue_group'] = selection.active_site_residue_group
        for selection_box, include in self.selection_boxes.items():
            if include:
                context['selection'][selection_box] = selection.dict(selection_box)['selection'][selection_box]

        # get attributes of this class and add them to the context
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]
        return context


#Class rendering results from superposition workflow
class SuperpositionWorkflowResults(TemplateView):
    """
    Select download mode for the superposed structures. Full structures, superposed fragments only, select substructure.
    """

    template_name = 'common_structural_tools.html'

    #Left panel
    step = 3
    number_of_steps = 3
    title = "SELECT SUBSTRUCTURE"
    description = 'Download the desired substructures.'

    #Mid section
    mid_section = 'superposition_results.html'
    #Buttons - none


    def get_context_data (self, **kwargs):

        context = super(SuperpositionWorkflowResults, self).get_context_data(**kwargs)

        simple_selection = self.request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)

        if 'ref_file' in self.request.session.keys():
            ref_file = StringIO(self.request.session['ref_file'].file.read().decode('UTF-8'))
        elif selection.reference != []:
            ref_file = StringIO(selection.reference[0].item.get_cleaned_pdb())
        if 'alt_files' in self.request.session.keys():
            alt_files = [StringIO(alt_file.file.read().decode('UTF-8')) for alt_file in self.request.session['alt_files']]
        elif selection.targets != []:
            alt_files = [StringIO(x.item.get_cleaned_pdb()) for x in selection.targets if x.type in ['structure', 'structure_model', 'structure_model_Inactive', 'structure_model_Intermediate', 'structure_model_Active']]

        superposition = ProteinSuperpose(deepcopy(ref_file),alt_files, selection)
        out_structs = superposition.run()
        if 'alt_files' in self.request.session.keys():
            alt_file_names = [x.name for x in self.request.session['alt_files']]
        else:
            alt_file_names = []
            for x in selection.targets:
                if x.type=='structure':
                    alt_file_names.append('{}_{}.pdb'.format(x.item.protein_conformation.protein.entry_name, x.item.pdb_code.index))
                elif x.type=='structure_model' or x.type=='structure_model_Inactive' or x.type=='structure_model_Intermediate' or x.type=='structure_model_Active':
                    alt_file_names.append('Class{}_{}_{}_{}_GPCRdb.pdb'.format(class_dict[x.item.protein.family.slug[:3]], x.item.protein.entry_name, x.item.state.name, x.item.main_template.pdb_code.index))
        if len(out_structs) == 0:
            self.success = False
        elif len(out_structs) >= 1:
            io = PDBIO()
            self.request.session['alt_structs'] = {}
            for alt_struct, alt_file_name in zip(out_structs, alt_file_names):
                tmp = StringIO()
                io.set_structure(alt_struct)
                io.save(tmp)
                self.request.session['alt_structs'][alt_file_name] = tmp

            self.success = True

        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]
        return context

class SuperpositionWorkflowDownload(View):
    """
    Serve the (sub)structures depending on user's choice.
    """

    def get(self, request, *args, **kwargs):

        if self.kwargs['substructure'] == 'select':
            return HttpResponseRedirect('/structure/superposition_workflow_selection')

        io = PDBIO()
        out_stream = BytesIO()
        zipf = zipfile.ZipFile(out_stream, 'w')
        simple_selection = self.request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)
        self.alt_substructure_mapping = {}
        #reference
        if 'ref_file' in request.session.keys():
            self.request.session['ref_file'].file.seek(0)
            ref_struct = PDBParser(PERMISSIVE=True, QUIET=True).get_structure('ref', StringIO(self.request.session['ref_file'].file.read().decode('UTF-8')))[0]
            gn_assigner = GenericNumbering(structure=ref_struct)
            gn_assigner.assign_generic_numbers()
            self.ref_substructure_mapping = gn_assigner.get_substructure_mapping_dict()
            ref_name = self.request.session['ref_file'].name
        elif selection.reference != []:
            ref_struct = PDBParser(PERMISSIVE=True, QUIET=True).get_structure('ref', StringIO(selection.reference[0].item.get_cleaned_pdb()))[0]
            gn_assigner = GenericNumbering(structure=ref_struct)
            gn_assigner.assign_generic_numbers()
            self.ref_substructure_mapping = gn_assigner.get_substructure_mapping_dict()
            if selection.reference[0].type=='structure':
                ref_name = '{}_{}_ref.pdb'.format(selection.reference[0].item.protein_conformation.protein.entry_name, selection.reference[0].item.pdb_code.index)
            elif selection.reference[0].type=='structure_model' or selection.reference[0].type=='structure_model_Inactive' or selection.reference[0].type=='structure_model_Intermediate' or selection.reference[0].type=='structure_model_Active':
                ref_name = 'Class{}_{}_{}_{}_GPCRdb_ref.pdb'.format(class_dict[selection.reference[0].item.protein.family.slug[:3]], selection.reference[0].item.protein.entry_name,
                                                                    selection.reference[0].item.state.name, selection.reference[0].item.main_template.pdb_code.index)

        alt_structs = {}
        for alt_id, st in self.request.session['alt_structs'].items():
            st.seek(0)
            alt_structs[alt_id] = PDBParser(PERMISSIVE=True, QUIET=True).get_structure(alt_id, st)[0]
            gn_assigner = GenericNumbering(structure=alt_structs[alt_id])
            gn_assigner.assign_generic_numbers()
            self.alt_substructure_mapping[alt_id] = gn_assigner.get_substructure_mapping_dict()

        if self.kwargs['substructure'] == 'full':

            io.set_structure(ref_struct)
            tmp = StringIO()
            io.save(tmp)
            zipf.writestr(ref_name, tmp.getvalue())

            for alt_name in self.request.session['alt_structs']:
                tmp = StringIO()
                io.set_structure(alt_structs[alt_name])
                io.save(tmp)
                zipf.writestr(alt_name, tmp.getvalue())

        elif self.kwargs['substructure'] == 'substr':

            consensus_gn_set = CASelector(SelectionParser(selection), ref_struct, alt_structs.values()).get_consensus_gn_set()
            io.set_structure(ref_struct)
            tmp = StringIO()
            io.save(tmp, GenericNumbersSelector(consensus_gn_set))
            zipf.writestr(ref_name, tmp.getvalue())
            for alt_name in self.request.session['alt_structs']:
                tmp = StringIO()
                io.set_structure(alt_structs[alt_name])
                io.save(tmp, GenericNumbersSelector(consensus_gn_set))
                zipf.writestr(alt_name, tmp.getvalue())

        elif self.kwargs['substructure'] == 'custom':

            io.set_structure(ref_struct)
            tmp = StringIO()
            io.save(tmp, SubstructureSelector(self.ref_substructure_mapping, parsed_selection=SelectionParser(selection)))

            zipf.writestr(ref_name, tmp.getvalue())
            for alt_name in self.request.session['alt_structs']:
                tmp = StringIO()
                io.set_structure(alt_structs[alt_name])
                io.save(tmp, SubstructureSelector(self.alt_substructure_mapping[alt_name], parsed_selection=SelectionParser(selection)))
                zipf.writestr(alt_name, tmp.getvalue())

        zipf.close()
        if len(out_stream.getvalue()) > 0:
            response = HttpResponse(content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename="Superposed_structures.zip"'
            response.write(out_stream.getvalue())

        if 'ref_file' in request.FILES:
            request.session['ref_file'] = request.FILES['ref_file']
        if 'alt_files' in request.FILES:
            request.session['alt_files'] = request.FILES.getlist('alt_files')

        return response

# DEPRECATED FUNCTION
class FragmentSuperpositionIndex(TemplateView):

    template_name = 'common_structural_tools.html'

    #Left panel
    step = 1
    number_of_steps = 1

    documentation_url = settings.DOCUMENTATION_URL
    docs = 'sites.html#pharmacophore-generation'

    title = "SUPERPOSE FRAGMENTS OF CRYSTAL STRUCTURES"
    description = """
    The tool implements a fragment-based pharmacophore method, as published in <a href='http://www.ncbi.nlm.nih.gov/pubmed/25286328'>Fidom K, et al (2015)</a>. Interacting ligand moiety - residue pairs extracted from selected crystal structures of GPCRs are superposed onto the input pdb file based on gpcrdb generic residue numbers. Resulting aligned ligand fragments can be used for placement of pharmacophore features.

    Upload a pdb file you want to superpose the interacting moiety - residue pairs.

    Once you have selected all your targets, click the green button.
        """

    #Input file form data
    header = "Select a file to upload:"
    #Can't control the class properly - staying with the dirty explicit html code
    form_id='fragments'
    form_code = """
    Pdb file:<input id="id_pdb_file" name="pdb_file" type="file" /></br>
    Similarity:</br>
    <input id="similarity" name="similarity" type="radio" value="identical" /> Use fragments with identical residues</br>
    <input checked="checked" id="similarity" name="similarity" type="radio" value="similar" /> Use fragments with residues of similar properties</br>

    Fragments:</br>
    <input checked="checked" id="representative" name="representative" type="radio" value="closest" /> Use fragments from the evolutionary closest crystal structure</br>
    <input id="representative" name="representative" type="radio" value="any" /> Use all available fragments</br></br>
    State:<select id="id_state" name="state">
    <option value="active">Antagonist-bound structures</option>
    <option value="inactive">Agonist-bound structures</option>
    </select>
    """
    url = '/structure/fragment_superposition_results'
    mid_section = "upload_file_form.html"
    form_height = 350

    #Buttons
    buttons = {
        'continue' : {
            'label' : 'Retrieve fragments',
            'color' : 'success',
            },
        }


    def get_context_data (self, **kwargs):

        context = super(FragmentSuperpositionIndex, self).get_context_data(**kwargs)
        # get attributes of this class and add them to the context
        context['form_code'] = str(self.form_code)
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]

        return context


# DEPRECATED FUNCTION
class FragmentSuperpositionResults(TemplateView):

    template_name = "common_structural_tools.html"

    #Left panel - blank
    #Mid section
    mid_section = 'fragment_superposition_results.html'
    #Buttons - none

    def post (self, request, *args, **kwargs):

        frag_sp = FragmentSuperpose(StringIO(request.FILES['pdb_file'].file.read().decode('UTF-8', 'ignore')),request.FILES['pdb_file'].name)
        superposed_fragments = []
        superposed_fragments_repr = []
        if request.POST['similarity'] == 'identical':
            if request.POST['representative'] == 'any':
                superposed_fragments = frag_sp.superpose_fragments()
            else:
                superposed_fragments_repr = frag_sp.superpose_fragments(representative=True, state=request.POST['state'])
                superposed_fragments = frag_sp.superpose_fragments()
        else:
            if request.POST['representative'] == 'any':
                superposed_fragments = frag_sp.superpose_fragments(use_similar=True)
            else:
                superposed_fragments_repr = frag_sp.superpose_fragments(representative=True, use_similar=True, state=request.POST['state'])
                superposed_fragments = frag_sp.superpose_fragments(use_similar=True)
        if superposed_fragments == []  and superposed_fragments_repr == []:
            self.message = "No fragments were aligned."
        else:
            io = PDBIO()
            out_stream = BytesIO()
            zipf = zipfile.ZipFile(out_stream, 'a', zipfile.ZIP_DEFLATED)
            for fragment, pdb_data in superposed_fragments:
                io.set_structure(pdb_data)
                tmp = StringIO()
                io.save(tmp)
                if request.POST['representative'] == 'any':
                    zipf.writestr(fragment.generate_filename(), tmp.getvalue())
                else:
                    zipf.writestr("all_fragments//{!s}".format(fragment.generate_filename()), tmp.getvalue())
            if superposed_fragments_repr != []:
                for fragment, pdb_data in superposed_fragments_repr:
                    io.set_structure(pdb_data)
                    tmp = StringIO()
                    io.save(tmp)
                    zipf.writestr("representative_fragments//{!s}".format(fragment.generate_filename()), tmp.getvalue())
            zipf.close()
            if len(out_stream.getvalue()) > 0:
                request.session['outfile'] = { 'interacting_moiety_residue_fragments.zip' : out_stream, }
                self.outfile = 'interacting_moiety_residue_fragments.zip'
                self.success = True
                self.zip = 'zip'
                self.message = '{:n} fragments were superposed.'.format(len(superposed_fragments))

        context = super(FragmentSuperpositionResults, self).get_context_data(**kwargs)
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]

        return render(request, self.template_name, context)


#==============================================================================
class TemplateTargetSelection(AbsReferenceSelection):
    """
    Starting point for template selection workflow. Target selection.
    """

    type_of_selection = 'reference'
    # Left panel
    description = 'Select a reference target by searching or browsing in the middle column.' \
        + '\n\nThe selected reference target will appear in the right column.' \
        + '\n\nOnce you have selected your reference target, either proceed with all TMs alignment ("Find template"' \
        + 'button) or specify the sequence segments manualy ("Advanced segment selection" button).'
    step = 1
    number_of_steps = 2
    redirect_on_select = False

    docs = 'structures.html#template-selection'

    # Mid section

    # Right panel
    buttons = OrderedDict()
    buttons['continue'] = {
        'label': 'Find template',
        'url': '/structure/template_browser',
        'color': 'success',
    }
    buttons['segments'] = {
        'label' : 'Advanced segment selection',
        'url' : '/structure/template_segment_selection',
        'color' : 'info',
    }

    selection_boxes = OrderedDict([('reference', True),
        ('targets', False),
        ('segments', False),])



#==============================================================================
class TemplateSegmentSelection(AbsSegmentSelection):
    """
    Advanced selection of sequence segments for template search.
    """
   #Left panel
    step = 2
    number_of_steps = 2

    docs = 'structures.html#template-selection'

    #Mid section
    #mid_section = 'segment_selection.html'

    #Right panel
    segment_list = True
    buttons = {
        'continue': {
            'label': 'Find template',
            'url': '/structure/template_browser',
            'color': 'success',
        },
    }
    # OrderedDict to preserve the order of the boxes
    selection_boxes = OrderedDict([('reference', True),
        ('targets', False),
        ('segments', True),])



#==============================================================================
class TemplateBrowser(TemplateView):
    """
    Fetching Structure data and ordering by similarity
    """

    template_name = "template_browser.html"

    def get_context_data (self, **kwargs):

        context = super(TemplateBrowser, self).get_context_data(**kwargs)

        # get simple selection from session
        simple_selection = self.request.session.get('selection', False)

        # make an alignment
        a = Alignment()
        a.ignore_alternative_residue_numbering_schemes = True

        # load the selected reference into the alignment
        a.load_reference_protein_from_selection(simple_selection)

        # fetch
        qs = Structure.objects.all().exclude(structure_type__slug__startswith='af-').select_related(
            "pdb_code__web_resource",
            "protein_conformation__protein__species",
            "protein_conformation__protein__source",
            "protein_conformation__protein__family__parent__parent__parent",
            "publication__web_link__web_resource").prefetch_related(
            "stabilizing_agents",
            "protein_conformation__protein__parent__endogenous_gtp_set__ligand__ligand_type",
            Prefetch("ligands", queryset=StructureLigandInteraction.objects.filter(
            annotated=True).exclude(structure__structure_type__slug__startswith='af-').prefetch_related('ligand__ligand_type', 'ligand_role')))

        # Dirty but fast
        qsd = {}
        for st in qs:
            qsd[st.protein_conformation.protein.id] = st

        # add proteins to the alignment
        a.load_proteins([x.protein_conformation.protein for x in qs])

        if simple_selection.segments != []:
            a.load_segments_from_selection(simple_selection)
        else:
            a.load_segments(ProteinSegment.objects.filter(slug__in=['TM1', 'TM2', 'TM3', 'TM4','TM5','TM6', 'TM7']))

        a.build_alignment()
        a.calculate_similarity()

        context['structures'] = []
        for prot in a.proteins[1:]:
            try:
                context['structures'].append([prot.similarity, prot.identity, qsd[prot.protein.id]])
                del qsd[prot.protein.id]
            except KeyError:
                pass
        return context

#==============================================================================
class PDBClean(TemplateView):
    """
    Extraction, packing and serving out the pdb records selected via structure/template browser.
    """
    template_name = "pdb_download.html"

    def get(self, request, *args, **kwargs):
        context = super(PDBClean, self).get_context_data(**kwargs)
        if request.path.endswith('pdb_download_custom'):
            context['trigger_download'] = True

        self.success = False
        self.posted = False
        context['pref'] = True

        # get simple selection from session
        simple_selection = self.request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)

        if len(selection.targets)>100:
            return HttpResponse("Cannot process more than 100 structures", status=400)
        elif selection.targets != []:
            self.success = True
            context['targets'] = selection.targets

        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = super(PDBClean, self).get_context_data(**kwargs)

        self.posted = True
        pref, context['pref'] = True, True
        water, context['water'] = False, False
        hets, context['hets'] = False, False

        if 'pref_chain' not in request.POST.keys():
            pref, context['pref'] = False, False
        if 'water' in request.POST.keys():
            water, context['water'] = True, True
        if 'hets' in request.POST.keys():
            hets, context['hets'] = True, True

        # get simple selection from session
        simple_selection = request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)
        out_stream = BytesIO()
        io = PDBIO()
        zipf = zipfile.ZipFile(out_stream, 'w', zipfile.ZIP_DEFLATED)
        structs = []
        if selection.targets != []:
            if selection.targets != [] and selection.targets[0].type == 'structure':
                request.session['substructure_mapping'] = OrderedDict()
                for selected_struct in [x for x in selection.targets if x.type == 'structure']:
                    struct_name = '{}_{}.pdb'.format(selected_struct.item.protein_conformation.protein.parent.entry_name, selected_struct.item.pdb_code.index)
                    if hets:
                        lig_names = [x.pdb_reference for x in StructureLigandInteraction.objects.filter(structure=selected_struct.item, annotated=True)]
                    else:
                        lig_names = None
                    gn_assigner = GenericNumberingFromDB(selected_struct.item, PDBParser(QUIET=True).get_structure(struct_name, StringIO(selected_struct.item.get_cleaned_pdb(pref, water, lig_names)))[0])
                    tmp = StringIO()
                    io.set_structure(gn_assigner.assign_generic_numbers())
                    request.session['substructure_mapping'][struct_name] = gn_assigner.get_substructure_mapping_dict()
                    io.save(tmp)
                    zipf.writestr(struct_name, tmp.getvalue())
                    del gn_assigner, tmp
                    structs.append(selected_struct.item.id)
                for struct in selection.targets:
                    selection.remove('targets', 'structure', struct.item.id)
                for struct_id in structs:
                    s = Structure.objects.get(id=struct_id)
                    selection.add('targets', 'structure', SelectionItem('structure', s))

            elif selection.targets != [] and selection.targets[0].type in ['structure_model', 'structure_model_Inactive', 'structure_model_Intermediate', 'structure_model_Active']:
                for hommod in [x for x in selection.targets if x.type in ['structure_model', 'structure_model_Inactive', 'structure_model_Intermediate', 'structure_model_Active']]:
                    mod_name = 'Class{}_{}_{}_{}_{}_GPCRDB.pdb'.format(class_dict[hommod.item.protein.family.slug[:3]], hommod.item.protein.entry_name,
                                                                                  hommod.item.state.name, hommod.item.main_template.pdb_code.index, hommod.item.version)
                    tmp = StringIO(hommod.item.pdb)
                    request.session['substructure_mapping'] = 'full'
                    zipf.writestr(mod_name, tmp.getvalue())
                    del tmp

                    # stat file
                    # rotamers = StructureModelStatsRotamer.objects.filter(homology_model=hommod.item).prefetch_related('residue','backbone_template','rotamer_template').order_by('residue__sequence_number')
                    # stats_data = 'Segment,Sequence_number,Generic_number,Backbone_template,Rotamer_template\n'
                    # for r in rotamers:
                    #     try:
                    #         gn = r.residue.generic_number.label
                    #     except:
                    #         gn = '-'
                    #     if r.backbone_template:
                    #         bt = r.backbone_template.pdb_code.index
                    #     else:
                    #         bt = '-'
                    #     if r.rotamer_template:
                    #         rt = r.rotamer_template.pdb_code.index
                    #     else:
                    #         rt = '-'
                    #     stats_data+='{},{},{},{},{}\n'.format(r.residue.protein_segment.slug, r.residue.sequence_number, gn, bt, rt)
                    # stats_name = mod_name[:-3]+'templates.csv'
                    # zipf.writestr(stats_name, stats_data)
                    # del stats_data

                for mod in selection.targets:
                    selection.remove('targets', 'structure_model', mod.item.id)

            # export simple selection that can be serialized
            simple_selection = selection.exporter()

            request.session['selection'] = simple_selection
            request.session['cleaned_structures'] = out_stream
        self.success = True
        context['prepared_structures'] = True
        context['targets'] = selection.targets
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]

        if selection.targets != [] and selection.targets[0].type == 'structure_model':
            return zipf
        else:
            return render(request, self.template_name, context)


class PDBSegmentSelection(AbsSegmentSelection):

    #Left panel
    step = 2
    number_of_steps = 2

    #Mid section
    #mid_section = 'segment_selection.html'

    #Right panel
    segment_list = True

    # OrderedDict to preserve the order of the boxes
    selection_boxes = OrderedDict([('reference', False),
        ('targets', False),
        ('segments', True),])

    def get_context_data(self, **kwargs):

        self.buttons = {
            'continue': {
                'label': 'Download substructures',
                'url': '/structure/pdb_download_custom',
                'color': 'success',
            },
        }
        context = super(PDBSegmentSelection, self).get_context_data(**kwargs)

        simple_selection = self.request.session.get('selection', False)
        selection = Selection()
        if simple_selection:
            selection.importer(simple_selection)

        context['selection'] = {}
        # context['selection']['site_residue_groups'] = selection.site_residue_groups
        # context['selection']['active_site_residue_group'] = selection.active_site_residue_group

        context['ignore_residue_selection'] = True
        for selection_box, include in self.selection_boxes.items():
            if include:
                context['selection'][selection_box] = selection.dict(selection_box)['selection'][selection_box]

        # get attributes of this class and add them to the context
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not(a[0].startswith('__') and a[0].endswith('__')):
                context[a[0]] = a[1]
        return context

#==============================================================================
class PDBDownload(View):
    """
    Serve the PDB (sub)structures depending on user's choice.
    """

    def get(self, request, hommods=False, *args, **kwargs):
        if self.kwargs['substructure'] == 'select':
            return HttpResponseRedirect('/structure/pdb_segment_selection')

        if self.kwargs['substructure'] == 'full':
            out_stream = request.session['cleaned_structures']

        elif self.kwargs['substructure'] == 'custom':
            simple_selection = request.session.get('selection', False)
            selection = Selection()
            if simple_selection:
                selection.importer(simple_selection)
            io = PDBIO()
            zipf_in = zipfile.ZipFile(request.session['cleaned_structures'], 'r')
            out_stream = BytesIO()
            zipf_out = zipfile.ZipFile(out_stream, 'w', zipfile.ZIP_DEFLATED)
            for name in zipf_in.namelist():
                tmp = StringIO()
                io.set_structure(PDBParser(QUIET=True).get_structure(name, StringIO(zipf_in.read(name).decode('utf-8')))[0])
                io.save(tmp, SubstructureSelector(request.session['substructure_mapping'][name], parsed_selection=SelectionParser(selection)))
                zipf_out.writestr(name, tmp.getvalue())

            zipf_in.close()
            zipf_out.close()

        if len(out_stream.getvalue()) > 0:
            response = HttpResponse(content_type="application/zip")
            if hommods == False:
                response['Content-Disposition'] = 'attachment; filename="pdb_structures.zip"'
            else:
                response['Content-Disposition'] = 'attachment; filename="GPCRDB_homology_models.zip"'
            response.write(out_stream.getvalue())

        return response

#==============================================================================
def ConvertStructuresToProteins(request):
    "For alignment from structure browser"

    simple_selection = request.session.get('selection', False)
    selection = Selection()
    if simple_selection:
        selection.importer(simple_selection)
    if selection.targets != []:
        for struct in selection.targets:
            prot = struct.item.protein_conformation.protein.parent
            selection.remove('targets', 'structure', struct.item.id)
            selection.add('targets', 'protein', SelectionItem('protein', prot))
        if selection.reference != []:
            selection.add('targets', 'protein', selection.reference[0])
    # export simple selection that can be serialized
    simple_selection = selection.exporter()

    # add simple selection to session
    request.session['selection'] = simple_selection

    return HttpResponseRedirect('/alignment/segmentselection')


def ConvertStructureModelsToProteins(request):
    "For alignment from homology model browser"
    simple_selection = request.session.get('selection', False)
    selection = Selection()
    if simple_selection:
        selection.importer(simple_selection)
    if selection.targets != []:
        for struct_mod in selection.targets:
            if hasattr(struct_mod.item, 'protein'):
                if not struct_mod.item.protein.accession:
                    prot = struct_mod.item.protein.parent
                else:
                    prot = struct_mod.item.protein
                selection.remove('targets', 'structure_model', struct_mod.item.id)
                selection.add('targets', 'protein', SelectionItem('protein', prot))
            elif hasattr(struct_mod.item, 'receptor_protein'):
                if not struct_mod.item.receptor_protein.accession:
                    prot = struct_mod.item.receptor_protein.parent
                else:
                    prot = struct_mod.item.receptor_protein
                selection.remove('targets', 'structure_complex_receptor', struct_mod.item.id)
                selection.add('targets', 'protein', SelectionItem('protein', prot))
            elif hasattr(struct_mod.item, 'pdb_code'):
                prot = struct_mod.item.protein_conformation.protein.parent
                selection.remove('targets', 'structure', struct_mod.item.id)
                selection.add('targets', 'protein', SelectionItem('protein', prot))

        if selection.reference != []:
            selection.add('targets', 'protein', selection.reference[0])
    # export simple selection that can be serialized
    simple_selection = selection.exporter()

    # add simple selection to session
    request.session['selection'] = simple_selection

    return HttpResponseRedirect('/alignment/segmentselection')

def ConvertStructureComplexSignprotToProteins(request):
    "For alignment from complex model browser, specifically for signprots"
    simple_selection = request.session.get('selection', False)
    selection = Selection()
    if simple_selection:
        selection.importer(simple_selection)
    if selection.targets != []:
        for struct_mod in selection.targets:
            if hasattr(struct_mod.item, 'sign_protein'):
                prot = struct_mod.item.sign_protein
                selection.remove('targets', 'structure_complex_signprot', struct_mod.item.id)
                selection.add('targets', 'protein', SelectionItem('protein', prot))
            else:
                prot = SignprotComplex.objects.get(structure=struct_mod.item).protein
                selection.remove('targets', 'structure', struct_mod.item.id)
                selection.add('targets', 'protein', SelectionItem('protein', prot))
        if selection.reference != []:
            selection.add('targets', 'protein', selection.reference[0])
    # export simple selection that can be serialized
    simple_selection = selection.exporter()

    # add simple selection to session
    request.session['selection'] = simple_selection

    return HttpResponseRedirect('/alignment/segmentselectiongprot')


def HommodDownload(request):
    "Download selected homology models in zip file"
    pks = request.GET['ids'].split(',')

    hommodels = [StructureModel.objects.get(pk=pk) for pk in pks]

    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as backup_zip:
        for hommod in hommodels:
            io = StringIO(hommod.pdb_data.pdb)

            if not hommod.protein.accession:
                mod_name = 'Class{}_{}_{}_refined_{}_{}_GPCRDB.pdb'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.parent.entry_name,
                                                                   hommod.main_template.pdb_code.index, hommod.state.name, hommod.version)
                stat_name = 'Class{}_{}_{}_refined_{}_{}_GPCRDB.templates.csv'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.parent.entry_name,
                                                                   hommod.main_template.pdb_code.index, hommod.state.name, hommod.version)
            else:
                mod_name = 'Class{}_{}_{}_{}_{}_GPCRDB.pdb'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.entry_name,
                                                                          hommod.state.name, 'AF', hommod.version)
                stat_name = 'Class{}_{}_{}_{}_{}_GPCRDB.templates.csv'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.entry_name,
                                                                          hommod.state.name, 'AF', hommod.version)
            backup_zip.writestr(mod_name, io.getvalue())
            if hommod.stats_text:
                stats_text = StringIO(hommod.stats_text.stats_text)
                backup_zip.writestr(stat_name, stats_text.getvalue())

    response = HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'GPCRDB_homology_models' + ".zip"
    response['Content-Length'] = zip_io.tell()
    return response

def ComplexmodDownload(request):
    "Download selected complex homology models in zip file"
    pks = request.GET['ids'].split(',')

    hommodels = StructureComplexModel.objects.filter(pk__in=pks).prefetch_related('receptor_protein__family','main_template__pdb_code').all()
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as backup_zip:
        for hommod in hommodels:
            io = StringIO(hommod.pdb_data.pdb)
            stats_text = StringIO(hommod.stats_text.stats_text)
            if not hommod.receptor_protein.accession:
                mod_name = 'Class{}_{}-{}_{}_refined_{}_GPCRDB.pdb'.format(class_dict[hommod.receptor_protein.family.slug[:3]], hommod.receptor_protein.parent.entry_name,
                                                                   hommod.sign_protein.entry_name, hommod.main_template.pdb_code.index, hommod.version)
                stat_name = 'Class{}_{}-{}_{}_refined_{}_GPCRDB.templates.csv'.format(class_dict[hommod.receptor_protein.family.slug[:3]], hommod.receptor_protein.parent.entry_name,
                                                                   hommod.sign_protein.entry_name, hommod.main_template.pdb_code.index, hommod.version)
            else:
                mod_name = 'Class{}_{}-{}_{}_{}_GPCRDB.pdb'.format(class_dict[hommod.receptor_protein.family.slug[:3]], hommod.receptor_protein.entry_name,
                                                                   hommod.sign_protein.entry_name, hommod.main_template.pdb_code.index, hommod.version)
                stat_name = 'Class{}_{}-{}_{}_{}_GPCRDB.templates.csv'.format(class_dict[hommod.receptor_protein.family.slug[:3]], hommod.receptor_protein.entry_name,
                                                                   hommod.sign_protein.entry_name, hommod.main_template.pdb_code.index, hommod.version)
            backup_zip.writestr(mod_name, io.getvalue())
            backup_zip.writestr(stat_name, stats_text.getvalue())
    response = HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'GPCRDB_complex_homology_models' + ".zip"
    response['Content-Length'] = zip_io.tell()
    return response

def SingleModelDownload(request, modelname, fullness, state=None, csv=False):
    "Download single homology model"
    zip_io = BytesIO()
    if state:
        hommod = StructureModel.objects.get(protein__entry_name=modelname.lower(), state__slug=state)
    else:
        hommod = StructureModel.objects.get(protein__entry_name=modelname.lower())
    stat_name = None
    stats_lines = ''
    if not hommod.protein.accession:
        version = hommod.pdb_data.pdb.split('\n')[0][-10:]
        mod_name = 'Class{}_{}_{}_refined_{}_{}_GPCRdb.pdb'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.parent.entry_name,
                                                                 hommod.main_template.pdb_code.index, hommod.state.name, version)
        stat_name = 'Class{}_{}_{}_refined_{}_{}_GPCRdb.templates.csv'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.parent.entry_name,
                                                                 hommod.main_template.pdb_code.index, hommod.state.name, version)
    else:
        if hommod.main_template:
            mod_name = 'Class{}_{}_{}_{}_{}_GPCRdb.pdb'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.entry_name,
                                                                           hommod.state.name, hommod.main_template.pdb_code.index, hommod.version)
            stat_name = 'Class{}_{}_{}_{}_{}_GPCRdb.templates.csv'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.entry_name,
                                                                           hommod.state.name, hommod.main_template.pdb_code.index, hommod.version)
        else:
            mod_name = 'Class{}_{}_{}_{}_{}_GPCRdb.pdb'.format(class_dict[hommod.protein.family.slug[:3]], hommod.protein.entry_name,
                                                                           hommod.state.name, 'AF', hommod.version)
    pdb_lines = hommod.pdb_data.pdb
    if stat_name:
        stats_lines = hommod.stats_text.stats_text

    if fullness=='noloops':
        filtered_lines = ''
        remark_line_count = 0
        for line in pdb_lines.split('\n'):
            if line.startswith('REMARK'):
                filtered_lines+=line+'\n'
                remark_line_count+=1
        filtered_lines+='REMARK    {} ALL LOOPS REMOVED AFTER MODELING\n'.format(remark_line_count+1)
        if not hommod.protein.accession:
            helix_resis = Residue.objects.filter(protein_conformation__protein=hommod.protein.parent, protein_segment__category='helix').values_list('sequence_number', flat=True)
        else:
            helix_resis = Residue.objects.filter(protein_conformation__protein=hommod.protein, protein_segment__category='helix').values_list('sequence_number', flat=True)
        p = PDBParser(get_header=True)
        pdb = p.get_structure('pdb', StringIO(pdb_lines))[0]

        for chain in pdb:
            to_remove = []
            for res in chain:
                if res.id[1] not in helix_resis and res.id[0]==' ':
                    to_remove.append(res.id)
            for i in to_remove:
                chain.detach_child(i)
        io = StringIO()
        pdbio = PDBIO()
        pdbio.set_structure(pdb)
        pdbio.save(io)
        io = StringIO(filtered_lines+io.getvalue())
        filtered_stats_lines = ''
        for i in stats_lines.split('\n'):
            if i.startswith('Segment'):
                filtered_stats_lines+=i+'\n'
                continue
            if len(i)<2:
                continue
            resnum = int(i.split(',')[1])
            if resnum in helix_resis:
                filtered_stats_lines+=i+'\n'
        stats_text = StringIO(filtered_stats_lines)
        mod_name = mod_name.split('.')[0]+'_WL'+'.pdb'
        if stat_name:
            stat_name = stat_name.split('.')[0]+'_WL'+'.templates.csv'
    else:
        io = StringIO(pdb_lines)
        stats_text = StringIO(stats_lines)
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as backup_zip:
        backup_zip.writestr(mod_name, io.getvalue())
        if stat_name:
            backup_zip.writestr(stat_name, stats_text.getvalue())
    response = HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=%s' % mod_name.split('.')[0] + ".zip"
    response['Content-Length'] = zip_io.tell()

    return response

def SingleComplexModelDownload(request, modelname, signprot, csv=False):
    "Download single homology model"

    zip_io = BytesIO()
    if signprot=='complex':
        hommod = StructureComplexModel.objects.get(receptor_protein__entry_name=modelname.lower())
        mod_name = 'Class{}_{}-{}_{}_refined_{}_GPCRdb.pdb'.format(class_dict[hommod.receptor_protein.family.slug[:3]], hommod.receptor_protein.parent.entry_name,
                                                            hommod.sign_protein.entry_name, hommod.main_template.pdb_code.index, hommod.version)
        stat_name = 'Class{}_{}-{}_{}_refined_{}_GPCRdb.templates.csv'.format(class_dict[hommod.receptor_protein.family.slug[:3]], hommod.receptor_protein.parent.entry_name,
                                                            hommod.sign_protein.entry_name, hommod.main_template.pdb_code.index, hommod.version)
    else:
        hommod = StructureComplexModel.objects.get(receptor_protein__entry_name=modelname, sign_protein__entry_name=signprot)
        mod_name = 'Class{}_{}-{}_{}_{}_GPCRdb.pdb'.format(class_dict[hommod.receptor_protein.family.slug[:3]], hommod.receptor_protein.entry_name,
                                                            hommod.sign_protein.entry_name, hommod.main_template.pdb_code.index, hommod.version)
        stat_name = 'Class{}_{}-{}_{}_{}_GPCRdb.templates.csv'.format(class_dict[hommod.receptor_protein.family.slug[:3]], hommod.receptor_protein.entry_name,
                                                            hommod.sign_protein.entry_name, hommod.main_template.pdb_code.index, hommod.version)
    io = StringIO(hommod.pdb_data.pdb)
    stats_text = StringIO(hommod.stats_text.stats_text)
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as backup_zip:
        backup_zip.writestr(mod_name, io.getvalue())
        backup_zip.writestr(stat_name, stats_text.getvalue())
    response = HttpResponse(zip_io.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=%s' % mod_name.split('.')[0] + ".zip"
    response['Content-Length'] = zip_io.tell()

    return response

def ServePdbOutfile (request, outfile, replacement_tag):

    root, ext = os.path.splitext(outfile)
    out_stream = request.session['outfile'][outfile]
    response = HttpResponse(content_type="chemical/x-pdb")
    response['Content-Disposition'] = 'attachment; filename="{}_{}.pdb"'.format(root, replacement_tag)
    response.write(out_stream.getvalue())

    return response


def ServeZipOutfile (request, outfile):

    out_stream = request.session['outfile'][outfile]
    response = HttpResponse(content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(outfile)
    response.write(out_stream.getvalue())

    return response

def RenderTrees(request):
    number = request.GET['number']
    tree = open(settings.STATICFILES_DIRS[0] +'/home/images/00'+number+'_tree.xml').read()
    legend = open(settings.STATICFILES_DIRS[0] +'/home/images/00'+number+'_legend.svg').read()
    context = {'tree':tree, 'leg':legend, 'num':number}
    return render(request, 'phylogenetic_trees.html', context)

# def webform(request):
#   form = construct_form()
#   context = {'form':form}
#   return render(request, 'web_form.html',context)
#
# def webform_two(request, slug=None):
#   context = {}
#   if slug:
#       c = Construct.objects.filter(name=slug).get()
#       # print(c.json)
#       # test = ast.literal_eval(c.json)
#       # print(test)
#       json_data = json.loads(c.json)
#       if 'raw_data' not in json_data:
#           json_data = convert_ordered_to_disordered_annotation(json_data)
#       else:
#           if 'csrfmiddlewaretoken' in json_data['raw_data']:
#               del json_data['raw_data']['csrfmiddlewaretoken'] #remove to prevent errors
#
#       context = {'edit':json.dumps(json_data)}
#   return render(request, 'web_form_2.html',context)
#
# def webformdata(request) :
#
#   data = request.POST
#   raw_data = deepcopy(data)
#   purge_keys = ('Please Select','aamod_position','wt_aa','mut_aa','insert_pos_type','protein_type','deletion','csrfmiddlewaretoken')
#   data = dict((k, v) for k, v in data.items() if v!='' and v!='Please Select') #remove empty
#   deletions = []
#   mutations = []
#   contact_info= OrderedDict()
#   construct_crystal=OrderedDict()
#   auxiliary=OrderedDict()
#   expression=OrderedDict()
#   solubilization = OrderedDict()
#   crystallization = OrderedDict()
#   modifications = []
#
#   error = 0
#   error_msg = []
#   for key,value in sorted(data.items()):
#       try:
#           if key.startswith('delet_start'):
#               deletions.append({'start':value, 'end':data[key.replace('start','end')], 'origin':'user', 'type':'range'})
#               data.pop(key, None)
#               data.pop(key.replace('start','end'), None)
#           elif key.startswith('ins_start'):
#               deletions.append({'start':value, 'end':data[key.replace('start','end')], 'origin':'insertion'+key.replace('ins_start',''), 'type':'range'})
#               data.pop(key, None)
#               data.pop(key.replace('start','end'), None)
#               data.pop(key.replace('ins_start',''), None)
#           elif key.startswith(('deletion_single', 'insert_pos_single')):
#               if key.startswith('insert_pos_single'):
#                   deletions.append({'pos':value, 'origin':'insertion'+key.replace('insert_pos_single',''), 'type':'single'})
#                   data.pop(key.replace('insert_pos_single',''), None)
#               else:
#                   deletions.append({'pos':value, 'origin':'user', 'type':'single'})
#               data.pop(key, None)
#
#           if key.startswith('aa_no'):
#               pos_id = key.replace('aa_no','')
#               # if pos_id=='':
#               #   mut_id='1'
#               # else:
#               #   mut_id=pos_id.replace('_','')
#
#               if 'mut_remark'+pos_id in data:
#                   remark = data['mut_remark'+pos_id]
#               else:
#                   remark = ''
#
#               mutations.append({'pos':value,'wt':data['wt_aa'+pos_id],'mut':data['mut_aa'+pos_id], 'type':data['mut_type'+pos_id], 'remark':remark})
#               data.pop(key, None)
#               data.pop('wt_aa'+pos_id, None)
#               data.pop('mut_aa'+pos_id, None)
#               data.pop('mut_type'+pos_id, None)
#
#           if key.startswith(('date','name_cont', 'pi_name',
#               'pi_address','address','url','pi_email' )):
#               contact_info[key]=value
#               data.pop(key, None)
#
#           if key.startswith(('pdb', 'pdb_name',
#               'uniprot','ligand_name', 'ligand_activity', 'ligand_conc', 'ligand_conc_unit','ligand_id','ligand_id_type')):
#               construct_crystal[key]=value
#               data.pop(key, None)
#
#           if key.startswith('position'):
#               pos_id = key.replace('position','')
#               if pos_id=='':
#                   aux_id='1'
#               else:
#                   aux_id=pos_id.replace('_','')
#
#               if 'aux'+aux_id not in auxiliary:
#                   auxiliary['aux'+aux_id] = {'position':value,'type':data['protein_type'+pos_id],'presence':data['presence'+pos_id]}
#
#                   data.pop(key, None)
#                   data.pop('protein_type'+pos_id, None)
#                   data.pop('presence'+pos_id, None)
#
#           if key.startswith(('tag', 'fusion_prot', 'signal', 'linker_seq','prot_cleavage', 'other_prot_cleavage' )):
#               temp = key.split('_')
#               if len(temp)==4:
#                   pos_id = "_"+temp[3]
#                   aux_id=pos_id.replace('_','')
#               elif len(temp)==3:
#                   pos_id = "_"+temp[2]
#                   aux_id=pos_id.replace('_','')
#               elif len(temp)==2 and temp[1].isdigit():
#                   pos_id = "_"+temp[1]
#                   aux_id=pos_id.replace('_','')
#               else:
#                   pos_id = ''
#                   aux_id = '1'
#               # print(key,aux_id,pos_id)
#
#               if 'aux'+aux_id not in auxiliary:
#                   auxiliary['aux'+aux_id] = {'position':data['position'+pos_id],'type':data['protein_type'+pos_id],'presence':data['presence'+pos_id]}
#
#                   data.pop('position'+pos_id, None)
#                   data.pop('protein_type'+pos_id, None)
#                   data.pop('presence'+pos_id, None)
#
#               # if value=='Other':
#               #     auxiliary['aux'+aux_id]['other'] = data['other_'+auxiliary['aux'+aux_id]['type']+pos_id]
#               #     data.pop('other_'+auxiliary['aux'+aux_id]['type']+pos_id,None)
#
#               auxiliary['aux'+aux_id]['subtype'] = value
#               data.pop(key, None)
#
#           if key.startswith(('expr_method', 'host_cell_type',
#                   'host_cell', 'expr_remark','expr_other','other_host','other_host_cell' )):
#               expression[key]=value
#               data.pop(key, None)
#
#           if key.startswith(('deterg_type','deterg_concentr','deterg_concentr_unit','solub_additive','additive_concentr','addit_concentr_unit','chem_enz_treatment','sol_remark')):
#               solubilization[key]=value
#               data.pop(key, None)
#
#           elif key.startswith(('crystal_type','crystal_method','other_method','other_crystal_type',
#                              'protein_concentr','protein_conc_unit','temperature','ph_single','ph',
#                              'ph_range_one','ph_range_two','crystal_remark','lcp_lipid','lcp_add',
#                              'lcp_conc','lcp_conc_unit','detergent','deterg_conc','deterg_conc_unit','lipid','lipid_concentr','lipid_concentr_unit',
#                              'other_deterg','other_deterg_type', 'other_lcp_lipid','other_lipid')):
#               crystallization[key]=value
#               data.pop(key, None)
#
#           if key.startswith('chemical_comp') and not key.startswith('chemical_comp_type'):
#
#               if 'chemical_components' not in crystallization:
#                   crystallization['chemical_components'] = []
#
#               # print(key)
#               if key!='chemical_comp': #not first
#                   comp_id = key.replace('chemical_comp','')
#               else:
#                   comp_id = ''
#
#               crystallization['chemical_components'].append({'component':value,'type':data['chemical_comp_type'+comp_id],'value':data['concentr'+comp_id],'unit':data['concentr_unit'+comp_id]})
#               data.pop(key, None)
#               data.pop('concentr'+comp_id, None)
#               data.pop('concentr_unit'+comp_id, None)
#               data.pop('chemical_comp_type'+comp_id, None)
#
#
#           if key.startswith('aamod') and not key.startswith('aamod_position') and not key.startswith('aamod_pair') and not key=='aamod_position' and not key=='aamod_single':
#               if key!='aamod': #not first
#                   mod_id = key.replace('aamod','')
#               else:
#                   mod_id = ''
#
#               if data['aamod_position'+mod_id]=='single':
#                   pos = ['single',data['aamod_single'+mod_id]]
#                   data.pop('aamod_single'+mod_id, None)
#               elif data['aamod_position'+mod_id]=='range':
#                   pos = ['range',[data['aamod_start'+mod_id],data['aamod_end'+mod_id]]]
#                   data.pop('aamod_start'+mod_id, None)
#                   data.pop('aamod_end'+mod_id, None)
#               elif data['aamod_position'+mod_id]=='pair':
#                   pos = ['pair',[data['aamod_pair_one'+mod_id],data['aamod_pair_two'+mod_id]]]
#                   data.pop('aamod_pair_one'+mod_id, None)
#                   data.pop('aamod_pair_two'+mod_id, None)
#
#               remark = ''
#               if 'mod_remark'+mod_id in data:
#                   remark = data['mod_remark'+mod_id]
#               modifications.append({'type':value,'remark':remark,'position':pos })
#               data.pop(key, None)
#               data.pop('mod_remark'+mod_id, None)
#               data.pop('aamod_position'+mod_id, None)
#
#           if key.startswith(purge_keys):
#               data.pop(key, None)
#       except BaseException as e:
#           error_msg.append(str(e))
#           error = 1
#
#   auxiliary = OrderedDict(sorted(auxiliary.items()))
#
#   context = OrderedDict( [('contact_info',contact_info), ('construct_crystal',construct_crystal),
#                          ('auxiliary' , auxiliary),  ('deletions',deletions), ('mutations',mutations),
#                          ('modifications', modifications), ('expression', expression), ('solubilization',solubilization),
#                          ('crystallization',crystallization),  ('unparsed',data),  ('raw_data',raw_data), ('error', error), ('error_msg',error_msg)] )
#
#   add_construct(context)
#
#   if error==0:
#       dump_dir = '/protwis/construct_dump'
#       # dump_dir = '/web/sites/files/construct_data' #for sites
#       if not os.path.exists(dump_dir):
#           os.makedirs(dump_dir)
#       ts = int(time.time())
#       json_data = context
#       json.dump(json_data, open(dump_dir+"/"+str(ts)+"_"+construct_crystal['pdb']+".json", 'w'), indent=4, separators=(',', ': '))
#
#       context['data'] = sorted(data.items())
#       #context['data'] = sorted(raw_data.items())
#
#       recipients = ['christian@munk.be']
#       emaillist = [elem.strip().split(',') for elem in recipients]
#       msg = MIMEMultipart()
#       msg['Subject'] = 'GPCRdb: New webform data'
#       msg['From'] = 'gpcrdb@gmail.com'
#       msg['Reply-to'] = 'gpcrdb@gmail.com'
#
#       msg.preamble = 'Multipart massage.\n'
#
#       part = MIMEText("Hi, please find the attached file")
#       msg.attach(part)
#
#       part = MIMEApplication(open(str(dump_dir+"/"+str(ts)+"_"+construct_crystal['pdb']+".json"),"rb").read())
#       part.add_header('Content-Disposition', 'attachment', filename=str(dump_dir+"/"+str(ts)+"_"+construct_crystal['pdb']+".json"))
#       msg.attach(part)
#
#
#       server = smtplib.SMTP("smtp.gmail.com:587")
#       server.ehlo()
#       server.starttls()
#       server.login("gpcrdb@gmail.com", "gpcrdb2016")
#
#       server.sendmail(msg['From'], emaillist , msg.as_string())
#
#       context['filename'] = str(ts)+"_"+construct_crystal['pdb']
#
#   return render(request, 'web_form_results.html', context)
#
# def webform_download(request,slug):
#   dump_dir = '/protwis/construct_dump'
#   # dump_dir = '/web/sites/files/construct_data' #for sites
#   file = dump_dir+"/"+str(slug)+".json"
#   out_stream = open(file,"rb").read()
#   response = HttpResponse(content_type="application/json")
#   response['Content-Disposition'] = 'attachment; filename="{}"'.format(file)
#   response.write(out_stream)
#   return response
