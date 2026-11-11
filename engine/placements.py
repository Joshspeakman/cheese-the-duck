"""Shared world positions for the original habitat/building/decoration systems."""
from dataclasses import dataclass

@dataclass
class WorldPlacement:
    item_id: str
    x: float
    y: float
    instance: str = ''
    footprint: object = None
    scale: float = 1.
    role: str = ''

    def get_display_position(self):
        return self.x * 20 / 132, self.y * 12 / 42


def habitat_placements(game):
    # Classic's whole-prop bounce is presentation, not a moving destination.
    # Ultra has its own articulated object animation at this fixed position.
    return [WorldPlacement(p.item_id,p.x*132/20,p.y*42/12,p.instance_id)
            for p in game.habitat.get_visible_placed_items()]


def grounded(game,placements,records=None):
    if records is None:records=getattr(getattr(game,'living_pond',None),'state',{}).get('grounds',{})
    result=[]
    for p in placements:
        record=records.get(p.instance)
        if record and record.get('id')==p.item_id:
            if record.get('stored'):continue
            p=WorldPlacement(p.item_id,record['x']*132/20,record['y']*42/12,p.instance)
        result.append(p)
    return result


def outdoor_decorations(game,raw=False,records=None):
    result=[]
    for room_id in ('garden','pond'):
        room=getattr(getattr(game,'decorations',None),'rooms',{}).get(room_id)
        if not room or not room.unlocked:continue
        for decoration in room.decorations:
            x,y=decoration.position
            left,width=(6,62) if room_id=='garden' else (72,52)
            result.append(WorldPlacement(decoration.decoration_id,left+x/room.size[0]*width,22+y/room.size[1]*16,decoration.instance_id))
    return result if raw else grounded(game,result,records)


def complete_structures(game,raw=False,records=None):
    result=[]
    for index,structure in enumerate(game.building.structures):
        if structure.status.value!='complete':continue
        p=getattr(structure,'position',None)
        result.append(WorldPlacement(structure.blueprint_id,p[0]*132/10 if p else 8+index*12,p[1]*42/8 if p else 32,structure.instance_id))
    return result if raw else grounded(game,result,records)


def pond_installations(pond):
    """Garden beds and community works also occupy the native ground plane."""
    from engine.pond_layout import FOOTPRINTS
    result=[]
    projects={'reed_beds':('reed',4,7),'orchard':('tree_oak',14,5),
              'observatory':('telescope',15,4),'clubhouse':('wooden_cottage',15,6),
              'workshop':('workbench',5,6),'trail':('bridge',10,8)}
    for key,(item,x,y) in projects.items():
        if pond.state['projects'][key]['stage']:
            result.append(WorldPlacement(item,x*132/20,y*42/12,'project:'+key,role='project'))
    for plot in pond.game.garden.plots.values():
        if not plot.is_unlocked:continue
        item=plot.plant.plant_id if plot.plant else 'garden_plot'
        f=FOOTPRINTS.get(item,FOOTPRINTS['garden_plot'])
        scale=min(1,18/f['width'],14/f['height'])
        # The bed reserves the mature plant's envelope even while empty. Planting
        # a taller flower must not move an established garden around the pond.
        shape=dict(f,width=18,height=14,floor=False)
        result.append(WorldPlacement(item,(4+plot.plot_id*3.5)*132/20,3*42/12,
                                     'garden:'+str(plot.plot_id),shape,scale,'garden'))
    return result


def physical_belongings(game):
    """Include stored and indoor belongings; their histories must survive a move."""
    from world.physical_identity import saved_identity
    seen = set()
    groups = [('habitat', p.item_id, p) for p in game.habitat.placed_items + game.habitat.stored_placements]
    groups += [('decoration', p.decoration_id, p) for room in game.decorations.rooms.values() for p in room.decorations]
    groups += [('decoration', p.decoration_id, p) for p in game.decorations.stored_placements]
    groups += [('structure', p.blueprint_id, p) for p in game.building.structures]
    for index, (source, item, p) in enumerate(groups):
        while not p.instance_id or p.instance_id in seen:
            # Repair duplicated imported identities once on the actual saved
            # object, never manufacture a fresh identity during rendering.
            p.instance_id = saved_identity({'item': item, 'duplicate': p.instance_id}, source, index)
        seen.add(p.instance_id)
        yield source, item, p.instance_id
