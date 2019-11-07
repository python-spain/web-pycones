# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.core.management.base import BaseCommand
from proposals.models import Proposal


class Command(BaseCommand):

    args = "<destination>"
    help = "Creates proposals files"

    def handle(self, *args, **options):
        exports = 0
        for proposal in Proposal.objects.all():
            title, abstract, description, additional_notes = (
                proposal.title_es if proposal.title_es else proposal.title_en,
                proposal.abstract_es if proposal.abstract_es.raw else proposal.abstract_en,
                proposal.description_es if proposal.description_es else proposal.description_en,
                proposal.additional_notes_es if proposal.additional_notes_es.raw else proposal.additional_notes_en,
            )
            file_name = "%s - %s.md" % (proposal.pk, title)
            file_name = file_name.replace("#", "")
            file_name = file_name.replace("!", "")
            file_name = file_name.replace("/", "")
            try:
                file_name = os.path.join(args[0], file_name)
            except IndexError:
                pass
            content = [
                "# %s\n" % title,
                "Nivel: %s" % proposal.audience_level,
                "Tipo: %s" % proposal.kind.name,
                "\n",
                "# Breve descripción\n",
                description,
                "\n# Resumen detallado\n",
                abstract.raw,
                "\n# Notas adicionales\n",
                additional_notes.raw
            ]
            content = "\n".join(content)
            f = open(file_name, "w")
            f.writelines(content)
            f.close()
            exports += 1
        print("Exportadas %s/%s propuestas" % (exports, Proposal.objects.count()))
