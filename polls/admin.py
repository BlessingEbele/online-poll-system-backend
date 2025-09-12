from django.contrib import admin
from .models import Poll, Option, Vote

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 1
    # remove autocomplete_fields

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    inlines = [VoteInline]

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    inlines = [VoteInline]

# Remove Vote from standalone admin registration
# @admin.register(Vote)
# class VoteAdmin(admin.ModelAdmin):
#     pass
