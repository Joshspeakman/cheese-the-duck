"""Saved ground anchors for belongings from the older room/building grids.

Those grids describe construction and room slots, not the pond shoreline. Both
walking destinations and scene snapshots read these same native world anchors.
Ownership, construction progress and individual object histories stay original.
"""
from engine.pond_layout import PondLayout, FOOTPRINTS, REVISION, bounds
from engine.placements import outdoor_decorations, complete_structures,pond_installations


class PondGrounds:
    def __init__(self, pond):
        self.pond=pond
        self.records=pond.state['grounds']
        self.signature=None
        self.sources={}

    def reconcile(self, force=False):
        from world.habitat import Habitat
        sources=[*complete_structures(self.pond.game,raw=True),*outdoor_decorations(self.pond.game,raw=True),*pond_installations(self.pond)]
        signature=tuple((p.item_id,p.instance,p.x,p.y) for p in sources)
        if not force and signature==self.signature:return False
        self.signature=signature
        self.sources={p.instance:p for p in sources}
        reserved=[]
        policy=PondLayout(Habitat(),lambda:reserved)
        # New construction finds room around established grounds, rather than
        # taking a preferred spot first and pushing an existing garden aside.
        for p in sorted(sources,key=lambda p:p.instance not in self.records):
            origin=[p.x,p.y]
            old=self.records.get(p.instance)
            if old and old.get('origin')==origin:
                if old.get('stored'):
                    self.records[p.instance]=dict(old,id=p.item_id,revision=REVISION)
                    continue
                preferred=[old['x'],old['y']]
            else:preferred=list(p.get_display_position())
            spot=policy.find(p.item_id,preferred,instance=p.instance,footprint=p.footprint)
            record=dict(id=p.item_id,origin=origin,x=spot[0] if spot else preferred[0],
                        y=spot[1] if spot else preferred[1],stored=not bool(spot),revision=REVISION)
            self.records[p.instance]=record
            if spot:reserved.append((p.item_id,*spot,p.instance,p.footprint))
        return True  # Includes removed installations: invalidate their snapshots.

    def installations(self):
        result=[]
        for identity,source in self.sources.items():
            if not source.role:continue
            record=self.records.get(identity)
            if record and not record['stored']:
                result.append(dict(id=source.item_id,instance=identity,x=record['x']*132/20,
                                   y=record['y']*42/12,scale=source.scale,role=source.role,
                                   footprint=source.footprint))
        return result

    def obstacles(self):
        for p in [*outdoor_decorations(self.pond.game,records=self.records),*complete_structures(self.pond.game,records=self.records)]:
            yield (p.item_id,*p.get_display_position(),p.instance)
        for p in self.installations():
            yield (p['id'],p['x']*20/132,p['y']*12/42,p['instance'],p['footprint'])

    def handles(self,item,instance):
        return instance in self.sources and self.sources[instance].item_id==item

    def command(self,action,item,instance,x=None,y=None):
        if not self.handles(item,instance):return False,'Choose an owned copy from Arrange.'
        record=self.records[instance]
        if action=='layout_store':
            record['stored']=True
            return True,'Put away safely. Its history and progress are kept.'
        layout=self.pond.layout
        footprint=self.sources[instance].footprint
        if action=='layout_auto':
            spot=layout.find(item,[record['x'],record['y']],instance,footprint)
            if not spot:return False,'There is no clear space for the whole object. It is kept safely.'
            x,y=spot
        ok,message=layout.check(item,x,y,instance,footprint)
        if not ok:return ok,message
        record.update(x=x,y=y,stored=False)
        return True,'Placed '+item.replace('_',' ')+'.'

    def snapshot(self,layout):
        # External copies are first-class Arrange choices, including overflow.
        # Do not offer stale records whose original owner/structure was removed.
        ids={i['id'] for i in layout['items']}
        for identity,source in self.sources.items():
            key=source.item_id;record=self.records.get(identity)
            if key not in FOOTPRINTS or not record:continue
            if key not in ids:
                layout['items'].append(dict(id=key,footprint=FOOTPRINTS[key]));ids.add(key)
            placed=not record['stored']
            layout['copies'].append(dict(id=key,instance=identity,placed=placed,footprint=source.footprint,
                                         role=source.role,scale=source.scale,
                                         label='Garden bed '+str(int(identity.split(':')[1])+1) if source.role=='garden' else
                                               'Community '+identity.split(':')[1].replace('_',' ') if source.role=='project' else None))
            if placed:layout['placed'].append(dict(id=key,instance=identity,x=record['x'],y=record['y'],box=bounds(key,record['x'],record['y'],source.footprint)))
        # These now appear in placed, so the UI must not count them twice.
        layout['obstacles']=[o for o in layout['obstacles'] if o.get('instance') not in self.sources]
        return layout
