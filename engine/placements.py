"""Shared world positions for the original habitat/building/decoration systems."""
from dataclasses import dataclass

@dataclass
class WorldPlacement:
    item_id: str
    x: float
    y: float

    def get_display_position(self):
        return self.x * 20 / 132, self.y * 12 / 42


def habitat_placements(game):
    # Classic's whole-prop bounce is presentation, not a moving destination.
    # Ultra has its own articulated object animation at this fixed position.
    return [WorldPlacement(p.item_id,p.x*132/20,p.y*42/12)
            for p in game.habitat.get_visible_placed_items()]


def outdoor_decorations(game):
    result=[]
    for room_id in ('garden','pond'):
        room=getattr(getattr(game,'decorations',None),'rooms',{}).get(room_id)
        if not room or not room.unlocked:continue
        for decoration in room.decorations:
            x,y=decoration.position
            left,width=(6,62) if room_id=='garden' else (72,52)
            result.append(WorldPlacement(decoration.decoration_id,left+x/room.size[0]*width,22+y/room.size[1]*16))
    return result


def complete_structures(game):
    result=[]
    for index,structure in enumerate(game.building.structures):
        if structure.status.value!='complete':continue
        p=getattr(structure,'position',None)
        result.append(WorldPlacement(structure.blueprint_id,p[0]*132/10 if p else 8+index*12,p[1]*42/8 if p else 32))
    return result
