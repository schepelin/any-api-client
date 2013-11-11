# -*- coding: utf-8 -*-

from any_api_client.core import bind_method

__all__ = (
    'SupervisorAPI',
)

class SupervisorAPI(object):

    def __init__(self, api_url):
        self.api_url = api_url

    get_clan_dossier = bind_method(
        path='/get_clan_dossier/', accepts_params=['clan_id'])

    move_clan_to_gm = bind_method(
        path='/move_clan_to_gm/',
        accepts_params=['clan_id', 'map_id', 'performer_id'])

    remove_clan_from_gm = bind_method(
        path='/remove_clan_from_gm/',
        accepts_params=['clan_id', 'map_id', 'performer_id', 'clan_assets'])

