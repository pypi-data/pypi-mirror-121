#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Augmenting the supported types
from extended_json_schema_validator.extensible_validator import ExtensibleValidator

from .extensions.curie_search import CurieSearch
from .extensions.ontology_term import OntologyTerm
from extended_json_schema_validator.extensions.unique_check import UniqueKey
from extended_json_schema_validator.extensions.pk_check import PrimaryKey
from extended_json_schema_validator.extensions.fk_check import ForeignKey
from .extensions.foreign_property_check import ForeignProperty

class FairGTracksValidator(ExtensibleValidator):
	# This has been commented out, as we are following the format validation path
	CustomTypes = {
	#	'curie': CurieSearch.IsCurie,
	#	'term': OntologyTerm.IsTerm
	}

	CustomFormats = [
		CurieSearch,
		OntologyTerm
	]
	
	CustomValidators = {
		None: [
			CurieSearch,
			OntologyTerm,
			UniqueKey,
			PrimaryKey,
			ForeignKey,
			ForeignProperty
		]
	}
	
	def __init__(self,customFormats=CustomFormats, customTypes=CustomTypes, customValidators=CustomValidators, config={}, isRW=True):
		super().__init__(customFormats, customTypes, customValidators, config, jsonRootTag='fair_tracks', isRW=isRW)
