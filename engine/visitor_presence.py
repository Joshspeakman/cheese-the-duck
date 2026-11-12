"""One physical Pip across his visit and story appearances.

Presence is transient. Story choices, visit history and both existing memory
records remain untouched; reconciling those memories is a separate migration.
"""
PIP = 'lost_duckling'


def story_owns_pip(pond):
    story = pond.state.get('story') if pond else None
    return isinstance(story, dict) and story.get('id') == PIP


def defer_story(pond, story_id):
    visit = pond.game.atmosphere.current_visitor
    return story_id == PIP and bool(visit and visit[0].id == PIP)


def reconcile(game):
    """Return whether an obsolete duplicate rare visit was removed."""
    atmosphere = game.atmosphere
    owns = story_owns_pip(game.living_pond)
    if owns:
        atmosphere.excluded_visitors.add(PIP)
    else:
        atmosphere.excluded_visitors.discard(PIP)
    visit = atmosphere.current_visitor
    if owns and visit and visit[0].id == PIP:
        atmosphere.current_visitor = None
        return True
    return False
