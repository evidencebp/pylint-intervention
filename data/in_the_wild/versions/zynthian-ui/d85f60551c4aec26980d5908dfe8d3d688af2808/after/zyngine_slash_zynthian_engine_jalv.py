# -*- coding: utf-8 -*-
#******************************************************************************
# ZYNTHIAN PROJECT: Zynthian Engine (zynthian_engine_jalv)
#
# zynthian_engine implementation for Jalv Plugin Host
#
# Copyright (C) 2015-2018 Fernando Moyano <jofemodo@zynthian.org>
#
#******************************************************************************
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the LICENSE.txt file.
#
#******************************************************************************

import os
import json
import logging
from os.path import isfile
from collections import OrderedDict

from . import zynthian_engine
from . import zynthian_controller

#------------------------------------------------------------------------------
# Module methods
#------------------------------------------------------------------------------

def get_jalv_plugins():
	if isfile(zynthian_engine_jalv.JALV_LV2_CONFIG_FILE):
		with open(zynthian_engine_jalv.JALV_LV2_CONFIG_FILE,'r') as f:
			zynthian_engine_jalv.plugins_dict=json.load(f, object_pairs_hook=OrderedDict)
	return zynthian_engine_jalv.plugins_dict

#------------------------------------------------------------------------------
# Jalv Engine Class
#------------------------------------------------------------------------------

class zynthian_engine_jalv(zynthian_engine):

	#------------------------------------------------------------------------------
	# Plugin List
	#------------------------------------------------------------------------------

	JALV_LV2_CONFIG_FILE = "{}/jalv/plugins.json".format(zynthian_engine.config_dir)

	plugins_dict = OrderedDict([
		("Dexed", {'TYPE': "MIDI Synth",'URL': "https://github.com/dcoredump/dexed.lv2"}),
		("Helm", {'TYPE': "MIDI Synth",'URL': "http://tytel.org/helm"}),
		("MDA ePiano", {'TYPE': "MIDI Synth",'URL': "http://moddevices.com/plugins/mda/EPiano"}),
		("MDA Piano", {'TYPE': "MIDI Synth",'URL': "http://moddevices.com/plugins/mda/Piano"}),
		("MDA JX10", {'TYPE': "MIDI Synth",'URL': "http://moddevices.com/plugins/mda/JX10"}),
		("MDA DX10", {'TYPE': "MIDI Synth",'URL': "http://moddevices.com/plugins/mda/DX10"}),
		("OBXD", {'TYPE': "MIDI Synth",'URL': "https://obxd.wordpress.com"}),
		("SynthV1", {'TYPE': "MIDI Synth",'URL': "http://synthv1.sourceforge.net/lv2"}),
		("Noize Mak3r", {'TYPE': "MIDI Synth",'URL': "http://kunz.corrupt.ch/products/tal-noisemaker"}),
		("Triceratops", {'TYPE': "MIDI Synth",'URL': "http://nickbailey.co.nr/triceratops"}),
		("Raffo MiniMoog", {'TYPE': "MIDI Synth",'URL': "http://example.org/raffo"})
	])

	# ---------------------------------------------------------------------------
	# Controllers & Screens
	# ---------------------------------------------------------------------------

	plugin_ctrl_info = {
		"Dexed": {
		},
		"Helm": {
		},
		"MDA DX10": {
			"ctrls": [
				['volume',7,96],
				['mod-wheel',1,0],
				['sustain on/off',64,'off','off|on']
			],
			"ctrl_screens": [['MIDI Controllers',['volume','mod-wheel','sustain on/off']]]
		},
		"MDA JX10": {
			"ctrls": [
				['volume',7,96],
				['mod-wheel',1,0],
			],
			"ctrl_screens": [['MIDI Controllers',['volume','mod-wheel']]]
		},
		"MDA ePiano": {
			"ctrls": [
				['volume',7,96],
				['mod-wheel',1,0],
				['sustain on/off',64,'off','off|on']
			],
			"ctrl_screens": [['MIDI Controllers',['volume','mod-wheel','sustain on/off']]]
		},
		"MDA Piano": {
			"ctrls": [
				['volume',7,96],
				['mod-wheel',1,0],
				['sustain on/off',64,'off','off|on']
			],
			"ctrl_screens": [['MIDI Controllers',['volume','mod-wheel','sustain on/off']]]
		},
		"Noize Mak3r": {
		},
		"Obxd": {
		},
		"synthv1": {
		}
	}

	_ctrls = None
	_ctrl_screens = None

	#----------------------------------------------------------------------------
	# ZynAPI variables
	#----------------------------------------------------------------------------

	zynapi_instance = None

	#----------------------------------------------------------------------------
	# Initialization
	#----------------------------------------------------------------------------

	def __init__(self, plugin_name, plugin_type, zyngui=None):
		super().__init__(zyngui)

		self.type = plugin_type
		self.name = "Jalv/" + plugin_name
		self.nickname = "JV/" + plugin_name

		self.plugin_name = plugin_name
		self.plugin_url = self.plugins_dict[plugin_name]['URL']

		self.learned_cc = [[None for c in range(128)] for chan in range(16)]
		self.learned_zctrls = {}

		if self.config_remote_display():
			self.command = ("/usr/local/bin/jalv {}".format(self.plugin_url))		#TODO => Is possible to run plugins UI?
		else:
			self.command = ("/usr/local/bin/jalv {}".format(self.plugin_url))

		self.command_prompt = "\n> "

		output = self.start()

		# Get Plugin & Jack names from Jalv starting text ...
		self.jackname = None
		if output:
			for line in output.split("\n"):
				if line[0:15]=="JACK Real Name:":
					self.jackname = line[16:].strip()
					logging.debug("Jack Name => {}".format(self.jackname))
					break
				elif line[0:10]=="JACK Name:":
					self.plugin_name = line[11:].strip()
					logging.debug("Plugin Name => {}".format(self.plugin_name))

		# Set static MIDI Controllers from hardcoded plugin info
		try:
			self._ctrls = self.plugin_ctrl_info[self.plugin_name]['ctrls']
			self._ctrl_screens = self.plugin_ctrl_info[self.plugin_name]['ctrl_screens']
		except:
			logging.info("No defined MIDI controllers for '{}'.".format(self.plugin_name))

		# Generate LV2-Plugin Controllers
		self.lv2_zctrl_dict = self.get_lv2_controllers_dict()
		self.generate_ctrl_screens(self.lv2_zctrl_dict)

		# Get preset list from plugin host
		self.bank_npresets = {}
		self.preset_list = self._get_preset_list()
		self.bank_list = self._get_bank_list()

		self.reset()

	# ---------------------------------------------------------------------------
	# Layer Management
	# ---------------------------------------------------------------------------

	def add_layer(self, layer):
		layer.listen_midi_cc = False
		super().add_layer(layer)
		self.set_midi_chan(layer)

	# ---------------------------------------------------------------------------
	# MIDI Channel Management
	# ---------------------------------------------------------------------------

	def set_midi_chan(self, layer):
		if self.plugin_name=="Triceratops":
			self.lv2_zctrl_dict["midi_channel"].set_value(layer.midi_chan+1.5)

	#----------------------------------------------------------------------------
	# Bank Managament
	#----------------------------------------------------------------------------

	def _get_bank_list(self):
		logging.info("Getting Bank List from LV2 Plugin ...")

		bank_list = []
		output = self.proc_cmd("\get_banks")
		for line in sorted(output.split("\n")):
			try:
				parts = line.split(" => ")
				if len(parts)==2:
					title = parts[0].strip()
					url = parts[1].strip()
					if url in self.bank_npresets:
						bank_list.append((url, None, title, None))
			except Exception as e:
				logging.error(e)

		if "NoBank" in self.bank_npresets:
			bank_list.append(("NoBank", None, "NoBank", None))
		elif len(bank_list)==0:
			bank_list.append(("", None, "", None))

		return bank_list


	def get_bank_list(self, layer=None):
		return self.bank_list


	def set_bank(self, layer, bank):
		return True

	#----------------------------------------------------------------------------
	# Preset Managament
	#----------------------------------------------------------------------------

	def _get_preset_list(self):
		logging.info("Getting Preset List from LV2 Plugin ...")

		self.bank_npresets = {}
		preset_list = []
		output=self.proc_cmd("\get_presets")
		for line in sorted(output.split("\n")):
			try:
				parts = line.split(" => ")
				if len(parts)==2:
					title = parts[0].strip()

					uri_parts = parts[1].strip().split(", ")
					uri_preset = uri_parts[0].strip()
					uri_banks = uri_parts[1:]
					if len(uri_banks)==0:
						uri_banks.append("NoBank")
					preset_list.append((uri_preset,None,title,uri_banks))

					#Count presets/bank
					for uri in uri_banks:
						try:
							self.bank_npresets[uri] += 1
						except:
							self.bank_npresets[uri] = 1

			except Exception as e:
				logging.error(e)

		return preset_list


	def get_preset_list(self, bank):
		bank_preset_list = []
		for preset in  self.preset_list:
			if bank[0] in preset[3]:
				bank_preset_list.append(preset)
		return bank_preset_list


	def set_preset(self, layer, preset, preload=False):
		output=self.proc_cmd("\set_preset {}".format(preset[0]))

		#Parse new controller values
		for line in output.split("\n"):
			try:
				parts=line.split(" = ")
				if len(parts)==2:
					self.lv2_zctrl_dict[parts[0]]._set_value(float(parts[1]))
			except Exception as e:
				logging.error(e)

		return True


	def cmp_presets(self, preset1, preset2):
		try:
			if preset1[0]==preset2[0]:
				return True
			else:
				return False
		except:
			return False

	#----------------------------------------------------------------------------
	# Controllers Managament
	#----------------------------------------------------------------------------

	def get_lv2_controllers_dict(self):
		logging.info("Getting Controller List from LV2 Plugin ...")
		output=self.proc_cmd("\info_controls")
		zctrls=OrderedDict()
		for line in output.split("\n"):
			parts=line.split(" => ")
			if len(parts)==2:
				symbol=parts[0]
				try:
					info=json.JSONDecoder().decode(parts[1])

					#If there is points info ...
					if len(info['points'])>1:
						labels=[]
						values=[]
						for p in info['points']:
							labels.append(p['label'])
							values.append(p['value'])
						try:
							val=info['value']
						except:
							val=labels[0]
						zctrls[symbol]=zynthian_controller(self,symbol,info['label'],{
							'graph_path': info['index'],
							'value': val,
							'labels': labels,
							'ticks': values,
							'value_min': values[0],
							'value_max': values[-1],
							'is_toggle': info['is_toggle'],
							'is_integer': info['is_integer']
						})

					#If it's a normal controller ...
					else:
						r=info['max']-info['min']
						if info['is_integer']:
							if r==1 and info['is_toggle']:
								if info['value']==0: val='off'
								else: val='on'
								zctrls[symbol]=zynthian_controller(self,symbol,info['label'],{
									'graph_path': info['index'],
									'value': val,
									'labels': ['off','on'],
									'ticks': [0,1],
									'value_min': 0,
									'value_max': 1,
									'is_toggle': True,
									'is_integer': True
								})
							else:
								zctrls[symbol]=zynthian_controller(self,symbol,info['label'],{
									'graph_path': info['index'],
									'value': int(info['value']),
									'value_default': int(info['default']),
									'value_min': int(info['min']),
									'value_max': int(info['max']),
									'is_toggle': False,
									'is_integer': True
								})
						else:
								zctrls[symbol]=zynthian_controller(self,symbol,info['label'],{
									'graph_path': info['index'],
									'value': info['value'],
									'value_default': info['default'],
									'value_min': info['min'],
									'value_max': info['max'],
									'is_toggle': False,
									'is_integer': False
								})

				#If control info is not OK
				except Exception as e:
					logging.error(e)

		return zctrls


	def generate_ctrl_screens(self, zctrl_dict=None):
		if zctrl_dict is None:
			zctrl_dict=self.zctrl_dict

		if self._ctrl_screens is None:
			self._ctrl_screens=[]

		c=1
		ctrl_set=[]
		for symbol, zctrl in zctrl_dict.items():
			try:
				#logging.debug("CTRL {}".format(symbol))
				ctrl_set.append(symbol)
				if len(ctrl_set)>=4:
					#logging.debug("ADDING CONTROLLER SCREEN {}#{}".format(self.plugin_name,c))
					self._ctrl_screens.append(["{}#{}".format(self.plugin_name,c),ctrl_set])
					ctrl_set=[]
					c=c+1
			except Exception as err:
				logging.error("Generating Controller Screens => {}".format(err))

		if len(ctrl_set)>=1:
			#logging.debug("ADDING CONTROLLER SCREEN #"+str(c))
			self._ctrl_screens.append(["{}#{}".format(self.plugin_name,c),ctrl_set])


	def get_controllers_dict(self, layer):
		# Get plugin static controllers
		zctrls=super().get_controllers_dict(layer)
		# Add plugin native controllers
		zctrls.update(self.lv2_zctrl_dict)
		return zctrls


	def send_controller_value(self, zctrl):
		self.proc_cmd("\set_control %d, %.6f" % (zctrl.graph_path, zctrl.value))

	#----------------------------------------------------------------------------
	# MIDI learning
	#----------------------------------------------------------------------------

	def init_midi_learn(self, zctrl):
		if zctrl.graph_path:
			logging.info("Learning '{}' ({}) ...".format(zctrl.symbol,zctrl.graph_path))


	def midi_unlearn(self, zctrl):
		if zctrl.graph_path in self.learned_zctrls:
			logging.info("Unlearning '{}' ...".format(zctrl.symbol))
			try:
				self.learned_cc[zctrl.midi_learn_chan][zctrl.midi_learn_cc] = None
				del self.learned_zctrls[zctrl.graph_path]
				return zctrl._unset_midi_learn()
			except Exception as e:
				logging.warning("Can't unlearn => {}".format(e))


	def set_midi_learn(self, zctrl ,chan, cc):
		try:
			# Clean current binding if any ...
			try:
				self.learned_cc[chan][cc].midi_unlearn()
			except:
				pass
			# Add midi learning info
			self.learned_zctrls[zctrl.graph_path] = zctrl
			self.learned_cc[chan][cc] = zctrl
			return zctrl._set_midi_learn(chan, cc)
		except Exception as e:
			logging.error("Can't learn {} => {}".format(zctrl.symbol, e))


	def reset_midi_learn(self):
		logging.info("Reset MIDI-learn ...")
		self.learned_zctrls = {}
		self.learned_cc = [[None for chan in range(16)] for cc in range(128)]


	def cb_midi_learn(self, zctrl, chan, cc):
		return self.set_midi_learn(zctrl, chan, cc)

	#----------------------------------------------------------------------------
	# MIDI CC processing
	#----------------------------------------------------------------------------

	def midi_control_change(self, chan, ccnum, val):
		try:
			self.learned_cc[chan][ccnum].midi_control_change(val)
		except:
			pass

	# ---------------------------------------------------------------------------
	# API methods
	# ---------------------------------------------------------------------------

	@classmethod
	def init_zynapi_instance(cls, plugin_name, plugin_type):
		if cls.zynapi_instance and cls.zynapi_instance != "JV/" + plugin_name:
			cls.zynapi_instance.stop()
			cls.zynapi_instance = None

		if not cls.zynapi_instance:
			cls.zynapi_instance = cls(plugin_name, plugin_type)


	@classmethod
	def zynapi_get_banks(cls):
		banks=[]
		for b in cls.zynapi_instance.get_bank_list():
			banks.append({
				'text': b[2],
				'name': b[2],
				'fullpath': b[0],
				'raw': b
			})
		return banks


	@classmethod
	def zynapi_get_presets(cls, bank):
		presets=[]
		for p in cls.zynapi_instance.get_preset_list(bank['raw']):
			presets.append({
				'text': p[2],
				'name': p[2],
				'fullpath': p[0],
				'raw': p
			})
		return presets


	@classmethod
	def zynapi_install(cls, dpath, bank_path):
		fname, ext = os.path.splitext(dpath)
		native_ext = cls.native_formats()

		if os.path.isdir(dpath):
			if ext=='.lv2'
				shutil.move(dpath, zynthian_engine.my_data_dir + "/presets/lv2/")
			else:
				#Call preset converter
				pass
		else:
			if ext[1:]==native_ext:
				#Call preset converter
				pass
			else:
				raise Exception("File doesn't look like a {} preset!".format(native_ext))


	@classmethod
	def zynapi_get_formats(cls):
		formats = "zip,tgz,tar.gz"
		fmt = cls.zynapi_native_formats()
		if fmt:
			formats = fmt + "," + formats

		return formats


	@classmethod
	def zynapi_martifact_formats(cls):
		fmt = cls.zynapi_native_formats()
		if fmt:
			return fmt
		else:
			return "lv2"


	@classmethod
	def zynapi_native_formats(cls):
		if cls.zynapi_instance.plugin_name=="Dexed":
			return "syx"
		elif cls.zynapi_instance.plugin_name=="synthv1":
			return "synthv1"
		elif cls.zynapi_instance.plugin_name=="padthv1":
			return "padthv1"
		#elif cls.zynapi_instance.plugin_name=="Helm":
		#	return "helm"


#******************************************************************************
