from wagtail.core.blocks import StructBlock, PageChooserBlock, IntegerBlock


class AgendaBlock(StructBlock):
    index = PageChooserBlock(page_type=['EditionIndex'])

    class Meta:
        template = 'agenda/agenda_block.html'
